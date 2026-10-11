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
        "peer_margins": {"Peer A": src(0.30), "Peer B": src(0.18)},
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

    def test_margin_below_every_peer(self):
        d = self.broken()
        d["peer_margins"] = {"Peer A": src(0.40)}
        self.assertFlag(d, "below every peer")

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


# --- Forward DCF with named scenarios (type "dcf", module 3) ---

sys.path.insert(0, os.path.join(SCRIPTS, "..", "..", "valuation-dcf", "scripts"))
import dcf  # noqa: E402

DCF_GENERATOR = os.path.join(SCRIPTS, "..", "..", "valuation-dcf", "scripts", "dcf.py")


def clean_scenarios():
    """Two stories that pass every check, with numbers from dcf.py."""
    d = {k: copy.deepcopy(v) for k, v in CLEAN.items()
         if k not in ("equity_value", "enterprise_value", "grid", "headline")}
    d["type"] = "dcf"
    d["price"]["value"] = 250.0  # between the two stories
    d["scenarios"] = {
        "grows_up": {
            "narrative": "Matures like its peers",
            "growth": {"start": 0.14, "end": 0.05}, "target_margin": 0.25,
            "evidence": [{"claim": "peer margins 18-30%", "source": "10-Ks"},
                         {"claim": "guidance 14%", "source": "8-K"}],
        },
        "squeezed": {
            "narrative": "AI pressure stalls margins",
            "growth": {"start": 0.10, "end": 0.03}, "target_margin": 0.10,
            "evidence": [{"claim": "seat counts falling", "source": "10-Q"},
                         {"claim": "pricing pressure", "source": "earnings call"}],
        },
    }
    for name, sc in d["scenarios"].items():
        sc.update(dcf.value_scenario(d, sc))
    d["sensitivity"] = [
        {"scenario": n, "wacc": w, "terminal_growth": 0.03,
         "value_per_share": dcf.value_scenario(d, sc, w, 0.03)["value_per_share"]}
        for n, sc in d["scenarios"].items() for w in (0.09, 0.10, 0.11)
    ]
    return d


CLEAN_DCF = clean_scenarios()


class GrowthPaths(unittest.TestCase):
    def test_constant_fade_and_list_agree(self):
        args = (3e9, 0.05)
        const = model.enterprise_value(*args, 0.1, 0.25, 0.10, 0.03)
        fade = model.enterprise_value(*args, {"start": 0.1, "end": 0.1}, 0.25, 0.10, 0.03)
        lst = model.enterprise_value(*args, [0.1] * 10, 0.25, 0.10, 0.03)
        self.assertAlmostEqual(const, fade, places=3)
        self.assertAlmostEqual(const, lst, places=3)

    def test_fade_is_straight_line(self):
        path = model.growth_path({"start": 0.14, "end": 0.05}, 10)
        self.assertAlmostEqual(path[0], 0.14)
        self.assertAlmostEqual(path[-1], 0.05)
        self.assertAlmostEqual(path[1] - path[0], path[-1] - path[-2])

    def test_wrong_length_path_rejected(self):
        with self.assertRaises(ValueError):
            model.growth_path([0.1] * 9, 10)


class CheckerBase(unittest.TestCase):
    """Helpers shared by the checker test classes (no tests of its own)."""

    def check(self, d):
        code, out = run(d)
        self.assertEqual(code, 0, out)
        return out

    def assertError(self, d, fragment):
        out = self.check(d)
        self.assertEqual(out["status"], "errors_found", out)
        self.assertTrue(any(fragment in e for e in out["errors"]), out["errors"])

    def assertFlag(self, d, fragment):
        out = self.check(d)
        self.assertTrue(any(fragment in f for f in out["flags"]), out["flags"])



class ScenarioChecker(CheckerBase):
    def broken(self):
        return copy.deepcopy(CLEAN_DCF)

    def test_clean_passes(self):
        out = self.check(CLEAN_DCF)
        self.assertEqual(out["status"], "pass", out)

    def test_generator_cli_matches_library(self):
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
            json.dump(CLEAN_DCF, f)
            path = f.name
        try:
            proc = subprocess.run([sys.executable, DCF_GENERATOR, path], capture_output=True, text=True)
        finally:
            os.unlink(path)
        out = json.loads(proc.stdout)
        for name, sc in CLEAN_DCF["scenarios"].items():
            self.assertEqual(out["scenarios"][name]["value_per_share"], sc["value_per_share"])
            self.assertEqual(len(out["scenarios"][name]["years"]), 10)
        # 3 discount rates x 3 terminal rates (all under the 4% cap) x 2 scenarios
        self.assertEqual(len(out["sensitivity"]), 18)

    def test_value_edited_by_hand(self):
        d = self.broken()
        d["scenarios"]["grows_up"]["value_per_share"] *= 1.05
        self.assertError(d, "does not match the model")

    def test_one_scenario_is_not_a_range(self):
        d = self.broken()
        del d["scenarios"]["squeezed"]
        d["sensitivity"] = [c for c in d["sensitivity"] if c["scenario"] == "grows_up"]
        self.assertError(d, "at least 2 scenarios")

    def test_story_without_evidence(self):
        d = self.broken()
        d["scenarios"]["squeezed"]["evidence"] = [{"claim": "AI", "source": ""}]
        self.assertError(d, "sourced evidence items")

    def test_story_without_narrative(self):
        d = self.broken()
        d["scenarios"]["squeezed"]["narrative"] = ""
        self.assertError(d, "no narrative")

    def test_scenario_terminal_growth_over_cap(self):
        d = self.broken()
        d["scenarios"]["grows_up"]["terminal_growth"] = 0.05
        self.assertError(d, "exceeds the cap")

    def test_sensitivity_cell_edited(self):
        d = self.broken()
        d["sensitivity"][0]["value_per_share"] += 20
        self.assertError(d, "sensitivity cells do not match")

    def test_sensitivity_missing_rate(self):
        d = self.broken()
        d["sensitivity"] = [c for c in d["sensitivity"] if c["wacc"] != 0.11]
        self.assertError(d, "no discount rate 11.0%")

    def test_price_outside_both_stories(self):
        d = self.broken()
        d["price"]["value"] = 10_000
        self.assertFlag(d, "outside the scenario range")

    def test_stories_too_close(self):
        d = self.broken()
        sq = d["scenarios"]["squeezed"]
        sq.update(growth=copy.deepcopy(d["scenarios"]["grows_up"]["growth"]), target_margin=0.245)
        sq.update(dcf.value_scenario(d, sq))
        d["sensitivity"] = [
            {"scenario": n, "wacc": w, "terminal_growth": 0.03,
             "value_per_share": dcf.value_scenario(d, sc, w, 0.03)["value_per_share"]}
            for n, sc in d["scenarios"].items() for w in (0.09, 0.10, 0.11)
        ]
        self.assertFlag(d, "don't differ enough")

    def test_growth_not_converged(self):
        d = self.broken()
        sc = d["scenarios"]["grows_up"]
        sc["growth"] = 0.14
        sc.update(dcf.value_scenario(d, sc))
        d["sensitivity"] = [c for c in d["sensitivity"] if c["scenario"] != "grows_up"] + [
            {"scenario": "grows_up", "wacc": w, "terminal_growth": 0.03,
             "value_per_share": dcf.value_scenario(d, sc, w, 0.03)["value_per_share"]}
            for w in (0.09, 0.10, 0.11)]
        self.assertFlag(d, "step down at the terminal year is abrupt")

    def test_unknown_type_is_unusable(self):
        d = self.broken()
        d["type"] = "lbo"
        code, out = run(d)
        self.assertEqual(code, 1)
        self.assertIn("unknown type", out["error"])


# --- Peer comparison (type "comps", module 4) ---

sys.path.insert(0, os.path.join(SCRIPTS, "..", "..", "benchmarking", "scripts"))
import comps  # noqa: E402

COMPS_GENERATOR = os.path.join(SCRIPTS, "..", "..", "benchmarking", "scripts", "comps.py")


def peer(price, shares, revenue, growth, fcf, cash=1e9, debt=0.0):
    return {"price": src(price, date="2026-10-09"), "shares": src(shares),
            "cash": src(cash), "debt": src(debt), "revenue_ttm": src(revenue),
            "revenue_growth": src(growth), "fcf_after_sbc_ttm": src(fcf)}


def clean_comps():
    """Five peers whose multiples rise with the rule of 40, the target inside their range."""
    d = {k: copy.deepcopy(CLEAN[k]) for k in
         ("company", "as_of", "currency", "price", "shares", "debt", "cash")}
    d["type"] = "comps"
    d["target"] = {"revenue_ttm": src(3.4e9), "revenue_growth": src(0.18),
                   "fcf_after_sbc_ttm": src(0.06 * 3.4e9)}
    d["selection_rules"] = ["B2B subscription software", "revenue $1-15B", "growth 8-25%"]
    d["peers"] = {
        "P1": peer(100, 100e6, 5e9, 0.08, 0.15 * 5e9),
        "P2": peer(150, 100e6, 4e9, 0.12, 0.18 * 4e9),
        "P3": peer(200, 100e6, 4e9, 0.16, 0.20 * 4e9),
        "P4": peer(260, 100e6, 3e9, 0.20, 0.22 * 3e9),
        "P5": peer(120, 100e6, 3e9, 0.10, 0.12 * 3e9),
    }
    d["candidates"] = [{"name": n, "included": True, "reason": "fits all rules"} for n in d["peers"]]
    d["candidates"].append({"name": "Too Small Inc", "included": False, "reason": "revenue $0.4B"})
    out = comps.run(d)
    for name, m in out["peers"].items():
        d["peers"][name].update({k: m[k] for k in ("enterprise_value", "ev_revenue", "rule_of_40")})
    d["methods"] = out["methods"]
    d["regression"] = {k: out["regression"][k] for k in ("slope", "intercept", "r2", "residual_spread")}
    d["range"] = dict(out["regression_band"], basis="regression_band")
    mid = (d["range"]["low"] + d["range"]["high"]) / 2
    d["price"]["value"] = round(mid, 2)
    return d


CLEAN_COMPS = clean_comps()


class CompsModel(unittest.TestCase):
    def test_perfect_line_is_recovered(self):
        reg = comps.fit([0.1, 0.2, 0.3, 0.4], [3.0, 5.0, 7.0, 9.0])
        self.assertAlmostEqual(reg["slope"], 20.0)
        self.assertAlmostEqual(reg["intercept"], 1.0)
        self.assertAlmostEqual(reg["r2"], 1.0)
        self.assertAlmostEqual(reg["residual_spread"], 0.0)

    def test_peer_ev_and_multiples(self):
        m = comps.peer_metrics(peer(100, 10e6, 500e6, 0.2, 50e6, cash=200e6, debt=100e6))
        self.assertEqual(m["enterprise_value"], 900_000_000)  # 1,000M + 100M - 200M
        self.assertAlmostEqual(m["ev_revenue"], 1.8)
        self.assertAlmostEqual(m["ev_fcf"], 18.0)
        self.assertAlmostEqual(m["rule_of_40"], 0.30)  # 20% growth + 10% margin

    def test_negative_fcf_has_no_ev_fcf(self):
        self.assertIsNone(comps.peer_metrics(peer(100, 10e6, 500e6, 0.2, -5e6))["ev_fcf"])

    def test_cli_matches_library(self):
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
            json.dump(CLEAN_COMPS, f)
            path = f.name
        try:
            proc = subprocess.run([sys.executable, COMPS_GENERATOR, path], capture_output=True, text=True)
        finally:
            os.unlink(path)
        self.assertEqual(json.loads(proc.stdout)["methods"], CLEAN_COMPS["methods"])


class CompsChecker(CheckerBase):
    def broken(self):
        return copy.deepcopy(CLEAN_COMPS)

    def test_clean_passes(self):
        self.assertEqual(self.check(CLEAN_COMPS)["status"], "pass", self.check(CLEAN_COMPS))

    def test_no_selection_rules(self):
        d = self.broken()
        d["selection_rules"] = []
        self.assertError(d, "no selection_rules")

    def test_exclusion_without_reason(self):
        d = self.broken()
        d["candidates"][-1]["reason"] = ""
        self.assertError(d, "excluded without a reason")

    def test_peer_not_from_candidates(self):
        d = self.broken()
        d["peers"]["Sneaky"] = copy.deepcopy(d["peers"]["P1"])
        self.assertError(d, "do not match the candidates")

    def test_too_few_peers(self):
        d = self.broken()
        for n in ("P3", "P4", "P5"):
            del d["peers"][n]
        d["candidates"] = [c for c in d["candidates"] if c["name"] in d["peers"] or not c["included"]]
        self.assertError(d, "need at least 3")

    def test_unsourced_peer_input(self):
        d = self.broken()
        d["peers"]["P2"]["revenue_ttm"]["source"] = ""
        self.assertError(d, "P2: revenue_ttm has no source")

    def test_peer_multiple_edited(self):
        d = self.broken()
        d["peers"]["P3"]["ev_revenue"] = 9.9
        self.assertError(d, "do not match comps.py")

    def test_method_value_edited(self):
        d = self.broken()
        d["methods"]["median_ev_revenue"] *= 1.2
        self.assertError(d, "do not match comps.py")

    def test_range_not_the_band(self):
        d = self.broken()
        d["range"]["high"] *= 1.3
        self.assertError(d, "is not the regression band")

    def test_range_beyond_methods(self):
        d = self.broken()
        vals = d["methods"].values()
        d["range"] = {"low": min(vals), "high": max(vals) * 1.5, "basis": "methods"}
        self.assertError(d, "beyond the methods")

    def test_stale_peer_price(self):
        d = self.broken()
        d["peers"]["P1"]["price"]["date"] = "2026-08-01"
        self.assertFlag(d, "P1: price dated")

    def test_target_outside_peer_scores(self):
        d = self.broken()
        d["target"]["revenue_growth"]["value"] = 0.60
        out = comps.run(d)
        d["methods"] = out["methods"]
        d["range"] = dict(out["regression_band"], basis="regression_band")
        self.assertFlag(d, "extrapolating")

    def test_price_outside_peer_range(self):
        d = self.broken()
        d["price"]["value"] = 5.0
        self.assertFlag(d, "outside the peer range")

    def test_dcf_inputs_not_required(self):
        self.assertNotIn("discount_rate", CLEAN_COMPS)


class WriteBack(unittest.TestCase):
    """--write saves generator output into valuation.json, which then passes the checker."""

    def roundtrip(self, generator, d, strip):
        d = copy.deepcopy(d)
        strip(d)
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
            json.dump(d, f)
            path = f.name
        try:
            subprocess.run([sys.executable, generator, path, "--write"], check=True,
                           capture_output=True, text=True)
            with open(path) as f:
                written = json.load(f)
        finally:
            os.unlink(path)
        code, out = run(written)
        self.assertEqual((code, out["status"]), (0, "pass"), out)

    def test_comps_write(self):
        def strip(d):
            for p in d["peers"].values():
                for k in ("enterprise_value", "ev_revenue", "rule_of_40"):
                    p.pop(k)
            d["methods"], d["regression"] = {}, {}
            del d["range"]
        self.roundtrip(COMPS_GENERATOR, CLEAN_COMPS, strip)

    def test_dcf_write(self):
        def strip(d):
            for sc in d["scenarios"].values():
                sc["value_per_share"] = 0
            d["sensitivity"] = []
        self.roundtrip(DCF_GENERATOR, CLEAN_DCF, strip)
