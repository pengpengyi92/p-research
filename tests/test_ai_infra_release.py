"""Validate the released taxonomy, verified public source metadata and disclosure scope."""
from datetime import datetime, timedelta
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
CAT = ROOT / "repo" / "ai-infra"
DOC = ROOT / "paper" / "ai-infra"
NEW_FILES = [CAT / "README.md", CAT / "catalog.json", DOC / "working-paper.md", DOC / "article.md"]


class AIInfraReleaseTests(unittest.TestCase):
    def test_seven_layers_and_exact_public_snapshot(self):
        catalog = json.loads((CAT / "catalog.json").read_text(encoding="utf-8"))
        self.assertEqual(catalog["status"], "REFERENCE_ONLY / NOT_RUN")
        self.assertEqual(datetime.fromisoformat(catalog["observed_at"]).utcoffset(), timedelta(hours=8))
        self.assertEqual([layer["id"] for layer in catalog["layers"]], [f"L{i}" for i in range(1, 8)])
        entries = [entry for layer in catalog["layers"] for entry in layer["entries"]]
        self.assertTrue(all(len(layer["entries"]) == 4 for layer in catalog["layers"]))
        self.assertEqual(len({entry["repository"].lower() for entry in entries}), 28)
        text = (CAT / "README.md").read_text(encoding="utf-8")
        for entry in entries:
            with self.subTest(entry=entry["repository"]):
                self.assertTrue(entry["reference_only"])
                self.assertRegex(entry["commit"], r"^[0-9a-f]{40}$")
                self.assertEqual(entry["url"], "https://github.com/" + entry["repository"])
                self.assertTrue(entry["entry_paths"])
                for path in [entry["readme_path"], entry["license_path"], *entry["entry_paths"]]:
                    self.assertNotIn("..", Path(path).parts)
                    self.assertIn(entry["url"] + "/blob/" + entry["commit"] + "/" + path, text)
                if entry["existing_card"]:
                    self.assertTrue((CAT / entry["existing_card"]).is_file())

    def test_public_provenance_without_private_urls(self):
        for file in NEW_FILES:
            with self.subTest(file=file.name):
                text = file.read_text(encoding="utf-8")
                self.assertIn("Selected shared from P University", text)
                self.assertIn("PINF", text)
                self.assertIn("P Compute", text)
                self.assertNotRegex(text, r"(?i)github\.com/pengpengyi92/(?:p[-_]?university|pinf|p[-_]?compute|p-dd)(?:/|\b)")
                self.assertNotRegex(text, r"(?<![A-Za-z0-9])[A-Za-z]:[/\\]")
                if file.suffix == ".md":
                    for path in re.findall(r"\[[^\]]+\]\(([^)\s]+)\)", text):
                        if not path.startswith(("https://", "#")):
                            target = (file.parent / path).resolve()
                            self.assertTrue(target.is_relative_to(ROOT) and target.is_file(), path)
