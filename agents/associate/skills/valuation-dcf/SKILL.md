---
name: valuation-dcf
description: Value a company per share with a discounted cash flow model under named, evidence-backed scenarios (stories), with sensitivity tables. Use for any "what is it worth" module built on a DCF.
---

# Valuation: DCF under named scenarios

## Stories, not dials

Bear/base/bull usually turns one story's dial up or down. That hides the real question,
which is usually *which story is true*. Build each scenario as a distinct, internally
consistent story about the business, then value it. The output is "if you believe A,
it's worth $X; if B, $Y", with the evidence for each, set against today's price.

A good pair of stories:
- **Differs in mechanism**, not just magnitude ("matures like its peers" vs "AI pressure
  keeps it from maturing"), so the evidence can tell them apart.
- **Is internally consistent:** growth, margin and reinvestment fit together. A
  company growing 3% doesn't need heavy R&D; a squeezed company doesn't hit peer margins.
- **Rests on sourced evidence:** at least two facts per story, each with a source (gate
  rule). Evidence that only one story explains is the most valuable kind.

## Method

1. **Reuse, don't re-derive.** Discount rate, terminal growth (and its cap), diluted
   shares, cash, debt and debt-like adjustments come from Module 2's `valuation.json`
   unless the brief says otherwise. Re-run anything load-bearing (charter rule); if you
   change one, say why in Escalations.
2. **Ground in the fact pack, not the price.** Start each story from reported history
   and guidance. **Never tune a story to land on today's price.** Where the price falls
   relative to the stories is a finding, not a target.
3. **Write each story** in `valuation.json` under `scenarios` (format in
   `implied-expectations/scripts/valuation_check.py`):
   - `narrative`: one or two sentences on what has to be true about the business.
   - `growth`: usually a fade `{"start": ..., "end": ...}`: year 1 anchored on guidance,
     year 10 near terminal growth. A list of 10 rates is fine if the story has a shape
     (for example a dip then recovery).
   - `target_margin`: long-run FCF margin after SBC, reached over `margin_ramp_years`.
   - `evidence`: `[{"claim", "source"}]`, at least two.
4. **Stock-based compensation:** expense it (FCF after SBC), the same as Module 2. Count
   it once.
5. **Value it:**
   ```
   python3 agents/associate/skills/valuation-dcf/scripts/dcf.py valuation.json
   ```
   Paste each scenario's numbers and the `sensitivity` list into `valuation.json`. Use
   `years` for the memo's drivers table. **Never edit values by hand**: the gate
   recomputes every one.
6. **Check yourself:** run `valuation_check.py valuation.json` and address every flag.

## Reading the result

- **Price between the stories:** the market is weighing both. Say roughly what mix the
  price implies (where it sits between them), and which evidence would move it.
- **Price outside both:** the market sees something neither story captures. That's a
  finding: name what it might be, and escalate if it matters.
- **Stories close together:** they aren't different enough to inform a decision. Find
  the mechanism that really separates them.
- **Terminal value above 75% of EV:** the answer is mostly about years 11+. Say so.

## Output format

Module memo per AGENTS.md (load `module-memo`), plus:

1. **Answer:** "If [story A], HubSpot is worth $X per share; if [story B], $Y. Today's
   price of $P (date) sits [between / outside] them, closer to [A/B]."
2. **The stories table:** narrative, growth path (year 1 → year 10), target margin, the
   value per share, terminal share, and the evidence for each, with sources.
3. **Drivers table:** revenue, growth, margin and FCF by year for each story (from `years`).
4. **Sensitivity table:** discount rate ±1 point × terminal growth ±0.5 point, per story.
5. **What decides it:** the 2–3 facts that would tell you which story is true, and where
   to watch for them (next earnings, a KPI, a disclosure).

## Failure modes

- **Tuned stories:** a "base case" that happens to land on the price.
- **One-sided evidence:** a vivid bear story and a bull story with no sources.
- **Inconsistent stories:** high growth with low reinvestment, or squeezed margins with
  peer-level SBC discipline.
- **Abrupt terminal step:** 12% growth in year 10 then 3% forever. Fade toward terminal.
- **Different inputs from Module 2** without saying so, so the two modules can't be
  compared.

## Handoff

The EM sets the stories against Module 4 (peer comparison), which is built
independently. **Don't read Module 4's output.** Record the per-share values and their
key inputs in Exhibit A for the final answer.
