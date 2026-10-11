# Brief 02: What the price implies

**Engagement:** Project Hub · **From:** EM
**Skill:** `implied-expectations`
**Depends on:** Brief 01 (fact pack)

## Question
What revenue growth and profit margins does today's share price assume?

## Why it matters
This tests the working answer: that the price assumes fast growth *and* rising margins.
It also turns the debate from "what is it worth?" into "are these assumptions realistic?"

## Method
Reverse DCF. Start from today's enterprise value (market value of equity plus debt minus
cash, using the fact pack) and solve for the growth and margin path that justifies it.
Show a grid of combinations (10-year revenue growth × long-run free cash flow margin)
that produce today's value.

## Limits set by the EM
- **Shares:** use a fully diluted count (basic shares plus RSUs, PSUs and options by the
  treasury stock method) from the Q2 2026 10-Q. The fact pack has basic shares only.
- **Terminal growth** must not exceed long-run nominal GDP growth. State the figure you
  use and cite it.
- **Discount rate:** derive it, cite every input, and show the result at ±1 percentage
  point.
- **Stock-based compensation:** treat it as a real cost, and say how.
- **Peers:** compare the implied long-run margin with these mature software companies:
  Adobe (ADBE), Salesforce (CRM), Intuit (INTU) and Autodesk (ADSK). Use each one's
  latest fiscal-year free cash flow after SBC as a share of revenue, from its 10-K. The
  peer set is fixed here so the benchmark can't be chosen to fit the answer.

## Sources
Fact pack figures, the share price (with date and source), and filings for any peer
margins.

## Output
`valuation.json` in the format the skill gives (the gate checks it), and `memo.md`, answer first: "At $X per share (date), the market is pricing in roughly Y%
annual revenue growth for 10 years and a Z% long-run free cash flow margin." Follow it
with the grid, the inputs table and a verdict on how demanding that is.
