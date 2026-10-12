# Brief 04: Peer comparison

**Engagement:** Project Hub II · **From:** EM
**Skill:** `benchmarking`
**Depends on:** 01 (accepted); pinned price from 02. **May read:** `modules/01-fact-pack/`, `engagement.json` (pinned facts), your module folder.
**Must not read:** `engagement.md`, `modules/02-implied-expectations/`, `modules/03-dcf-scenarios/`. This is the independent cross-check on the DCF.
**Must not read (all modules):** `engagements/hubspot-value/`, `docs/engagements/`, `docs/HANDOVER.md`, `engagements/hubspot-value-2/log.md`. This is an independent re-run; using the earlier engagement invalidates it.

## Question
What do listed software peers suggest HubSpot is worth per share?

## Why it matters
Branch D: a second, independent view of value. If it lands far from the DCF, the gap is
itself a finding.

## Peer selection (set by the EM before anyone sees a multiple)

**Rules.** A peer must meet all of these, on its latest filings:
1. Files 10-K and 10-Q reports with the SEC.
2. Most of its revenue is subscription or cloud software.
3. It sells mainly to businesses.
4. TTM revenue between $1B and $15B.
5. TTM revenue growth between 8% and 25%.

**Candidates.** Apply the rules to each and record the decision with the figure that
decides it. Don't add or drop any other way.

Salesforce (CRM), Adobe (ADBE), Intuit (INTU), Autodesk (ADSK), Workday (WDAY),
ServiceNow (NOW), Atlassian (TEAM), Datadog (DDOG), Snowflake (SNOW), Zoom (ZM),
DocuSign (DOCU), Dropbox (DBX), Box (BOX), Twilio (TWLO), Klaviyo (KVYO),
Freshworks (FRSH), Sprout Social (SPT), monday.com (MNDY), Zscaler (ZS), Okta (OKTA)

If fewer than 5 pass, escalate rather than loosening a rule.

## Method
1. Apply the selection rules.
2. For each peer: enterprise value, revenue (TTM; forward if freely available), revenue
   growth, FCF-after-SBC margin, EV/revenue, EV/FCF, each with source and date. Peer
   prices: one date for all, as close as possible to the pinned price date.
3. Adjust for growth and margin: fit EV/revenue against rule-of-40 score (growth + FCF
   margin), as the skill describes. Also report the plain medians.
4. Apply to HubSpot for a value range per share, using the pinned diluted shares, cash,
   debt and price exactly.

## Sources
Peers' SEC filings and share prices (date and source). Free sources only. If a forward
estimate isn't freely available, use trailing figures and say so.

## Output
`valuation.json` (type `comps`; the gate checks it) and `memo.md`, answer first: a value
range per share next to the pinned price. State confidence. Then the peer table (Source
column), the selection decisions, and the main reason HubSpot deserves a higher or lower
multiple than the median peer.
