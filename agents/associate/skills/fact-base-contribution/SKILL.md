---
name: fact-base-contribution
description: Tag findings with machine-readable metadata and submit them to the engagement fact base; resolve number conflicts per protocol. Load at every module handoff.
---

# Fact-base contribution

The fact base is the firm's rule of "one number for one quantity": when two modules use
HubSpot's TTM revenue, they use the same record. It is not built yet (Phase 5 of
`docs/PROJECT_PLAN.md`). Until it is, **Exhibit A of your memo is your contribution**,
written so the fact base can load it later without re-reading the filings.

## Record format (one row per quantity and period)

| Field | Meaning |
|---|---|
| Quantity | What it is: "Total revenue", "Diluted shares" |
| Period / date | FY2025, Q2 2026, TTM Jun-26, or an as-of date for balances |
| Value | As filed, with units ($ thousands as filed, or stated) |
| Definition | How it is defined, especially for company KPIs and non-GAAP |
| Basis | GAAP, Non-GAAP, KPI, Market (prices), Estimate, or Derived (show formula) |
| Source | Filing or page, with link |
| Grade | Source grade from `source-vetting` |

Mark derived rows with their formula. Estimates go in their own section, never mixed
into facts.

## Reuse before you re-derive

If an earlier module in this engagement already reports the quantity, use its value and
cite that module, after re-running it if it is load-bearing for you (charter rule). If
your value differs, that is a conflict, not a choice.

## Conflict protocol

Same quantity, same period, different values:

1. **Check definitions first.** Most conflicts are two definitions (basic vs diluted,
   pre- vs post-SBC, revised vs original). If so, it isn't a conflict: record both,
   labelled.
2. **Restatements:** the latest filing supersedes. Record the earlier value in the row's
   definition ("revised; originally X") and name the filing that changed it.
3. **Genuine disagreement** you can't adjudicate: escalate to the EM. Don't pick
   quietly, and don't average.

## Superseding vs forking

- **Supersede** when the newer value replaces the old for the same definition (a
  restatement, a newer filing for the same period).
- **Fork** when it is a different definition of the same idea (old vs new NRR method).
  Keep both, with distinct names.

## Failure modes

- Unlabelled basis (a non-GAAP margin read later as GAAP).
- Derived numbers without formulas, which can't be rechecked.
- Silently taking the newer value without noting a restatement.
- A second module re-deriving a quantity slightly differently, creating two "truths".

## Handoff

Name in the memo which quantities later modules will need (for example the EV bridge
and discount rate for a DCF), so the EM can point the next brief at your rows.
