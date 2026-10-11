# Module 02: What the price implies (reverse DCF)

**Engagement:** Project Hub · **Module:** 02-implied-expectations · **From:** Associate · **To:** EM
**As of:** 2026-10-11 (price: close 2026-10-09; latest reported quarter: Q2 2026, ended 2026-06-30) · **Confidence:** Medium

## Answer

**At $228.30 per share (NYSE close, 2026-10-09), the market is pricing in roughly 9% annual revenue growth for 10 years and a 17% long-run free cash flow margin (after SBC).** *(Estimate.)* That is not demanding. The price does need margins to rise a lot, from 4.2% today to about 17%. But 17% is below all four mature peers the brief names (22.5% to 33.3%). It also looks below what management's reported 2030 targets would deliver. Fast growth is not needed. If HubSpot reaches even the lowest peer margin (Autodesk, 22.5%), the price is justified at just 5.8% growth a year. **This cuts against the working answer** ("the price assumes fast growth *and* rising margins"). See Escalation 1.

## Support

**Exhibit 1: Long-run FCF margin after SBC that justifies today's EV ($10.66B)**, by 10-year revenue growth (rows) and discount rate (columns). *Estimates*, produced by `reverse_dcf.py` and not edited by hand.

| 10-yr revenue growth | 9.5% (−1 pt) | **10.5% (base)** | 11.5% (+1 pt) |
|---|---|---|---|
| 4% | 22.0% | 26.4% † | 31.1% † |
| 6% | 18.5% | 22.2% | 26.2% † |
| 8% | 15.5% | 18.7% | 22.1% |
| **9% (headline)** | 14.2% | **▶ 17.2%** | 20.3% |
| 10% | 13.0% | 15.8% | 18.7% |
| 12% | 11.0% | 13.3% | 15.8% |
| 14% (H2 2026 guided run-rate) | 9.3% | 11.2% | 13.4% |
| 16% | 7.8% | 9.5% | 11.4% |
| 18% | 6.6% | 8.1% | 9.7% |
| 20% | 5.6% | 6.9% | 8.2% |

▶ = headline. † = above the lowest peer (Autodesk 22.5%). **No cell is above the best peer (Adobe 33.3%).**
Peers (fact, latest 10-K, FCF after SBC ÷ revenue): Adobe 33.3%, Intuit 30.6%, Salesforce 26.2%, Autodesk 22.5%. HubSpot TTM: 4.2%.

1. **The headline growth rate is anchored on guidance, not chosen to fit.** FY2026 guidance implies about 14% growth in H2 2026, down from 25%, 21% and 19% in FY2023–25 (fact pack). If growth fades in a straight line from 14% in year 1 to about 4% by year 10, ending near the terminal rate, it compounds to **9.0% a year** *(estimate)*. That takes revenue from $3.45B to about $8.2B by year 10. Steady 14% growth would need only an 11.2% margin.
2. **The implied margin is below every peer's on the same definition.** All margins here are OCF − capex − capitalized software − SBC, divided by revenue, from each company's latest 10-K. The peers are not standing still: they grew 9.6% (Salesforce) to 17.5% (Autodesk) in their latest year *(derived)*. So 9% growth with a 17% margin is a weaker combination than any of the four achieves today.
3. **The real work in the price is SBC and margin repair, not growth.** HubSpot converts 19.1% of revenue to FCF before SBC, but SBC takes 14.9% of revenue (peers: 8.2–10.9%). One way to reach 17.2% is SBC falling to 10% of revenue plus pre-SBC FCF rising to about 27%. *(Hypothesis about the path, not tested.)* A secondary source reports that the September 2026 Analyst Day set 2030 targets of a 30% non-GAAP operating margin and SBC at 10% of revenue. If these are confirmed, they would imply about 20% after SBC. *(Unverified, grade C; see Escalation 3.)*
4. **The conclusion survives every input I could stress.** The implied margin at 9% growth stays between 14.4% and 21.2% in every case below, and under the lowest peer's 22.5% in all of them:

| Sensitivity (at 9% growth, 10.5%) | Implied margin |
|---|---|
| Base | 17.2% |
| Terminal growth 2.5% / 3.5% / 4.0% (cap) | 18.0% / 16.3% / 15.4% |
| Discount rate 9.5% / 11.5% | 14.2% / 20.3% |
| Price $197.67 (2026-09-29 low close) / $231.84 (10-08 high close) | 14.4% / 17.5% |
| Price +20% ($273.96) | 21.2% |
| Basic shares only (understates; shown for scale) | 16.1% |
| +1M more RSUs than counted | 17.5% |
| Capitalized SBC (~$55M/yr) also deducted from base margin | 17.6% |
| Margin reaches target in 5 years, not 10 | 15.6% |

   The price at which the headline margin would equal the lowest peer's (22.5%) is **$288** per share *(derived)*, 26% above today's price. **Terminal value is 66.5% of EV** at the headline (64–69% across the base column), below the 75% "answer is all terminal value" threshold.
5. **Base rates (judgment).** Mauboussin's *Base Rate Book* (Credit Suisse, 2016) shows that 20%+ growth for 10 years is rare at this size: only 3.0% of companies starting at $1.25–2.0B of real revenue did it. Neither the price nor the guidance needs that. I could not retrieve the book's table for a ~9% (nominal) path, so I call it unremarkable by judgment, not by cited base rate.

## Escalations to the EM

1. **The analysis points against the working answer (highest priority under the charter).** The working answer says the price assumes "fast growth *and* rising margins". The evidence says it assumes **moderate growth (about 9%) and margins rising to a level below every named peer**. The margin leg is real: 4% to 17% is a large expansion. But it is not demanding against peers. The growth leg is not supported. The engagement question may be closer to "is HubSpot structurally worse than Autodesk on margins?" than "can it keep growing fast?". I am not changing the storyline; that is the EM's call.
2. **The brief's share-count instruction cannot be met to the letter.** The Q2 2026 10-Q has no table of RSUs, PSUs or options outstanding. It gives only the anti-dilutive exclusions (2,745K RSUs/PSUs, a Q2 weighted average) and 46K of treasury-stock-method dilutive equivalents (Note 3). I used basic 49,658K + 2,745K + 46K = **52,449K diluted** (+5.6%), all as of 2026-06-30, the same date as the cash balance. I cross-checked it against the FY2025 10-K: 1,471K RSUs/PSUs at 2025-12-31, plus 2026 grants at a share price about two-thirds lower, makes ~2.7–2.9M plausible *(estimate)*. A full award roll-forward arrives with the FY2026 10-K. The error is about ±0.5M shares, which moves the margin by about ±0.4 points.
3. **The Analyst Day targets (2026-09-17) are from one secondary source.** I used The Cerbat Gem (2026-09-18): 30% non-GAAP operating margin, 20% GAAP operating margin and SBC at 10% of revenue, all by 2030. ir.hubspot.com blocks automated access (403). These figures are context only and feed no number in the grid. **Please verify them from IR** before Module 3 uses them for its base case.
4. **The price is volatile.** It closed between $197.67 and $231.84 over the 10 trading days to 2026-10-09 (+15%). The verdict holds across that range (14.4–17.5%), but the headline figures should be refreshed on the day the final range goes to the Partner.

## Assumptions and method

| Choice | Value | Why |
|---|---|---|
| Model | 10-yr explicit, constant growth, margin ramps linearly from 4.17% to target by year 10, Gordon terminal value | Skill's `reverse_dcf.py`; checked by `valuation_check.py` (status: **pass, no flags**) |
| SBC | **Expensed**: deducted from FCF (cash-flow-statement SBC, $514.7M TTM) | SBC is a real cost to owners; deducted once and future dilution not also modelled. Buybacks are a use of FCF, so they are not deducted. Same definition for peers |
| Existing unvested awards | Counted in diluted shares | These are claims that already exist. Future grants are covered by the SBC deduction. Small overlap: some of the RSUs counted also show up in future SBC expense (standard practice; tends to make the price look a bit more demanding, not less) |
| Discount rate | **10.5%** = 5.24% + 1.25 × 4.20% (10.49%, rounded) | CAPM. No debt, so the discount rate is the cost of equity. Beta is bottom-up (industry, cash-corrected) and agrees with the 1.24 regression beta |
| Terminal growth | **3.0%**, cap 4.0% | Cap = FOMC longer-run 2.0% real + 2.0% inflation. Set 1 point below the cap because a mature franchise should not outgrow the economy forever. Sensitivity includes the cap |
| EV bridge | Equity $11,974M − cash and investments $1,383M + restructuring $70M = **EV $10,661M** | Debt is zero. Restructuring cash ($65–75M midpoint, 8-K 2026-10-06) is a committed outflow not in TTM FCF. Operating leases ($237M) are *not* added: lease payments already reduce OCF, so adding them would double-count |
| Peer margins | Single latest fiscal year, from the 10-K, as the brief fixes | Prior-year margins were lower (Adobe 28.1%, Salesforce 24.4%, Intuit 21.9%, Autodesk 14.4%; *derived*). Autodesk's prior year was depressed by its billing-cycle change. Even on prior years the headline is below three of four peers |
| Headline growth | 9.0% | Guided H2 2026 exit rate (~14%) faded linearly to ~4% by year 10. This is my construction; consensus long-term growth is not available from free sources |

## Confidence: Medium

The inputs that set EV (price, shares, cash, TTM FCF) are facts or simple arithmetic on them, and they tie to the fact pack. But the discount rate, terminal growth and headline growth path are judgment inputs, and the share count rests on a weighted-average proxy. **The verdict is less sensitive than the headline number**: no tested combination puts the implied margin above the lowest peer. **Top 2 things that would change the answer:** (1) **Growth collapsing below ~6%.** Q3 2026 results (early November) are the next read: at 5.8% growth the price needs Autodesk's margin. (2) **A re-rating to about $288 or more.** At that price, 9% growth needs a 22.5% margin and the verdict moves to "demanding".

## Open issues and gaps

- **Module 3 should reuse these, unchanged:** discount rate 10.5% (and its three inputs), terminal growth 3.0% / cap 4.0%, diluted shares 52,449K, cash $1,383.2M, restructuring $70M, EV $10,660.9M, base FCF margin after SBC 4.17%. See Exhibit A. Price and shares go stale with the Q3 10-Q.
- **Not done:** consensus forecasts (no free source); Base Rate Book table for a ~9% path; the exact FY2025 capitalized SBC (the 10-K text search found no match, so I used ~$55M, 2 × the H1 average, in one sensitivity only *(estimate)*); Analyst Day targets from a primary source.
- **The model is end-of-year, single-stage.** A mid-year discounting convention would lower every implied margin by about 0.5–1 point. That is conservative for the verdict.
- **Skills:** `implied-expectations` is complete and was followed. The closing trio (`module-memo`, `fact-base-contribution`, `confidentiality-check`) were used as written; they are no longer stubs.
- **Confidentiality check: pass.** Sources are public (SEC filings, US Treasury, Federal Reserve, Damodaran's published data, public price history, one public news article). There is no client data-room material and no other-client material. Peer data are public 10-K figures for named public companies; no client is named.

---

## Exhibit A: Every figure, with lineage

Values in $ thousands as filed unless noted. Grades: A = audited 10-K; A− = reviewed 10-Q; B = 8-K / official statistical source; C = secondary web source.

**Sources**
- [S1] HubSpot 10-Q Q2 2026 (filed 2026-08-05): https://www.sec.gov/Archives/edgar/data/1404655/000119312526335232/hubs-20260630.htm
- [S2] HubSpot 10-K FY2025 (filed 2026-02-11): https://www.sec.gov/Archives/edgar/data/1404655/000119312526046646/hubs-20251231.htm
- [S3] HubSpot 8-K, restructuring (filed 2026-10-06): https://www.sec.gov/Archives/edgar/data/1404655/000119312526414965/d183135d8k.htm
- [S4] Adobe 10-K FY2025 (FYE 2025-11-28): https://www.sec.gov/Archives/edgar/data/796343/000079634326000003/adbe-20251128.htm
- [S5] Salesforce 10-K FY2026 (FYE 2026-01-31): https://www.sec.gov/Archives/edgar/data/1108524/000110852426000060/crm-20260131.htm
- [S6] Intuit 10-K FY2026 (FYE 2026-07-31, filed 2026-09-09): https://www.sec.gov/Archives/edgar/data/896878/000089687826000037/intu-20260731.htm
- [S7] Autodesk 10-K FY2026 (FYE 2026-01-31): https://www.sec.gov/Archives/edgar/data/769397/000076939726000015/adsk-20260131.htm
- [S8] Price history: https://stockanalysis.com/stocks/hubs/history/ and https://www.financialcontent.com/quote/NY:HUBS/historical (accessed 2026-10-11; identical OHLC)
- [S9] US Treasury daily par yield curve, Oct 2026: https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?type=daily_treasury_yield_curve&field_tdr_date_value_month=202610 ; cross-check FRED DGS10: https://fred.stlouisfed.org/series/DGS10
- [S10] Damodaran implied ERP (2026-10-01): https://pages.stern.nyu.edu/~adamodar/New_Home_Page/home.htm
- [S11] Damodaran industry betas (Jan 2026): https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/Betas.html ; regression cross-check https://stockanalysis.com/stocks/hubs/statistics/
- [S12] FOMC Summary of Economic Projections (2026-09-16): https://www.federalreserve.gov/monetarypolicy/fomcprojtabl20260916.htm
- [S13] The Cerbat Gem, "HubSpot Unveils AI Agent Strategy, Lifts 2030 Margin Targets at Analyst Day" (2026-09-18): https://www.thecerbatgem.com/?p=10395683
- [S14] Mauboussin et al., *The Base Rate Book* (Credit Suisse, 2016), as quoted at https://thesmartinvestor.com.sg/a-new-world-of-accelerating-growth

### A1. Facts (HubSpot)

| Quantity | Period / date | Value | Definition | Basis | Source (grade) |
|---|---|---|---|---|---|
| Share price | 2026-10-09 close | $228.30 | NYSE close; range 10 days to 10-09: $197.67–231.84 | Market | S8 (B) |
| Basic shares outstanding | 2026-06-30 | 49,658K | Balance sheet | GAAP | S1 (A−) |
| RSUs + PSUs excluded as anti-dilutive | Q2 2026 (wtd. avg.) | 2,745K | Note 3; zero strike, counted in full | GAAP | S1 (A−) |
| Dilutive equivalents (TSM) | Q2 2026 (wtd. avg.) | 46K | Options, RSUs, ESPP, PSUs (Note 3) | GAAP | S1 (A−) |
| Options excluded as anti-dilutive | Q2 2026 | 95K | Out of the money at Q2 prices; not counted | GAAP | S1 (A−) |
| RSUs / PSUs / options outstanding | 2025-12-31 | 1,396K / 75K / 174K (WAEP $286.89) | Cross-check only | GAAP | S2 (A) |
| Cash + ST + LT investments | 2026-06-30 | 1,383,208 | 958,314 + 379,629 + 45,265 | GAAP | S1 (A−); fact pack A4 |
| Debt | 2026-06-30 | 0 | Notes settled June 2025; revolver undrawn | GAAP | S1 (A−) |
| Restructuring charges | Mostly Q4 2026 | $65–75M | ~7% of workforce; mostly cash severance | Guidance | S3 (B) |
| Revenue | TTM Jun-26 | 3,448,998 | FY25 3,131,266 + H1'26 1,792,735 − H1'25 1,475,003 | Derived (GAAP) | S1, S2 |
| OCF / PP&E / cap. software / SBC | TTM Jun-26 | 856,365 / 58,869 / 139,059 / 514,712 | Same TTM formula on each cash-flow line | Derived (GAAP) | S1, S2 |
| FCF before SBC | TTM Jun-26 | 658,437 (19.09%) | OCF − PP&E − cap. software | Derived | as above |
| FCF after SBC | TTM Jun-26 | 143,725 (**4.17%**) | FCF before SBC − SBC | Derived | as above |
| Capitalized SBC (not expensed) | H1 2026 / H1 2025 | $27.6M / $28.8M | Excluded from SBC expense (Note 14) | GAAP | S1 (A−) |

### A2. Facts (peers, latest fiscal year, $M)

| Peer | FY end | Revenue | OCF | PP&E | Cap. software | SBC | FCF after SBC % | FCF before SBC % | Revenue growth | Prior-yr FCF after SBC % | Source |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Adobe | 2025-11-28 | 23,769 | 10,031 | 179 | — | 1,942 | **33.3%** | 41.4% | 10.5% | 28.1% | S4 (A) |
| Salesforce | 2026-01-31 | 41,525 | 14,996 | 594 | — | 3,509 | **26.2%** | 34.7% | 9.6% | 24.4% | S5 (A) |
| Intuit | 2026-07-31 | 21,448 | 8,838 | 175 | 46 | 2,056 | **30.6%** | 40.2% | 13.9% | 21.9% | S6 (A) |
| Autodesk | 2026-01-31 | 7,206 | 2,452 | 43 | — | 788 | **22.5%** | 33.4% | 17.5% | 14.4% | S7 (A) |

"—" = no separate capitalized-software investing outflow tagged in XBRL. Percentages are derived: (OCF − PP&E − cap. software − SBC) ÷ revenue. Prior-year inputs (Adobe FY2024 8,056 / 183 / 1,833 / 21,505; Salesforce FY2025 13,092 / 658 / 3,183 / 37,895; Intuit FY2025 6,207 / 84 / 40 / 1,968 / 18,831; Autodesk FY2025 1,607 / 40 / 683 / 6,131) come from the same 10-Ks.

### A3. Market and macro inputs

| Quantity | Date | Value | Source (grade) |
|---|---|---|---|
| 10-year Treasury par yield | 2026-10-09 | 5.24% (FRED 10-08: 5.22%) | S9 (B) |
| Implied equity risk premium, S&P 500 | 2026-10-01 | 4.20% | S10 (B) |
| Beta, Software (System & Application), unlevered, cash-corrected | Jan 2026 | 1.25 (levered 1.24 regression, HUBS 5Y) | S11 (B / C) |
| FOMC longer-run real GDP growth / PCE inflation (median) | 2026-09-16 | 2.0% / 2.0% | S12 (B) |
| Analyst Day 2030 targets | 2026-09-17 | 30% non-GAAP op. margin; 20% GAAP op. margin; SBC 10% of revenue | S13 (C, unverified) |
| Share of $1.25–2.0B companies with 20%+ 10-yr growth | 1950–2015 | 3.0% | S14 (C) |

### A4. Estimates (this module; tag as *estimate* in the fact base)

| Quantity | Value | Formula / method |
|---|---|---|
| Diluted shares | 52,449K | 49,658 + 2,745 + 46 |
| Equity value | $11,974.1M | $228.30 × 52,449K |
| Enterprise value | $10,660.9M | Equity − 1,383.2 cash + 70.0 restructuring (midpoint) |
| Cost of equity = discount rate | 10.49% → 10.5% | 5.24% + 1.25 × 4.20% |
| Terminal growth | 3.0% (cap 4.0%) | Judgment below FOMC nominal (2.0% + 2.0%) |
| Headline growth | 9.0% | Linear fade 14% → 4.1% over years 1–10; CAGR |
| **Headline implied margin** | **17.15% after SBC** | `reverse_dcf.py`, 9% growth, 10.5% |
| Terminal value share at headline | 66.5% | `reverse_dcf.py` |
| Growth needed at lowest / median / best peer margin | 5.8% / 3.2% / 1.4% | `implied_growth`, 10.5% |
| Price at which headline margin = 22.5% | $288 | EV at 22.5% margin ($13.79B) + cash − restructuring, ÷ diluted shares |

Model files: `valuation.json` (all inputs with sources, plus the grid); `valuation_check.py` result: pass, 0 errors, 0 flags.

---

## EM review (2026-10-11)

Accepted; passes the gate (`valuation_result.json`: pass, no flags). Checked independently
of the Associate: the $228.30 close on 2026-10-09 (stockanalysis.com daily history), the
10-year Treasury (FRED DGS10 5.22% on 10-08), Adobe's OCF and SBC (EDGAR, tie to the
peer row), the diluted share arithmetic, and a re-run of the model: 17.15% at 9% growth,
5.85% growth at Autodesk's margin, 16.2% on basic shares, 21.2% at an 11.5% discount
rate with 2.5% terminal growth. All tie; the verdict holds in every case.

**For the Partner (escalation 1 is a storyline decision, not the EM's):** "undemanding
against mature peers" assumes HubSpot *becomes* a mature peer. A low price can also mean
the market expects something these peers don't face, such as AI eroding seat-based
software, so growth and margins never get there. Module 3's bear case should test that
directly rather than assume convergence to peer margins.
