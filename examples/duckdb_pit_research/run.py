"""Run the frozen synthetic experiment and write a non-overwriting evidence pack."""

import argparse
from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import sys
import time

from . import duckdb_backend as sql
from .model import (
    ContractError,
    EquivalenceError,
    assert_equal,
    audit_provenance,
    canonical_bytes,
    evaluate,
    fingerprint,
    instant,
    python_labels,
    python_snapshots,
    split_plan,
    validate,
)

HERE = Path(__file__).parent
ROOT = HERE.parents[1]
FIXTURE = HERE / "fixtures/synthetic_v1.json"


def future_mutation(data, cutoff):
    changed = deepcopy(data)
    for row in changed["features"]:
        if instant(row["available_at"]) > cutoff:
            row["close_cents"] = (row["close_cents"] or 10000) + 5000
    for row in changed["memberships"]:
        if instant(row["available_at"]) > cutoff:
            row["is_member"] = not row["is_member"]
    return changed


def experiment(data, cost_bps_per_side=7.0):
    validate(data)
    reference, candidate = python_snapshots(data), sql.snapshots(data)
    reference_labels, candidate_labels = python_labels(data), sql.labels(data)
    assert_equal(reference, candidate)
    assert_equal(reference_labels, candidate_labels)
    audit_provenance(data, candidate)
    py_book = evaluate(data, reference, reference_labels, cost_bps_per_side)
    sql_book = evaluate(data, candidate, candidate_labels, cost_bps_per_side)
    if canonical_bytes(py_book) != canonical_bytes(sql_book):
        raise EquivalenceError("accounting outputs differ")
    mutations = []
    for name in sql.MUTATIONS:
        bad = sql.snapshots(data, mutation=name)
        try:
            assert_equal(reference, bad)
        except EquivalenceError as error:
            mutations.append({"mutation": name, "detected": True, "reason": str(error)})
        else:
            raise EquivalenceError("negative control survived: " + name)
    causal_checks = []
    for d in data["decisions"]:
        cutoff = instant(d["decision_at"])
        expected = [r for r in reference if r["decision_id"] == d["decision_id"]]
        changed = future_mutation(data, cutoff)
        for implementation in (python_snapshots, sql.snapshots):
            actual = [
                r
                for r in implementation(changed)
                if r["decision_id"] == d["decision_id"]
            ]
            assert_equal(expected, actual)
        causal_checks.append(
            {"decision_id": d["decision_id"], "python_and_sql_invariant": True}
        )
    changed = deepcopy(data)
    for row in changed["opens"]:
        row["open_cents"] += 777
    assert_equal(reference, python_snapshots(changed))
    assert_equal(reference, sql.snapshots(changed))
    sensitivity = {
        str(cost): {
            policy: stats["oos_net_return"]
            for policy, stats in evaluate(
                data, reference, reference_labels, cost
            ).items()
        }
        for cost in (0.0, 7.0, 20.0)
    }
    return {
        "artifact_version": "0.1.0",
        "data_class": "SYNTHETIC_ONLY",
        "seed": data["seed"],
        "fixture_canonical_sha256": fingerprint(data),
        "table_counts": {
            t: len(data[t]) for t in ("features", "memberships", "opens", "decisions")
        },
        "comparison": {
            "snapshot_rows": len(reference),
            "label_rows": len(reference_labels),
            "numeric_tolerance": 1e-12,
            "python_sql_equal": True,
            "portfolio_outputs_equal": True,
            "accounting_scope": "independent snapshots/labels; shared explicit accounting",
        },
        "split": split_plan(data),
        "cost_bps_per_side": cost_bps_per_side,
        "snapshots": reference,
        "labels": reference_labels,
        "policies": py_book,
        "cost_sensitivity_bps_per_side": sensitivity,
        "negative_controls": mutations,
        "future_data_checks": causal_checks,
        "label_to_signal_isolation": True,
        "limitations": [
            "Tiny synthetic partition, not economic OOS",
            "No fitted/tuned parameters",
            "Ex-post synthetic opens, zero market impact, daily round trips not netted",
            "No capacity, borrow, T+1, limits, lots, halt or corporate-action model",
            "No real alpha or production approval",
        ],
    }


def report_text(result):
    rows = [
        "# Synthetic PIT research results",
        "",
        "SYNTHETIC ONLY / NOT INVESTMENT PERFORMANCE / NO TRADE",
        "",
        f"Fixture canonical SHA-256: `{result['fixture_canonical_sha256']}`.",
        "",
        f"SQL/Python: {result['comparison']['snapshot_rows']} snapshots and {result['comparison']['label_rows']} labels match (tolerance1e-12).",
        "Portfolio outputs match using shared accounting, not two independent broker engines.",
        "",
        f"Mutation detection: {len(result['negative_controls'])}/{len(sql.MUTATIONS)}; future-data invariance: {len(result['future_data_checks'])} decision cutoffs in both implementations.",
        "Label perturbation does not alter either implementation's signals.",
        "",
        "## Calendar partition",
        "",
        "```json",
        json.dumps(result["split"], indent=2),
        "```",
        "",
        "## Three-decision synthetic OOS partition",
        "",
        "| Policy | Net return | Observations |",
        "| --- | ---: | ---: |",
    ]
    for name, stats in result["policies"].items():
        value = stats["oos_net_return"]
        rows.append(
            f"| {name} | {'MISSING' if value is None else format(value, '.6%')} | {stats['oos_observations']} |"
        )
    rows += [
        "",
        "Negative values are preserved. These hand-constructed data do not establish alpha,",
        "statistical significance, real OOS or generalization. Annualized Sharpe is NOT IDENTIFIABLE.",
        "",
        "## Cost sensitivity (return fraction, not percentage points)",
        "",
        "```json",
        json.dumps(result["cost_sensitivity_bps_per_side"], indent=2),
        "```",
        "",
        "Base cost7bps/side is a synthetic assumption (5commission +2slippage), not a venue fee.",
        "Each invested day opens and closes a unit gross book: turnover2; consecutive books are not netted.",
        "",
        "## Mutation diagnostics",
        "",
    ]
    rows += [
        "- " + r["mutation"] + ": DETECTED; " + r["reason"]
        for r in result["negative_controls"]
    ]
    rows += [
        "",
        "## Next bounded experiment",
        "",
        "Add a second predeclared synthetic fixture with different arrival lags and universe events.",
        "Do not tune on this result or treat passing software tests as a trading permission.",
        "",
    ]
    return "\n".join(rows)


def git_info():
    def query(*args):
        result = subprocess.run(
            ["git", *args], cwd=ROOT, capture_output=True, text=True, encoding="utf-8"
        )
        return result.stdout.strip() if result.returncode == 0 else None

    return {
        "head": query("rev-parse", "HEAD"),
        "dirty": bool(query("status", "--porcelain")),
        "note": "Source HEAD and content hashes at run time; output receipt commit is separate",
    }


def write_run(fixture, output, cost_bps_per_side=7.0):
    fixture, output = Path(fixture), Path(output)
    if output.exists():
        raise FileExistsError("output exists; choose a fresh run directory")
    data = json.loads(fixture.read_text(encoding="utf-8"))
    start, began, git = (
        time.perf_counter(),
        datetime.now(timezone.utc).isoformat(),
        git_info(),
    )
    result = experiment(data, cost_bps_per_side)
    import duckdb

    logic = [
        HERE / name
        for name in (
            "model.py",
            "duckdb_backend.py",
            "fixtures.py",
            "run.py",
            "requirements.txt",
            "verify_run.py",
        )
    ]
    logic += sorted((HERE / "sql").glob("*.sql"))
    manifest = {
        "artifact_version": "0.1.0",
        "started_at_utc": began,
        "finished_at_utc": datetime.now(timezone.utc).isoformat(),
        "wall_seconds_observed_single_run": time.perf_counter() - start,
        "git": git,
        "environment": {
            "python": platform.python_version(),
            "duckdb": duckdb.__version__,
            "os": platform.platform(),
        },
        "connection": {
            "threads": 1,
            "memory_limit": "128MB",
            "external_access": False,
            "process_rss": "UNMEASURED; memory_limit is not a process-RSS cap",
        },
        "input": {
            "name": fixture.name,
            "byte_sha256": hashlib.sha256(fixture.read_bytes()).hexdigest(),
            "canonical_sha256": fingerprint(data),
            "class": "SYNTHETIC_ONLY",
        },
        "code_sha256": {
            str(p.relative_to(HERE))
            .replace("\\", "/"): hashlib.sha256(p.read_bytes())
            .hexdigest()
            for p in logic
        },
        "parameters": {
            "cost_bps_per_side": cost_bps_per_side,
            "top_k": 1,
            "embargo_minutes": 60,
        },
        "run_command": "python -m examples.duckdb_pit_research.run --output <fresh-directory>",
        "results_sha256": hashlib.sha256(canonical_bytes(result)).hexdigest(),
        "rights": "Original synthetic fixture; no market/vendor/private data",
        "scientific_validity": "NOT MET",
        "production": "NO_GO",
    }
    output.mkdir(parents=True, exist_ok=False)
    (output / "RESULTS.json").write_bytes(canonical_bytes(result))
    (output / "RESEARCH_REPORT.md").write_text(
        report_text(result), encoding="utf-8", newline="\n"
    )
    manifest["output_sha256"] = {
        name: hashlib.sha256((output / name).read_bytes()).hexdigest()
        for name in ("RESULTS.json", "RESEARCH_REPORT.md")
    }
    (output / "RUN_MANIFEST.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8", newline="\n"
    )
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixture", type=Path, default=FIXTURE)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--cost-bps-per-side", type=float, default=7.0)
    args = parser.parse_args()
    try:
        result = write_run(args.fixture, args.output, args.cost_bps_per_side)
    except (ContractError, EquivalenceError, OSError, ValueError, RuntimeError) as exc:
        parser.exit(2, "research error: " + str(exc) + "\n")
    print(
        json.dumps(
            {
                "status": "ENGINEERING_CHECKS_PASS_SYNTHETIC_ONLY",
                "snapshots": result["comparison"]["snapshot_rows"],
                "mutations_detected": len(result["negative_controls"]),
                "top1_synthetic_oos_return": result["policies"]["positive_top1"][
                    "oos_net_return"
                ],
            }
        )
    )


if __name__ == "__main__":
    main()
