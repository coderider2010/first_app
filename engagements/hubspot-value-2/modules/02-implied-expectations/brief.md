# Brief 02: What the price implies

**Engagement:** Project Hub II · **From:** EM
**Skill:** `implied-expectations`
**Depends on:** 01 (accepted). **May read:** `engagements/hubspot-value-2/engagement.md`, `engagement.json`, `modules/01-fact-pack/`, your module folder.
**Must not read (all modules):** `engagements/hubspot-value/`, `docs/engagements/`, `docs/HANDOVER.md`, `engagements/hubspot-value-2/log.md`. This is an independent re-run; using the earlier engagement invalidates it.

## Question
What revenue growth and long-run free cash flow margin does today's share price assume?

## Why it matters
Branch B. The working answer (a hypothesis, not a finding) is that the price assumes fast
growth *and* rising margins. Report what the price implies whether or not it fits that.

## Method
Reverse DCF. From today's enterprise value (price × pinned diluted shares + pinned debt −
pinned cash), solve for the growth and margin paths that justify it. Show a grid of
10-year revenue CAGR × long-run FCF-after-SBC margin that reproduces today's value.

## Limits set by the EM
- **Shares, cash, debt:** use the values pinned in `engagement.json` exactly.
- **Price:** the latest close you can source by web search, with date and source. It will
  be pinned for all later modules.
- **Terminal growth:** no higher than long-run nominal US GDP growth; state and cite it.
- **Discount rate:** derive it (CAPM or similar), cite every input, show results at ±1 pt.
  It will be pinned for Module 03.
- **SBC** is a real cost: use FCF after SBC.
- **Peer benchmark (fixed here):** compare the implied long-run margin with Adobe (ADBE),
  Salesforce (CRM), Intuit (INTU) and Autodesk (ADSK), each one's latest fiscal-year
  FCF after SBC as a share of revenue, from its 10-K.

## Sources
Fact pack, the share price (date and source), peers' 10-Ks.

## Output
`valuation.json` in the skill's format (the gate checks it) and `memo.md`, answer first:
"At $X per share (date), the market is pricing in roughly Y% annual revenue growth for 10
years and a Z% long-run FCF-after-SBC margin." State confidence. Then the grid, an inputs
table with a Source column, the peer table, and how demanding the implied path is.
