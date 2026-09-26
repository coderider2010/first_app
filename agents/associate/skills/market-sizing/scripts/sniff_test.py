#!/usr/bin/env python3
"""Mechanical sniff tests for a market-sizing module.

Usage:
    python scripts/sniff_test.py sizing.json

Input: a JSON file describing the sizing. Required keys:
    market            str   e.g. "US pet insurance"
    year              int   the year the estimate is for
    currency          str   e.g. "USD"
    basis             str   "revenue" | "gmv" | "units" | "spend" | ...
    estimate          num   the headline number, in currency units (not millions)
    tolerance_pct     num   the decision's tolerance, e.g. 20 for +/-20%
    methods           obj   {"top_down": num, "bottom_up": num, ...} — >=2 entries

Optional keys (each unlocks further checks):
    growth_rate_pct        num   forecast CAGR, e.g. 12
    growth_horizon_years   num   horizon the CAGR is quoted over (default 5)
    shares                 obj   {"CompetitorName": fraction, ...} named-player shares
    shares_complete        bool  true if `shares` is meant to be exhaustive
    per_capita             obj   {"population": num, "anchor_low": num,
                                  "anchor_high": num, "unit": str}
                                  population = count of the denominator atom;
                                  anchors = plausible spend per atom, same currency

Output: JSON to stdout —
    status: "pass" | "flags_found" | "errors_found"
    errors: internal inconsistencies; the memo must not ship until they are fixed
    flags:  judgment calls the memo must explicitly address (not necessarily wrong)

Exit code is non-zero only for unusable input (missing file, bad JSON, missing
required keys). "errors_found" exits 0 — never treat a clean exit as a clean sizing.

A green run proves INTERNAL CONSISTENCY ONLY. It cannot tell you the market
definition is right, the sources are sound, or the atoms are the right atoms.
Those remain your job, per SKILL.md.
"""
import json
import math
import sys

REQUIRED = ["market", "year", "currency", "basis", "estimate", "tolerance_pct", "methods"]


def fail_input(msg):
    print(json.dumps({"error": msg}))
    sys.exit(1)


def sig_figs(x):
    """Count significant figures in a number as commonly quoted."""
    if x == 0:
        return 1
    s = f"{abs(x):.10e}"          # e.g. 4.7000000000e+09
    mantissa = s.split("e")[0].rstrip("0").replace(".", "")
    return max(1, len(mantissa))


def main():
    if len(sys.argv) != 2:
        fail_input("usage: sniff_test.py sizing.json")
    try:
        with open(sys.argv[1]) as f:
            d = json.load(f)
    except FileNotFoundError:
        fail_input(f"no such file: {sys.argv[1]}")
    except json.JSONDecodeError as e:
        fail_input(f"invalid JSON: {e}")

    missing = [k for k in REQUIRED if k not in d]
    if missing:
        fail_input(f"missing required keys: {missing}")
    if not isinstance(d["methods"], dict) or len(d["methods"]) < 2:
        fail_input("methods must contain >=2 independent estimates (triangulation rule)")

    errors, flags = [], []
    est = float(d["estimate"])
    tol = float(d["tolerance_pct"])
    methods = {k: float(v) for k, v in d["methods"].items()}
    lo, hi = min(methods.values()), max(methods.values())

    # --- Method triangulation ---
    spread = hi / lo - 1 if lo > 0 else math.inf
    if spread > 0.30:
        flags.append(
            f"method spread is {spread:.0%} (>{0.30:.0%}): reconcile the definitional "
            f"mismatch before presenting; do NOT average silently "
            f"(methods: { {k: f'{v:,.3g}' for k, v in methods.items()} })"
        )
    if not (lo <= est <= hi):
        errors.append(
            f"headline estimate {est:,.3g} lies outside the method range "
            f"[{lo:,.3g}, {hi:,.3g}] — the reconciliation does not support the number"
        )
    if spread * 100 > 2 * tol:
        flags.append(
            f"method spread ({spread:.0%}) exceeds twice the decision tolerance "
            f"(±{tol:.0f}%): say so in the memo and name the data that would close it"
        )

    # --- False precision ---
    if tol >= 15 and sig_figs(est) > 2:
        errors.append(
            f"estimate quoted to {sig_figs(est)} significant figures with ±{tol:.0f}% "
            f"tolerance — round to <=2 sig figs (false precision)"
        )

    # --- Growth compounding ---
    if "growth_rate_pct" in d:
        g = float(d["growth_rate_pct"]) / 100.0
        h = float(d.get("growth_horizon_years", 5))
        mult = (1 + g) ** h
        if mult > 3.0:
            flags.append(
                f"CAGR {g:.0%} over {h:.0f}y implies the market grows {mult:.1f}x — "
                f"extraordinary claim; the memo must defend it explicitly"
            )
        elif mult > 2.0:
            flags.append(
                f"CAGR {g:.0%} over {h:.0f}y implies the market doubles ({mult:.1f}x) — "
                f"confirm you believe it and say why"
            )
        if g < -0.5:
            errors.append(f"growth rate {g:.0%} looks like a data error (< -50%/yr)")

    # --- Share arithmetic ---
    if "shares" in d:
        tot = sum(float(v) for v in d["shares"].values())
        if any(float(v) > 1 for v in d["shares"].values()):
            errors.append("a single competitor share exceeds 100% — shares must be fractions")
        if tot > 1.005:
            errors.append(f"named shares sum to {tot:.1%} (>100%) — arithmetic broken")
        elif d.get("shares_complete") and tot < 0.90:
            flags.append(
                f"shares marked complete but sum to {tot:.1%} — either the list is not "
                f"exhaustive or the total market is oversized"
            )
        elif not d.get("shares_complete") and tot > 0.95:
            flags.append(
                f"named players already cover {tot:.1%} with the list marked incomplete — "
                f"total may be undersized"
            )

    # --- Implied per-atom spend vs anchors ---
    if "per_capita" in d:
        pc = d["per_capita"]
        for k in ("population", "anchor_low", "anchor_high"):
            if k not in pc:
                fail_input(f"per_capita requires '{k}'")
        implied = est / float(pc["population"])
        unit = pc.get("unit", "per atom")
        alo, ahi = float(pc["anchor_low"]), float(pc["anchor_high"])
        if not (alo <= implied <= ahi):
            errors.append(
                f"implied {implied:,.2f} {d['currency']} {unit} is outside the plausible "
                f"anchor range [{alo:,.2f}, {ahi:,.2f}] — the total or the atom count is wrong"
            )

    # --- Labeling ---
    for k, msg in (
        ("year", "estimate year"),
        ("currency", "currency"),
        ("basis", "basis (revenue vs GMV vs units)"),
    ):
        if not d.get(k):
            errors.append(f"missing {msg} — an unlabeled number is unusable downstream")

    status = "errors_found" if errors else ("flags_found" if flags else "pass")
    print(json.dumps({
        "status": status,
        "market": d["market"],
        "estimate": est,
        "checks_run": True,
        "errors": errors,
        "flags": flags,
        "note": "green = internally consistent, NOT correct; definitions and sources remain your job",
    }, indent=2))


if __name__ == "__main__":
    main()
