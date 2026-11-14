"""Offline catalog contracts, not third-party runtime or model evaluation."""
from datetime import datetime
import json
from pathlib import Path
import re
import unittest
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
CAT = ROOT / ("ml-repo" if (ROOT / "ml-repo/catalog.json").exists() else "repo")
LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)\s]+)\)")
DRIVE = re.compile(r"(?<![A-Za-z0-9])[A-Za-z]:[/\\]")


class RepoCatalogTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads((CAT / "catalog.json").read_text(encoding="utf-8"))
        cls.entries = cls.data["entries"]

    def test_schema_scope_and_unique_sources(self):
        self.assertEqual(self.data["schema_version"], 1)
        self.assertFalse(self.data["complete_ecosystem_inventory"])
        self.assertIn(self.data["profile"], ("ml", "research", "systems"))
        self.assertEqual(self.data["timezone"], "Asia/Shanghai")
        self.assertEqual(len({x["source"]["repository"] for x in self.entries}), len(self.entries))
        self.assertEqual(len({x["card"] for x in self.entries}), len(self.entries))

    def test_public_source_pins_and_verified_entries(self):
        for entry in self.entries:
            source = entry["source"]
            self.assertFalse(source["private"])
            self.assertFalse(source["archived"])
            self.assertRegex(source["head"], r"^[a-f0-9]{40}$")
            self.assertTrue(source["observed_at"].endswith("+08:00"))
            self.assertGreaterEqual(len(source["entry_paths"]), 2)
            self.assertTrue(source["url"].startswith("https://github.com/"))

    def test_each_card_has_specific_reasons_and_unrun_plan(self):
        for entry in self.entries:
            text = (CAT / entry["card"]).read_text(encoding="utf-8")
            for item in ("Last reviewed", self.data["project"], entry["inclusion_reason"],
                         entry["source"]["head"], "## 用途", "## 为何在本仓库收录",
                         "## 源码入口", "## 学习路线", "## 练习（未执行）",
                         "## 贡献证据", "## 许可与限制", "NOT RUN / UNMEASURED"):
                self.assertIn(item, text, entry["card"])
            self.assertGreater(len(entry["inclusion_reason"]), 20)

    def test_local_markdown_targets_are_safe_and_exist(self):
        for path in CAT.rglob("*.md"):
            for href in LINK.findall(path.read_text(encoding="utf-8")):
                if re.match(r"[a-z]+:", href) or href.startswith("#"):
                    continue
                target = (path.parent / unquote(href.split("#", 1)[0])).resolve()
                self.assertTrue(target.is_relative_to(ROOT.resolve()), (path.name, href))
                self.assertTrue(target.exists(), (path.name, href))

    def test_code_links_match_pinned_source_metadata(self):
        checked = 0
        for entry in self.entries:
            src = entry["source"]
            allowed = {src["readme_path"], src["license_path"], *src["entry_paths"]}
            text = (CAT / entry["card"]).read_text(encoding="utf-8")
            for href in LINK.findall(text):
                match = re.fullmatch(r"https://github.com/([^/]+/[^/]+)/blob/([a-f0-9]{40})/(.+)", href)
                if not match or match.group(1) != src["repository"]:
                    continue
                self.assertEqual(match.group(2), src["head"])
                self.assertIn(match.group(3), allowed)
                checked += 1
        self.assertGreaterEqual(checked, 3 * len(self.entries))

    def test_observed_pr_states_are_not_inferred_from_closed(self):
        for entry in self.entries:
            src = entry["source"]
            self.assertFalse(src["contribution_search"]["incomplete_results"])
            observed = datetime.fromisoformat(src["observed_at"])
            for pr in src["contributions"]:
                self.assertEqual(pr["author"], "pengpengyi92")
                self.assertIn(pr["state"], ("OPEN", "MERGED", "CLOSED_UNMERGED"))
                self.assertEqual(pr["merged_at"] is not None, pr["state"] == "MERGED")
                self.assertLessEqual(datetime.fromisoformat(pr["updated_at"].replace("Z", "+00:00")), observed)
                self.assertIn("| " + pr["state"] + " |", (CAT / entry["card"]).read_text(encoding="utf-8"))

    def test_no_pr_candidates_do_not_claim_an_accepted_contribution(self):
        for entry in self.entries:
            if not entry["source"]["contributions"]:
                text = (CAT / entry["card"]).read_text(encoding="utf-8")
                self.assertIn("阅读候选", text)
                self.assertIn("不声称", text)
            self.assertEqual(entry["source"]["runtime_evaluation"], "NOT RUN in this catalog task")

    def test_permission_and_data_model_boundaries_remain_visible(self):
        for entry in self.entries:
            text = (CAT / entry["card"]).read_text(encoding="utf-8")
            if entry["source"]["license_path"]:
                self.assertIn("数据/模型权重", text)
            else:
                self.assertIn("NEEDS_PERMISSION", text)
            if entry["slug"] == "videorag":
                self.assertIn("组件级许可", text)
            if entry["slug"] == "safetensors":
                self.assertIn("供应链", text)

    def test_no_workstation_paths_or_credentials_in_authored_catalog(self):
        files = [CAT / "catalog.json", CAT / "README.md", CAT / "HOW_TO_STUDY.md"]
        files += [CAT / e["card"] for e in self.entries]
        for path in files:
            text = path.read_text(encoding="utf-8")
            for pattern in (DRIVE, r"github_pat_[A-Za-z0-9_]{30,}", r"gh[pousr]_[A-Za-z0-9]{30,}", r"file://"):
                self.assertIsNone(re.search(pattern, text), path.name)

    def test_https_is_not_a_drive_and_real_drive_is_detected(self):
        self.assertIsNone(DRIVE.search("https://github.com/example/repo"))
        self.assertIsNotNone(DRIVE.search("local C:/private/example"))


if __name__ == "__main__":
    unittest.main()
