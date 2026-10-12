# Engagement: Project Hub II (what is HubSpot worth per share?)

**Status:** In progress · Plan approved 2026-10-12 · **Started:** 2026-10-12 · **Partner:** the user · **EM:** main session (`/engagement`)

## The client and the question

**Client:** a hypothetical buyer looking at HubSpot, Inc. (NYSE: HUBS). This is the second,
independent run of the demo engagement: it tests whether the EM-plus-Associates machine
reproduces an answer without access to the first run.

**Scope:** standalone value of the equity only. Synergies, deal terms, control premium and
deal risks are out of scope.

## Key question

> What is HubSpot worth per share, and how does that compare with today's share price?

## Working answer (a hypothesis to test, not a conclusion)

> Today's share price assumes HubSpot keeps growing faster than mature software peers while
> expanding its free cash flow margin (after stock-based compensation) toward theirs. Its
> value depends on whether that margin expansion is realistic.

Confidence: **low** (no analysis yet). Branches and the module that tests each:

| Branch of the hypothesis | Tested by |
|---|---|
| A. Our numbers are right (one fact base) | 01 fact pack |
| B. The price assumes fast growth *and* rising margins | 02 what the price implies |
| C. On fundamentals, value is near / above / below the price (two stories) | 03 DCF |
| D. Peers' multiples give a value consistent with C | 04 peer comparison |

Disconfirmation: the "Squeezed" story in 03 and the independent peer view in 04 carry the
strongest case against the working answer.

## Output

A one-page answer: value per share under two stories ("grows up" and "squeezed") and from
peers, today's price for comparison, the 2–3 assumptions that move value most, and every
number traced to an accepted module.

## The work: four modules

| Module | Question it answers | Skill | Skill status |
|---|---|---|---|
| 01. Company fact pack | What are HubSpot's actual reported numbers, incl. fully diluted shares? | `company-profile` | Stub |
| 02. What the price implies | What growth and margins does today's price assume? | `implied-expectations` | Full |
| 03. DCF under two stories | What is it worth if it grows up vs. gets squeezed? | `valuation-dcf` | Full |
| 04. Peer comparison | What do listed software peers suggest it is worth? | `benchmarking` | Full |

Briefs: [01](modules/01-fact-pack/brief.md) · [02](modules/02-implied-expectations/brief.md) ·
[03](modules/03-dcf-scenarios/brief.md) · [04](modules/04-peer-comparison/brief.md)

**Order:** 01 → 02 → (03 and 04 in parallel). 02 runs before 03/04 because it fixes the
shared price, discount rate and terminal growth, which are then pinned in `engagement.json`.
03 and 04 are independent cross-checks of each other: neither reads the other, and 03 does
not read 02's conclusion. About 4 Associate runs, plus re-work if a receipt fails.

**Pinned inputs** (filled in `engagement.json` as modules are accepted): diluted shares,
cash incl. investments, debt, price {value, date, source}, discount rate, terminal growth.

## Sources (free only)

- SEC EDGAR (10-K, 10-Q, 8-K earnings releases, XBRL company facts) via the `edgar` tools.
- HubSpot investor relations releases and presentations.
- Peers' SEC filings.
- Share prices through web search, cited with date and source.
- If a free source can't supply a figure, the memo says so rather than estimating silently.

## Partner checkpoints

1. Approve this plan and the four briefs.
2. Approve the final answer.
