"""Offline byte/Git-object verification, not a test of tutor effectiveness."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath

HERE = Path(__file__).resolve().parent


def git_object_id(kind: str, data: bytes) -> str:
    return hashlib.sha1(f"{kind} {len(data)}\0".encode("ascii") + data).hexdigest()


def git_tree_id(entries: list[dict]) -> str:
    nodes = {}
    for entry in entries:
        parts = PurePosixPath(entry["path"]).parts
        cursor = nodes
        for part in parts[:-1]:
            node = cursor.setdefault(part, {})
            if not isinstance(node, dict):
                raise ValueError("file/directory collision")
            cursor = node
        if parts[-1] in cursor:
            raise ValueError("duplicate file/directory path")
        cursor[parts[-1]] = (entry["mode"], entry["git_blob_sha1"])

    def walk(folder):
        children = []
        for name, value in folder.items():
            mode, oid = ("40000", walk(value)) if isinstance(value, dict) else value
            sort_key = name.encode("utf-8") + (b"/" if mode == "40000" else b"")
            raw = mode.encode("ascii") + b" " + name.encode("utf-8") + b"\0" + bytes.fromhex(oid)
            children.append((sort_key, raw))
        return git_object_id("tree", b"".join(raw for _, raw in sorted(children)))

    return walk(nodes)


def verify(snapshot: Path, manifest: dict) -> dict:
    expected = {}
    for entry in manifest["files"]:
        relative = entry["path"]
        path = PurePosixPath(relative)
        if (not path.parts or path.is_absolute() or ".." in path.parts
                or ".git" in path.parts or "\\" in relative or ":" in relative):
            raise ValueError("unsafe snapshot path")
        if relative in expected:
            raise ValueError("duplicate manifest path")
        if entry["mode"] != "100644":
            raise ValueError("unsupported snapshot file mode")
        expected[relative] = entry
    actual = {}
    for path in snapshot.rglob("*"):
        if path.is_symlink() or ".git" in path.relative_to(snapshot).parts:
            raise ValueError("nested Git metadata or symlink in snapshot")
        if path.is_file():
            actual[path.relative_to(snapshot).as_posix()] = path
    if set(expected) != set(actual):
        raise ValueError("snapshot inventory mismatch")
    for relative, entry in expected.items():
        data = actual[relative].read_bytes()
        if (len(data) != entry["size_bytes"]
                or hashlib.sha256(data).hexdigest() != entry["sha256"]
                or git_object_id("blob", data) != entry["git_blob_sha1"]):
            raise ValueError(f"snapshot content mismatch: {relative}")
    tree = git_tree_id(list(expected.values()))
    if tree != manifest["upstream"]["root_tree_sha1"]:
        raise ValueError("snapshot Git tree mismatch")
    return {"status": "PASS_SNAPSHOT_INTEGRITY", "files_verified": len(expected),
            "upstream_commit": manifest["upstream"]["commit_sha1"],
            "root_tree_sha1": tree, "behavioral_evaluation": "NOT RUN"}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--snapshot", type=Path, default=HERE / "upstream")
    parser.add_argument("--manifest", type=Path, default=HERE / "SOURCE_MANIFEST.json")
    args = parser.parse_args()
    try:
        result = verify(args.snapshot, json.loads(args.manifest.read_text(encoding="utf-8")))
    except (ValueError, KeyError, OSError) as error:
        parser.exit(1, f"Snapshot verification failed: {error}\n")
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
