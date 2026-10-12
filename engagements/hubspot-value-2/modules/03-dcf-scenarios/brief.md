# Brief 03: DCF under two stories

**Engagement:** Project Hub II · **From:** EM
**Skill:** `valuation-dcf`
**Depends on:** 01 and 02 (accepted). **May read:** `modules/01-fact-pack/`, `engagement.json` (pinned facts), your module folder.
**Must not read:** `engagement.md`, `modules/02-implied-expectations/`, `modules/04-peer-comparison/`. 03 and 04 are independent views of value, and this DCF must be built from fundamentals, not from what the price implies.
**Must not read (all modules):** `engagements/hubspot-value/`, `docs/engagements/`, `docs/HANDOVER.md`, `engagements/hubspot-value-2/log.md`. This is an independent re-run; using the earlier engagement invalidates it.

## Question
What is HubSpot worth per share under two stories about its future?

1. **Grows up:** HubSpot matures like established software companies. Growth fades from
   today's rate (fact pack) toward the economy's rate, and the FCF-after-SBC margin rises
   toward the mature-peer range.
2. **Squeezed:** AI pressure on per-seat software keeps HubSpot from maturing. Growth fades
   faster, to low single digits, and the margin stalls well below mature peers.

Neither story is the expected answer. Report the value each produces, and which (if
either) the evidence favours.

## Why it matters
Branch C, the main answer to the engagement's question.

## Method
10-year DCF with a terminal value. Each story states its drivers: revenue growth path,
FCF-after-SBC margin path, reinvestment, discount rate, terminal growth.
- Ground each story in the fact pack (history and guidance). Do not look up or tune to the
  share price beyond the pinned figure, which you use only for the final comparison.
- Say what each story has to believe (e.g. "net revenue retention returns to N%").
- **Each story needs its own evidence,** at least two sourced facts. For Squeezed, look for
  signs of AI pressure in HubSpot's filings and calls (seats, pricing and packaging, what
  management says about AI) and in peers'. Evidence that only one story explains is the
  most useful. If you can't find evidence for a story, say so: that is a finding.
- Mature-peer margin range: Adobe, Salesforce, Intuit, Autodesk, latest fiscal-year
  FCF after SBC / revenue from their 10-Ks (use `pinned.peer_margins` if present).

## Limits set by the EM
- Discount rate, terminal growth, diluted shares, cash, debt and price: use the values
  pinned in `engagement.json` exactly. Do not refresh the price.
- SBC is a real cost (through FCF after SBC); do not also count dilution twice.
- Report the share of value from the terminal value; flag it if above 75%.
- Sensitivity table: discount rate (±1 pt) × terminal growth (±0.5 pt), per story.

## Output
`valuation.json` (type `dcf`; the gate checks it) and `memo.md`, answer first: value per
share under each story next to the pinned price, and which story the price is closer to.
State confidence. Then the stories table with evidence (Source column), the drivers table,
the sensitivity table, and the 2–3 facts that would tell us which story is true.
