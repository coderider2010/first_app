---
name: benchmarking
description: Pull and normalize operational or financial benchmarks across companies. Use for any 'how do we compare' module; never compare unnormalized metrics.
---

# Benchmarking (and peer valuation)

## The peer set is the answer

Choose different peers and you get a different answer, so the choice must be made
before anyone sees the numbers it produces. The **EM's brief sets the selection rules
and the candidate list**. Your job is to apply the rules to every candidate, on real
data, and record each decision:

- **Included:** meets every rule; show the figures that prove it.
- **Excluded:** fails a rule; name the rule and the figure ("TTM revenue $41.5B, above
  the $15B limit").

Never add a peer that isn't a candidate, and never drop one without a recorded reason.
If the rules leave fewer than 5 peers, say so and escalate rather than loosening a rule
yourself. The gate checks that every peer came through this record.

## Normalize before you compare

Walk down this ladder for every figure, for the target and every peer:

1. **Definition:** FCF here means operating cash flow − capex − capitalized software −
   SBC (after SBC), the same as Modules 2 and 3. Revenue is total GAAP revenue.
2. **Period:** trailing twelve months to each company's latest 10-Q or 10-K. Fiscal
   years differ (Salesforce ends in January, Intuit in July), so build TTM for each
   (latest annual + current year-to-date − prior year-to-date).
3. **Growth:** TTM revenue over the TTM a year earlier.
4. **Price and shares:** price dated within 7 days of the as-of date; diluted shares
   from the latest filing. EV = price × diluted shares + debt (including convertible
   notes) − cash and investments.
5. **Currency and basis:** all USD; all GAAP inputs.

An unnormalized comparison is the classic error: one company's fiscal year against
another's TTM, or one's FCF before SBC against another's after.

## Method

1. Fill `valuation.json` (type `comps`; format in
   `implied-expectations/scripts/valuation_check.py`): the target's TTM revenue, growth
   and FCF; the selection rules (copied from the brief); every candidate with its
   decision; and each included peer's sourced inputs.
2. Run:
   ```
   python3 agents/associate/skills/benchmarking/scripts/comps.py valuation.json --write
   ```
   It computes each peer's EV, EV/revenue, EV/FCF and rule of 40 score, fits EV/revenue
   against the rule of 40, and values the target three ways. **Don't edit its numbers.**
3. **Choose the range basis.** If the fit is decent (r² ≥ 0.3), use the regression band
   (fitted multiple ± one residual spread). If not, use the spread of the three methods
   (`"basis": "methods"`) and say the growth adjustment didn't hold.
4. Run `valuation_check.py valuation.json` and address every flag.

## Why adjust for growth and margin

A plain median treats a 25% grower like an 8% grower. The rule of 40 score (growth +
FCF margin) is the software industry's shorthand for "how good is this business": a
company growing 20% at a 20% margin scores 40. Regressing EV/revenue on that score asks
what multiple peers with the target's mix earn. With 5–8 peers it is rough: always show
the scatter (the peer table sorted by score is enough) and r².

**After-SBC caveat:** the target's FCF margin after SBC may be far below peers' (heavy
SBC), which lowers its score and the EV/FCF value sharply. That is a real difference,
not an error. Say how much of the gap is SBC.

## Output format

Module memo per AGENTS.md (load `module-memo`), plus:

1. **Answer:** "Listed peers imply $L–$H per share (basis), against today's $P (date)."
2. **Peer table:** each peer's EV, revenue, growth, FCF margin, rule of 40, EV/revenue,
   EV/FCF, sorted by score, with the target in its place. Show the full distribution:
   median *and* quartiles, not just the flattering end.
3. **Selection record:** the rules, then every candidate with its decision and reason.
4. **Methods table:** the three values per share, and why you chose the basis.
5. **The main reason** the target deserves a higher or lower multiple than the median.

## Failure modes

- **The convenient peer set:** peers picked, or dropped, after seeing the multiples.
- **Mixed periods or definitions:** fiscal year vs TTM, before vs after SBC.
- **Quartile cherry-picking:** quoting only the top quartile's multiple.
- **Extrapolation:** the target's score is outside every peer's; the regression is
  guessing beyond its data. Say so.
- **Stale or undated prices:** multiples move daily; date every price.

## Handoff

Module 4 is the independent cross-check on Module 3's DCF: **don't read Modules 2 or 3**
before submitting. The EM compares them. Record each peer's figures in Exhibit A so
the fact base can reuse them.
