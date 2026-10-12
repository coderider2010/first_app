# Brief 01: Company fact pack

**Engagement:** Project Hub II (what is HubSpot worth per share?) · **From:** EM
**Skill:** `company-profile` (stub: flag it, then follow the charter)
**Depends on:** nothing. **May read:** `engagements/hubspot-value-2/engagement.md`, `engagement.json`, your module folder.
**Must not read (all modules):** `engagements/hubspot-value/`, `docs/engagements/`, `docs/HANDOVER.md`, `engagements/hubspot-value-2/log.md`. This is an independent re-run; using the earlier engagement invalidates it.

## Question
What are HubSpot's actual reported numbers? Cover the last three fiscal years, the latest
reported quarter and the trailing twelve months (TTM).

## Why it matters
Branch A: every later module uses these numbers. Shares, cash and debt from this module
will be pinned in `engagement.json` and used by all other modules unchanged.

## What to collect
- Revenue: total, subscription and professional services; year-over-year growth
- Gross margin; operating margin, GAAP and non-GAAP
- Stock-based compensation
- Operating cash flow, capital expenditure, free cash flow; and FCF **after SBC**
  (FCF minus SBC), the engagement's standard FCF definition
- Cash, cash equivalents and investments (short and long term); debt incl. convertible
  notes (principal and carrying value; note maturity and conversion price)
- **Fully diluted share count** at the latest balance-sheet date: basic shares outstanding
  plus RSUs, PSUs and options by the treasury stock method, with each component and its
  source. State the share price you used for the treasury stock method and its date.
  If the convertible notes are in the money, say whether they add shares.
- Customers, average subscription revenue per customer, net revenue retention
- Management's guidance for the current year, if published (cite the release)

## Depth
Exact, as reported. No estimates except the treasury-stock calculation, which you show.
Label every number GAAP or non-GAAP.

## Sources
SEC EDGAR via the `edgar` tools (10-K, 10-Q, 8-K releases, XBRL), plus HubSpot investor
relations. Each figure needs its filing, period and source URL.

## Output
- `memo.md`: answer first (one paragraph: the business in numbers), a stated confidence
  level (high/medium/low), then a table of every figure with columns
  Item | Value | Period | Definition | GAAP/non-GAAP | Source.
- A short "Inputs to pin" table: diluted shares, cash incl. investments, debt (and which
  measure of debt), each with source.
- Escalate (`escalation.md`) if two filings disagree on the same figure, e.g. after a
  restatement.
