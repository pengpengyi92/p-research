"""Offline invariants for the public research catalogue, not external code."""
import json
from pathlib import Path
import unittest


FOLDER = Path(__file__).resolve().parents[1] / "docs/research/2026-11-13-quant-python-sql-repos"


class QuantPythonSQLCatalogueTests(unittest.TestCase):
    def setUp(self):
        self.catalogue = json.loads((FOLDER / "REPOSITORY_SOURCES.json").read_text(encoding="utf-8"))

    def test_fixed_shortlist_has_ten_unique_repository_identities(self):
        repositories = self.catalogue["repositories"]
        self.assertEqual(len(repositories), 10)
        self.assertEqual(len({item["repository"] for item in repositories}), 10)

    def test_metadata_has_primary_urls_and_observation_times(self):
        for item in self.catalogue["repositories"]:
            with self.subTest(repository=item["repository"]):
                self.assertEqual(item["url"], "https://github.com/" + item["repository"])
                self.assertEqual(item["source"], "https://api.github.com/repos/" + item["repository"])
                self.assertTrue(item["observed_at_utc"])
                self.assertIsInstance(item["archived"], bool)
                self.assertTrue(item["license_spdx_metadata"])

    def test_both_different_bt_projects_are_identified(self):
        names = {item["repository"] for item in self.catalogue["repositories"]}
        self.assertIn("mementum/backtrader", names)
        self.assertIn("pmorissette/bt", names)

    def test_delivery_documents_exist(self):
        for name in ("README.md", "SOURCES.md", "VALIDATION.md", "TRAINING_PLAN.md", "BENCHMARK_CARD.md"):
            self.assertTrue((FOLDER / name).is_file(), name)

    def test_pinned_fix_and_untested_limits_are_visible(self):
        text = (FOLDER / "VALIDATION.md").read_text(encoding="utf-8")
        self.assertIn("37452621f549ba121e6fbe1063d92a8301c2d9ad", text)
        self.assertIn("NOT RUN", text)
        self.assertIn("1,216 PASS", text)


if __name__ == "__main__":
    unittest.main()
