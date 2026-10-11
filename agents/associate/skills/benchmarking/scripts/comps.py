#!/usr/bin/env python3
"""Peer comparison (trading multiples): what listed peers imply a company is worth.

Usage:
    python scripts/comps.py valuation.json            print the results
    python scripts/comps.py valuation.json --write    also save them into valuation.json
                                                      (sets range to the regression band
                                                      unless a range is already there)

Reads a valuation.json of type "comps" (format in
implied-expectations/scripts/valuation_check.py) and prints JSON to stdout:
    peers       for each included peer: EV, EV/revenue, EV/FCF, FCF margin, and its
                "rule of 40" score (revenue growth + FCF margin after SBC)
    regression  EV/revenue fitted on the rule of 40 score across peers: slope,
                intercept, r2, and the spread (standard deviation) of the residuals
    methods     value per share for the target under each method:
                  median_ev_revenue      median peer EV/revenue x target revenue
                  rule_of_40_regression  the fitted multiple at the target's score
                  median_ev_fcf          median peer EV/FCF x target FCF (after SBC)
    regression_band  the regression value +/- one residual spread, per share

Paste the results into valuation.json; the gate recomputes them.

Why adjust: a faster-growing or more profitable company deserves a higher multiple,
so a plain median compares unlike with like. The rule of 40 score combines growth and
margin in one number, so the regression asks "what multiple do peers with this mix
of growth and profit get?" With 5-8 peers the fit is rough: read r2 before trusting it.

All rates are decimals; money is in currency units.
"""
import json
import statistics
import sys


def val(v):
    """A number, or the "value" of a sourced {"value", "source"} object."""
    return float(v["value"] if isinstance(v, dict) else v)


def peer_metrics(p):
    ev = val(p["price"]) * val(p["shares"]) + val(p["debt"]) - val(p["cash"])
    revenue, fcf = val(p["revenue_ttm"]), val(p["fcf_after_sbc_ttm"])
    margin = fcf / revenue
    return {
        "enterprise_value": round(ev),
        "ev_revenue": round(ev / revenue, 3),
        "ev_fcf": round(ev / fcf, 2) if fcf > 0 else None,
        "fcf_margin": round(margin, 4),
        "rule_of_40": round(val(p["revenue_growth"]) + margin, 4),
    }


def fit(xs, ys):
    """Ordinary least squares y = a + b x; returns slope, intercept, r2, residual spread."""
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    sxx = sum((x - mx) ** 2 for x in xs)
    if sxx == 0:
        raise ValueError("all peers have the same rule of 40 score: nothing to fit")
    slope = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sxx
    intercept = my - slope * mx
    resid = [y - (intercept + slope * x) for x, y in zip(xs, ys)]
    ss_tot = sum((y - my) ** 2 for y in ys)
    r2 = 1 - sum(r * r for r in resid) / ss_tot if ss_tot else 0.0
    spread = (sum(r * r for r in resid) / (n - 2)) ** 0.5 if n > 2 else float("nan")
    return {"slope": round(slope, 4), "intercept": round(intercept, 4),
            "r2": round(r2, 3), "residual_spread": round(spread, 4)}


def target_metrics(d):
    t = d["target"]
    revenue = val(t["revenue_ttm"])
    margin = val(t["fcf_after_sbc_ttm"]) / revenue
    return revenue, val(t["fcf_after_sbc_ttm"]), val(t["revenue_growth"]) + margin


def per_share(d, ev):
    """Target equity value per share from an enterprise value."""
    net_claims = (val(d["debt"]) - val(d["cash"])
                  + sum(val(a) for a in d.get("other_ev_adjustments", [])))
    return round((ev - net_claims) / val(d["shares"]), 2)


def run(d):
    peers = {name: peer_metrics(p) for name, p in d["peers"].items()}
    multiples = [m["ev_revenue"] for m in peers.values()]
    fcf_multiples = [m["ev_fcf"] for m in peers.values() if m["ev_fcf"] is not None]
    reg = fit([m["rule_of_40"] for m in peers.values()], multiples)
    revenue, fcf, score = target_metrics(d)
    fitted = reg["intercept"] + reg["slope"] * score
    methods = {
        "median_ev_revenue": per_share(d, statistics.median(multiples) * revenue),
        "rule_of_40_regression": per_share(d, fitted * revenue),
    }
    if fcf_multiples and fcf > 0:
        methods["median_ev_fcf"] = per_share(d, statistics.median(fcf_multiples) * fcf)
    band = {
        "low": per_share(d, (fitted - reg["residual_spread"]) * revenue),
        "high": per_share(d, (fitted + reg["residual_spread"]) * revenue),
    }
    return {
        "peers": peers,
        "regression": dict(reg, target_rule_of_40=round(score, 4),
                           target_fitted_ev_revenue=round(fitted, 3)),
        "methods": methods,
        "regression_band": band,
    }


def write_back(path, d, out):
    """Merge computed numbers into valuation.json, so nothing is copied by hand."""
    for name, m in out["peers"].items():
        d["peers"][name].update(m)
    d["methods"] = out["methods"]
    d["regression"] = {k: out["regression"][k] for k in ("slope", "intercept", "r2", "residual_spread")}
    d.setdefault("range", dict(out["regression_band"], basis="regression_band"))
    with open(path, "w") as f:
        json.dump(d, f, indent=2)


def main():
    args = [a for a in sys.argv[1:] if a != "--write"]
    if len(args) != 1:
        print(json.dumps({"error": "usage: comps.py valuation.json [--write]"}))
        sys.exit(1)
    try:
        with open(args[0]) as f:
            d = json.load(f)
        out = run(d)
        if "--write" in sys.argv:
            write_back(args[0], d, out)
    except (OSError, json.JSONDecodeError, KeyError, ValueError, TypeError,
            ZeroDivisionError, statistics.StatisticsError) as e:
        print(json.dumps({"error": f"{type(e).__name__}: {e}"}))
        sys.exit(1)
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
