"""Tests for the EM's receipt check (agents/engagement-manager/scripts/em_receipt.py).

Each test builds a throwaway engagement with one module folder and checks the verdict.
"""
import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from test_valuation_check import CLEAN_DCF

SCRIPT = Path(__file__).resolve().parents[1] / "agents" / "engagement-manager" / "scripts" / "em_receipt.py"

MEMO = """# Module 03

## Answer
It is worth $300 per share.

**Confidence:** Medium

## Exhibit A

| Quantity | Period | Value | Source |
|---|---|---|---|
| Revenue | TTM | 3,449 | S1 (A) |
| Cash | 2026-06-30 | 1,383 | S2 (A-) |
| Shares | 2026-07-31 | 52.4M | S3 (A-) |
| Debt | 2026-06-30 | 0 | S2 (A-) |

| Other table | No source column |
|---|---|
| ignored | row |
"""


class Receipt(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.eng = Path(self._tmp.name) / "engagements" / "acme"
        self.module = self.eng / "modules" / "03-dcf"
        self.module.mkdir(parents=True)

    def tearDown(self):
        self._tmp.cleanup()

    def write(self, name, content, where=None):
        if not isinstance(content, str):
            content = json.dumps(content)
        ((where or self.module) / name).write_text(content)

    def run_check(self, seed=7):
        proc = subprocess.run([sys.executable, str(SCRIPT), str(self.module), "--seed", str(seed)],
                              capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        return json.loads(proc.stdout)

    def pin(self, **pinned):
        self.write("engagement.json", {"pinned": pinned}, where=self.eng)

    def test_clean_module_is_ready(self):
        self.write("memo.md", MEMO)
        self.write("valuation.json", CLEAN_DCF)
        out = self.run_check()
        self.assertEqual(out["verdict"], "ready_to_review", out)
        self.assertEqual(len(out["spot_checks"]), 3)

    def test_spot_checks_come_only_from_sourced_tables(self):
        self.write("memo.md", MEMO)
        for seed in range(10):
            for row in self.run_check(seed)["spot_checks"]:
                self.assertNotIn("ignored", row)
                self.assertNotIn("---", row)

    def test_spot_checks_vary_with_the_seed(self):
        self.write("memo.md", MEMO)
        picks = {tuple(self.run_check(seed)["spot_checks"]) for seed in range(10)}
        self.assertGreater(len(picks), 1)

    def test_missing_answer_section(self):
        self.write("memo.md", MEMO.replace("## Answer", "## Summary"))
        self.assertIn("no Answer section", " ".join(self.run_check()["problems"]))

    def test_missing_confidence(self):
        self.write("memo.md", MEMO.replace("**Confidence:** Medium", ""))
        self.assertIn("confidence level", " ".join(self.run_check()["problems"]))

    def test_no_sourced_table(self):
        self.write("memo.md", "## Answer\nX.\n\nConfidence: high\n")
        self.assertIn("no table with a Source column", " ".join(self.run_check()["problems"]))

    def test_verifier_errors_are_problems(self):
        self.write("memo.md", MEMO)
        bad = copy.deepcopy(CLEAN_DCF)
        bad["scenarios"]["grows_up"]["value_per_share"] *= 2
        self.write("valuation.json", bad)
        out = self.run_check()
        self.assertEqual(out["verdict"], "needs_fix")
        self.assertIn("does not match the model", " ".join(out["problems"]))

    def test_shares_differ_from_pinned(self):
        self.write("memo.md", MEMO)
        self.write("valuation.json", CLEAN_DCF)
        self.pin(shares=CLEAN_DCF["shares"]["value"] * 1.04)
        self.assertIn("engagement pins", " ".join(self.run_check()["problems"]))

    def test_matching_pins_pass(self):
        self.write("memo.md", MEMO)
        self.write("valuation.json", CLEAN_DCF)
        self.pin(shares=CLEAN_DCF["shares"]["value"], cash=CLEAN_DCF["cash"]["value"],
                 price={"value": CLEAN_DCF["price"]["value"], "date": CLEAN_DCF["price"]["date"]})
        self.assertEqual(self.run_check()["verdict"], "ready_to_review")

    def test_price_date_differs_from_pinned(self):
        self.write("memo.md", MEMO)
        self.write("valuation.json", CLEAN_DCF)
        self.pin(price={"value": CLEAN_DCF["price"]["value"], "date": "2026-09-30"})
        self.assertIn("price date", " ".join(self.run_check()["problems"]))

    def test_escalation_is_reported(self):
        self.write("memo.md", MEMO)
        self.write("escalation.md", "Sources conflict.")
        self.assertEqual(self.run_check()["verdict"], "escalated")


if __name__ == "__main__":
    unittest.main()
