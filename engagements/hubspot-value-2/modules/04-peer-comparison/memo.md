# Module 04: Peer comparison (trading multiples)

**Engagement:** Project Hub II (what is HubSpot worth per share?) · **Module:** 04 peer comparison · **From:** Associate · **To:** EM
**As of:** prices at close 9 Oct 2026; financials TTM to each company's latest 10-Q/10-K (Jun-26 or Jul-26). Written 2026-10-12.
**Confidence:** **Low** on the value range: the three methods disagree by 2.8x and the growth adjustment failed (r² 0.03). **High** on the inputs: every peer figure is filed or is arithmetic on filed figures, the method reproduces Module 01's HubSpot numbers exactly, and every price matches a second source to the cent.

---

## Answer

**Listed peers imply $178–$502 per share for HubSpot (spread of three methods; the growth-and-margin regression did not hold), against today's $228.30 (close 9 Oct 2026).** The range is wide because the two ways of reading peers point in opposite directions, and that gap is the finding. On revenue, HubSpot is the cheapest company in the set: 3.07x EV/revenue against a peer median of 6.37x, which would mean $445. On cash, it is expensive: 73.6x EV/FCF after SBC against a median of 55.5x, which means $178. The market is valuing HubSpot on its cash flow, not its revenue. That cash flow is thin: FCF after SBC is 4.2% of revenue against a peer median of 14.9%. **None of that gap is stock-based compensation.** HubSpot's SBC (14.9% of revenue) is slightly *below* the peer median (16.2%). The gap is in cash generation before SBC: an OCF margin of 24.8% vs 32.1%, plus heavier capex and capitalized software (5.7% of revenue vs 2.3%). The price sits between the median and the upper quartile of the cash lens ($178–$234), and far below every point of the revenue lens ($308 at the cheapest peer's multiple).

## Support

**Exhibit 1. Peers sorted by rule-of-40 score, HubSpot in place (USD millions; prices 9 Oct 2026; TTM to latest filing)**

| Company | EV | TTM revenue | Growth | FCF-after-SBC margin | Rule of 40 | EV/revenue | EV/FCF after SBC | Source |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| Autodesk | 49,583 | 7,790.0 | 17.9% | 27.4% | 45.3% | 6.37x | 23.3x | 10-Q Jul-26, 10-K FY26 [P1] |
| ServiceNow | 153,483 | 14,732.0 | 22.2% | 16.3% | 38.5% | 10.42x | 64.1x | 10-Q Jun-26, 10-K FY25 [P3] |
| DocuSign | 14,398 | 3,361.2 | 8.6% | 17.6% | 26.2% | 4.28x | 24.3x | 10-Q Jul-26, 10-K FY26 [P4] |
| Okta | 39,982 | 3,073.0 | 11.2% | 14.9% | 26.1% | 13.01x | 87.3x | 10-Q Jul-26, 10-K FY26 [P7] |
| ***HubSpot (at $228.30)*** | *10,580* | *3,449.0* | *21.1%* | *4.2%* | *25.3%* | *3.07x* | *73.6x* | *Module 01; pins* |
| Workday | 48,766 | 10,155.0 | 13.3% | 11.8% | 25.1% | 4.80x | 40.7x | 10-Q Jul-26, 10-K FY26 [P2] |
| Twilio | 46,916 | 5,572.3 | 17.8% | 7.1% | 25.0% | 8.42x | 117.8x | 10-Q Jun-26, 10-K FY25 [P6] |
| Box | 6,318 | 1,234.1 | 9.6% | 9.2% | 18.8% | 5.12x | 55.5x | 10-Q Jul-26, 10-K FY26 [P5] |
| **Peer quartiles (Q1 / median / Q3)** | | | 9.6 / 13.3 / 17.9% | 9.2 / 14.9 / 17.6% | | **4.96 / 6.37 / 9.42x** | **32.5 / 55.5 / 75.7x** | |

*Revenue is fact (GAAP, filed); TTM, growth, margins, EV and multiples are estimates (derived; formulas in Exhibit A). EV = price × fully diluted shares + debt − cash and investments. FCF after SBC = OCF − capex − capitalized software − SBC.*

**Exhibit 2. Methods: value per HubSpot share (estimates; `comps.py`, numbers not edited)**

| Method | Multiple applied | Value/share | vs $228.30 |
|---|---|---:|---:|
| Median EV/FCF after SBC × HubSpot TTM FCF after SBC ($143.7M) | 55.5x | **$178.48** | −22% |
| Median EV/revenue × HubSpot TTM revenue ($3,449.0M) | 6.37x | **$445.32** | +95% |
| Rule-of-40 regression at HubSpot's 25.3% score | 7.23x fitted | **$502.00** | +120% |
| *Range used (basis: methods)* | | ***$178–$502*** | |
| *Inter-quartile, EV/FCF lens (illustrative)* | 32.5–75.7x | *$116–$234* | |
| *Inter-quartile, EV/revenue lens (illustrative)* | 4.96–9.42x | *$353–$646* | |

**Why "methods" and not the regression band.** The rule-of-40 fit has r² = 0.03 (gate flag: weak fit), far below the skill's 0.3 threshold, so the ±1-residual band ($270–$734) means nothing here. Growth alone explains a little (r² 0.14). Margin alone explains nothing (r² 0.00). In this set, the market is not paying for rule-of-40 scores. Okta (26.1% score, 13.0x) and DocuSign (26.2% score, 4.3x) have the same score and multiples three times apart. So I lean on the plain medians, as the gate flag says. They disagree by 2.8x, which is far outside the charter's 30% tolerance, and **I have not averaged them**. HubSpot's score (25.3%) is inside the peer range (18.8%–45.3%), so the regression is not extrapolating. That is moot given the fit.

1. **HubSpot trades below every peer on revenue and above the median on cash. The market prices it on cash.** At 3.07x EV/revenue, HubSpot is cheaper than DocuSign (4.28x), which grows 8.6% to HubSpot's 21.1%. At 73.6x EV/FCF after SBC, it sits just under the peer upper quartile (75.7x). At 16.1x EV/FCF *before* SBC, it is just under the peer median (18.1x, which would imply $253; illustrative). Read together, investors treat HubSpot's revenue as worth less than peers' because less of it turns into cash.
2. **The margin gap is 10.7 points, and SBC explains none of it.** FCF after SBC is 4.2% at HubSpot against a peer median of 14.9%. Decomposed against peer medians: SBC/revenue 14.9% vs 16.2% (HubSpot better by 1.3 points); FCF before SBC 19.1% vs 31.1% (HubSpot 12.0 points worse). Within the pre-SBC gap, capex plus capitalized software is 5.7% vs 2.3% (about 3.4 points; HubSpot capitalizes $139M of software a year, 4.0% of revenue), and OCF margin is 24.8% vs 32.1% (about 7.3 points). This corrects the skill's prior that a heavy-SBC target is penalized for SBC. Here the issue is the operating cash margin.
3. **HubSpot's growth premium is real today but fading.** TTM growth of 21.1% is second only to ServiceNow (22.2%) and well above the peer median of 13.3%. But Q3 2026 guidance is +14% (Module 01), about the peer median. At 14% growth and today's margin, HubSpot's rule-of-40 score would be about 18%, below every peer, and the (weak) regression would give $471 (illustrative, extrapolating). Peers do not reward growth reliably here: ServiceNow (22%) gets 10.4x, but Okta (11%) gets 13.0x.
4. **Main reason HubSpot deserves a *lower* revenue multiple than the median peer: it converts far less revenue into owner cash** (4.2% vs 14.9% after SBC), and its growth edge is converging to the peer median. Against that, the after-SBC margin is expanding fast (−8.4% FY2023 → 4.2% TTM; Module 01). Each point of margin moved toward peers adds $34.5M of FCF, about **$37 per share at the median 55.5x** (illustrative). The upside case on peers is a margin story, not a growth story.
5. **The range is robust to the judgment calls; its width is not.** Excluding Twilio (the closest rule-2 call): $158–$485. Valuing peers' shares on GAAP-diluted counts instead of the full-RSU basis used for HubSpot: $165–$476. Neither moves the answer's shape: a cash lens of about $160–$180 and a revenue lens of $400+.

## Escalations to the EM

1. **The peer lenses disagree by 2.8x ($178 vs $502), so this module cannot cross-check the DCF with a single number.** For the DCF comparison, I suggest reading the cash lens (median to upper quartile, $178–$234) as the like-for-like check, because it is the same FCF-after-SBC definition the DCF discounts. The revenue lens ($353–$646 inter-quartile) is what HubSpot would be worth *if* it reached peer cash margins. If the DCF lands well above about $250, it is assuming that convergence, and the EM should check that it says so.
2. **Not against the storyline as far as I can see, but it sharpens it** (I haven't read `engagement.md`, per the brief). At $228.30 the market pays near the median peer cash multiple and the lowest revenue multiple in the set. Peers give no sign that the stock is mispriced on today's cash flow. Any argument that it is undervalued rests on margin expansion.
3. **Material items the brief didn't ask about.** (a) ServiceNow spent $8.8B on acquisitions in H1 2026 (goodwill +$6.3B, including Armis). Its EV includes these, but its TTM revenue includes only post-close revenue, so its 10.4x is modestly overstated. (b) Autodesk closed MaintainX after its 31 Jul balance sheet, using cash. EV and revenue are both pre-deal, so they are consistent. (c) Box's KKR Series A preferred ($500M, converts at $27.00) is in the money at $36.39 and is counted as 18.5M shares. (d) Okta's 13.0x follows a large 2026 rally. I verified the price at two sources and found no takeover news.

## Assumptions and method

| Choice | Value | Why |
|---|---|---|
| Peer set | 7 of 20 candidates (Exhibit 3) | EM's rules applied mechanically on latest filings. None added or dropped otherwise. |
| Price date | Close 9 Oct 2026 for all, same as the HubSpot pin | Last close before the as-of date. Yahoo chart API matched by stockanalysis.com for all 8 tickers. |
| TTM | Latest FY + current YTD − prior YTD, from SEC XBRL | Skill rule. The same code reproduces Module 01's HubSpot revenue, OCF, capex, capitalized software and SBC exactly. |
| FCF after SBC | OCF − capex − capitalized software − SBC | Engagement definition. Capitalized software is a separate line at Box, Twilio and Okta. DocuSign includes it in PP&E purchases. Autodesk, Workday and ServiceNow show none. |
| Peer shares | Period-end basic + all unvested RSUs/PSUs + in-the-money options (TSM at 9 Oct price) + in-the-money convertible preferred | Same basis as HubSpot's pin (basic + all RSUs). Twilio and Okta RSU counts come from their latest 10-Ks (Dec-25, Jan-26), because their 10-Qs don't disclose them. GAAP-diluted alternative in Support 5. |
| Cash | Cash + marketable or short- and long-term investments | Matches HubSpot's pin. Strategic, non-marketable and equity-method investments excluded. |
| Debt | Borrowings and notes at balance-sheet carrying value, including converts | Leases excluded, as for HubSpot. Box's $460M converts are out of the money ($43.46 conversion), so treated as debt. |
| Forward multiples | Not used | No free consensus source I could cite at grade B. Trailing figures throughout, per brief. |
| Range basis | Methods ($178–$502) | r² 0.03 < 0.3 (skill rule) |

## Confidence

**Low** for the value range, because the methods disagree by 2.8x and the growth adjustment explains about 3% of the multiple spread. The inputs themselves are **high** (filed, reproduced and cross-checked). **Top two things that would change the answer:** (1) **HubSpot's FCF-after-SBC margin.** It drives the cash lens linearly, at about $37 a share per point at the median multiple. Q3 2026 results (early November) and the restructuring savings will move it. (2) **The peer set's high-multiple names.** Okta (13.0x) and ServiceNow (10.4x) set the upper quartile of the revenue lens. A rule tweak that removed either (none is proposed) would pull the median EV/revenue to 5.74x ($404); removing both would give 5.12x ($363). The cash lens moves far less.

## Open issues and gaps

- **Data age:** Twilio and Okta RSU counts are 5–6 months old (10-K). Autodesk reports shares in whole millions. Options at Autodesk, Workday and DocuSign are immaterial and use older disclosures. Total effect on any peer's EV is under 2%.
- **Twilio (rule 2)** is a judgment: 75% of revenue is usage fees on its cloud platform. I read "cloud software" to include usage-priced cloud platforms, because the EM's list carries Snowflake and Datadog. The ex-Twilio view is in Support 5. EM to confirm.
- **DocuSign (8.6%) and Box (9.6%)** pass the 8% growth floor narrowly. **Zscaler (25.4%) and ServiceNow ($14.73B)** sit just outside and just inside rule limits. All were recorded as computed, with no rounding to pass or fail.
- **Skill notes for the EM:** `benchmarking` is a full skill (not a stub). Its SBC caveat assumes the target's gap is SBC. Here it isn't, so the memo answers "how much is SBC" with "none".
- **Confidentiality check: pass.** All sources are public: SEC EDGAR filings (XBRL and documents) and public market prices. There is no client-confidential or other-client material. I did not read `engagement.md`, Modules 02/03, `log.md`, the earlier engagement, `docs/engagements/` or `docs/HANDOVER.md`.

**Quantities later work will need:** Exhibit 1 multiples and quartiles; the three method values; HubSpot's current EV ($10,580M), EV/revenue (3.07x) and EV/FCF after SBC (73.6x); the margin decomposition (Support 2).

---

## Exhibit 3. Selection record (rules set by the EM before any multiple was seen)

Rules: (1) files 10-K and 10-Q with the SEC; (2) most revenue is subscription or cloud software; (3) sells mainly to businesses; (4) TTM revenue $1B–$15B; (5) TTM revenue growth 8%–25%. TTM to each company's latest 10-Q/10-K; growth is TTM over prior-year TTM.

| Candidate | Decision | Deciding figure |
|---|---|---|
| Salesforce (CRM) | Excluded, rule 4 | TTM revenue $43.9B (Jul-26) > $15B |
| Adobe (ADBE) | Excluded, rule 4 | $26.0B (Aug-26) > $15B |
| Intuit (INTU) | Excluded, rule 4 | $21.4B (FY Jul-26) > $15B |
| Autodesk (ADSK) | **Included** | $7.79B; +17.9%; subscription 95% of Q2 revenue; B2B |
| Workday (WDAY) | **Included** | $10.16B; +13.3%; subscription 93%; enterprise |
| ServiceNow (NOW) | **Included** | $14.73B (< $15B); +22.2%; subscription 97%; enterprise |
| Atlassian (TEAM) | Excluded, rule 5 | +26.0% ($6.57B vs $5.22B, FY Jun-26) > 25% |
| Datadog (DDOG) | Excluded, rule 5 | +31.5% ($3.97B vs $3.02B) |
| Snowflake (SNOW) | Excluded, rule 5 | +32.0% ($5.43B vs $4.12B) |
| Zoom (ZM) | Excluded, rule 5 | +5.0% ($4.99B vs $4.75B) < 8% |
| DocuSign (DOCU) | **Included** | $3.36B; +8.6%; subscription 98%; businesses of all sizes |
| Dropbox (DBX) | Excluded, rule 5 | −0.0% ($2.532B vs $2.533B) |
| Box (BOX) | **Included** | $1.23B; +9.6%; practically all subscription; enterprise |
| Twilio (TWLO) | **Included** (rule 2 by judgment) | $5.57B; +17.8%; 75% usage fees on its cloud platform, 25% subscription; B2B |
| Klaviyo (KVYO) | Excluded, rule 5 | +28.9% ($1.39B vs $1.08B) |
| Freshworks (FRSH) | Excluded, rule 4 | $0.90B < $1B |
| Sprout Social (SPT) | Excluded, rule 4 | $0.48B < $1B |
| monday.com (MNDY) | Excluded, rule 1 | Files 20-F (13 Mar 2026) and 6-K, not 10-K/10-Q |
| Zscaler (ZS) | Excluded, rule 5 | +25.4% ($3.35B vs $2.67B, FY Jul-26) > 25% |
| Okta (OKTA) | **Included** | $3.07B; +11.2%; subscription 98%; B2B |

Seven pass (at least 5 required). Boundary cases (Atlassian, Zscaler, ServiceNow) were re-pulled through the EDGAR MCP from the 10-K, independently of the bulk XBRL download. They tie.

## Exhibit A. Fact base (peer inputs with lineage; $ millions unless stated)

**Source key.** Grades per `source-vetting`: 10-K A; 10-Q A−; prices B.

| Key | Company | Latest filing (balance sheet, current YTD) | Other filings used for the FY and prior-year YTD figures (latest filing reporting each period, per SEC XBRL) |
|---|---|---|---|
| P1 | Autodesk | 10-Q 31 Jul 2026, https://www.sec.gov/Archives/edgar/data/769397/000076939726000061/adsk-20260731.htm | 0000769397-26-000015; 0000769397-25-000117 |
| P2 | Workday | 10-Q 31 Jul 2026, https://www.sec.gov/Archives/edgar/data/1327811/000132781126000044/wday-20260731.htm | 0001327811-26-000014; 0001327811-25-000184 |
| P3 | ServiceNow | 10-Q 30 Jun 2026, https://www.sec.gov/Archives/edgar/data/1373715/000137371526000076/now-20260630.htm | 0001373715-26-000007; 0001373715-25-000276 |
| P4 | DocuSign | 10-Q 31 Jul 2026, https://www.sec.gov/Archives/edgar/data/1261333/000126133326000099/docu-20260731.htm | 0001261333-26-000021; 0001261333-25-000132 |
| P5 | Box | 10-Q 31 Jul 2026, https://www.sec.gov/Archives/edgar/data/1372612/000119312526368289/box-20260731.htm | https://www.sec.gov/Archives/edgar/data/1372612/000119312526098466/box-20260131.htm; 0000950170-25-111701 |
| P6 | Twilio | 10-Q 30 Jun 2026, https://www.sec.gov/Archives/edgar/data/1447669/000144766926000092/twlo-20260630.htm | https://www.sec.gov/Archives/edgar/data/1447669/000144766926000021/twlo-20251231.htm; 0001447669-25-000122 |
| P7 | Okta | 10-Q 31 Jul 2026, https://www.sec.gov/Archives/edgar/data/1660134/000166013426000069/okta-20260731.htm | https://www.sec.gov/Archives/edgar/data/1660134/000166013426000020/okta-20260131.htm; 0001660134-25-000157 |
| PX | Prices | Close 9 Oct 2026: Yahoo Finance chart API (query1.finance.yahoo.com/v8/finance/chart/{ticker}), matched to the cent by stockanalysis.com/stocks/{ticker}/history | grade B |
| T | HubSpot | Module 01 Exhibit A and engagement.json pins. TTM re-derived here and ties. | |

**A1. TTM flows (Derived = FY + YTD − prior YTD; GAAP; grade A/A−)**

| Company | TTM end | Revenue | Prior TTM | Growth | OCF | Capex | Cap. software | SBC | FCF | FCF after SBC | Margin |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Autodesk | Jul-26 | 7,790.0 | 6,605.0 | 17.9% | 2,896.0 | 57.0 | 0 | 706.0 | 2,839.0 | 2,133.0 | 27.4% |
| Workday | Jul-26 | 10,155.0 | 8,959.0 | 13.3% | 3,081.0 | 237.0 | 0 | 1,646.0 | 2,844.0 | 1,198.0 | 11.8% |
| ServiceNow | Jun-26 | 14,732.0 | 12,057.0 | 22.2% | 5,308.0 | 728.0 | 0 | 2,185.0 | 4,580.0 | 2,395.0 | 16.3% |
| DocuSign | Jul-26 | 3,361.2 | 3,095.4 | 8.6% | 1,323.7 | 125.4¹ | incl.¹ | 606.2² | 1,198.3 | 592.1 | 17.6% |
| Box | Jul-26 | 1,234.1 | 1,125.7 | 9.6% | 394.5 | 5.3 | 39.5 | 235.7 | 349.7 | 113.9 | 9.2% |
| Twilio | Jun-26 | 5,572.3 | 4,729.4 | 17.8% | 1,060.7 | 10.9³ | 61.2 | 590.3 | 988.6 | 398.3 | 7.1% |
| Okta | Jul-26 | 3,073.0 | 2,763.0 | 11.2% | 987.0 | 8.0 | 18.0 | 503.0 | 961.0 | 458.0 | 14.9% |
| HubSpot (check) | Jun-26 | 3,449.0 | 2,847.9 | 21.1% | 856.4 | 58.9 | 139.1 | 514.7 | 658.4 | 143.7 | 4.2% |

¹ DocuSign reports capitalized software within "purchases of property and equipment". ² DocuSign's SBC expense (`AllocatedShareBasedCompensationExpense`); it has no separate cash-flow tag. ³ Twilio's "purchases of long-lived assets". Box's capitalized software is tagged `PaymentsToAcquireIntangibleAssets` ("Capitalized software costs" on its cash-flow statement). Examples of the formula: Autodesk revenue 7,206 + 3,980 − 3,396; ServiceNow OCF 5,444 + 2,257 − 2,393.

**A2. EV bridge inputs (balances at the 10-Q date; prices 9 Oct 2026)**

| Company | Price (B) | Fully diluted shares (M; estimate) | Composition | Cash & investments (A−) | Debt (A−) |
|---|---:|---:|---|---:|---:|
| Autodesk | 235.35 | 214.413 | 209.0 basic + 5.413 RSUs/PSUs | 4,357 (4,098 + 57 + 202) | 3,478 (ST debt 994 + current notes 499 + LT notes 1,985) |
| Workday | 186.59 | 263.574 | 241.175 + 22.315 RSUs/PSUs + 0.084 options (TSM) | 3,403 (661 + 2,742) | 2,989 (999 + 1,990) |
| ServiceNow | 140.86 | 1,083.864 | 1,033.862 + 46.824 RSUs + 3.178 options (7.339M at $79.87, TSM) | 6,707 (2,503 + 2,161 + 2,043) | 7,517 (ST 2,082 + LT 5,435) |
| DocuSign | 71.08 | 216.257 | 188.176 + 28.018 RSUs + 0.063 options | 973.1 (528.2 + 249.5 + 195.4) | 0 |
| Box | 36.39 | 173.398 | 137.201 + 17.219 RSUs + 0.459 options + 18.519 Series A as-converted ($500M / $27.00) | 444.1 (342.9 + 101.3) | 452.2 (2029 converts, carrying; principal 460) |
| Twilio | 289.47 | 167.821 | 153.572 + 13.664 RSUs (Dec-25, 10-K) + 0.585 options (0.902M at $101.75) | 2,656.3 (823.3 + 1,833.1) | 993.2 (2029/2031 senior notes) |
| Okta | 232.13 | 182.145 | 174.817 (A+B) + 6.758 RSUs incl. market-based (Jan-26, 10-K) + 0.570 options (1.07M at $108.43) | 2,299 (763 + 1,536) | 0 (converts repaid 15 Jun 2026) |
| HubSpot (pins) | 228.30 | 52.403 | 49.658 + 2.745 RSUs/PSUs | 1,383.2 | 0 |

Excluded from cash: strategic, non-marketable and equity-method investments (Autodesk $392M, Workday $231M, ServiceNow $2,073M, Twilio $251M). Operating leases are excluded from debt for all companies, as for HubSpot. Machine-readable inputs and computed multiples are in `valuation.json`.

## EM review (2026-10-12)

**Verdict: accepted.** Receipt check: `ready_to_review`, no problems; pinned HubSpot inputs match. Verifier flag (weak rule-of-40 fit, r² 0.03): addressed in the memo.

Re-pulled / re-computed by the EM:
- Spot check, HubSpot row: EV 228.30 × 52.403 − 1,383.2 = 10,580.4; 3.07x revenue; 73.6x FCF after SBC ✓.
- Spot check, peer quartiles: recomputed from the seven peers' EV, revenue and FCF. EV/revenue 4.96 / 6.36 / 9.42x and EV/FCF 32.5 / 55.5 / 75.7x ✓ (inclusive quartiles). Growth 9.6 / 13.3 / 17.9% and margin 9.2 / 14.9 / 17.6% ✓ but on the exclusive method: two quartile conventions in one table. Medians, which drive every value, are identical either way; noted, not material.
- Spot check, Okta: TTM revenue 2,919 − 1,416 + 1,570 = $3,073M (EDGAR XBRL) ✓; close $232.13 on 9 Oct 2026 (Yahoo chart API) ✓; 13.01x / 87.3x ✓. Autodesk close $235.35 ✓.
- Values: median EV/revenue → $445; median EV/FCF after SBC → $178.47 ✓.

**EM correction (form, in the open):** the memo's range high ($502) is the rule-of-40 regression, which the memo itself rejects (r² 0.03). The engagement answer therefore reports the two peer lenses separately (revenue $445, cash $178) and does not use the $502 regression value as a bound. No figure is changed.

**Escalations:** (1) cash lens as the like-for-like check: agreed for synthesis, with the revenue lens shown beside it. (2) ServiceNow acquisitions, (3) Box preferred as-converted, (4) Okta rally: accepted as handled; Twilio exclusion sensitivity ($158–$485) noted.
