# Brief 04: Peer comparison

**Engagement:** Project Hub · **From:** EM
**Skill:** `benchmarking`
**Depends on:** Brief 01. **Do not read the output of Modules 02 or 03.** This module
is the independent cross-check on the DCF, so it must not see the DCF's answer.

## Question
What do listed software peers suggest HubSpot is worth per share?

## Why it matters
It gives a second, independent view of value. If it lands far from the DCF, the gap
itself is a finding.

## Peer selection (set by the EM before anyone sees a multiple)

**Rules.** A peer must meet all of these, on its latest filings:
1. Files 10-K and 10-Q reports with the SEC (so its figures are on EDGAR).
2. Most of its revenue is subscription or cloud software.
3. It sells mainly to businesses.
4. TTM revenue between $1B and $15B (HubSpot: $3.45B).
5. TTM revenue growth between 8% and 25% (HubSpot: 21%).

**Candidates.** Apply the rules to each and record the decision with the figure that
decides it. Don't add or drop any other way.

Salesforce (CRM), Adobe (ADBE), Intuit (INTU), Autodesk (ADSK), Workday (WDAY),
ServiceNow (NOW), Atlassian (TEAM), Datadog (DDOG), Snowflake (SNOW), Zoom (ZM),
DocuSign (DOCU), Dropbox (DBX), Box (BOX), Twilio (TWLO), Klaviyo (KVYO),
Freshworks (FRSH), Sprout Social (SPT), monday.com (MNDY), Zscaler (ZS), Okta (OKTA)

If fewer than 5 pass, escalate rather than loosening a rule.

## Method
1. Apply the selection rules above.
2. For each peer, record enterprise value, revenue (trailing and forward where available),
   revenue growth, free cash flow margin, EV/revenue and EV/free cash flow, each with its
   source and date.
   Use the same FCF definition as the rest of the engagement: after SBC.
3. Adjust for growth and margin: fit EV/revenue against the rule of 40 score, as the
   skill describes.
4. Apply the adjusted multiples to HubSpot to get a value range per share. Use HubSpot's
   diluted share count and cash from the fact pack and its Q2 2026 10-Q, re-run.

## Sources
Peers' SEC filings and share prices (with date and source). Free sources only. If a
forward estimate isn't freely available, use trailing figures and say so.

## Output
`valuation.json` (type `comps`; the gate checks it) and `memo.md`, answer first: a value range per share next to today's price, followed by the
peer table, the selection rules and the main reason HubSpot deserves a higher or lower
multiple than the median peer.
