---
name: source-vetting
description: Grade a source's reliability by methodology, incentives, and recency before its data enters the fact base. Use before relying on any unfamiliar source for a load-bearing number.
---

# Source vetting

Every number inherits the reliability of its source. Grade the source once and record
the grade with every figure that uses it.

## Grades

| Grade | Meaning | Examples |
|---|---|---|
| **A** | Audited, or legally liable filing | 10-K financial statements |
| **A−** | Reviewed or liable but unaudited | 10-Q statements, 10-K/10-Q text and KPIs |
| **B** | Company-issued, not audited | 8-K earnings releases, non-GAAP figures, guidance, IR decks |
| **B** | Reputable data with a published method | Treasury yields, exchange prices, Damodaran datasets |
| **C** | Secondary, method unclear | News articles, market-research summaries, aggregator sites |
| **D** | Unverifiable | Unsourced blogs, forum posts, AI-generated summaries |

Load-bearing numbers need A or B. A C source can corroborate but not carry the answer.
Never present D.

## Questions to ask of an unfamiliar source

- **Method:** does it say how the number was produced? Can you reproduce it?
- **Incentive:** who paid for it, and would they prefer a particular answer? (Companies
  prefer flattering non-GAAP measures; research houses prefer big markets.)
- **Track record:** has it been right before? Does it correct its errors?
- **Recency:** is it the latest figure? Prices need a date and time; filings need a
  period.

## Circular sourcing

Five articles quoting one press release is one source, not five. Trace a figure back to
where it was first published before counting it as independent. Two methods resting on
one source don't triangulate (lesson from the first run, HANDOVER).

## Market prices

Share prices come from web search here. Record the price, the date (and whether it is a
close), and the site. Cross-check against a second site; if they differ by more than
1%, find out why (different date, after-hours) before using either.

## Failure modes

- Quoting a market-research figure as fact. Research houses' definitions vary 3–5 times.
- Using a search-result summary instead of the page it summarizes.
- Mixing a company's non-GAAP figure with a peer's GAAP figure.
- A price with no date.

## Handoff

Record the grade in Exhibit A's Grade column (see `fact-base-contribution`).
