"""Offline contracts for role-specific public cross-lists, not model evaluation."""
from copy import deepcopy
from datetime import datetime
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import unittest
from unittest.mock import patch
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
CAT = ROOT / "repo" / "cv-dl-rl"
SPEC = importlib.util.spec_from_file_location("focus_crosslist_builder", CAT / "build_catalog.py")
BUILDER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BUILDER)
LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)\s]+)\)")


class CrossListTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.snapshot, cls.view = BUILDER.load()
        cls.rows = cls.snapshot["entries"]
        cls.annotations = cls.view["entries"]

    def test_schema_project_profile_and_reference_scope(self):
        self.assertEqual(self.view["schema_version"], 1)
        self.assertEqual(BUILDER.PROFILES[self.view["project"]], self.view["profile"])
        self.assertFalse(self.view["complete_ecosystem_inventory"])
        self.assertEqual(self.view["status"], "REFERENCE_ONLY / NOT_RUN")

    def test_public_provenance_byte_hash_and_frozen_identity(self):
        self.assertEqual(hashlib.sha256((CAT / "pml_snapshot.json").read_bytes()).hexdigest(), BUILDER.SOURCE_SHA256)
        self.assertEqual(self.view["provenance"]["commit"], BUILDER.SOURCE_COMMIT)
        self.assertIn(BUILDER.SOURCE_COMMIT, self.view["provenance"]["snapshot_url"])
        self.assertEqual(self.view["provenance"]["path"], "ml-repo/cv-dl-rl/snapshot.json")

    def test_unique43_and_category_counts(self):
        self.assertEqual(len(self.rows), 43)
        self.assertEqual(len({r["repository"].casefold() for r in self.rows}), 43)
        counts = {k: sum(k in r["categories"] for r in self.rows) for k in BUILDER.CATEGORIES}
        self.assertEqual(counts, {"computer-vision": 16, "deep-learning": 11, "reinforcement-learning": 16})

    def test_target_specific_questions_not_copied_learning_notes(self):
        source = {r["repository"]: r for r in self.rows}
        self.assertEqual(len({r["question"] for r in self.annotations}), 43)
        for row in self.annotations:
            self.assertNotEqual(row["question"], source[row["repository"]]["use"])
            for key in ("question", "baseline", "measure"):
                self.assertTrue(row[key].strip())
            self.assertEqual(row["result"], "NOT_RUN")
            self.assertEqual(row["gain"], "UNMEASURED")
        opencv = next(r for r in self.annotations if r["repository"] == "opencv/opencv")
        token = "接口" if self.view["profile"] == "systems" else "增益"
        self.assertIn(token, opencv["question"])

    def test_existing_three_ai_infra_projects_crosslink_not_new_cards(self):
        linked = {r["repository"] for r in self.annotations if r["existing_links"]}
        self.assertEqual(linked, {"deepspeedai/DeepSpeed", "pytorch/torchtitan", "NVIDIA/Megatron-LM"})
        for row in self.annotations:
            for href in row["existing_links"]:
                self.assertTrue((CAT / href).resolve().is_file())

    def test_primary_pins_original_times_and_public_only(self):
        imported = datetime.fromisoformat(self.view["imported_at"])
        count = 0
        for row in self.rows:
            self.assertFalse(row["private"])
            self.assertFalse(row["fork"])
            self.assertRegex(row["head"], r"^[a-f0-9]{40}$")
            for key in ("metadata_observed_at", "sources_observed_at"):
                time = datetime.fromisoformat(row[key])
                self.assertEqual(time.utcoffset().total_seconds(), 28800)
                self.assertLessEqual(time, imported)
            for source in row["sources"]:
                count += 1
                self.assertIn("/blob/" + row["head"] + "/", source["url"])
                self.assertRegex(source["sha256"], r"^[a-f0-9]{64}$")
        self.assertEqual(count, 89)

    def test_generated_pages_include_all89_exact_pins(self):
        seen = set()
        for key in BUILDER.CATEGORIES:
            text = (CAT / (key + ".md")).read_text(encoding="utf-8")
            for row in self.rows:
                if key in row["categories"]:
                    for source in row["sources"]:
                        self.assertIn(source["url"], text)
                        seen.add(source["url"])
        self.assertEqual(len(seen), 89)

    def test_rights_and_maintenance_not_flattened_away(self):
        rows = {r["repository"]: r for r in self.rows}
        self.assertEqual(sum(r["archived"] for r in self.rows), 2)
        self.assertEqual(sum(r["license_signal"] == "NOASSERTION" for r in self.rows), 9)
        self.assertEqual(rows["Farama-Foundation/Minigrid"]["reuse_policy"], "reference-only-license-clarification")
        self.assertIn("modified MIT", rows["d2l-ai/d2l-en"]["source_review_note"])
        self.assertEqual(rows["ultralytics/ultralytics"]["license_class"], "reciprocal-signal-review-text")

    def test_local_links_public_patterns_and_lf(self):
        allowed = {s["url"] for r in self.rows for s in r["sources"]}
        for path in list(CAT.glob("*.md")) + list(CAT.glob("*.json")):
            self.assertNotIn(b"\r", path.read_bytes(), path.name)
            text = path.read_text(encoding="utf-8")
            for pattern in (r"(?<![A-Za-z0-9])[A-Za-z]:[/\\]", r"github_pat_[A-Za-z0-9_]{30,}", r"gh[pousr]_[A-Za-z0-9]{30,}", r"file://"):
                self.assertIsNone(re.search(pattern, text), path.name)
            if path.suffix != ".md":
                continue
            for href in LINK.findall(text):
                if href.startswith("https://github.com/") and "/blob/" in href and "/pengpengyi92/P-ML/" not in href:
                    self.assertIn(href, allowed)
                elif not re.match(r"[a-z]+:", href) and not href.startswith("#"):
                    target = (path.parent / unquote(href.split("#", 1)[0])).resolve()
                    self.assertTrue(target.is_relative_to(ROOT.resolve()))
                    self.assertTrue(target.is_file(), (path, href))

    def test_deterministic_output_and_no_stale_pages(self):
        for name, expected in BUILDER.outputs().items():
            self.assertEqual((CAT / name).read_bytes(), expected.encode("utf-8"))

    def test_changed_imported_source_bytes_are_rejected(self):
        with patch.object(Path, "read_bytes", return_value=b"changed source"):
            with self.assertRaises(ValueError):
                BUILDER.load()

    def test_private_or_fork_source_negative_controls(self):
        for key in ("private", "fork"):
            data = deepcopy(self.snapshot)
            data["entries"][0][key] = True
            with self.assertRaises(ValueError):
                BUILDER.validate_data(data, self.view)

    def test_duplicate_and_identity_mismatch_negative_controls(self):
        data = deepcopy(self.view)
        data["entries"][1]["repository"] = data["entries"][0]["repository"]
        with self.assertRaises(ValueError):
            BUILDER.validate_data(self.snapshot, data)
        data["entries"][1]["repository"] = "unknown/unknown"
        with self.assertRaises(ValueError):
            BUILDER.validate_data(self.snapshot, data)

    def test_wrong_profile_or_completeness_is_rejected(self):
        data = deepcopy(self.view)
        data["profile"] = "research" if data["profile"] == "systems" else "systems"
        with self.assertRaises(ValueError):
            BUILDER.validate_data(self.snapshot, data)
        data = deepcopy(self.view)
        data["complete_ecosystem_inventory"] = True
        with self.assertRaises(ValueError):
            BUILDER.validate_data(self.snapshot, data)

    def test_result_promotion_is_rejected(self):
        data = deepcopy(self.view)
        data["entries"][0]["result"] = "MEASURED_WIN"
        with self.assertRaises(ValueError):
            BUILDER.validate_data(self.snapshot, data)
        data["entries"][0]["result"] = "NOT_RUN"
        data["entries"][0]["gain"] = "10% faster"
        with self.assertRaises(ValueError):
            BUILDER.validate_data(self.snapshot, data)

    def test_wrong_timestamp_or_future_observation_is_rejected(self):
        view = deepcopy(self.view)
        view["imported_at"] = "2020-01-01T00:00:00+08:00"
        with self.assertRaises(ValueError):
            BUILDER.validate_data(self.snapshot, view)
        view["imported_at"] = "2026-11-15T00:00:00"
        with self.assertRaises(ValueError):
            BUILDER.validate_data(self.snapshot, view)

    def test_path_escape_and_missing_baseline_are_rejected(self):
        data = deepcopy(self.view)
        data["entries"][0]["existing_links"] = ["../../../../outside.md"]
        with self.assertRaises(ValueError):
            BUILDER.validate_data(self.snapshot, data)
        data = deepcopy(self.view)
        data["entries"][0]["baseline"] = ""
        with self.assertRaises(ValueError):
            BUILDER.validate_data(self.snapshot, data)

    def test_no_upstream_network_or_external_imports_in_generator(self):
        import ast
        tree = ast.parse((CAT / "build_catalog.py").read_text(encoding="utf-8"))
        modules = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                modules.update(n.name.split(".")[0] for n in node.names)
            elif isinstance(node, ast.ImportFrom):
                modules.add(node.module.split(".")[0])
        self.assertEqual(modules, {"argparse", "datetime", "hashlib", "json", "pathlib", "re"})
        self.assertNotIn("subprocess", modules)


if __name__ == "__main__":
    unittest.main()
