import copy
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
FOLDER = ROOT / "skills" / "jane-street-socratic-tutor"
SPEC = importlib.util.spec_from_file_location("jane_street_snapshot", FOLDER / "verify_snapshot.py")
VERIFIER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VERIFIER)


class JaneStreetSnapshotTests(unittest.TestCase):
    def setUp(self):
        self.manifest = json.loads((FOLDER / "SOURCE_MANIFEST.json").read_text(encoding="utf-8"))

    def fixture(self):
        cache = ROOT / ".cache" / "snapshot-tests"
        cache.mkdir(parents=True, exist_ok=True)
        temp = tempfile.TemporaryDirectory(dir=cache)
        self.addCleanup(temp.cleanup)
        target = Path(temp.name) / "snapshot"
        shutil.copytree(FOLDER / "upstream", target)
        return target

    def test_exact_snapshot(self):
        result = VERIFIER.verify(FOLDER / "upstream", self.manifest)
        self.assertEqual(result["files_verified"], 6)
        self.assertEqual(result["behavioral_evaluation"], "NOT RUN")

    def test_pinned_origin(self):
        upstream = self.manifest["upstream"]
        self.assertEqual(upstream["repository"], "janestreet/agent_skills")
        self.assertEqual(upstream["commit_sha1"], "7c6715c29548a3b39d4a9545c698ee4fd17a7213")
        self.assertEqual(upstream["root_tree_sha1"], "6dd590cb153ac1e0073914cb2e89029d9fdef04e")
        self.assertEqual(self.manifest["modifications_to_upstream"], "NONE")

    def test_license_preserves_jane_street_copyright(self):
        text = (FOLDER / "upstream" / "LICENSE.md").read_text(encoding="utf-8")
        self.assertIn("Jane Street Group, LLC", text)
        self.assertIn("The MIT License", text)

    def test_changed_skill_is_rejected(self):
        target = self.fixture()
        skill = target / "socratic-tutor" / "SKILL.md"
        skill.write_bytes(skill.read_bytes() + b"\nchanged\n")
        with self.assertRaisesRegex(ValueError, "content mismatch"):
            VERIFIER.verify(target, self.manifest)

    def test_missing_license_is_rejected(self):
        target = self.fixture()
        (target / "LICENSE.md").unlink()
        with self.assertRaisesRegex(ValueError, "inventory mismatch"):
            VERIFIER.verify(target, self.manifest)

    def test_extra_file_is_rejected(self):
        target = self.fixture()
        (target / "unexpected.txt").write_bytes(b"extra")
        with self.assertRaisesRegex(ValueError, "inventory mismatch"):
            VERIFIER.verify(target, self.manifest)

    def test_path_escape_is_rejected(self):
        self.manifest["files"][0]["path"] = "../outside"
        with self.assertRaisesRegex(ValueError, "unsafe"):
            VERIFIER.verify(FOLDER / "upstream", self.manifest)

    def test_duplicate_manifest_entry_is_rejected(self):
        self.manifest["files"].append(copy.deepcopy(self.manifest["files"][0]))
        with self.assertRaisesRegex(ValueError, "duplicate"):
            VERIFIER.verify(FOLDER / "upstream", self.manifest)

    def test_executable_mode_is_not_silently_accepted(self):
        self.manifest["files"][0]["mode"] = "100755"
        with self.assertRaisesRegex(ValueError, "unsupported"):
            VERIFIER.verify(FOLDER / "upstream", self.manifest)

    def test_git_empty_blob_golden(self):
        self.assertEqual(VERIFIER.git_object_id("blob", b""), "e69de29bb2d1d6434b8b29ae775ad8c2e48c5391")

    def test_git_empty_tree_golden(self):
        self.assertEqual(VERIFIER.git_tree_id([]), "4b825dc642cb6eb9a060e54bf8d69288fbee4904")

    def test_tree_order_is_canonical(self):
        self.assertEqual(VERIFIER.git_tree_id(self.manifest["files"]),
                         VERIFIER.git_tree_id(list(reversed(self.manifest["files"]))))

    def test_nested_git_metadata_is_rejected(self):
        target = self.fixture()
        (target / ".git").mkdir()
        with self.assertRaisesRegex(ValueError, "Git metadata"):
            VERIFIER.verify(target, self.manifest)


if __name__ == "__main__":
    unittest.main()
