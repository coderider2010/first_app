#!/usr/bin/env python3
"""Forward DCF: value per share for each named scenario, plus a sensitivity table.

Usage:
    python scripts/dcf.py valuation.json            print the results
    python scripts/dcf.py valuation.json --write    also save them into valuation.json

Reads a valuation.json of type "dcf" (format in
implied-expectations/scripts/valuation_check.py) and prints JSON to stdout:
    scenarios    for each scenario: enterprise_value, equity_value, value_per_share,
                 terminal_share, and the year-by-year revenue and FCF (for the memo)
    sensitivity  value per share for each scenario at the base discount rate +/- 1
                 point x terminal growth +/- 0.5 point (capped at the terminal cap)

Paste the numbers into valuation.json; the gate recomputes them. It uses the same
model as reverse_dcf.py (one model, so modules 2 and 3 cannot drift apart):
growth may be a constant, a {"start", "end"} straight-line fade, or N yearly rates;
the FCF margin (after SBC) moves in a straight line to target_margin over
margin_ramp_years.
"""
import json
import os
import sys

sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "implied-expectations", "scripts"))
import reverse_dcf as model  # noqa: E402

val = model.val_of


def net_claims(d):
    """What sits between EV and equity: debt - cash + debt-like adjustments."""
    return val(d["debt"]) - val(d["cash"]) + sum(val(a) for a in d.get("other_ev_adjustments", []))


def value_scenario(d, sc, wacc=None, terminal_growth=None):
    m = model.model_inputs(d)
    wacc = val(d["discount_rate"]) if wacc is None else wacc
    g_t = val(sc.get("terminal_growth", d["terminal_growth"])) if terminal_growth is None else terminal_growth
    ramp = int(sc["margin_ramp_years"]) if sc.get("margin_ramp_years") else m["ramp"]
    target = float(sc["target_margin"])
    args = (m["base_revenue"], m["base_margin"], sc["growth"], target, wacc, g_t, m["horizon"], ramp)
    ev = model.enterprise_value(*args)
    equity = ev - net_claims(d)
    return {
        "enterprise_value": round(ev),
        "equity_value": round(equity),
        "value_per_share": round(equity / val(d["shares"]), 2),
        "terminal_share": round(model.terminal_share(*args), 3),
    }


def yearly(d, sc):
    """Revenue, growth, margin and FCF by year, for the memo's drivers table."""
    m = model.model_inputs(d)
    ramp = int(sc["margin_ramp_years"]) if sc.get("margin_ramp_years") else (m["ramp"] or m["horizon"])
    target, revenue, rows = float(sc["target_margin"]), m["base_revenue"], []
    for t, g in enumerate(model.growth_path(sc["growth"], m["horizon"]), start=1):
        revenue *= 1 + g
        margin = m["base_margin"] + (target - m["base_margin"]) * min(t / ramp, 1.0)
        rows.append({"year": t, "growth": round(g, 4), "revenue": round(revenue),
                     "margin": round(margin, 4), "fcf": round(revenue * margin)})
    return rows


def main():
    args = [a for a in sys.argv[1:] if a != "--write"]
    if len(args) != 1:
        print(json.dumps({"error": "usage: dcf.py valuation.json [--write]"}))
        sys.exit(1)
    try:
        with open(args[0]) as f:
            d = json.load(f)
        wacc, cap = val(d["discount_rate"]), d["terminal_growth"].get("cap")
        out = {"scenarios": {}, "sensitivity": []}
        for name, sc in d["scenarios"].items():
            out["scenarios"][name] = dict(value_scenario(d, sc), years=yearly(d, sc))
            g_base = val(sc.get("terminal_growth", d["terminal_growth"]))
            for w_off in (-0.01, 0.0, 0.01):
                for g_off in (-0.005, 0.0, 0.005):
                    w, g = round(wacc + w_off, 6), round(g_base + g_off, 6)
                    if cap is not None and g > float(cap) + 1e-9:
                        continue
                    out["sensitivity"].append({
                        "scenario": name, "wacc": w, "terminal_growth": g,
                        "value_per_share": value_scenario(d, sc, w, g)["value_per_share"],
                    })
        if "--write" in sys.argv:
            for name, res in out["scenarios"].items():
                d["scenarios"][name].update({k: v for k, v in res.items() if k != "years"})
            d["sensitivity"] = out["sensitivity"]
            with open(args[0], "w") as f:
                json.dump(d, f, indent=2)
    except (OSError, json.JSONDecodeError, KeyError, ValueError, TypeError) as e:
        print(json.dumps({"error": f"{type(e).__name__}: {e}"}))
        sys.exit(1)
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
