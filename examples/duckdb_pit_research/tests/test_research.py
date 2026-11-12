"""Real DuckDB execution, independent reference, adversarial and regression checks."""

from copy import deepcopy
from datetime import timedelta, timezone
import json
from pathlib import Path
import random
import subprocess
import sys
import tempfile
import unittest

from examples.duckdb_pit_research import duckdb_backend as sql
from examples.duckdb_pit_research.fixtures import build_fixture
from examples.duckdb_pit_research.model import (
    ContractError,
    EquivalenceError,
    assert_equal,
    audit_provenance,
    canonical_bytes,
    evaluate,
    instant,
    python_labels,
    python_snapshots,
    split_plan,
    validate,
)
from examples.duckdb_pit_research.run import (
    FIXTURE,
    ROOT,
    experiment,
    future_mutation,
    write_run,
)
from examples.duckdb_pit_research.verify_run import verify_run


class PITResearchTests(unittest.TestCase):
    def setUp(self):
        self.data = build_fixture()

    def row(self, decision="D0", symbol="SYN_A", data=None):
        return next(
            r
            for r in python_snapshots(data or self.data)
            if r["decision_id"] == decision and r["symbol"] == symbol
        )

    def check_mutant(self, name):
        with self.assertRaises(EquivalenceError):
            assert_equal(python_snapshots(self.data), sql.snapshots(self.data, name))

    def test_frozen_fixture_matches_generator(self):
        self.assertEqual(json.loads(FIXTURE.read_text(encoding="utf-8")), self.data)

    def test_sql_python_snapshot_equivalence(self):
        a, b = python_snapshots(self.data), sql.snapshots(self.data)
        self.assertEqual(len(a), 16)
        assert_equal(a, b)
        audit_provenance(self.data, b)

    def test_sql_python_forward_label_equivalence(self):
        a, b = python_labels(self.data), sql.labels(self.data)
        self.assertEqual(len(a), 24)
        assert_equal(a, b)

    def test_hand_computed_golden_signal_and_missing_value(self):
        self.assertEqual(self.row()["signal"], 0.05)
        self.assertEqual(self.row(symbol="SYN_B")["signal"], 0.01)
        missing = self.row(symbol="SYN_C")
        self.assertEqual(missing["status"], "MISSING_VALUE")
        self.assertIsNone(missing["signal"])

    def test_future_revision_does_not_replace_known_original(self):
        self.assertEqual(self.row()["current_id"], "SYN_A-2026-01-09-r0")
        self.assertEqual(self.row()["current_close_cents"], 10500)

    def test_market_session_not_latest_arrival_defines_lookback(self):
        row = self.row("D3")
        self.assertEqual(row["previous_id"], "SYN_A-2026-01-13-r0")
        # A late Jan9 revision arrived after the Jan13 close but is not the previous session.
        self.check_mutant("latest_arrival")

    def test_exact_availability_boundary_is_inclusive(self):
        self.assertEqual(self.row("D3")["current_id"], "SYN_A-2026-01-14-r0")
        changed = deepcopy(self.data)
        target = next(
            f for f in changed["features"] if f["feature_id"] == "SYN_A-2026-01-14-r0"
        )
        target["available_at"] = (
            instant(target["available_at"]) + timedelta(microseconds=1)
        ).isoformat()
        self.assertEqual(
            self.row("D3", data=changed)["current_id"], "SYN_A-2026-01-13-r0"
        )
        assert_equal(python_snapshots(changed), sql.snapshots(changed))

    def test_late_bar_is_not_backfilled(self):
        self.assertEqual(self.row("D2", "SYN_B")["current_id"], "SYN_B-2026-01-12-r0")

    def test_dynamic_membership_and_unannounced_addition(self):
        identities = {(r["decision_id"], r["symbol"]) for r in sql.snapshots(self.data)}
        self.assertNotIn(("D3", "SYN_B"), identities)
        self.assertNotIn(("D4", "SYN_D"), identities)
        self.assertIn(("D5", "SYN_D"), identities)

    def test_future_data_invariance_for_every_cutoff(self):
        original = python_snapshots(self.data)
        for decision in self.data["decisions"]:
            with self.subTest(decision=decision["decision_id"]):
                mutated = future_mutation(self.data, instant(decision["decision_at"]))
                expected = [
                    r for r in original if r["decision_id"] == decision["decision_id"]
                ]
                for implementation in (python_snapshots, sql.snapshots):
                    actual = [
                        r
                        for r in implementation(mutated)
                        if r["decision_id"] == decision["decision_id"]
                    ]
                    assert_equal(expected, actual)

    def test_labels_cannot_change_features(self):
        changed = deepcopy(self.data)
        for row in changed["opens"]:
            row["open_cents"] += 1234
        original = python_snapshots(self.data)
        assert_equal(original, python_snapshots(changed))
        assert_equal(original, sql.snapshots(changed))
        self.assertNotEqual(python_labels(self.data), python_labels(changed))

    def test_event_time_only_mutation_detected(self):
        self.check_mutant("event_time_only")
        with self.assertRaisesRegex(ContractError, "future feature"):
            audit_provenance(self.data, sql.snapshots(self.data, "event_time_only"))

    def test_publication_only_mutation_detected(self):
        self.check_mutant("published_only")

    def test_global_latest_before_asof_mutation_detected(self):
        self.check_mutant("global_latest_before_asof")

    def test_future_membership_mutation_detected(self):
        self.check_mutant("future_membership")
        with self.assertRaisesRegex(ContractError, "future membership"):
            audit_provenance(self.data, sql.snapshots(self.data, "future_membership"))

    def test_duplicate_feature_key_rejected(self):
        self.data["features"].append(deepcopy(self.data["features"][0]))
        with self.assertRaises(ContractError):
            sql.snapshots(self.data)

    def test_duplicate_open_rejected(self):
        self.data["opens"].append(deepcopy(self.data["opens"][0]))
        with self.assertRaisesRegex(ContractError, "duplicate key"):
            validate(self.data)

    def test_schema_missing_and_extra_field_rejected(self):
        for kind in ("missing", "extra"):
            changed = deepcopy(self.data)
            if kind == "missing":
                changed["features"][0].pop("available_at")
            else:
                changed["features"][0]["future_target"] = 999
            with (
                self.subTest(kind=kind),
                self.assertRaisesRegex(ContractError, "fields"),
            ):
                validate(changed)

    def test_invalid_price_values_rejected(self):
        for bad in (0, -1, 1.5, float("nan"), True):
            changed = deepcopy(self.data)
            changed["features"][0]["close_cents"] = bad
            with (
                self.subTest(value=bad),
                self.assertRaisesRegex(ContractError, "positive integer"),
            ):
                validate(changed)

    def test_naive_timestamp_rejected(self):
        self.data["decisions"][0]["decision_at"] = "2026-01-12T09:00:00"
        with self.assertRaisesRegex(ContractError, "timezone"):
            validate(self.data)

    def test_invalid_availability_order_rejected(self):
        self.data["features"][0]["available_at"] = "2026-01-08T15:00:00+00:00"
        with self.assertRaisesRegex(ContractError, "available before event"):
            validate(self.data)

    def test_revision_arrival_cannot_go_backwards(self):
        target = next(
            f for f in self.data["features"] if f["feature_id"] == "SYN_A-2026-01-09-r1"
        )
        target["published_at"] = target["event_at"]
        target["available_at"] = target["event_at"]
        with self.assertRaisesRegex(ContractError, "revision availability"):
            validate(self.data)

    def test_fill_must_be_strictly_after_decision(self):
        self.data["decisions"][0]["fill_at"] = self.data["decisions"][0]["decision_at"]
        with self.assertRaisesRegex(ContractError, "decision < fill"):
            validate(self.data)

    def test_shifted_label_horizon_rejected(self):
        self.data["decisions"][0]["exit_at"] = self.data["decisions"][0]["decision_at"]
        with self.assertRaises(ContractError):
            validate(self.data)

    def test_purge_and_embargo_prevent_train_oos_overlap(self):
        plan = split_plan(self.data)
        self.assertEqual(plan["train"], ["D0", "D1"])
        self.assertEqual(plan["purged"], ["D2"])
        first = min(
            instant(d["decision_at"])
            for d in self.data["decisions"]
            if d["decision_id"] in plan["oos"]
        )
        for decision in self.data["decisions"]:
            if decision["decision_id"] in plan["train"]:
                self.assertLess(
                    instant(decision["exit_at"]) + timedelta(minutes=60), first
                )

    def test_higher_cost_never_improves_same_book(self):
        snapshots, labels = python_snapshots(self.data), python_labels(self.data)
        low, high = evaluate(self.data, snapshots, labels, 0), evaluate(
            self.data, snapshots, labels, 20
        )
        for policy in low:
            self.assertLessEqual(
                high[policy]["oos_net_return"], low[policy]["oos_net_return"]
            )
            for a, b in zip(low[policy]["daily"], high[policy]["daily"]):
                self.assertLessEqual(b["net_return"], a["net_return"])

    def test_cash_exposure_turnover_and_cost_are_zero(self):
        book = evaluate(
            self.data, python_snapshots(self.data), python_labels(self.data)
        )
        for row in book["cash"]["daily"]:
            self.assertEqual(
                (
                    row["gross_exposure"],
                    row["round_trip_turnover"],
                    row["cost_return"],
                    row["net_return"],
                ),
                (0, 0, 0, 0),
            )
        for row in book["positive_top1"]["daily"]:
            self.assertLessEqual(row["gross_exposure"], 1)
            self.assertAlmostEqual(
                row["round_trip_turnover"], 2 * row["gross_exposure"]
            )

    def test_missing_price_label_is_not_zero_return(self):
        self.data["opens"] = [
            p
            for p in self.data["opens"]
            if not (
                p["symbol"] == "SYN_A" and p["event_at"] == "2026-01-15T09:30:00+00:00"
            )
        ]
        py, db = python_labels(self.data), sql.labels(self.data)
        assert_equal(py, db)
        book = evaluate(self.data, python_snapshots(self.data), py)
        day = next(
            d for d in book["positive_top1"]["daily"] if d["decision_id"] == "D3"
        )
        self.assertEqual(day["status"], "MISSING_LABEL")
        self.assertIsNone(day["net_return"])
        self.assertIsNone(book["positive_top1"]["oos_net_return"])

    def test_negative_synthetic_outcome_is_preserved(self):
        book = evaluate(
            self.data, python_snapshots(self.data), python_labels(self.data)
        )
        self.assertLess(book["positive_top1"]["oos_net_return"], 0)
        self.assertIsNone(book["positive_top1"]["annualized_sharpe"])

    def test_ordering_of_input_rows_is_irrelevant(self):
        changed = deepcopy(self.data)
        rng = random.Random(42)
        for table in ("features", "opens", "memberships", "decisions"):
            rng.shuffle(changed[table])
        expected = python_snapshots(self.data)
        assert_equal(expected, python_snapshots(changed))
        assert_equal(expected, sql.snapshots(changed))

    def test_aware_timezone_offsets_normalize_to_utc(self):
        changed = deepcopy(self.data)
        for table in ("features", "opens", "memberships", "decisions"):
            for row in changed[table]:
                for key in row:
                    if key.endswith("_at"):
                        row[key] = (
                            instant(row[key])
                            .astimezone(timezone(timedelta(hours=8)))
                            .isoformat()
                        )
        expected = python_snapshots(self.data)
        assert_equal(expected, python_snapshots(changed))
        assert_equal(expected, sql.snapshots(changed))

    def test_unknown_mutation_rejected(self):
        with self.assertRaisesRegex(ContractError, "unknown diagnostic"):
            sql.snapshots(self.data, "SELECT arbitrary")

    def test_external_access_disabled(self):
        with sql.connect(self.data) as con:
            self.assertFalse(
                con.execute(
                    "SELECT current_setting('enable_external_access')"
                ).fetchone()[0]
            )
            self.assertEqual(
                con.execute("SELECT current_setting('threads')").fetchone()[0], 1
            )

    def test_deterministic_end_to_end_results(self):
        first = experiment(self.data)
        second = experiment(self.data)
        self.assertEqual(canonical_bytes(first), canonical_bytes(second))
        self.assertEqual(len(first["negative_controls"]), 5)
        self.assertTrue(first["label_to_signal_isolation"])

    def test_output_pack_hash_and_no_overwrite(self):
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / "run"
            result = write_run(FIXTURE, output)
            self.assertEqual(
                (output / "RESULTS.json").read_bytes(), canonical_bytes(result)
            )
            manifest = json.loads(
                (output / "RUN_MANIFEST.json").read_text(encoding="utf-8")
            )
            self.assertEqual(manifest["environment"]["duckdb"], "2.0.0")
            self.assertEqual(manifest["production"], "NO_GO")
            self.assertNotIn(str(ROOT), json.dumps(manifest))
            with self.assertRaises(FileExistsError):
                write_run(FIXTURE, output)

    def test_cli_missing_input_fails_with_exit_two(self):
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "examples.duckdb_pit_research.run",
                "--fixture",
                ".cache/missing-fixture.json",
                "--output",
                ".cache/should-not-exist",
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=15,
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("research error", result.stderr)

    def test_nonfinite_or_negative_cost_rejected(self):
        for bad in (-1, float("nan"), float("inf")):
            with (
                self.subTest(value=bad),
                self.assertRaisesRegex(ContractError, "nonnegative cost"),
            ):
                evaluate(
                    self.data,
                    python_snapshots(self.data),
                    python_labels(self.data),
                    bad,
                )

    def test_tutor_diagnostic_is_question_only_and_one_at_a_time(self):
        questions = json.loads(
            (FIXTURE.parents[1] / "tutor/QUESTIONS.json").read_text(encoding="utf-8")
        )
        self.assertTrue(questions["one_question_at_a_time"])
        self.assertEqual(len(questions["diagnostic"]), 5)
        for item in questions["diagnostic"]:
            self.assertNotIn("answer", item)
            self.assertTrue(item["question"])

    def test_tutor_does_not_invent_observed_mastery(self):
        state = json.loads(
            (FIXTURE.parents[1] / "tutor/SESSION_STATE.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(state["observed_checks"], [])
        self.assertTrue(all(level is None for level in state["skills"].values()))
        self.assertFalse(state["public_response_storage_authorized"])

    def test_eadb_three_documents_exist(self):
        for name in ("PROJECT_GUIDE.md", "TESTING_AND_DEBUGGING.md", "UPGRADE.md"):
            self.assertTrue((FIXTURE.parents[1] / "docs" / name).is_file())

    def test_nonpositive_nav_is_rejected_not_compounded(self):
        with self.assertRaisesRegex(ContractError, "bankruptcy"):
            evaluate(
                self.data, python_snapshots(self.data), python_labels(self.data), 10000
            )

    def test_seed_type_is_explicit(self):
        self.data["seed"] = True
        with self.assertRaisesRegex(ContractError, "integer seed"):
            validate(self.data)

    def test_membership_revision_order_uses_normalized_instants(self):
        revised = deepcopy(self.data["memberships"][0])
        revised.update(
            membership_id="A-revised",
            revision=1,
            effective_at="2026-01-01T08:00:00+08:00",
            published_at="2025-12-31T23:59:00+00:00",
            available_at="2025-12-31T23:59:00+00:00",
        )
        self.data["memberships"].append(revised)
        with self.assertRaisesRegex(ContractError, "revision availability"):
            validate(self.data)

    def test_zero_signals_take_no_position(self):
        for row in self.data["features"]:
            if row["close_cents"] is not None:
                row["close_cents"] = 10000
        snapshots = python_snapshots(self.data)
        assert_equal(snapshots, sql.snapshots(self.data))
        result = evaluate(self.data, snapshots, python_labels(self.data))[
            "positive_top1"
        ]
        self.assertEqual(result["oos_net_return"], 0)
        self.assertTrue(all(row["weights"] == {} for row in result["daily"]))

    def test_positive_signal_tie_break_is_deterministic(self):
        row = next(
            f for f in self.data["features"] if f["feature_id"] == "SYN_B-2026-01-09-r0"
        )
        row["close_cents"] = 10500
        snapshots = python_snapshots(self.data)
        assert_equal(snapshots, sql.snapshots(self.data))
        day = evaluate(self.data, snapshots, python_labels(self.data))["positive_top1"][
            "daily"
        ][0]
        self.assertEqual(day["weights"], {"SYN_A": 1.0})

    def test_run_byte_integrity_verifier(self):
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / "run"
            write_run(FIXTURE, output)
            self.assertEqual(verify_run(output)["status"], "PASS_RUN_BYTE_INTEGRITY")

    def test_tampered_result_bytes_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / "run"
            write_run(FIXTURE, output)
            with (output / "RESULTS.json").open("a", encoding="utf-8") as stream:
                stream.write(" ")
            with self.assertRaisesRegex(ValueError, "output hash"):
                verify_run(output)

    def test_tampered_human_report_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / "run"
            write_run(FIXTURE, output)
            with (output / "RESEARCH_REPORT.md").open("a", encoding="utf-8") as stream:
                stream.write("unsupported success claim")
            with self.assertRaisesRegex(ValueError, "output hash"):
                verify_run(output)


if __name__ == "__main__":
    unittest.main()
