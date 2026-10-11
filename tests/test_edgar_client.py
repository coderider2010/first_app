"""Offline tests for the EDGAR connector's pure logic (no network).

The key behaviour: XBRL repeats each period in several filings, and a row's `fy` is the
filing's year, not the period's. consolidate_facts must key on the period's dates, keep
the latest filing's value, and flag restatements.
"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "connectors" / "edgar"))
from edgar_client import (EdgarError, check_sec_url, classify_period,  # noqa: E402
                          consolidate_facts, html_to_text, keyword_snippets)

CIK = "0001404655"


def row(start, end, val, accn, filed, fy, form="10-K"):
    return {"start": start, "end": end, "val": val, "accn": accn, "filed": filed,
            "fy": fy, "fp": "FY", "form": form}


class ClassifyPeriod(unittest.TestCase):
    def test_kinds(self):
        self.assertEqual(classify_period(None, "2025-12-31"), "instant")
        self.assertEqual(classify_period("2025-04-01", "2025-06-30"), "quarter")
        self.assertEqual(classify_period("2025-01-01", "2025-12-31"), "annual")
        self.assertEqual(classify_period("2025-01-01", "2025-06-30"), "ytd-6-months")
        self.assertEqual(classify_period("2025-01-01", "2025-09-30"), "ytd-9-months")


class ConsolidateFacts(unittest.TestCase):
    def test_one_value_per_period_from_latest_filing(self):
        rows = [
            row("2023-01-01", "2023-12-31", 100, "A-23", "2024-02-14", fy=2023),
            row("2023-01-01", "2023-12-31", 100, "A-25", "2026-02-11", fy=2025),
            row("2023-01-01", "2023-12-31", 100, "A-24", "2025-02-12", fy=2024),
        ]
        [f] = consolidate_facts(rows, CIK, {"A-25": "doc25.htm"})
        self.assertEqual(f["period_end"], "2023-12-31")
        self.assertEqual(f["accession"], "A-25")
        self.assertEqual(f["reported_in_filings"], 3)
        self.assertFalse(f["restated"])
        self.assertTrue(f["source_url"].endswith("/1404655/A25/doc25.htm"))

    def test_fy_field_is_not_used_to_label_the_period(self):
        # The FY2025 10-K reports 2023 revenue with fy=2025; it must stay a 2023 period.
        [f] = consolidate_facts([row("2023-01-01", "2023-12-31", 1, "X", "2026-02-11", fy=2025)], CIK)
        self.assertEqual(f["period_end"], "2023-12-31")
        self.assertNotIn("fy", f)

    def test_restatement_is_flagged_and_latest_wins(self):
        rows = [row("2024-01-01", "2024-12-31", 500, "OLD", "2025-02-12", 2024),
                row("2024-01-01", "2024-12-31", 480, "NEW", "2026-02-11", 2025)]
        [f] = consolidate_facts(rows, CIK)
        self.assertEqual(f["value"], 480)
        self.assertTrue(f["restated"])
        self.assertEqual(f["earlier_values"], [500])

    def test_quarter_and_ytd_kept_apart(self):
        rows = [row("2025-04-01", "2025-06-30", 10, "Q", "2025-08-06", 2025, "10-Q"),
                row("2025-01-01", "2025-06-30", 19, "Q", "2025-08-06", 2025, "10-Q")]
        kinds = sorted(f["period_type"] for f in consolidate_facts(rows, CIK))
        self.assertEqual(kinds, ["quarter", "ytd-6-months"])

    def test_sorted_oldest_first_and_link_without_primary_doc(self):
        rows = [row("2025-01-01", "2025-12-31", 3, "C", "2026-02-11", 2025),
                row("2024-01-01", "2024-12-31", 2, "B", "2025-02-12", 2024)]
        out = consolidate_facts(rows, CIK)
        self.assertEqual([f["value"] for f in out], [2, 3])
        self.assertTrue(out[0]["source_url"].endswith("/1404655/B/"))


class FilingText(unittest.TestCase):
    def test_html_to_text_drops_markup_and_hidden_xbrl(self):
        raw = ("<html><style>p{}</style><ix:header>HIDDEN</ix:header>"
               "<p>Revenue&nbsp;grew</p><div>by 19%</div></html>")
        text = html_to_text(raw)
        self.assertIn("Revenue grew", text)
        self.assertIn("by 19%", text)
        self.assertNotIn("HIDDEN", text)
        self.assertNotIn("<", text)

    def test_keyword_snippets_case_insensitive_and_non_overlapping(self):
        text = "x" * 50 + " Customers rose. " + "z" * 40 + " customers again " + "y" * 50
        hits = keyword_snippets(text, ["customers"], context_chars=10)
        self.assertEqual(len(hits), 2)
        self.assertLessEqual(hits[0]["end"], hits[1]["start"])


class UrlGuard(unittest.TestCase):
    def test_only_sec_hosts(self):
        check_sec_url("https://www.sec.gov/Archives/edgar/data/1/2/a.htm")
        check_sec_url("https://data.sec.gov/api/xbrl/companyfacts/CIK1.json")
        for bad in ["https://example.com/a", "http://www.sec.gov/a",
                    "https://www.sec.gov.evil.com/a", "file:///etc/passwd"]:
            with self.assertRaises(EdgarError, msg=bad):
                check_sec_url(bad)


if __name__ == "__main__":
    unittest.main()
