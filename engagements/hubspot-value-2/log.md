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
- 01 accepted. Spot checks re-pulled from EDGAR (diluted-share components, buybacks, FY26 guidance) plus TTM revenue, cash, debt: all tie.
- Escalation 1 (share count) adjudicated. Rule: pin the point count from the latest 10-Q balance sheet plus gross unvested awards from the closest filing disclosure; an omission under the 0.5% pin tolerance is accepted and stated rather than estimated. Pinned 52.403M (range 51.33–52.69M). Revisit at the Q3 10-Q.
- Escalation 5 (FY2023 immaterial revision) accepted; accounting item, reported to Partner for information.
- Out-of-scope items for the Partner: CLO resigned 8 Oct 2026 (8-K); 7% workforce cut 1 Oct 2026 ($65–75M, mostly Q4). No new module; noted for answer caveats.
- Pinned shares, cash, debt, FCF definition. Commissioning 02.
- 02 accepted. EM re-pulled price (Yahoo), 10y yield (Treasury.gov), Autodesk margin (EDGAR) and re-computed the headline with independent code: all tie.
- Pinned price $228.30 (9 Oct 2026), discount rate 10.5%, terminal growth 3.0% (cap 4.0%), EV convention, peer margins.
- Rule (restructuring): brief's EV definition governs over skill default; announced restructuring excluded (~0.1 pt).
- ESCALATION, analysis contradicts the working answer: price implies ~10% growth and a 15.6% FCF-after-SBC margin, below every mature peer (22.5–33.3%). The "fast growth AND rising margins" branch holds only on the margin half, and the margin bar is below peers. Taken to the Partner the same day with replicate / proceed / change options. 03 and 04 on hold pending the decision.
- Partner dismissed the escalation question without choosing. 03 and 04 stay on hold until the Partner decides.
- Partner chose PROCEED on the 02 escalation (EM recommendation): working answer unchanged for now; 03 and 04 serve as the independent replication. Revisit the working answer at synthesis. Commissioning 03 and 04 in parallel.
- 03 accepted. Spot checks re-pulled from EDGAR (revenue halves, FY23 SBC %, customers) and both stories plus crossed case and a sensitivity cell re-computed with independent EM code: all tie. Result kept out of engagement.md/engagement.json (04 still running).
