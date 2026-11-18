import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SHA = "68463dd562640ada92a9dbbb1a1a5091b0811866"


class AutoSwarmAITests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog = json.loads((ROOT / "repo/catalog.json").read_text("utf-8"))
        cls.entries = [e for e in cls.catalog["entries"] if e["source"]["repository"] == "HKUDS/AutoSwarm"]

    def test_one_entry_and_ai_category(self):
        self.assertEqual(len(self.entries), 1)
        entry = self.entries[0]
        self.assertEqual(entry["category"], "ai-agents-and-swarms")
        self.assertIn("AI", entry["tags"])
        self.assertEqual(entry["card"], "ai/agents-and-swarms/autoswarm.md")
        self.assertEqual(len(self.catalog["entries"]), 11 if self.catalog["profile"] == "systems" else 12)

    def test_pinned_development_source_without_runtime_claim(self):
        source = self.entries[0]["source"]
        self.assertEqual(source["head"], SHA)
        self.assertEqual(source["package_version"], "2.0.0.dev0")
        self.assertFalse(source["private"])
        self.assertEqual(source["runtime_evaluation"], "NOT RUN in this catalog task")
        self.assertFalse(source["missing_candidates"])
        self.assertEqual(source["license_signal"], "MIT")
        for path in source["entry_paths"]:
            self.assertRegex(source["verified_objects"][path]["git_blob"], r"^[a-f0-9]{40}$")
        text = (ROOT / "repo" / self.entries[0]["card"]).read_text("utf-8")
        self.assertIn("NOT RUN / UNMEASURED", text)
        self.assertIn("不是稳定发布声明", text)

    def test_historical_pr_is_not_current_implementation(self):
        source = self.entries[0]["source"]
        self.assertEqual(source["contribution_search"]["total_count"], 1)
        self.assertEqual(source["contributions"][0]["number"], 45)
        self.assertEqual(source["contributions"][0]["state"], "OPEN")
        self.assertIsNone(source["contributions"][0]["merged_at"])
        text = (ROOT / "repo" / self.entries[0]["card"]).read_text("utf-8")
        self.assertIn("不能从旧 PR 标题推断已实现", text)
        self.assertIn(self.entries[0]["learning_question"], text)

    def test_ai_entrypoints_and_research_history(self):
        for path in ("repo/ai/README.md", "repo/ai/agents-and-swarms/README.md"):
            self.assertTrue((ROOT / path).is_file())
        if self.catalog["profile"] == "research":
            history = json.loads((ROOT / "repo/ai/agents-and-swarms/autoswarm-history.json").read_text("utf-8"))
            self.assertEqual(history["entry"]["source"]["head"], "96f0b026300186f7a51bff787b204ecc7ce1db03")
            text = (ROOT / "repo/agents-and-memory/autoswarm.md").read_text("utf-8")
            self.assertIn("历史卡", text)


if __name__ == "__main__":
    unittest.main()
