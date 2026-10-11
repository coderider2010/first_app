"""Tests for the reverse DCF model (reverse_dcf.py) and its checker (valuation_check.py).

Run from the repo root:
    python3 -m unittest discover tests -v

The model tests compare against cases that can be solved by hand. The checker
tests plant one problem in an otherwise clean valuation and check it is reported;
the checker runs as a subprocess, the way the agent and the gate run it.
"""
import copy
import json
import os
import subprocess
import sys
import tempfile
import unittest

SCRIPTS = os.path.join(
    os.path.dirname(__file__), "..",
    "agents", "associate", "skills", "implied-expectations", "scripts",
)
sys.path.insert(0, SCRIPTS)
import reverse_dcf as model  # noqa: E402

CHECKER = os.path.join(SCRIPTS, "valuation_check.py")
GENERATOR = os.path.join(SCRIPTS, "reverse_dcf.py")


def src(value, **extra):
    return dict({"value": value, "source": "test fixture"}, **extra)


def clean_valuation():
    """A reverse DCF that passes every check. Tests copy it and break one thing."""
    price, shares, debt, cash = 400.0, 50e6, 0.0, 1.4e9
    equity = price * shares
    d = {
        "type": "reverse_dcf",
        "company": "Example Software",
        "as_of": "2026-10-10",
        "currency": "USD",
        "price": src(price, date="2026-10-09"),
        "shares": src(shares, basis="diluted"),
        "debt": src(debt),
        "cash": src(cash),
        "equity_value": equity,
        "enterprise_value": equity + debt - cash,
        "base_revenue": src(3.4e9, period="TTM"),
        "base_fcf_margin": src(0.05, definition="(OCF - capex - SBC) / revenue"),
        "sbc_treatment": "expense",
        "discount_rate": src(
            0.10, risk_free=src(0.045), beta=src(1.1), equity_risk_premium=src(0.05)
        ),
        "terminal_growth": src(0.03, cap=0.04, cap_source="test fixture"),
        "horizon_years": 10,
        "peer_margins": {"Peer A": src(0.30), "Peer B": src(0.25)},
    }
    d["grid"] = model.build_grid(d, [0.08, 0.12, 0.16])
    base = next(c for c in d["grid"] if c["growth"] == 0.12 and c["wacc"] == 0.10)
    d["headline"] = {"growth": 0.12, "margin": base["margin"], "wacc": 0.10}
    return d


CLEAN = clean_valuation()


def run(d):
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
        json.dump(d, f)
        path = f.name
    try:
        proc = subprocess.run([sys.executable, CHECKER, path], capture_output=True, text=True)
    finally:
        os.unlink(path)
    return proc.returncode, json.loads(proc.stdout)


class Model(unittest.TestCase):
    def test_flat_margin_one_year_equals_perpetuity_formula(self):
        # One year of FCF then a growing perpetuity collapses to R(1+g)m / (r - gT).
        ev = model.enterprise_value(100.0, 0.2, 0.05, 0.2, 0.10, 0.03, horizon=1)
        self.assertAlmostEqual(ev, 100 * 1.05 * 0.2 / (0.10 - 0.03), places=9)

    def test_implied_margin_round_trips(self):
        ev = model.enterprise_value(3e9, 0.05, 0.12, 0.27, 0.10, 0.03)
        self.assertAlmostEqual(model.implied_margin(ev, 3e9, 0.05, 0.12, 0.10, 0.03), 0.27, places=9)

    def test_implied_growth_round_trips(self):
        ev = model.enterprise_value(3e9, 0.05, 0.14, 0.25, 0.10, 0.03)
        self.assertAlmostEqual(model.implied_growth(ev, 3e9, 0.05, 0.25, 0.10, 0.03), 0.14, places=6)

    def test_implied_growth_none_when_unreachable(self):
        self.assertIsNone(model.implied_growth(1e15, 3e9, 0.05, 0.01, 0.10, 0.03))

    def test_faster_growth_needs_lower_margin(self):
        args = (CLEAN["enterprise_value"], 3.4e9, 0.05)
        slow = model.implied_margin(*args, 0.08, 0.10, 0.03)
        fast = model.implied_margin(*args, 0.16, 0.10, 0.03)
        self.assertGreater(slow, fast)

    def test_generator_cli_matches_library(self):
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
            json.dump(dict(CLEAN, grid_growths=[0.12]), f)
            path = f.name
        try:
            out = subprocess.run([sys.executable, GENERATOR, path], capture_output=True, text=True)
        finally:
            os.unlink(path)
        grid = json.loads(out.stdout)["grid"]
        self.assertEqual(len(grid), 3)  # base rate and +/- 1 point
        base = next(c for c in grid if c["wacc"] == 0.10)
        self.assertEqual(base["margin"], CLEAN["headline"]["margin"])


class Checker(unittest.TestCase):
    def assertError(self, d, fragment):
        code, out = run(d)
        self.assertEqual(code, 0)
        self.assertEqual(out["status"], "errors_found", out)
        self.assertTrue(any(fragment in e for e in out["errors"]), out["errors"])

    def assertFlag(self, d, fragment):
        code, out = run(d)
        self.assertEqual(code, 0)
        self.assertTrue(any(fragment in f for f in out["flags"]), out["flags"])

    def broken(self):
        return copy.deepcopy(CLEAN)

    def test_clean_passes(self):
        code, out = run(CLEAN)
        self.assertEqual((code, out["status"]), (0, "pass"), out)

    def test_equity_not_price_times_shares(self):
        d = self.broken()
        d["equity_value"] *= 1.1
        self.assertError(d, "price x shares")

    def test_ev_bridge_broken(self):
        d = self.broken()
        d["cash"]["value"] = 0
        self.assertError(d, "equity + debt - cash")

    def test_terminal_growth_above_cap(self):
        d = self.broken()
        d["terminal_growth"]["value"] = 0.05
        self.assertError(d, "exceeds its cap")

    def test_terminal_growth_cap_missing(self):
        d = self.broken()
        del d["terminal_growth"]["cap"]
        self.assertError(d, "needs a cap")

    def test_terminal_growth_at_or_above_discount_rate(self):
        d = self.broken()
        d["terminal_growth"].update(value=0.10, cap=0.12)
        self.assertError(d, ">= discount rate")

    def test_discount_rate_not_derived_from_inputs(self):
        d = self.broken()
        d["discount_rate"]["value"] = 0.08
        self.assertError(d, "does not match its inputs")

    def test_discount_rate_input_unsourced(self):
        d = self.broken()
        d["discount_rate"]["beta"] = 1.1
        self.assertError(d, "beta has no source")

    def test_blended_rate_with_debt(self):
        d = self.broken()
        d["discount_rate"].update(debt_weight=src(0.5), cost_of_debt=src(0.05), tax_rate=src(0.2))
        self.assertError(d, "blended with debt")

    def test_sbc_ignored(self):
        d = self.broken()
        d["sbc_treatment"] = "none"
        self.assertError(d, "sbc_treatment must be")

    def test_sbc_as_dilution_is_flagged(self):
        d = self.broken()
        d["sbc_treatment"] = "dilution"
        self.assertFlag(d, "before SBC")

    def test_grid_edited_by_hand(self):
        d = self.broken()
        d["grid"][0]["margin"] += 0.02
        self.assertError(d, "do not reproduce")

    def test_grid_missing_sensitivity_column(self):
        d = self.broken()
        d["grid"] = [c for c in d["grid"] if c["wacc"] != 0.11]
        self.assertError(d, "no column at discount rate 11.0%")

    def test_headline_not_on_the_curve(self):
        d = self.broken()
        d["headline"]["margin"] += 0.03
        self.assertError(d, "does not reproduce today's value")

    def test_unsourced_price(self):
        d = self.broken()
        d["price"]["source"] = ""
        self.assertError(d, "price has no source")

    def test_stale_price(self):
        d = self.broken()
        d["price"]["date"] = "2026-09-01"
        self.assertFlag(d, "days older than as_of")

    def test_basic_shares_flagged(self):
        d = self.broken()
        d["shares"]["basis"] = "basic"
        self.assertFlag(d, "not on a diluted basis")

    def test_margin_above_every_peer(self):
        d = self.broken()
        d["peer_margins"] = {"Peer A": src(0.10)}
        self.assertFlag(d, "above every peer")

    def test_no_peers_flagged(self):
        d = self.broken()
        del d["peer_margins"]
        self.assertFlag(d, "no peer_margins")

    def test_missing_required_key_is_unusable_input(self):
        d = self.broken()
        del d["grid"]
        code, out = run(d)
        self.assertEqual(code, 1)
        self.assertIn("missing required keys", out["error"])


if __name__ == "__main__":
    unittest.main()
