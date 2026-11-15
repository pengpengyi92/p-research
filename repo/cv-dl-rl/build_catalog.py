"""Render role-specific cross-lists from a byte-preserved public P-ML snapshot."""
import argparse
from datetime import datetime
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
CAT = ROOT / "repo" / "cv-dl-rl"
SOURCE_SHA256 = "2867982492edd317a0d0c6ce9bec1584e66acc11d946ac0e8d58deae2eaf9478"
SOURCE_COMMIT = "f0492b80f9f97527926b7aa1cb1290c2ef73699b"
CATEGORIES = {"computer-vision": "Computer Vision", "deep-learning": "Deep Learning", "reinforcement-learning": "Reinforcement Learning"}
PROFILES = {"P-CSDSAI": "systems", "P-Research": "research"}


def validate_data(snapshot, view):
    if PROFILES.get(view["project"]) != view["profile"]:
        raise ValueError("Project/profile mismatch")
    if view.get("complete_ecosystem_inventory") is not False or view["status"] != "REFERENCE_ONLY / NOT_RUN":
        raise ValueError("Reference scope cannot become a completeness/result claim")
    imported = datetime.fromisoformat(view["imported_at"])
    if imported.utcoffset() is None or imported.utcoffset().total_seconds() != 28800:
        raise ValueError("Asia/Shanghai timestamp required")
    provenance = view["provenance"]
    if provenance["commit"] != SOURCE_COMMIT or provenance["sha256"] != SOURCE_SHA256:
        raise ValueError("Frozen public source identity changed")
    sources, annotations = snapshot["entries"], view["entries"]
    if len(sources) != 43 or len(annotations) != 43:
        raise ValueError("Fixed43-project cross-list required")
    names = [row["repository"].casefold() for row in sources]
    authored = [row["repository"].casefold() for row in annotations]
    if len(set(names)) != 43 or len(set(authored)) != 43 or set(names) != set(authored):
        raise ValueError("Duplicate or mismatched repository identities")
    for row in sources:
        if row["private"] or row["fork"]:
            raise ValueError("Only captured public primary sources may enter this view")
        if not set(row["categories"]) <= CATEGORIES.keys():
            raise ValueError("Unknown source category")
        for key in ("metadata_observed_at", "sources_observed_at"):
            if datetime.fromisoformat(row[key]) > imported:
                raise ValueError("Import predates captured source observation")
    for row in annotations:
        if not all(isinstance(row.get(key), str) and row[key].strip() for key in ("question", "baseline", "measure")):
            raise ValueError("Question, independent baseline and measurement required")
        if row["result"] != "NOT_RUN" or row["gain"] != "UNMEASURED":
            raise ValueError("Curation cannot become a measured experiment")
        for href in row["existing_links"]:
            target = (CAT / href).resolve()
            if not target.is_relative_to(ROOT.resolve()) or not target.is_file():
                raise ValueError("Existing cross-link escapes or is absent")


def load():
    data = (CAT / "pml_snapshot.json").read_bytes()
    if hashlib.sha256(data).hexdigest() != SOURCE_SHA256:
        raise ValueError("Imported source bytes differ from public provenance")
    snapshot = json.loads(data.decode("utf-8"))
    view = json.loads((CAT / "view.json").read_text(encoding="utf-8"))
    validate_data(snapshot, view)
    return snapshot, view


def cell(value):
    return str(value).replace("|", "\\|").replace("\n", " ")


def outputs():
    snapshot, view = load()
    by_name = {row["repository"]: row for row in view["entries"]}
    result = {}
    for category, title in CATEGORIES.items():
        chosen = [row for row in snapshot["entries"] if category in row["categories"]]
        lines = [
            "# " + view["project"] + " · " + title,
            "",
            "**View:** `" + view["profile"] + "`. **Selected:** " + str(len(chosen)) + ".",
            "**Imported:** `" + view["imported_at"] + "`; upstream observation times remain in the unchanged public snapshot.",
            "",
            "Original target-specific questions, not executed experiments. **NOT_RUN / UNMEASURED**.",
            "[Index](README.md) · [Protocol and provenance](METHOD.md) · [Source metadata](pml_snapshot.json) · [View annotations](view.json)",
            "",
            "| Project / role | 本仓库的问题 | Baseline /拟测量 | 来源、许可与边界 |",
            "| --- | --- | --- | --- |",
        ]
        for row in chosen:
            note = by_name[row["repository"]]
            pins = " · ".join("[" + source["path"] + "](" + source["url"] + ")" for source in row["sources"])
            state = "ARCHIVED" if row["archived"] else "not archived; support not established"
            rights = (row["license_signal"] or "unclassified") + " / " + row["license_class"]
            if row.get("source_review_note"):
                rights += " / " + row["source_review_note"]
            if row["reuse_policy"] == "reference-only-license-clarification":
                rights += " / REFERENCE ONLY: CLARIFY LICENSE"
            existing = ""
            if note["existing_links"]:
                existing = " · " + " · ".join("[已有导读](" + href + ")" for href in note["existing_links"])
            lines.append(
                "| [" + row["repository"] + "](" + row["url"] + ") · `" + cell(row["role"]) + "`" + existing
                + " | " + cell(note["question"])
                + " | Baseline: " + cell(note["baseline"]) + "; Measure: " + cell(note["measure"])
                + " | " + pins + "; " + cell(state + " / " + rights) + "; " + cell(row["boundary"]) + " |"
            )
        result[category + ".md"] = "\n".join(lines) + "\n"
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    expected = outputs()
    if args.check:
        bad = [name for name, content in expected.items()
               if not (CAT / name).exists() or (CAT / name).read_bytes() != content.encode("utf-8")]
        if bad:
            raise SystemExit("Stale/missing generated pages: " + ", ".join(bad))
    else:
        for name, content in expected.items():
            (CAT / name).write_text(content, encoding="utf-8", newline="\n")
    print("PASS: " + str(len(expected)) + " pages,43 projects, byte-preserved public source, no upstream execution")


if __name__ == "__main__":
    main()
