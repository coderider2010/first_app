# Module 03: DCF scenarios ("Grows up" vs "Squeezed")

**Engagement:** Project Hub · **Module:** 03-dcf-scenarios · **From:** Associate · **To:** EM
**As of:** 2026-10-11 (price: NYSE close 2026-10-09, still the latest; latest reported quarter: Q2 2026, ended 2026-06-30) · **Confidence:** Medium

## Answer

**If HubSpot grows up like its peers, it is worth about $344 per share; if AI pressure squeezes it, about $149. Today's price of $228.30 (close 2026-10-09) sits between the two, closer to Squeezed.** *(Estimates.)* Read as a probability mix, the price gives Grows up about a 41% weight (25–42% across the last two weeks' $198–232 range). **The price does not assume "fast growth and rising margins".** Grows up's growth path (14% fading to 4%, a 9.0% compound rate) needs only a 15.7% margin after SBC to justify $228, against the story's 25%. The market accepts the growth but doubts the margin, and that is the main thing separating the stories. This cuts against the working answer (Escalation 1).

## Support

**Exhibit 1: Two stories, valued.** 10-year DCF, discount rate 10.5%, terminal growth 3.0%, FCF after SBC. *Estimates* from `dcf.py`; the gate recomputes every value.

| | **Grows up** | **Squeezed** |
|---|---|---|
| What has to be true | AI agents and credits add to seat revenue rather than replacing it. Net adds recover toward 9–10K a quarter, NRR returns to at least 103.5% (FY2025), SBC falls to ~8% of revenue | AI budgets, price cuts and token costs hold back expansion. Net adds stay at the guided 5–6K a quarter, NRR drifts below 100%, SBC stays near 13% |
| Revenue growth, yr 1 → yr 10 | 14% → 4%, straight-line fade (9.0% compound; revenue 2.4× to $8.1B) | 12%, 9, 7, 6, 5, 4, then 3% from year 7 (5.5% compound; 1.7× to $5.9B) |
| FCF margin after SBC (today 4.2%) | 25% by year 7 (pre-SBC ~33% − SBC ~8%) | Stalls at 12% from year 5 (pre-SBC ~25% − SBC ~13%) |
| Enterprise value | $16.7B (4.8× TTM revenue) | $6.5B (1.9×) |
| **Value per share** | **$343.75** (+51% vs price) | **$149.21** (−35%) |
| Terminal value share of EV | 61.5% | 54.7% |
| Evidence (detail in Exhibit A3) | 8-K: management "remains confident" in its long-term margin targets [S3]. Margin repair under way: non-GAAP op. margin 15.5% → 20.3%, SBC 19.9% → 14.9% of revenue [S1] | Net adds fell to 6,988 in Q2 2026 from 9,724 a year earlier; guided to 5–6K [S4, S5]. CEO: "unpredictable AI costs … are impacting budgets"; entry prices lowered [S6] |
| | Seat and credit expansion still lifted NRR in Q2; credit consumption grew [S6]. Peers raised FCF margins through the AI period, e.g. Autodesk 14.4% → 22.5% [S2] | New 10-K risk factor on generic LLMs and vibe coding forcing price cuts (absent in FY2024) [S7, S8]. AI inference is now in cost of revenue; gross margin fell 85.0% → 82.4% [S1, S4] |

**Exhibit 2: Sensitivity, value per share** (discount rate ±1 point × terminal growth ±0.5 point; *estimates*, `dcf.py`)

| Discount rate → | 9.5% | **10.5%** | 11.5% |
|---|---|---|---|
| Grows up, g = 2.5% / **3.0%** / 3.5% | $384 / $403 / $425 | $331 / **$344** / $359 | $290 / $299 / $310 |
| Squeezed, g = 2.5% / **3.0%** / 3.5% | $164 / $170 / $178 | $145 / **$149** / $154 | $130 / $133 / $137 |

No cell moves either story across today's price. Every Grows up cell is above $228, and every Squeezed cell is below it.

1. **The stories differ in mechanism, and margin does most of the work.** Swapping only the margin between the stories moves value by $116–156 per share. Swapping only the growth path moves it by $39–79 *(estimates)*. The question is therefore less "will HubSpot keep growing?" than "does AI let HubSpot reach peer margins, or does it eat them through price cuts and inference costs?" This matches Module 2.
2. **The best evidence for each story comes from the same Q2 2026 call.** Squeezed: net adds missed by about 25%, and downgrade pressure came as customers "optimize their overall spend" around AI. NRR fell to 102%, entry prices were cut, and management assumes the headwinds persist. Grows up: the pressure is *not* yet seat loss. "Seat and credit expansion" still lifted NRR, "customer dollar retention remained healthy in the high 80s", and credits grew despite price cuts. The pure "AI shrinks seats" mechanism has no support in HubSpot's own data yet; the squeeze shows up through budgets, price and new-customer conversion. *(Fact for the quotes; the transcript is grade C. See Escalation 2.)*
3. **Management is betting publicly on Grows up's margin leg.** It raised FY2026 operating-income guidance while trimming revenue. It restructured about 7% of staff and still "remains confident" in the 2030 targets. A secondary source reports those targets as 30% non-GAAP operating margin with SBC at 10%, roughly 19–20% after SBC by 2030. Grows up passes that path (19.1% in year 5) and then goes further. The CEO also says the AI pivot "is transforming product, pricing", which supports either story.
4. **The answer holds under every input I stressed** *(estimates)*:

| Stress (base: GU $344 / SQ $149) | Grows up | Squeezed |
|---|---|---|
| Target margin −5 / +5 points | $282 / $406 | $110 / $189 |
| Growth −2 / +2 points every year | $297 / $398 | $132 / $170 |
| Margin ramp over 10 years (Module 2's convention) | $323 | $138 |
| Basic shares only (49.87M; overstates value) | $362 | $157 |

   Only the Squeezed +5-point margin case ($189) comes within 20% of the price, and none crosses it. **Terminal value is 55–62% of EV**, below the 75% flag, so the answer does not rest mainly on years 11 and beyond.
5. **What decides it (watch list):**
   - **NRR and net customer adds**, in Q3 2026 results (early November) and FY2026 NRR in the 10-K (February 2027). Grows up needs adds back toward 9–10K a quarter and NRR at 103.5% or more. Squeezed predicts adds of 5–6K or fewer and NRR below 102%.
   - **Gross margin against AI costs.** The non-GAAP subscription margin fell from 87.1% to 85.3% year on year. Further erosion with flat pricing is a Squeezed signature. Stabilising while credits grow fits Grows up.
   - **SBC as a share of revenue.** Grows up needs 14.9% to fall to about 8–10%; Squeezed has it stuck near 13%. Watch the guided FY2027 SBC.

## Escalations to the EM

1. **The analysis points against the working answer (highest priority).** The Partner kept "the price assumes fast growth and rising margins" as the hypothesis to test. It fails the test. At $228 the market pays for about 41% of Grows up and 59% of Squeezed. Grows up's ~9% growth is fully accepted, but only about a 16% margin after SBC is priced, against the story's 25%. The low bar reflects a priced-in risk that AI caps margins, and the filings show real evidence of that risk. It is neither a clear bargain nor a clear trap; which it is depends on the three watch-list facts. I am not changing the storyline.
2. **The most discriminating evidence rests on a grade-C transcript.** The Q2 2026 call quotes come from a third-party transcript (platformaeronaut.com). HubSpot's IR file host returned 403 to automated access. The net-add numbers are verified against the 10-Qs; the quotes on NRR (102%), seats, downgrades and pricing are not. **Please verify against the FactSet transcript on ir.hubspot.com** before the Partner sees them. The Analyst Day 2030 targets are still single-source (grade C), as in Module 2. They feed no number here; the Grows up margin of 25% comes from the peer range, not from the targets.
3. **Material and not in the brief: Q2 NRR was 102%.** The fact pack says no 2026 NRR exists in SEC filings. The call gives 102% (down 1 point) and guides FY2026 to "roughly flat". If verified, it belongs in the fact pack (method: new 2025 definition, presumably).
4. **Inputs reused from Module 2, unchanged, and re-run:** 10.5% discount rate (5.24% + 1.25 × 4.20% = 10.49%), terminal growth 3.0% (cap 4.0%), 52,449K diluted shares, $1,383.2M cash, $0 debt, $70M restructuring, base margin 4.17%. All recomputed from EDGAR on 2026-10-11 and tie. **Price refresh:** no new close since Module 2 (10-10 and 10-11 are a weekend), so $228.30 stands. One difference: Module 2's headline used a constant 9% growth; the fade path behind it (14% → 4%) implies 16.6% rather than 17.2% at the same price. That is immaterial to both modules' conclusions.

## Assumptions and method

| Choice | Value | Why |
|---|---|---|
| Model | 10-year explicit, end-of-year discounting, Gordon terminal value; FCF margin moves linearly from 4.17% to target over the ramp | `dcf.py`, the same engine as Module 2's `reverse_dcf.py`; `valuation_check.py`: **pass, 0 errors, 0 flags** |
| SBC | **Expensed** in FCF (after-SBC margin), not modelled again as dilution. Existing unvested RSUs/PSUs are in diluted shares | Counted once, as in Module 2. Future grants are the expense |
| Reinvestment | Inside the FCF margin. Capex plus capitalized software is 5.7% of revenue today ($198M TTM), held at ~5–6% in both stories; S&M and R&D are expensed, so they sit in the pre-SBC margin | The model has no separate reinvestment line. Consistency: Grows up's ~33% pre-SBC margin matches Autodesk's 33.4% while it grew 17.5%. Squeezed's 25% at 3% growth needs price cuts and inference costs to absorb the S&M savings that slower growth would normally free up. That is the story's mechanism |
| Year 1 | Covers H2 2026 + H1 2027 (base is TTM to Jun-26) | Grows up: the guided H2 2026 run-rate (~14%). Squeezed: 14% in H2, then lower on 5–6K net adds and "net new ARR … below constant currency revenue growth" → ~12% |
| Terminal | 3.0% for both stories; year-10 growth 4% (GU) and 3% (SQ), so no abrupt step | EM limit: reuse Module 2. Implied terminal multiple is 13.7× year-10 FCF |
| Margin ramps | Grows up 7 years, Squeezed 5 years | GU: passes management's reported 2030 path around year 5. SQ: margins stall early, which is the story |
| Not tuned to price | Drivers set from guidance, history and peers before valuing. Neither value is within 30% of the price (+51% / −35%) | Brief rule |

## Confidence: Medium

The bridge, base year and discount-rate arithmetic are facts or simple arithmetic and tie to Modules 1 and 2. But each story's margin target and growth path are judgment, and the most telling evidence (call quotes) is grade C until verified. **Top 2 things that would change the answer:** (1) **Q3 2026 NRR and net adds** (early November). These move the price-implied mix and could retire one story. (2) **The long-run margin.** Each 5 points moves value by $40–62 per share, more than any other input.

## Open issues and gaps

- **Triangulation:** this DCF is one path. The second, independent path is Module 4 (peers), which by design I did not read; the EM reconciles the two. As a consistency check, Module 2's reverse DCF reproduces today's price within this model.
- **Not done:** HubSpot does not disclose seat counts or credit revenue, so the seat mechanism cannot be measured directly. There are no consensus forecasts (no free source). The Analyst Day revenue targets were not found. The model uses end-of-year discounting; mid-year would raise both values by about 5%.
- **Stale soon:** Q3 2026 10-Q (early November) updates the share count (buybacks: 49.87M basic at 2026-07-31), cash, NRR and net adds.
- **Skills:** `valuation-dcf` is complete and was followed. The closing trio (`module-memo`, `fact-base-contribution`, `confidentiality-check`) was applied.
- **Confidentiality check: pass.** Sources are public: SEC filings, public price history, a public third-party call transcript and one public news article. There is no client data-room material and no other-client material. Brief 04's output was not read.
- **Fact base:** later modules need Exhibit A4 (scenario values, drivers, mix). The NRR 102% row (A3) is a candidate fact-pack update once verified.

---

## Exhibit A: Every figure, with lineage

Grades: A = audited 10-K; A− = reviewed 10-Q; B = 8-K / market data; C = secondary web source.

**Sources**
- [S1] Module 01 fact pack (`modules/01-fact-pack/memo.md`, Exhibits A1–A6), from HubSpot 10-Ks, 10-Qs and 8-K Ex. 99.1s cited there
- [S2] Module 02 (`modules/02-implied-expectations/memo.md` and `valuation.json`): discount rate, terminal growth, shares, EV bridge, peer margins
- [S3] HubSpot 8-K, restructuring and guidance (filed 2026-10-06): https://www.sec.gov/Archives/edgar/data/1404655/000119312526414965/d183135d8k.htm
- [S4] HubSpot 10-Q Q2 2026: https://www.sec.gov/Archives/edgar/data/1404655/000119312526335232/hubs-20260630.htm
- [S5] HubSpot 10-Q Q1 2026: https://www.sec.gov/Archives/edgar/data/1404655/000119312526212122/hubs-20260331.htm
- [S6] HubSpot Q2 2026 earnings call (2026-08-05), third-party transcript: https://transcripts.platformaeronaut.com/transcripts/HUBS-2Q26-transcript
- [S7] HubSpot 10-K FY2025: https://www.sec.gov/Archives/edgar/data/1404655/000119312526046646/hubs-20251231.htm
- [S8] HubSpot 10-K FY2024: https://www.sec.gov/Archives/edgar/data/1404655/000095017025018873/hubs-20241231.htm
- [S9] HubSpot 8-K Ex. 99.1, CEO letter (2026-10-06): https://www.sec.gov/Archives/edgar/data/1404655/000119312526414965/d183135dex991.htm
- [S10] Salesforce 10-K FY2026: https://www.sec.gov/Archives/edgar/data/1108524/000110852426000060/crm-20260131.htm
- [S11] Price history: https://stockanalysis.com/stocks/hubs/history/ and https://www.financialcontent.com/quote/NY:HUBS/historical (accessed 2026-10-11; agree)
- [S12] The Cerbat Gem, Analyst Day article (2026-09-18): https://www.thecerbatgem.com/?p=10395683

### A1. Inputs reused from Module 2 (re-run 2026-10-11)

| Quantity | Date / period | Value | Basis | Source (grade) |
|---|---|---|---|---|
| Share price | Close 2026-10-09 | $228.30 (10-day range $197.67–231.84) | Market | S11 (B) |
| Diluted shares | 2026-06-30 | 52,449K = 49,658 basic + 2,745 RSUs/PSUs + 46 TSM | Derived (GAAP) | S4, S2 |
| Basic shares outstanding | 2026-07-31 | 49,866,201 | Fact | S4 cover (A−) |
| Cash + investments | 2026-06-30 | $1,383,208K (cash 958,314K, re-pulled from XBRL) | GAAP | S4 (A−) |
| Debt | 2026-06-30 | 0 | GAAP | S4 (A−) |
| Restructuring cash (EV adjustment) | Q4 2026–Q2 2027 | $70M (midpoint of $65–75M) | Guidance | S3 (B) |
| Revenue | TTM Jun-26 | $3,448,998K = 3,131,266 + 1,792,735 − 1,475,003 | Derived (GAAP) | S1 |
| OCF / PP&E / cap. software / SBC | TTM Jun-26 | 856,365 / 58,869 / 139,059 / 514,712 ($K; OCF and SBC re-pulled from XBRL) | Derived (GAAP) | S1, S4, S7 |
| FCF margin after SBC | TTM Jun-26 | 4.17% (143,725 / 3,448,998) | Derived | S1 |
| Capex + cap. software, % revenue | TTM Jun-26 | 5.7% (197,928 / 3,448,998) | Derived | S1 |
| Discount rate | 2026-10-09 | 10.5% = 5.24% + 1.25 × 4.20% | Estimate (CAPM) | S2 |
| Terminal growth / cap | — | 3.0% / 4.0% | Estimate / FOMC | S2 |
| Peer FCF margin after SBC, latest / prior FY | — | Adobe 33.3 / 28.1; Salesforce 26.2 / 24.4; Intuit 30.6 / 21.9; Autodesk 22.5 / 14.4 (%) | Derived (GAAP) | S2 (A) |

### A2. New facts (this module)

| Quantity | Period | Value | Definition | Basis | Source (grade) |
|---|---|---|---|---|---|
| Customers | 2025-03-31 / 2026-03-31 | 258,258 / 299,458 | Company KPI | KPI | S5 (A−) |
| Customers | 2025-06-30 / 2026-06-30 | 267,982 / 306,446 | Company KPI | KPI | S4 (A−) |
| Net customer adds | Q1 2026 / Q2 2026 / Q2 2025 | 10,752 / 6,988 / 9,724 | Change in period-end customers; Q1 2026 = 299,458 − 288,706 (2025-12-31, S7) | Derived (KPI) | S4, S5, S7 |
| Driver of customer growth | Q1, Q2 2026 | "increased demand for our lower-priced Starter products" | MD&A text | Fact | S4, S5 (A−) |
| AI in cost of revenue | Q2 2026 | Cost of subscription includes "AI inferencing costs" | Accounting policy text | Fact | S4 (A−) |
| Competition risk factor | FY2025 10-K, Q2 2026 10-Q vs FY2024 10-K | "generic LLMs", "general-purpose agents", "vibe coding" may force HubSpot to "decrease the prices". Present in FY2025 and Q2 2026; absent in FY2024 | Risk factor text | Fact | S7, S4, S8 (A) |
| Pricing model | FY2024 → FY2025 10-K | "recent seats-based pricing model changes" → "seats-based and consumption-based pricing model changes" | Risk factor text | Fact | S8, S7 (A) |
| Margin-target statement | 2026-10-06 | "remains confident in achieving its longer-term operating margin targets" | 8-K Item 2.02 | Fact | S3 (B) |
| Strategy statement | 2026-10-06 | Shift "to delivering outcomes for them with AI … transforming product, pricing"; layoffs "not driven by AI-related efficiencies"; ~660 roles | CEO letter | Fact | S9 (B) |
| Peer risk factor | Salesforce FY2026 | Attrition risk from "decreases in the number of users at our customers" and "increased prevalence of consumption-based pricing models" | Risk factor text | Fact | S10 (A) |

### A3. Call statements (Q2 2026, 2026-08-05; *unverified transcript, grade C*)

| Speaker | Statement |
|---|---|
| CFO | Net adds "below our 9,000 to 10,000 expectation and driven primarily by weaker conversion rates"; now ~5–6K a quarter |
| CFO | "net revenue retention was 102%, down a point year-over-year as continued seat and credit expansion was offset by other net upgrade headwinds"; FY2026 NRR "roughly flat"; "Customer dollar retention remained healthy in the high 80s" |
| CFO | "we're seeing some downgrade pressure as they sort of optimize their overall spend"; "Our Q3 and full year guidance reflects our expectation that the headwinds we saw in Q2 will persist"; "net new ARR growth to be below constant currency revenue growth" for FY2026 |
| CEO | "unpredictable AI costs across the broader landscape are impacting budgets"; "we introduced outcome-based pricing for several of our HubSpot agents, lowered entry price points"; introduced trials |
| CEO / CFO | "Total credits consumption grew in Q2 despite the pricing changes we made in April"; "two to three points of operating margin expansion in 2027"; SBC % of revenue to fall year over year |
| Analyst Day (S12, C) | 2030: 30% non-GAAP operating margin, 20% GAAP operating margin, SBC 10% of revenue |

### A4. Estimates (this module; tag as *estimate* in the fact base)

| Quantity | Grows up | Squeezed | Method |
|---|---|---|---|
| Growth path | 14% → 4% linear | 12, 9, 7, 6, 5, 4, 3, 3, 3, 3% | Judgment from guidance (A6 of S1) and A2–A3 |
| 10-yr compound growth / year-10 revenue | 9.0% / $8,130M | 5.5% / $5,869M | `dcf.py` years |
| Target margin after SBC / ramp | 25% / 7 yrs | 12% / 5 yrs | Judgment: GU in peer range (22.5–33.3%); SQ stalls |
| Enterprise value | $16,716.0M | $6,512.5M | `dcf.py` |
| Equity value (EV + cash − restructuring) | $18,029.2M | $7,825.7M | `dcf.py` |
| **Value per share** | **$343.75** | **$149.21** | ÷ 52,449K diluted shares |
| Terminal value share | 61.5% | 54.7% | `dcf.py` |
| Price-implied weight on Grows up | 40.7% (24.9–42.5% over the 10-day range) | — | (P − SQ) / (GU − SQ) |
| Margin that justifies the price at this story's growth | 15.7% | 20.0% | `implied_margin`, same model |
| Value with the other story's margin / growth | $188 / $265 | $265 / $188 | Swap test, same model |

**Drivers by year** (from `dcf.py`; $M; margin = FCF after SBC ÷ revenue)

| Year | GU growth | GU revenue | GU margin | GU FCF | SQ growth | SQ revenue | SQ margin | SQ FCF |
|---|---|---|---|---|---|---|---|---|
| 1 | 14.0% | 3,932 | 7.1% | 281 | 12.0% | 3,863 | 5.7% | 221 |
| 2 | 12.9% | 4,439 | 10.1% | 449 | 9.0% | 4,211 | 7.3% | 307 |
| 3 | 11.8% | 4,961 | 13.1% | 650 | 7.0% | 4,505 | 8.9% | 399 |
| 4 | 10.7% | 5,491 | 16.1% | 882 | 6.0% | 4,776 | 10.4% | 498 |
| 5 | 9.6% | 6,015 | 19.1% | 1,146 | 5.0% | 5,014 | 12.0% | 602 |
| 6 | 8.4% | 6,523 | 22.0% | 1,437 | 4.0% | 5,215 | 12.0% | 626 |
| 7 | 7.3% | 7,002 | 25.0% | 1,750 | 3.0% | 5,371 | 12.0% | 645 |
| 8 | 6.2% | 7,437 | 25.0% | 1,859 | 3.0% | 5,533 | 12.0% | 664 |
| 9 | 5.1% | 7,817 | 25.0% | 1,954 | 3.0% | 5,699 | 12.0% | 684 |
| 10 | 4.0% | 8,130 | 25.0% | 2,033 | 3.0% | 5,869 | 12.0% | 704 |

Model file: `valuation.json` (all inputs with sources, both scenarios with evidence, and the full sensitivity list); `valuation_check.py`: pass, 0 errors, 0 flags.

---

## EM review (2026-10-11)

Accepted; passes the gate (`valuation_check.py`: pass, no flags). Checked independently of
the Associate: both values recompute ($343.75, $149.21); the price's position between them
(40.7% toward Grows up); the swap test (margin swap moves value $116–156, growth swap
$39–79); net customer adds of 6,988 (Q2 2026) vs 9,724 (Q2 2025) from the Q1 and Q2 10-Qs;
and the vibe-coding risk factor, present in the FY2025 10-K and absent from the FY2024 10-K.

The earnings-call quotes (grade C, third-party transcript) are unverified and carry only
supporting weight; no number in the model depends on them. Q2 2026 NRR of 102% from the
call should enter the fact pack only after it is checked against the IR transcript.
