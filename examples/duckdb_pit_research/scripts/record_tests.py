"""Immutable, public-safe test command receipts for this optional example."""

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform
import re
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parents[1]


def git_value(*args):
    result = subprocess.run(
        ["git", *args], cwd=ROOT, capture_output=True, text=True, encoding="utf-8"
    )
    return result.stdout.strip() if result.returncode == 0 else None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--label", required=True)
    parser.add_argument("--suite", choices=["core", "example", "tutor"], required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if not re.fullmatch(r"[a-z0-9-]+", args.label):
        parser.error("safe label required")
    args.output.mkdir(parents=True, exist_ok=True)
    log, receipt = args.output / (args.label + ".txt"), args.output / (
        args.label + ".json"
    )
    if log.exists() or receipt.exists():
        parser.error("receipt exists; preserve previous runs")
    command = ["-X", "utf8", "-m", "unittest", "discover", "-s", "tests"]
    if args.suite == "example":
        command = [
            "-X",
            "utf8",
            "-m",
            "unittest",
            "discover",
            "-s",
            "examples/duckdb_pit_research/tests",
            "-v",
        ]
    elif args.suite == "tutor":
        command += ["-p", "test_jane_street_socratic_tutor.py", "-v"]
    started = datetime.now(timezone.utc).isoformat()
    head, dirty_before = git_value("rev-parse", "HEAD"), bool(
        git_value("status", "--porcelain")
    )
    result = subprocess.run(
        [sys.executable, *command],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=180,
    )
    output = (result.stdout + result.stderr).replace("\r\n", "\n")
    for path, replacement in [
        (str(ROOT), "[REPO]"),
        (str(Path(tempfile.gettempdir())), "[TEMP]"),
        (sys.base_prefix, "[PYTHON]"),
    ]:
        output = output.replace(path, replacement)
    output = re.sub(r"[A-Za-z]:[\\/][^\n\r\"']*", "[HOST_PATH]", output)
    log.write_text(output, encoding="utf-8", newline="\n")
    count = re.search(r"Ran (\d+) tests?", output)
    failures = re.search(r"FAILED \((.*?)\)", output)
    details = dict(
        (name, int(number))
        for name, number in re.findall(r"(failures|errors|skipped)=(\d+)", output)
    )
    total = int(count[1]) if count else None
    try:
        import duckdb

        version = duckdb.__version__
    except ImportError:
        version = "NOT_INSTALLED"
    value = {
        "git": {
            "head": head,
            "dirty_before": dirty_before,
            "dirty_after_test_before_receipt": bool(git_value("status", "--porcelain")),
        },
        "input_fixture_sha256": hashlib.sha256(
            (HERE / "fixtures/synthetic_v1.json").read_bytes()
        ).hexdigest(),
        "test_sources_sha256": {
            path.relative_to(ROOT)
            .as_posix(): hashlib.sha256(path.read_bytes())
            .hexdigest()
            for path in sorted(
                (HERE / "tests" if args.suite == "example" else ROOT / "tests").glob(
                    "test*.py"
                )
            )
        },
        "started_at_utc": started,
        "finished_at_utc": datetime.now(timezone.utc).isoformat(),
        "environment": {
            "python": platform.python_version(),
            "duckdb": version,
            "os": platform.platform(),
        },
        "command": "python " + " ".join(command),
        "exit_code": result.returncode,
        "total": total,
        "failures": details.get("failures", 0),
        "errors": details.get("errors", 0),
        "skipped": details.get("skipped", 0),
        "passed": total - sum(details.values()) if total is not None else None,
        "observed_summary": (
            failures[0] if failures else "OK" if result.returncode == 0 else "NONZERO"
        ),
        "log_sha256": hashlib.sha256(log.read_bytes()).hexdigest(),
        "redactions": "repo, interpreter, temporary and host paths replaced; no private raw logs published",
    }
    receipt.write_text(
        json.dumps(value, indent=2) + "\n", encoding="utf-8", newline="\n"
    )
    print(json.dumps(value, indent=2))
    print(output[-900:])
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
