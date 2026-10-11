#!/usr/bin/env python3
"""Reverse DCF: solve for the growth and margin a market price implies.

Usage:
    python scripts/reverse_dcf.py valuation.json

Reads the inputs block of valuation.json (see valuation_check.py for the full
format) and prints a JSON grid to stdout: for each (growth, discount rate) pair,
the long-run free cash flow margin that makes the DCF equal today's enterprise
value. Paste the grid into valuation.json and the memo; the gate recomputes it.

The model (deliberately simple, so every step can be checked by hand):
    revenue_t = base_revenue * (1 + g)^t                    t = 1..N
    margin_t  = base_margin + (target_margin - base_margin) * min(t / ramp, 1)
    fcf_t     = revenue_t * margin_t
    terminal  = fcf_N * (1 + g_T) / (r - g_T)               valued at the end of year N
    EV        = sum(fcf_t / (1 + r)^t) + terminal / (1 + r)^N

Free cash flow here is AFTER stock-based compensation (SBC treated as a cash cost),
so base_margin and the solved margin are both after SBC.

EV is a straight line in target_margin (every term is linear in it), so the
implied margin has an exact closed form: EV(m) = EV(0) + m * (EV(1) - EV(0)).
Implied growth for a given margin has no closed form and is found by bisection.

All rates are decimals: 0.12 means 12%.
"""
import json
import sys


def enterprise_value(base_revenue, base_margin, growth, target_margin, wacc,
                     terminal_growth, horizon=10, ramp=None):
    """DCF enterprise value under the model in the module docstring."""
    if wacc <= terminal_growth:
        raise ValueError("discount rate must exceed terminal growth")
    ramp = ramp or horizon
    ev, fcf = 0.0, 0.0
    for t in range(1, horizon + 1):
        margin = base_margin + (target_margin - base_margin) * min(t / ramp, 1.0)
        fcf = base_revenue * (1 + growth) ** t * margin
        ev += fcf / (1 + wacc) ** t
    terminal = fcf * (1 + terminal_growth) / (wacc - terminal_growth)
    return ev + terminal / (1 + wacc) ** horizon


def terminal_share(base_revenue, base_margin, growth, target_margin, wacc,
                   terminal_growth, horizon=10, ramp=None):
    """Fraction of EV that comes from the terminal value."""
    total = enterprise_value(base_revenue, base_margin, growth, target_margin, wacc,
                             terminal_growth, horizon, ramp)
    ramp = ramp or horizon
    margin_n = base_margin + (target_margin - base_margin) * min(horizon / ramp, 1.0)
    fcf_n = base_revenue * (1 + growth) ** horizon * margin_n
    terminal = fcf_n * (1 + terminal_growth) / (wacc - terminal_growth) / (1 + wacc) ** horizon
    return terminal / total if total else float("nan")


def implied_margin(target_ev, base_revenue, base_margin, growth, wacc,
                   terminal_growth, horizon=10, ramp=None):
    """Long-run FCF margin that makes EV equal target_ev (exact: EV is linear in it)."""
    args = (base_revenue, base_margin, growth)
    ev0 = enterprise_value(*args, 0.0, wacc, terminal_growth, horizon, ramp)
    ev1 = enterprise_value(*args, 1.0, wacc, terminal_growth, horizon, ramp)
    return (target_ev - ev0) / (ev1 - ev0)


def implied_growth(target_ev, base_revenue, base_margin, target_margin, wacc,
                   terminal_growth, horizon=10, ramp=None, lo=-0.5, hi=1.0):
    """Annual revenue growth that makes EV equal target_ev, by bisection.

    Returns None if no growth rate in [lo, hi] gets there (for example when the
    margin is so low that even very fast growth cannot justify the price).
    """
    def gap(g):
        return enterprise_value(base_revenue, base_margin, g, target_margin, wacc,
                                terminal_growth, horizon, ramp) - target_ev

    if gap(lo) > 0 or gap(hi) < 0:
        return None
    for _ in range(200):
        mid = (lo + hi) / 2
        if gap(mid) > 0:
            hi = mid
        else:
            lo = mid
    return (lo + hi) / 2


def val_of(v):
    """A number, or the "value" of a sourced {"value", "source"} object."""
    return float(v["value"] if isinstance(v, dict) else v)


def model_inputs(d):
    """Pull the model inputs out of a valuation.json dict."""
    return {
        "base_revenue": val_of(d["base_revenue"]),
        "base_margin": val_of(d["base_fcf_margin"]),
        "terminal_growth": val_of(d["terminal_growth"]),
        "horizon": int(d.get("horizon_years", 10)),
        "ramp": int(d["margin_ramp_years"]) if d.get("margin_ramp_years") else None,
    }


def build_grid(d, growths, wacc_offsets=(-0.01, 0.0, 0.01)):
    """Implied margin for each growth rate, at the base discount rate and +/- offsets."""
    m = model_inputs(d)
    ev = float(d["enterprise_value"])
    base_wacc = val_of(d["discount_rate"])
    grid = []
    for w_off in wacc_offsets:
        wacc = round(base_wacc + w_off, 6)
        for g in growths:
            margin = implied_margin(ev, m["base_revenue"], m["base_margin"], g, wacc,
                                    m["terminal_growth"], m["horizon"], m["ramp"])
            share = terminal_share(m["base_revenue"], m["base_margin"], g, margin, wacc,
                                   m["terminal_growth"], m["horizon"], m["ramp"])
            grid.append({"growth": g, "wacc": wacc, "margin": round(margin, 4),
                         "terminal_share": round(share, 3)})
    return grid


def main():
    if len(sys.argv) != 2:
        print(json.dumps({"error": "usage: reverse_dcf.py valuation.json"}))
        sys.exit(1)
    try:
        with open(sys.argv[1]) as f:
            d = json.load(f)
        growths = d.get("grid_growths", [0.06, 0.08, 0.10, 0.12, 0.14, 0.16, 0.18, 0.20])
        grid = build_grid(d, [float(g) for g in growths])
    except (OSError, json.JSONDecodeError, KeyError, ValueError, TypeError) as e:
        print(json.dumps({"error": f"{type(e).__name__}: {e}"}))
        sys.exit(1)
    print(json.dumps({"grid": grid}, indent=2))


if __name__ == "__main__":
    main()
