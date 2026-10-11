#!/usr/bin/env python3
"""Mechanical checks for a valuation module: catches classic DCF errors.

Usage:
    python scripts/valuation_check.py valuation.json

Input: a JSON file. Rates are decimals (0.095 = 9.5%); money is in currency units
(not millions). "Sourced" fields are objects {"value": ..., "source": "..."}.

Two types share most keys: "reverse_dcf" (what the price implies; module 2) and
"dcf" (value per share under named scenarios; module 3).

Required keys (both types):
    type              "reverse_dcf" or "dcf"
    company, as_of    str; as_of is the valuation date, YYYY-MM-DD
    currency          str
    price             {"value", "date", "source"}        share price used
    shares            {"value", "basis", "source"}       basis "diluted" or "basic"
    debt, cash        sourced numbers (cash includes investments)
    equity_value      price x shares
    enterprise_value  equity_value + debt - cash + sum(other_ev_adjustments)
    base_revenue      {"value", "period", "source"}      e.g. TTM revenue
    base_fcf_margin   {"value", "definition", "source"}  FCF after SBC / revenue
    sbc_treatment     "expense" (SBC deducted from FCF) or "dilution"
    discount_rate     {"value", "risk_free", "beta", "equity_risk_premium"}; each
                      input sourced. Optional "cost_of_debt", "tax_rate",
                      "debt_weight" (sourced) for a blended rate.
    terminal_growth   {"value", "source", "cap", "cap_source"}

Required for "reverse_dcf":
    equity_value, enterprise_value   as above
    grid              [{"growth", "wacc", "margin"}, ...] from reverse_dcf.py
    headline          {"growth", "margin", "wacc"}       the answer-first sentence

Required for "dcf" (generate the numbers with valuation-dcf/scripts/dcf.py):
    scenarios         {"name": {
                         "narrative": str, what the business has to be true for this,
                         "growth": number, {"start", "end"} fade, or a list of N rates,
                         "target_margin": long-run FCF margin after SBC,
                         "margin_ramp_years": optional (default horizon),
                         "terminal_growth": optional override (must respect the cap),
                         "evidence": [{"claim", "source"}, ...]   at least 2,
                         "enterprise_value", "equity_value", "value_per_share",
                         "terminal_share"}}                         at least 2 scenarios
    sensitivity       [{"scenario", "wacc", "terminal_growth", "value_per_share"}, ...]
                      must include the base discount rate +/- 1 point

Optional:
    horizon_years, margin_ramp_years   model settings (default 10, 10)
    other_ev_adjustments               [{"name", "value", "source"}], debt-like
                                       items added to EV (subtracted from equity)
    peer_margins                       {"Peer": {"value", "source"}} long-run
                                       FCF margins (same SBC treatment)

Output: JSON to stdout, same contract as sniff_test.py:
    status: "pass" | "flags_found" | "errors_found"
    errors: the memo must not ship until these are fixed
    flags:  judgment calls the memo must address explicitly

Exit code is non-zero only for unusable input. "errors_found" exits 0.

A green run proves INTERNAL CONSISTENCY ONLY: the arithmetic ties and the classic
traps are avoided. It cannot tell you the inputs are right.
"""
import json
import os
import sys
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import reverse_dcf as model  # noqa: E402

REQUIRED = [
    "type", "company", "as_of", "currency", "price", "shares", "debt", "cash",
    "base_revenue", "base_fcf_margin", "sbc_treatment", "discount_rate", "terminal_growth",
]
REQUIRED_BY_TYPE = {
    "reverse_dcf": ["equity_value", "enterprise_value", "grid", "headline"],
    "dcf": ["scenarios", "sensitivity"],
}
VALUE_TOL = 0.01       # scenario values must match a recompute within 1%
SCENARIOS_TOO_CLOSE = 0.10
MIN_EVIDENCE = 2
MONEY_TOL = 0.005      # bridge arithmetic must tie within 0.5%
RATE_TOL = 0.0025      # recomputed rates must match within 0.25 percentage points
MARGIN_TOL = 0.005     # grid margins must match a recompute within 0.5 points
MAX_MARGIN_AFTER_SBC = 0.35   # few mature software companies sustain more
TERMINAL_SHARE_FLAG = 0.75
STALE_PRICE_DAYS = 7


def fail_input(msg):
    print(json.dumps({"error": msg}))
    sys.exit(1)


def num(v):
    return float(v["value"] if isinstance(v, dict) else v)


def pct(x):
    return f"{x * 100:.1f}%"


def unsourced(v):
    return not (isinstance(v, dict) and str(v.get("source", "")).strip())


def main():
    if len(sys.argv) != 2:
        fail_input("usage: valuation_check.py valuation.json")
    try:
        with open(sys.argv[1]) as f:
            d = json.load(f)
    except FileNotFoundError:
        fail_input(f"no such file: {sys.argv[1]}")
    except json.JSONDecodeError as e:
        fail_input(f"invalid JSON: {e}")
    if d.get("type") not in REQUIRED_BY_TYPE:
        fail_input(f"unknown type {d.get('type')!r}; expected one of {list(REQUIRED_BY_TYPE)}")
    missing = [k for k in REQUIRED + REQUIRED_BY_TYPE[d["type"]] if k not in d]
    if missing:
        fail_input(f"missing required keys: {missing}")
    try:
        errors, flags = check_common(d)
        more = check_reverse(d) if d["type"] == "reverse_dcf" else check_scenarios(d)
        errors += more[0]
        flags += more[1]
    except (KeyError, TypeError, ValueError) as e:
        fail_input(f"malformed field: {type(e).__name__}: {e}")

    status = "errors_found" if errors else ("flags_found" if flags else "pass")
    print(json.dumps({
        "status": status,
        "company": d["company"],
        "type": d["type"],
        "checks_run": True,
        "errors": errors,
        "flags": flags,
        "note": "green = internally consistent, NOT correct; inputs and judgment remain your job",
    }, indent=2))


def check_common(d):
    """Checks that apply to any valuation: sources, shares, SBC, discount and terminal rates."""
    errors, flags = [], []

    # --- Sources: every input cited (brief rule; untraceable numbers are not presented) ---
    for key in ("price", "shares", "debt", "cash", "base_revenue", "base_fcf_margin"):
        if unsourced(d[key]):
            errors.append(f"{key} has no source")
    if not d["price"].get("date"):
        errors.append("price has no date: a price without a date cannot be checked")

    for a in d.get("other_ev_adjustments", []):
        if unsourced(a):
            errors.append(f"EV adjustment {a.get('name', '?')!r} has no source")
    if num(d["shares"]) <= 0:
        errors.append("shares must be positive")
    if d["shares"].get("basis") != "diluted":
        flags.append(
            "shares are not on a diluted basis: per-share value needs RSUs, PSUs and "
            "options (treasury stock method) or the equity value is understated"
        )

    # --- Price freshness ---
    try:
        age = (date.fromisoformat(d["as_of"]) - date.fromisoformat(d["price"]["date"])).days
        if age > STALE_PRICE_DAYS:
            flags.append(f"price is {age} days older than as_of: refresh it or say why not")
        if age < 0:
            errors.append("price date is after the valuation date (as_of)")
    except (ValueError, TypeError):
        errors.append("as_of and price.date must be YYYY-MM-DD")

    # --- Stock-based compensation ---
    sbc = d["sbc_treatment"]
    if sbc not in ("expense", "dilution"):
        errors.append(
            "sbc_treatment must be 'expense' (deduct SBC from FCF) or 'dilution' "
            "(model future share growth); ignoring SBC overstates value"
        )
    elif sbc == "dilution":
        flags.append(
            "sbc_treatment is 'dilution': reverse_dcf.py models SBC as an expense only, so "
            "the solved margins are before SBC; the memo must model share dilution "
            "separately and compare against pre-SBC peer margins"
        )

    # --- Discount rate: recompute from its inputs ---
    dr = d["discount_rate"]
    wacc = num(dr)
    for k in ("risk_free", "beta", "equity_risk_premium"):
        if k not in dr:
            errors.append(f"discount_rate.{k} missing: derive the rate, don't assert it")
        elif unsourced(dr[k]):
            errors.append(f"discount_rate.{k} has no source")
    if all(k in dr for k in ("risk_free", "beta", "equity_risk_premium")):
        cost_of_equity = num(dr["risk_free"]) + num(dr["beta"]) * num(dr["equity_risk_premium"])
        expected = cost_of_equity
        if "debt_weight" in dr:
            w = num(dr["debt_weight"])
            kd = num(dr.get("cost_of_debt", 0)) * (1 - num(dr.get("tax_rate", 0)))
            expected = (1 - w) * cost_of_equity + w * kd
        if abs(expected - wacc) > RATE_TOL:
            errors.append(
                f"discount rate {pct(wacc)} does not match its inputs ({pct(expected)} "
                f"from risk-free + beta x premium{' blended with debt' if 'debt_weight' in dr else ''})"
            )

    # --- Terminal growth ---
    tg = d["terminal_growth"]
    g_t = num(tg)
    if "cap" not in tg or unsourced({"source": tg.get("cap_source", "")}):
        errors.append("terminal_growth needs a cap (long-run nominal GDP growth) and cap_source")
    elif g_t > float(tg["cap"]) + 1e-9:
        errors.append(
            f"terminal growth {pct(g_t)} exceeds its cap {pct(float(tg['cap']))}: "
            f"no company outgrows the economy forever"
        )
    if unsourced(tg):
        errors.append("terminal_growth has no source")
    if g_t >= wacc:
        errors.append(
            f"terminal growth {pct(g_t)} >= discount rate {pct(wacc)}: the terminal "
            f"value is infinite or negative"
        )

    return errors, flags


def ev_to_equity(d):
    """Debt, cash and adjustments: equity = EV - net_claims."""
    return (num(d["debt"]) - num(d["cash"])
            + sum(num(a) for a in d.get("other_ev_adjustments", [])))


def check_reverse(d):
    """Reverse DCF: today's EV bridge, the grid, the headline, and how demanding it is."""
    errors, flags = [], []
    wacc, g_t, sbc = num(d["discount_rate"]), num(d["terminal_growth"]), d["sbc_treatment"]

    # --- Equity and enterprise value bridge ---
    price, shares = num(d["price"]), num(d["shares"])
    equity, ev = float(d["equity_value"]), float(d["enterprise_value"])
    if abs(price * shares - equity) > MONEY_TOL * abs(equity):
        errors.append(
            f"equity_value {equity:,.0f} != price x shares {price * shares:,.0f}"
        )
    bridge = equity + ev_to_equity(d)
    if abs(bridge - ev) > MONEY_TOL * abs(ev):
        errors.append(
            f"enterprise_value {ev:,.0f} != equity + debt - cash + adjustments "
            f"{bridge:,.0f}"
        )
    if ev <= 0:
        errors.append("enterprise value is not positive: a reverse DCF has nothing to solve")

    # --- Grid: recompute every cell ---
    m = model.model_inputs(d)
    grid = d["grid"]
    if not grid:
        errors.append("grid is empty")
    bad = []
    for cell in grid:
        g, w, margin = float(cell["growth"]), float(cell["wacc"]), float(cell["margin"])
        if w <= g_t:
            bad.append(f"growth {pct(g)} at {pct(w)}: discount rate <= terminal growth")
            continue
        solved = model.implied_margin(ev, m["base_revenue"], m["base_margin"], g, w,
                                      g_t, m["horizon"], m["ramp"])
        if abs(solved - margin) > MARGIN_TOL:
            bad.append(f"growth {pct(g)} at {pct(w)}: grid says {pct(margin)}, model gives {pct(solved)}")
    if bad:
        errors.append(
            "grid cells do not reproduce today's enterprise value (regenerate with "
            "reverse_dcf.py, don't edit by hand): " + "; ".join(bad[:5])
            + (f" (+{len(bad) - 5} more)" if len(bad) > 5 else "")
        )
    waccs = {round(float(c["wacc"]), 4) for c in grid}
    for off in (-0.01, 0.01):
        if round(wacc + off, 4) not in waccs:
            errors.append(f"grid has no column at discount rate {pct(wacc + off)} (brief: show ±1 point)")

    # --- Headline ---
    h = d["headline"]
    hg, hm, hw = float(h["growth"]), float(h["margin"]), float(h.get("wacc", wacc))
    if hw > g_t:
        solved = model.implied_margin(ev, m["base_revenue"], m["base_margin"], hg, hw,
                                      g_t, m["horizon"], m["ramp"])
        if abs(solved - hm) > MARGIN_TOL:
            errors.append(
                f"headline ({pct(hg)} growth, {pct(hm)} margin) does not reproduce today's "
                f"value: at {pct(hg)} growth the model needs {pct(solved)}"
            )
        share = model.terminal_share(m["base_revenue"], m["base_margin"], hg, hm, hw,
                                     g_t, m["horizon"], m["ramp"])
        if share > TERMINAL_SHARE_FLAG:
            flags.append(
                f"terminal value is {share:.0%} of EV at the headline: the answer rests on "
                f"years 11+, so say how sensitive it is to terminal growth"
            )

    # --- Plausibility of the implied expectations ---
    multiple = (1 + hg) ** m["horizon"]
    if multiple > 5:
        flags.append(
            f"headline growth compounds to {multiple:.1f}x revenue in {m['horizon']} years: "
            f"compare with how often companies of this size have done it"
        )
    ceiling = MAX_MARGIN_AFTER_SBC if sbc == "expense" else MAX_MARGIN_AFTER_SBC + 0.10
    if hm > ceiling:
        flags.append(
            f"headline margin {pct(hm)} is above {pct(ceiling)}, more than most mature "
            f"software companies sustain: name any that do"
        )
    if hm < num(d["base_fcf_margin"]):
        flags.append(
            f"headline margin {pct(hm)} is below today's {pct(num(d['base_fcf_margin']))}: "
            f"the price implies margins fall; check that is the reading you intend"
        )
    peers = d.get("peer_margins") or {}
    if not peers:
        flags.append("no peer_margins: the implied margin is not compared with mature peers")
    else:
        for name, p in peers.items():
            if unsourced(p):
                errors.append(f"peer margin for {name} has no source")
        top = max(num(p) for p in peers.values())
        low = min(num(p) for p in peers.values())
        if hm > top:
            flags.append(
                f"headline margin {pct(hm)} is above every peer (highest {pct(top)}): "
                f"the price assumes {d['company']} beats the best of its peers"
            )
        elif hm < low:
            flags.append(
                f"headline margin {pct(hm)} is below every peer (lowest {pct(low)}): the "
                f"price looks undemanding; check it against the working answer and "
                f"escalate if it cuts against it"
            )

    return errors, flags


def check_scenarios(d):
    """Forward DCF: recompute each scenario and the sensitivity table; test the stories."""
    errors, flags = [], []
    m = model.model_inputs(d)
    wacc, shares, cap = num(d["discount_rate"]), num(d["shares"]), d["terminal_growth"].get("cap")
    scenarios = d["scenarios"]
    if len(scenarios) < 2:
        errors.append("need at least 2 scenarios: one story is a forecast, not a range")

    values = {}
    for name, sc in scenarios.items():
        g_t = num(sc.get("terminal_growth", d["terminal_growth"]))
        if cap is not None and g_t > float(cap) + 1e-9:
            errors.append(f"{name}: terminal growth {pct(g_t)} exceeds the cap {pct(float(cap))}")
        if g_t >= wacc:
            errors.append(f"{name}: terminal growth {pct(g_t)} >= discount rate {pct(wacc)}")
            continue
        if not str(sc.get("narrative", "")).strip():
            errors.append(f"{name}: no narrative (say what has to be true about the business)")
        evidence = [e for e in sc.get("evidence", []) if not unsourced(e) and e.get("claim")]
        if len(evidence) < MIN_EVIDENCE:
            errors.append(
                f"{name}: {len(evidence)} sourced evidence items; need at least {MIN_EVIDENCE} "
                f"(each {{claim, source}}) or the story is a guess"
            )
        ramp = int(sc["margin_ramp_years"]) if sc.get("margin_ramp_years") else m["ramp"]
        path = model.growth_path(sc["growth"], m["horizon"])
        target = float(sc["target_margin"])
        ev = model.enterprise_value(m["base_revenue"], m["base_margin"], sc["growth"], target,
                                    wacc, g_t, m["horizon"], ramp)
        per_share = (ev - ev_to_equity(d)) / shares
        values[name] = per_share
        stated = float(sc["value_per_share"])
        if abs(stated - per_share) > VALUE_TOL * abs(per_share):
            errors.append(
                f"{name}: value per share {stated:,.2f} does not match the model "
                f"({per_share:,.2f}); regenerate with dcf.py, don't edit by hand"
            )
        share = model.terminal_share(m["base_revenue"], m["base_margin"], sc["growth"], target,
                                     wacc, g_t, m["horizon"], ramp)
        if share > TERMINAL_SHARE_FLAG:
            flags.append(f"{name}: terminal value is {share:.0%} of EV; say how sensitive it is")
        if path[-1] > g_t + 0.03:
            flags.append(
                f"{name}: growth is still {pct(path[-1])} in year {m['horizon']}, far above "
                f"terminal growth {pct(g_t)}: the step down at the terminal year is abrupt"
            )
        ceiling = MAX_MARGIN_AFTER_SBC if d["sbc_treatment"] == "expense" else MAX_MARGIN_AFTER_SBC + 0.10
        if target > ceiling:
            flags.append(f"{name}: target margin {pct(target)} is above {pct(ceiling)}; name who sustains it")
        peers = d.get("peer_margins") or {}
        if peers and target > max(num(p) for p in peers.values()):
            flags.append(f"{name}: target margin {pct(target)} is above every peer")

    if not d.get("peer_margins"):
        flags.append("no peer_margins: scenario margins are not compared with peers")

    # --- The stories must differ, and be compared with the price ---
    if len(values) >= 2:
        lo, hi = min(values.values()), max(values.values())
        if lo > 0 and hi / lo - 1 < SCENARIOS_TOO_CLOSE:
            flags.append(
                f"scenario values are within {SCENARIOS_TOO_CLOSE:.0%} of each other "
                f"({lo:,.0f} to {hi:,.0f}): the stories don't differ enough to inform a decision"
            )
        price = num(d["price"])
        if not (lo <= price <= hi):
            flags.append(
                f"today's price {price:,.2f} is outside the scenario range "
                f"({lo:,.2f} to {hi:,.2f}): the market believes neither story; say what it sees"
            )

    # --- Sensitivity table: recompute every cell ---
    sens = d["sensitivity"]
    bad, waccs = [], set()
    for cell in sens:
        name = cell.get("scenario")
        if name not in scenarios:
            bad.append(f"unknown scenario {name!r}")
            continue
        sc = scenarios[name]
        w, g_t = float(cell["wacc"]), float(cell["terminal_growth"])
        waccs.add(round(w, 4))
        if w <= g_t:
            bad.append(f"{name} at {pct(w)}/{pct(g_t)}: discount rate <= terminal growth")
            continue
        ramp = int(sc["margin_ramp_years"]) if sc.get("margin_ramp_years") else m["ramp"]
        ev = model.enterprise_value(m["base_revenue"], m["base_margin"], sc["growth"],
                                    float(sc["target_margin"]), w, g_t, m["horizon"], ramp)
        per_share = (ev - ev_to_equity(d)) / shares
        if abs(float(cell["value_per_share"]) - per_share) > VALUE_TOL * abs(per_share):
            bad.append(f"{name} at {pct(w)}/{pct(g_t)}: says {float(cell['value_per_share']):,.2f}, "
                       f"model gives {per_share:,.2f}")
    if bad:
        errors.append("sensitivity cells do not match the model: " + "; ".join(bad[:5])
                      + (f" (+{len(bad) - 5} more)" if len(bad) > 5 else ""))
    for off in (-0.01, 0.01):
        if round(wacc + off, 4) not in waccs:
            errors.append(f"sensitivity has no discount rate {pct(wacc + off)} (brief: ±1 point)")

    return errors, flags


if __name__ == "__main__":
    main()
