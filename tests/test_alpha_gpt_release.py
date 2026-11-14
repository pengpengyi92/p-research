"""Offline selected-release contracts; not scientific or complete IP validation."""

from datetime import datetime
import json
from pathlib import Path
import re
import unittest
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT / "paper/ai-alpha-research"
REPORT = ROOT / "report/2026-11-15-alpha-gpt-pengyi166/README.md"
UPDATE = ROOT / "update/2026-11-15-alpha-gpt-selected-release.md"
LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)\s]+)\)")
PRIVATE_URL = re.compile(r"https?://github\.com/[^/\s]+/(?:PWOL|P-University)(?:[/#?]|\b)", re.I)
DRIVE = re.compile(r"(?<![A-Za-z0-9])[A-Za-z]:[/\\]")


def sensitive_patterns(text):
    patterns = (
        PRIVATE_URL, DRIVE, r"file://", r"github_pat_[A-Za-z0-9_]{30,}",
        r"gh[pousr]_[A-Za-z0-9]{30,}", r"(?i)(?:ts_rank|ts_corr|trade_when)\s*\(",
    )
    return [str(pattern) for pattern in patterns if re.search(pattern, text)]


class AlphaGPTSelectedReleaseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads((PAPERS / "sources.json").read_text(encoding="utf-8"))
        cls.entries = {entry["id"]: entry for entry in cls.data["papers"]}
        cls.files = [path for path in PAPERS.rglob("*") if path.is_file()]
        cls.files += [REPORT, UPDATE]

    def test_schema_timestamp_and_unique_scope(self):
        self.assertEqual(self.data["schema_version"], 1)
        self.assertEqual(self.data["timezone"], "Asia/Shanghai")
        self.assertIsNotNone(datetime.fromisoformat(self.data["reviewed_at"]).utcoffset())
        self.assertEqual(set(self.entries), {"alpha-gpt", "alpha-gpt-2", "quantagent"})
        self.assertEqual(len(self.data["papers"]), 3)
        self.assertEqual(len({p["card"] for p in self.entries.values()}), 3)

    def test_verified_author_order_is_not_collapsed_to_one_author(self):
        self.assertEqual(self.entries["alpha-gpt"]["authors"],
                         ["Saizhuo Wang", "Hang Yuan", "Leon Zhou", "Lionel Ni", "Heung-Yeung Shum", "Jian Guo"])
        self.assertEqual(self.entries["alpha-gpt-2"]["authors"], ["Hang Yuan", "Saizhuo Wang", "Jian Guo"])
        self.assertEqual(self.entries["quantagent"]["authors"],
                         ["Saizhuo Wang", "Hang Yuan", "Lionel M. Ni", "Jian Guo"])

    def test_demo_and_preprint_statuses_remain_separate(self):
        self.assertEqual(self.entries["alpha-gpt"]["publication_status"], "PUBLISHED_SYSTEM_DEMONSTRATION")
        self.assertEqual(self.entries["alpha-gpt"]["venue"], "EMNLP 2025 System Demonstrations")
        self.assertEqual(self.entries["alpha-gpt-2"]["publication_status"], "PREPRINT_WORK_IN_PROGRESS")
        self.assertEqual(self.entries["quantagent"]["publication_status"], "PREPRINT")
        for key in ("alpha-gpt-2", "quantagent"):
            self.assertIsNone(self.entries[key]["venue"])

    def test_primary_versions_are_exact_and_external(self):
        versions = {"alpha-gpt": ("2308.00016", "v2", "2025-09-20"),
                    "alpha-gpt-2": ("2402.09746", "v1", "2024-02-15"),
                    "quantagent": ("2402.03755", "v1", "2024-02-06")}
        for key, entry in self.entries.items():
            self.assertEqual((entry["arxiv_id"], entry["arxiv_version"], entry["arxiv_version_date"]), versions[key])
            self.assertEqual(entry["version_url"], "https://arxiv.org/abs/" + "".join(versions[key][:2]))
            for field in ("primary_url", "fulltext_url", "version_url"):
                url = urlparse(entry[field])
                self.assertEqual(url.scheme, "https")
                self.assertIn(url.netloc, {"arxiv.org", "aclanthology.org"})

    def test_bibliography_keys_ids_and_authors_match_records(self):
        # This checks our bounded BibTeX serialization, not arbitrary BibTeX.
        bib = (PAPERS / "references.bib").read_text(encoding="utf-8")
        entries = {m.group(2): (m.group(1), m.group(3)) for m in
                   re.finditer(r"@(\w+)\{([^,]+),\n(.*?)\n\}", bib, re.S)}
        self.assertEqual(set(entries), {p["bibkey"] for p in self.entries.values()})
        for paper in self.entries.values():
            kind, body = entries[paper["bibkey"]]
            author = re.search(r"author = \{([^}]+)\}", body).group(1)
            names = [" ".join(reversed(name.split(", ", 1))) for name in author.split(" and ")]
            self.assertEqual(names, paper["authors"])
            if paper["id"] == "alpha-gpt":
                self.assertEqual(kind, "inproceedings")
                self.assertIn(paper["doi"], body)
                self.assertIn("System Demonstrations", body)
            else:
                self.assertEqual(kind, "misc")
                self.assertIn(paper["arxiv_id"], body)
                self.assertNotIn("booktitle", body)

    def test_local_links_exist_and_do_not_escape_repository(self):
        markdowns = [p for p in self.files if p.suffix == ".md"]
        markdowns += [ROOT / "README.md", ROOT / "paper/README.md", ROOT / "report/README.md"]
        for path in markdowns:
            for href in LINK.findall(path.read_text(encoding="utf-8")):
                if urlparse(href).scheme or href.startswith("#"):
                    continue
                target = (path.parent / unquote(href.split("#", 1)[0])).resolve()
                self.assertTrue(target.is_relative_to(ROOT.resolve()), (path.name, href))
                self.assertTrue(target.exists(), (path.name, href))

    def test_exact_release_inventory_excludes_media_and_data_mirrors(self):
        self.assertEqual({p.name for p in PAPERS.rglob("*") if p.is_file()},
                         {"README.md", "alpha-gpt.md", "alpha-gpt-2.md", "quantagent.md",
                          "PROVENANCE.md", "sources.json", "references.bib"})
        self.assertEqual({p.name for p in REPORT.parent.rglob("*") if p.is_file()}, {"README.md"})

    def test_unrun_experiments_cannot_become_results_by_curation(self):
        self.assertEqual(self.data["paper_replication"], "NOT RUN")
        self.assertEqual(self.data["model_or_economic_gain"], "UNMEASURED")
        for entry in self.entries.values():
            self.assertEqual(entry["independent_economic_reproduction"], "NOT RUN")
            card = (PAPERS / entry["card"]).read_text(encoding="utf-8")
            self.assertIn("NOT RUN", card)
        report = REPORT.read_text(encoding="utf-8")
        for term in ("NOT ESTABLISHED", "NO-GO", "166 WorldQuant BRAIN submissions", "2024 IQC /",
                     "adverse proxy outcomes", "hindsight-selected", "not evidence of 166 independent"):
            self.assertIn(term, report)

    def test_selected_attribution_and_rights_exclusions_are_explicit(self):
        text = (PAPERS / "PROVENANCE.md").read_text(encoding="utf-8")
        for term in ("P University / P Lab", "PAPER-PWOL-001", "2026-11-06", "2026-11-14",
                     "not the full working paper", "CC BY 4.0", "not an", "degree-granting university",
                     "Protected formulas", "private repository URLs", "endorsement"):
            self.assertIn(term, text.replace("**", "").replace("\n", " "))

    def test_authored_package_has_no_known_sensitive_patterns(self):
        for path in self.files:
            self.assertFalse(sensitive_patterns(path.read_text(encoding="utf-8")), path.name)

    def test_privacy_scan_rejects_private_url_path_and_formula_mutations(self):
        for text in ("https://github.com/example/PWOL/blob/main/example.md",
                     "https://github.com/example/P-University",
                     "C:/private/example", "ts_rank(secret, 5)"):
            self.assertTrue(sensitive_patterns(text), text)
        self.assertFalse(sensitive_patterns("https://arxiv.org/abs/2402.03755v1"))
        self.assertFalse(sensitive_patterns("PWOL remains proprietary; original formulas are excluded."))


if __name__ == "__main__":
    unittest.main()
