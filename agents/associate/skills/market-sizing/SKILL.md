---
name: market-sizing
description: Size a market or segment with triangulated, decision-grade estimates. Use for any "how big is X" module — TAM/SAM/SOM, segment sizing, share analysis, or growth outlook.
---

# Market Sizing

## Before you size anything

Restate, from the module brief, what decision this number feeds. The decision sets the
tolerance, and the tolerance sets the method:

- **Screening decision** ("is this market worth entering at all?") → ±50% is fine; two
  fast methods, hours not days.
- **Investment case** ("underwrite this acquisition") → ±15–20%; three methods, full
  bottom-up, sensitivity table.
- **Operational planning** ("how many reps to hire") → bottom-up only, at the geography /
  segment granularity of the plan.

Never deliver more precision than the decision needs. Never deliver less than it needs
and hide it with a point estimate.

## Method: always triangulate

Run at least two of the three, independently — do not let one method's inputs leak into
another's:

1. **Top-down**: total spend pool → successive filters to the target definition. Cite the
   pool source and every filter ratio. Weakness: inherits the analyst-report definition.
   Never rely on a single market-research figure; pull 2–3 and reconcile their scopes
   before using any of them.
2. **Bottom-up**: units × price, built from the natural atom of the market (stores,
   patients, seats, transactions, machines). This is the method the client's operators
   will believe, because it's built from objects they can count. Prefer it as the primary
   whenever atoms are countable.
3. **Proxy / analog**: infer from a correlated observable (adjacent-market ratios, revealed
   figures of a pure-play competitor grossed up by share, import data, job postings).
   Label it clearly as a proxy.

**Reconciliation is the deliverable.** Present all methods, the spread, and your reasoned
pick. If the spread exceeds the decision's tolerance, say so and name what data would
close the gap. If methods disagree >30%, find *why* (usually a definition mismatch)
before presenting anything.

## Sniff tests (run all that apply, show the ones that bite)

- Implied spend per capita / per household / per employee / per store — is it plausible
  against a known anchor?
- Do the named competitors' revenues sum to a believable share of your total?
- Does your growth rate, compounded 5 years, imply something absurd?
- Cross-currency and inflation: are all figures in the same year's real terms and stated
  currency?
- Does the historical series you built actually match the one public data point everyone
  knows (the "Wikipedia number")? If you deviate from the consensus figure, you must
  explain why yours is right — deviation without explanation reads as error.

## Output format

Module memo per AGENTS.md, plus the sizing-specific block:

1. **The number, framed**: "$X.XB (2026, global, revenue basis), ±Y%, growing Z%/yr" —
   definition explicit in the sentence. Basis (revenue vs GMV vs units) always named.
2. **Waterfall or pyramid exhibit**: from pool to target, every filter visible.
3. **Methods table**: each method, its estimate, its weakest assumption.
4. **Sensitivity**: the two assumptions that move the answer most, each swung to its
   plausible extremes.
5. **Assumptions table**: value, source, confidence, "what would change it".

## Failure modes to avoid (each has ended real careers)

- **The single-source TAM**: quoting one research house's number as fact. Their
  definitions vary 3–5x; you saw this yourself if you pulled three reports.
- **False precision**: "$14.72B" from a method with ±40% error bars. Round to the
  precision the method supports.
- **Definition drift**: sizing "AI consulting" in the top-down and "AI implementation
  services" in the bottom-up, then comparing them as if commensurable.
- **Motivated sizing**: the storyline wants a big number, so filters get generous. If you
  notice the storyline leaning on your assumptions, escalate to the EM — that pressure is
  exactly what the escalation rule exists for.
- **Sizing the wrong year**: mixing 2024 actuals, 2025 estimates, and 2026 forecasts in
  one figure without labeling.

## Handoff

Tag the memo with machine-readable metadata (market definition, geography, year, basis,
method list, confidence) so the firm knowledge base can index it. Your sizing becomes a
reusable firm asset; a future engagement's agent will triangulate against it. Sloppy
metadata today is a corrupted benchmark database next year.
