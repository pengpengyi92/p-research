"""Offline byte-integrity checks for a run, not economic validity or signatures."""

import argparse
import hashlib
import json
from pathlib import Path

from .model import fingerprint

HERE = Path(__file__).parent


def verify_run(output, fixture=HERE / "fixtures/synthetic_v1.json"):
    output, fixture = Path(output), Path(fixture)
    manifest = json.loads((output / "RUN_MANIFEST.json").read_text(encoding="utf-8"))
    data = fixture.read_bytes()
    if hashlib.sha256(data).hexdigest() != manifest["input"]["byte_sha256"]:
        raise ValueError("fixture byte hash mismatch")
    if fingerprint(json.loads(data)) != manifest["input"]["canonical_sha256"]:
        raise ValueError("fixture canonical hash mismatch")
    for path, expected in manifest["code_sha256"].items():
        relative = Path(path)
        if relative.is_absolute() or ".." in relative.parts:
            raise ValueError("unsafe code path")
        if hashlib.sha256((HERE / relative).read_bytes()).hexdigest() != expected:
            raise ValueError("source code hash mismatch: " + path)
    if set(manifest["output_sha256"]) != {"RESULTS.json", "RESEARCH_REPORT.md"}:
        raise ValueError("unexpected output inventory")
    for name, expected in manifest["output_sha256"].items():
        if hashlib.sha256((output / name).read_bytes()).hexdigest() != expected:
            raise ValueError("output hash mismatch: " + name)
    return {
        "status": "PASS_RUN_BYTE_INTEGRITY",
        "source_head": manifest["git"]["head"],
        "source_files": len(manifest["code_sha256"]),
        "outputs": 2,
        "scope": "Pinned byte comparison; not a signature, scientific alpha validation or learner assessment",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", type=Path, required=True)
    parser.add_argument(
        "--fixture", type=Path, default=HERE / "fixtures/synthetic_v1.json"
    )
    args = parser.parse_args()
    print(json.dumps(verify_run(args.run, args.fixture), indent=2))


if __name__ == "__main__":
    main()
