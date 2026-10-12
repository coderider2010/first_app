# Decision log: hubspot-value-2 (EM only; no module may read this file)

## 2026-10-12
- Engagement opened from `/engagement What is HubSpot worth per share?`.
- Slug `hubspot-value-2`: `engagements/hubspot-value/` exists and is never overwritten.
- This run is the HANDOVER "open test" (reproduce Project Hub end to end). To keep it a fair
  test, every brief bars the Associates from the earlier engagement (`engagements/hubspot-value/`,
  `docs/engagements/`, `docs/HANDOVER.md`). Briefs reuse Project Hub's structure and rules,
  not its numbers.
- Change from Project Hub: Module 03 does not read Module 02's memo (price-implied growth and
  margin); it gets only the pinned facts. Reason: avoid anchoring the DCF on the price.
  Module 02 runs before 03/04 only because it establishes the price, discount rate and
  terminal growth pins.
- Change from Project Hub: Brief 01 requires a fully diluted share count (treasury stock
  method), the gap HANDOVER recorded for the first fact pack.
- Disconfirmation (charter, >=20% of capacity): the "Squeezed" story in 03 and the independent
  peer cross-check in 04 carry the case against the working answer.
- Checkpoint 1: Partner approved the plan and the four briefs as written. Commissioning 01.
