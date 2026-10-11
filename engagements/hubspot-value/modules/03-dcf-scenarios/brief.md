# Brief 03: DCF scenarios

**Engagement:** Project Hub · **From:** EM
**Skill:** `valuation-dcf`
**Depends on:** Briefs 01 and 02. **Do not read Brief 04's output.** The two valuation
methods must stay independent.

## Question
What is HubSpot worth per share under two stories about its future?

1. **Grows up:** HubSpot matures like its peers. Growth fades from today's ~14% toward the
   economy's rate, and the margin after SBC rises into the peer range (Module 2: 22.5% to
   33.3%).
2. **Squeezed:** AI pressure on software sold per seat keeps HubSpot from maturing. Growth
   fades faster, to low single digits, and the margin stalls well below peers.

The Partner kept the working answer ("the price assumes fast growth and rising margins")
as the hypothesis to test. Module 2 found the price implies only ~9% growth and a ~17%
margin. These two stories test whether that low bar reflects a bargain or a real risk.

## Why it matters
This is the main answer to the engagement's question.

## Method
A 10-year discounted cash flow model with a terminal value. Each scenario states its
drivers explicitly: the revenue growth path, the margin path, reinvestment, the discount
rate and terminal growth.
- Ground each scenario in the fact pack (history and guidance), not in the share price.
  **Do not tune the base case to land on today's price.**
- Say what each story has to believe about the business. Example: "Grows up assumes net
  revenue retention returns to N%."
- **Each story needs its own evidence,** at least two sourced facts. For Squeezed, look
  for signs of AI pressure in HubSpot's own filings and calls (seat counts, pricing and
  packaging changes, what management says about AI) and in the peers'. Evidence that only
  one story explains is the most useful. If you can't find evidence for a story, say so:
  that is itself a finding.

## Limits set by the EM
- Use Module 2's discount rate (10.5%), terminal growth (3.0%, cap 4.0%), diluted shares
  and EV bridge, re-running them first. Refresh the share price (it moved 15% in two
  weeks).
- Treat stock-based compensation as a real cost, either through cash flow or through
  share dilution, and say which.
- Report what share of value comes from the terminal value, and flag it if that is
  above 75%.
- Include a sensitivity table: discount rate × terminal growth.

## Output
`valuation.json` (type `dcf`; the gate checks it) and `memo.md`, answer first: the value
per share under each story next to today's price, and which story the price is closer
to. Then the stories table with evidence, the drivers table, the sensitivity table, and
the 2–3 facts that would tell us which story is true.
