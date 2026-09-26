---
name: driver-tree
description: Decompose a metric's level or movement into a quantified, MECE driver tree and attribute the change to branches. Use for any "why did X change", "what moves X", or root-cause module.
---

# Driver Tree

## Two layers, never confused

A driver tree has an **arithmetic layer** and a **behavioral layer**, and the single
most important discipline in this skill is knowing which one you are standing in.

1. **Arithmetic layer**: an identity that decomposes the metric exactly.
   Revenue = customers × orders/customer × units/order × price/unit. Margin = price −
   cost, weighted by mix. This layer is *true by construction* — it cannot be wrong,
   only unhelpfully chosen.
2. **Behavioral layer**: hypotheses about what moves each arithmetic leaf (churn rose
   because onboarding changed; price/unit fell because mix shifted to SMB). This layer
   is *causal claim* — it can absolutely be wrong and needs corroboration.

The tree's arithmetic locates **where** the change happened. It never by itself
establishes **why**. "Volume fell in Germany" is a location, not a cause. Presenting
location as cause is this skill's cardinal sin.

## Building the arithmetic layer

- Choose the decomposition that matches the *levers the client can pull*. Revenue
  splits by geography, by product, by customer segment, or by the rate×volume chain —
  all arithmetically valid; only one aligns with the decision in the module brief.
  When in doubt, decompose along the hypothesis-tree branch the brief names.
- Branches must be MECE **and arithmetically closed**: child contributions must sum to
  the parent's delta. Compute the bridge (waterfall) at every level. An unexplained
  residual >5% of the delta means a missing branch or broken data — find it before
  going deeper. Interaction terms (price×volume cross effects) get their own labeled
  bar, never smeared across branches.
- Keep stocks and flows apart. Customer count (stock) and churn rate (flow) can both
  appear, but a branch may not mix them in one sum.
- Depth rule: stop splitting when a leaf is (a) directly actionable, (b) beyond the
  data's resolution, or (c) contributing <5% of the delta. A 7-level tree with dead
  leaves is theater; three honest levels beat seven decorative ones.

## Quantifying attribution

- Bridge each level: start value → contribution per child → end value, in the metric's
  own units *and* as % of the total delta.
- Rate-vs-mix decomposition wherever averages move: an average price can fall while
  every segment's price rises (mix shift). Always test for Simpson's-paradox structure
  before reporting an average's movement as a rate change.
- Percentages of percentages are banned in output. Express basis-point changes in the
  underlying quantity.

## Corroborating the behavioral layer

For each leaf that matters (top 2–3 contributors), the causal story needs at least one
independent corroboration: timing alignment (did the change start when the candidate
cause started?), cross-sectional contrast (did it happen where the cause was present
and not where absent?), cohort separation, or a natural experiment. State the causal
confidence separately from the arithmetic finding — the memo must let a reader accept
the *where* while doubting your *why*.

## Output

1. The tree exhibit: one page, contributions annotated, top drivers visually weighted.
2. The bridge/waterfall for the headline metric.
3. Per top driver: the behavioral hypothesis, its corroboration, causal confidence.
4. The residual, stated — even when small. A hidden residual reads as a hidden error.

## Failure modes

- **Location sold as cause** (see above — cardinal).
- **Non-closing tree**: contributions that don't sum; the client's analyst finds it
  in the first ten minutes and the engagement's credibility goes with it.
- **Decomposition mismatch**: a geographic tree for a pricing decision.
- **"Other" >10%**: a bucket that size is a missing branch wearing a trench coat.
- **Correlated branches treated as independent**: price cuts drove volume; their
  contributions are not separable without modeling the elasticity — say so.

## Handoff

File each leaf's value and the bridge in the fact base with full metadata. Driver
trees are the most reused artifact across engagement phases — the SteerCo version, the
implementation baseline, and next year's refresh all descend from this tree. Build it
as the reference implementation, not a one-off.
