"""Stdlib-only integration checks; optional DuckDB tests run in the example suite."""

import json
from pathlib import Path
import unittest

from examples.duckdb_pit_research.fixtures import build_fixture
from examples.duckdb_pit_research.model import (
    evaluate,
    python_labels,
    python_snapshots,
    split_plan,
    validate,
)

FOLDER = Path(__file__).resolve().parents[1] / "examples/duckdb_pit_research"


class DuckDBPITReferenceTests(unittest.TestCase):
    def test_frozen_fixture_and_reference_contract(self):
        data = json.loads(
            (FOLDER / "fixtures/synthetic_v1.json").read_text(encoding="utf-8")
        )
        self.assertEqual(data, build_fixture())
        validate(data)

    def test_independent_known_information_set_anchor(self):
        rows = python_snapshots(build_fixture())
        row = next(
            r for r in rows if (r["decision_id"], r["symbol"]) == ("D0", "SYN_A")
        )
        self.assertEqual(row["current_id"], "SYN_A-2026-01-09-r0")
        self.assertEqual(row["signal"], 0.05)

    def test_split_is_purged_without_training_a_model(self):
        plan = split_plan(build_fixture())
        self.assertEqual(plan["purged"], ["D2"])
        self.assertFalse(plan["fitted_parameters"])

    def test_negative_outcome_and_not_identifiable_sharpe(self):
        data = build_fixture()
        result = evaluate(data, python_snapshots(data), python_labels(data))
        self.assertLess(result["positive_top1"]["oos_net_return"], 0)
        self.assertIsNone(result["positive_top1"]["annualized_sharpe"])


if __name__ == "__main__":
    unittest.main()
