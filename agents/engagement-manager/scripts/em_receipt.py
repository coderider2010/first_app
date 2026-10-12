#!/usr/bin/env python3
"""The EM's receipt check: is a returned module ready to accept?

Usage:
    python agents/engagement-manager/scripts/em_receipt.py engagements/<eng>/modules/<id>
           [--seed N]

Reads the module folder and the engagement's engagement.json (two levels up) and
prints JSON to stdout:
    verdict        "ready_to_review" | "needs_fix" | "escalated"
    problems       must be fixed before the EM accepts (send back to the Associate)
    flags_to_confirm   verifier flags: confirm the memo addresses each one
    spot_checks    3 randomly chosen sourced rows from the memo: re-pull each from the
                   source yourself before accepting (the Associate can't predict which)

What it checks:
    - memo.md exists, has an Answer section and states a confidence level
    - the gate's verifier (sniff_test.py or valuation_check.py) passes when re-run
    - shared inputs in valuation.json match the values pinned in engagement.json
      ("pinned": {"shares": ..., "cash": ..., "debt": ..., "price": {"value", "date"}}),
      so every module uses one number for one quantity

A "ready_to_review" verdict is not acceptance. It means the mechanical checks pass;
the EM still re-pulls the spot checks and reads the memo (EM charter, quality review).
"""
import json
import random
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
SKILLS = REPO / "agents" / "associate" / "skills"
VERIFIERS = {
    "sizing.json": SKILLS / "market-sizing" / "scripts" / "sniff_test.py",
    "valuation.json": SKILLS / "implied-expectations" / "scripts" / "valuation_check.py",
}
PIN_TOL = 0.005
SPOT_CHECKS = 3
SEPARATOR = re.compile(r"^\|[\s:|-]+\|$")


def sourced_rows(memo):
    """Body rows of every markdown table whose header has a Source column.

    That is the Exhibit A format the fact-base-contribution skill sets, so these are
    the rows that claim a traceable source.
    """
    rows, lines = [], [line.strip() for line in memo.splitlines()]
    for i in range(len(lines) - 1):
        header, sep = lines[i], lines[i + 1]
        if not (header.startswith("|") and SEPARATOR.match(sep)):
            continue
        cells = [c.strip().strip("*").lower() for c in header.strip("|").split("|")]
        if not any(c.startswith("source") for c in cells):
            continue
        for row in lines[i + 2:]:
            if not row.startswith("|"):
                break
            rows.append(row)
    return rows


def val(v):
    return float(v["value"] if isinstance(v, dict) else v)


def check(module, seed=None):
    problems, flags, verdict = [], [], None
    if (module / "escalation.md").exists():
        verdict = "escalated"

    memo_path = module / "memo.md"
    memo = memo_path.read_text() if memo_path.exists() else ""
    if not memo:
        problems.append("memo.md is missing or empty")
    else:
        if not re.search(r"^#+\s*Answer\b", memo, re.MULTILINE | re.IGNORECASE):
            problems.append("memo has no Answer section (answer-first rule)")
        if not re.search(r"Confidence[^\n]*\b(high|medium|low)\b", memo, re.IGNORECASE):
            problems.append("memo does not state a confidence level (high/medium/low)")

    # --- Re-run the gate's verifier ---
    for name, verifier in VERIFIERS.items():
        path = module / name
        if not path.exists():
            continue
        proc = subprocess.run([sys.executable, str(verifier), str(path)],
                              capture_output=True, text=True)
        try:
            result = json.loads(proc.stdout)
        except json.JSONDecodeError:
            problems.append(f"{verifier.name} produced no readable verdict for {name}")
            continue
        if proc.returncode != 0:
            problems.append(f"{verifier.name} could not read {name}: {result.get('error')}")
        elif result["status"] == "errors_found":
            problems += [f"{name}: {e}" for e in result["errors"]]
        else:
            flags += result.get("flags", [])

    # --- One number for one quantity: compare with the pinned inputs ---
    engagement = module.parents[1] / "engagement.json"
    valuation = module / "valuation.json"
    if engagement.exists() and valuation.exists():
        pinned = json.loads(engagement.read_text()).get("pinned", {})
        v = json.loads(valuation.read_text())
        for key in ("shares", "cash", "debt", "price"):
            if key not in pinned or key not in v:
                continue
            want, got = val(pinned[key]), val(v[key])
            if abs(got - want) > PIN_TOL * max(abs(want), 1.0):
                problems.append(
                    f"{key} is {got:,.2f} but the engagement pins {want:,.2f}: use the pinned "
                    f"value or escalate why it should change"
                )
        if "price" in pinned and isinstance(v.get("price"), dict):
            if v["price"].get("date") != pinned["price"].get("date"):
                problems.append(
                    f"price date {v['price'].get('date')} differs from the pinned "
                    f"{pinned['price'].get('date')}"
                )

    # --- Random spot checks: sourced table rows ---
    rows = sourced_rows(memo)
    rng = random.Random(seed)
    spot = rng.sample(rows, min(SPOT_CHECKS, len(rows)))
    if memo and not rows:
        problems.append("no table with a Source column: nothing in the memo can be traced "
                        "(see the fact-base-contribution skill for the Exhibit A format)")

    if verdict is None:
        verdict = "needs_fix" if problems else "ready_to_review"
    return {"module": str(module), "verdict": verdict, "problems": problems,
            "flags_to_confirm": flags, "spot_checks": spot}


def main():
    args = sys.argv[1:]
    seed = None
    if "--seed" in args:
        i = args.index("--seed")
        seed = int(args[i + 1])
        del args[i:i + 2]
    if len(args) != 1 or not Path(args[0]).is_dir():
        print(json.dumps({"error": "usage: em_receipt.py <module folder> [--seed N]"}))
        sys.exit(1)
    print(json.dumps(check(Path(args[0]).resolve(), seed), indent=2))


if __name__ == "__main__":
    main()
