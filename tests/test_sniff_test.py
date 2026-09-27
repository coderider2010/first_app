"""Tests for the market-sizing verifier (sniff_test.py).

Run from the repo root:
    python3 -m unittest discover tests -v

Each test plants one problem in an otherwise clean sizing and checks that the
verifier reports it. The script is run as a subprocess, the same way the agent
runs it, so these tests also cover the command-line contract (JSON on stdout,
exit codes).
"""
import copy
import json
import os
import subprocess
import sys
import tempfile
import unittest

SCRIPT = os.path.join(
    os.path.dirname(__file__), "..",
    "agents", "associate", "skills", "market-sizing", "scripts", "sniff_test.py",
)

# A sizing that passes every check. Tests copy it and break one thing.
CLEAN = {
    "market": "US pet insurance",
    "year": 2026,
    "currency": "USD",
    "basis": "revenue",
    "estimate": 4.7e9,
    "tolerance_pct": 20,
    "methods": {"top_down": 4.5e9, "bottom_up": 5.0e9},
    "growth_rate_pct": 10,
    "shares": {"Trupanion": 0.3, "Nationwide": 0.2},
    "per_capita": {
        "population": 9e7, "anchor_low": 30, "anchor_high": 80,
        "unit": "per pet-owning household",
    },
}


def sizing(**changes):
    """Return a copy of CLEAN with the given keys replaced (None deletes a key)."""
    d = copy.deepcopy(CLEAN)
    for k, v in changes.items():
        if v is None:
            d.pop(k, None)
        else:
            d[k] = v
    return d


def run_raw(text):
    """Run the verifier on raw file contents; return (exit code, stdout)."""
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
        f.write(text)
        path = f.name
    try:
        proc = subprocess.run(
            [sys.executable, SCRIPT, path], capture_output=True, text=True
        )
    finally:
        os.unlink(path)
    return proc.returncode, proc.stdout


def run(d):
    """Run the verifier on a sizing dict; return (exit code, parsed JSON output)."""
    code, out = run_raw(json.dumps(d))
    return code, json.loads(out)


class Baseline(unittest.TestCase):
    def test_clean_sizing_passes(self):
        code, r = run(CLEAN)
        self.assertEqual(code, 0)
        self.assertEqual(r["status"], "pass", r)
        self.assertEqual(r["errors"], [])
        self.assertEqual(r["flags"], [])

    def test_errors_found_still_exits_zero(self):
        # The docstring's key warning: a clean exit is NOT a clean sizing.
        code, r = run(sizing(estimate=9e9))
        self.assertEqual(code, 0)
        self.assertEqual(r["status"], "errors_found")

    def test_errors_outrank_flags(self):
        # Wide spread (flag) plus estimate outside the range (error).
        code, r = run(sizing(methods={"a": 3e9, "b": 5e9}, estimate=6e9))
        self.assertEqual(r["status"], "errors_found")
        self.assertTrue(r["flags"])


class UnusableInput(unittest.TestCase):
    """Only unusable input exits non-zero."""

    def assertInputError(self, code, out, fragment):
        self.assertEqual(code, 1)
        self.assertIn(fragment, json.loads(out)["error"])

    def test_missing_file(self):
        proc = subprocess.run(
            [sys.executable, SCRIPT, "/no/such/file.json"],
            capture_output=True, text=True,
        )
        self.assertInputError(proc.returncode, proc.stdout, "no such file")

    def test_invalid_json(self):
        self.assertInputError(*run_raw("{not json"), "invalid JSON")

    def test_missing_required_key(self):
        self.assertInputError(*run_raw(json.dumps(sizing(basis=None))), "basis")

    def test_single_method_violates_triangulation(self):
        d = sizing(methods={"top_down": 4.7e9})
        self.assertInputError(*run_raw(json.dumps(d)), "triangulation")

    def test_per_capita_missing_key(self):
        d = sizing(per_capita={"population": 9e7, "anchor_low": 30})
        self.assertInputError(*run_raw(json.dumps(d)), "anchor_high")


class Triangulation(unittest.TestCase):
    def test_estimate_outside_method_range_is_error(self):
        _, r = run(sizing(estimate=5.5e9))
        self.assertTrue(any("outside the method range" in e for e in r["errors"]))

    def test_estimate_on_range_edge_is_fine(self):
        _, r = run(sizing(estimate=4.5e9))
        self.assertEqual(r["status"], "pass", r)

    def test_spread_over_30_pct_is_flag(self):
        _, r = run(sizing(methods={"a": 4e9, "b": 5.5e9}))  # 38% spread
        self.assertTrue(any("do NOT average silently" in f for f in r["flags"]))

    def test_spread_over_twice_tolerance_is_flag(self):
        # 25% spread: under the 30% rule, but over 2 x 10% tolerance.
        _, r = run(sizing(methods={"a": 4e9, "b": 5e9}, tolerance_pct=10))
        self.assertTrue(any("twice the decision tolerance" in f for f in r["flags"]))
        self.assertFalse(any("average silently" in f for f in r["flags"]))


class FalsePrecision(unittest.TestCase):
    def test_too_many_sig_figs_is_error(self):
        _, r = run(sizing(estimate=4.72e9))
        self.assertTrue(any("false precision" in e for e in r["errors"]))

    def test_tight_tolerance_allows_precision(self):
        # At +/-10% the decision needs precision, so 3 sig figs are fine.
        _, r = run(sizing(estimate=4.72e9, tolerance_pct=10))
        self.assertFalse(any("false precision" in e for e in r["errors"]))


class Growth(unittest.TestCase):
    def test_moderate_growth_is_fine(self):
        _, r = run(sizing(growth_rate_pct=10))  # 1.6x over 5y
        self.assertEqual(r["flags"], [])

    def test_doubling_is_flag(self):
        _, r = run(sizing(growth_rate_pct=15))  # 2.01x over 5y
        self.assertTrue(any("doubles" in f for f in r["flags"]))

    def test_tripling_is_extraordinary_flag(self):
        _, r = run(sizing(growth_rate_pct=25))  # 3.05x over 5y
        self.assertTrue(any("extraordinary" in f for f in r["flags"]))

    def test_horizon_changes_the_verdict(self):
        _, r = run(sizing(growth_rate_pct=15, growth_horizon_years=3))  # 1.5x
        self.assertEqual(r["flags"], [])

    def test_collapse_is_error(self):
        _, r = run(sizing(growth_rate_pct=-60))
        self.assertTrue(any("data error" in e for e in r["errors"]))


class Shares(unittest.TestCase):
    def test_share_above_one_is_error(self):
        # Someone typed 30 (percent) instead of 0.30 (fraction).
        _, r = run(sizing(shares={"A": 30}))
        self.assertTrue(any("must be fractions" in e for e in r["errors"]))

    def test_shares_over_100_pct_is_error(self):
        _, r = run(sizing(shares={"A": 0.6, "B": 0.5}))
        self.assertTrue(any("arithmetic broken" in e for e in r["errors"]))

    def test_complete_list_well_under_100_is_flag(self):
        _, r = run(sizing(shares={"A": 0.5, "B": 0.3}, shares_complete=True))
        self.assertTrue(any("marked complete" in f for f in r["flags"]))

    def test_incomplete_list_near_100_is_flag(self):
        _, r = run(sizing(shares={"A": 0.6, "B": 0.37}))
        self.assertTrue(any("undersized" in f for f in r["flags"]))


class PerCapita(unittest.TestCase):
    def test_implied_spend_outside_anchors_is_error(self):
        # $4.7B over 1M households = $4,700 each; anchors say $30-80.
        pc = dict(CLEAN["per_capita"], population=1e6)
        _, r = run(sizing(per_capita=pc))
        self.assertTrue(any("anchor range" in e for e in r["errors"]))

    @unittest.expectedFailure
    def test_zero_population_returns_json_not_a_crash(self):
        # KNOWN BUG: division by zero crashes with a traceback. When fixed,
        # this test will "unexpectedly pass" -- then remove the decorator.
        pc = dict(CLEAN["per_capita"], population=0)
        code, out = run_raw(json.dumps(sizing(per_capita=pc)))
        json.loads(out)


class Labeling(unittest.TestCase):
    def test_blank_currency_is_error(self):
        _, r = run(sizing(currency=""))
        self.assertTrue(any("missing currency" in e for e in r["errors"]))

    def test_blank_basis_is_error(self):
        _, r = run(sizing(basis=""))
        self.assertTrue(any("missing basis" in e for e in r["errors"]))

    def test_zero_year_is_error(self):
        _, r = run(sizing(year=0))
        self.assertTrue(any("missing estimate year" in e for e in r["errors"]))


if __name__ == "__main__":
    unittest.main()
