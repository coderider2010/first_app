---
name: implied-expectations
description: Reverse a market price into the growth and margins it assumes (reverse DCF), then judge how demanding those assumptions are. Use for any "what does the price imply", "what is priced in", or expectations-investing module.
---

# Implied Expectations (reverse DCF)

## The idea

A normal DCF turns assumptions into a value. A reverse DCF runs the other way: it takes
the price the market is paying and solves for the assumptions that would justify it.
(This is the approach of Rappaport and Mauboussin's *Expectations Investing*.) The point
is to change the debate. "Is it worth $X?" invites opinion. "The price needs 15% growth
for ten years and a 30% margin; has any company done that?" can be checked.

Many growth and margin pairs produce the same value, so the answer is a **curve**, shown
as a grid, plus one headline point on it that you justify.

## Method

1. **Enterprise value today.** Price (dated, cited) × **diluted** shares, plus debt, minus
   cash and investments. Diluted means basic shares plus RSUs, PSUs and in-the-money
   options (treasury stock method), from the latest 10-Q equity note. Add other debt-like
   items only if you can source them, as `other_ev_adjustments`.
2. **Starting point.** Base revenue (usually TTM) and base FCF margin, both from the fact
   pack. Re-run any load-bearing fact-pack number before using it (charter rule).
3. **Stock-based compensation.** Default: treat it as an expense. FCF = operating cash
   flow − capex − capitalized software − SBC. SBC is paid in shares instead of cash, but
   it is a real cost to existing owners. Do it **once**: never deduct SBC *and* also
   model share dilution from it, and never neither. If you choose `dilution` instead,
   the script's margins are pre-SBC; say so and model share growth separately.
4. **Discount rate.** Derive it, don't assert it. CAPM: risk-free rate (10-year Treasury
   yield, dated and cited) + beta × equity risk premium (cite the source, such as
   Damodaran's published implied ERP). With little or no debt, the cost of equity is the
   discount rate. Cite every input. The grid always shows ±1 point.
5. **Terminal growth.** At or below long-run nominal GDP growth, cited. It must sit well
   below the discount rate. No company outgrows the economy forever.
6. **Solve.** Write the inputs into `valuation.json` (format in
   `scripts/valuation_check.py`), then run:
   ```
   python3 agents/associate/skills/implied-expectations/scripts/reverse_dcf.py valuation.json
   ```
   Paste its `grid` into `valuation.json`. **Never compute or edit grid cells by hand**:
   the gate recomputes every cell and blocks any that don't reproduce today's EV.
7. **Pick the headline.** Choose one growth rate and give a reason: for example, the
   consensus or guidance-anchored path. The headline margin is that row of the grid.
8. **Check yourself.** Run `scripts/valuation_check.py valuation.json` before submitting
   and address every flag in the memo.

## Judging how demanding it is (the verdict)

The grid is not the answer; the verdict is. Compare the implied pair against:

- **The company's own record:** growth over the last 3 years and the trend (decelerating?),
  current margin after SBC, and guidance.
- **Peers:** the long-run FCF margins (after SBC, same definition) of the mature peers
  the **brief names**. Take the peer set from the brief, not your own choice, so the
  benchmark can't be bent toward a conclusion. Pull their numbers from filings.
- **Base rates:** how often companies of this size sustain this growth for 10 years.
  Cite a source if you use one; otherwise say it is judgment.

Say plainly whether the price needs growth, margin, or both above what the evidence
supports. If the verdict contradicts the engagement's working answer, that is the
highest-priority escalation in the charter: say so, don't soften it.

## Output format

Module memo per AGENTS.md, plus:

1. **The sentence:** "At $X per share (date), the market is pricing in roughly Y% annual
   revenue growth for 10 years and a Z% long-run free cash flow margin (after SBC)."
2. **The grid:** rows = growth, columns = discount rate (base, −1, +1 point), cells =
   implied margin. Mark the headline cell, and shade cells above the best peer's margin.
3. **Inputs table:** every input with value, date, source.
4. **The verdict:** how demanding, against record, peers and base rates.
5. **Sensitivity:** terminal growth ±0.5 point, and the share of value from the terminal
   value at the headline.

## Failure modes

- **Basic shares.** Using cover-page shares understates the equity value and makes the
  price look cheaper than it is.
- **Pre-SBC margins compared to post-SBC peers,** or the reverse. Same definition on
  both sides, always.
- **Terminal value doing all the work.** If more than ~75% of value is beyond year 10,
  the answer is mostly about terminal assumptions; say so.
- **Asserted discount rate.** "We use 10%" with no derivation can't be checked or
  defended.
- **Hand-edited grids.** One typed cell that doesn't reproduce EV breaks the curve's logic.
- **Stale price.** A price more than a week old, or with no date, can't be checked.

## Handoff

Module 3 (DCF scenarios) reuses the discount rate, terminal growth, diluted shares and
EV bridge; record them in the memo's exhibit table with sources so it doesn't re-derive
them differently. Tag the headline pair as an *estimate*, not a fact.
