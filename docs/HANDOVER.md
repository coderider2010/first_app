# Analyst Agent — Handover Notes

Source of truth for design intent: the "Analyst Agent — Developer Handover Brief"
(claude.ai/artifact/4uRrzzTi664fHssm1fmuAb), written 2026-09-26. This file summarizes it
and records how the repo differs from it.

## Goal

Build the Analyst Agent ("Associate"): it takes a structured **module brief** from an
Engagement Manager (EM) and returns verified, client-ready analysis, with every number
traceable to a source. Roles: Analyst owns *truth*, EM owns *storyline*, Partner (human)
owns *relationship and commitment*. The Analyst never talks to a client.

The value is not the analysis itself but doing it with a firm's discipline:
triangulation, source lineage, escalation, and mechanical verification.

## Architecture (from the brief)

- **Claude Agent SDK / Claude Code plugin format.**
- **Progressive disclosure:** skill descriptions are the router and always sit in context.
  Skill bodies load on invocation, `references/` load on demand, and `scripts/` execute
  without ever entering context.
- **Three control layers:** culture (`AGENTS.md`) → curriculum (skills) → enforcement
  (hooks). Rules graduate toward hooks as they prove out.
- **Subagents per role:** fresh context per spawn, which enables clean-room replication.
- **Data via MCP:** EDGAR, market databases, expert transcripts, and the firm **fact base**.
- **Packaging:** the `diligence-pack` plugin (`.claude-plugin/plugin.json`, `agents/`,
  `skills/`, `commands/`, `.mcp.json`).

## What is in the repo (imported from `ai-consulting-firm.zip`)

- `agents/associate/AGENTS.md`: the Analyst charter.
- `agents/engagement-manager/AGENTS.md`: the EM charter.
- `agents/associate/skills/`: 22 skills. Four are complete (`market-sizing`,
  `ghost-deck`, `driver-tree`, `data-room-analysis`) and 18 are `STATUS: STUB`.

## Gaps between the brief and the zip

1. **`market-sizing/scripts/sniff_test.py` was missing from the zip.** It is now restored
   from the original chat, verbatim. Its original tests were not recovered, so new ones
   were written in `tests/test_sniff_test.py` (run: `python3 -m unittest discover tests -v`).
   The only change from the original is a fix: a `per_capita.population` of 0 or less now
   reports an error instead of crashing.
2. **Skills live at `agents/associate/skills/`, not a top-level `skills/`.** The plugin
   format expects `skills/` at the plugin root, so they need to move when packaging.
3. **No plugin scaffolding yet:** no `.claude-plugin/plugin.json`, `commands/`, or
   `.mcp.json`. The verifier hook exists as project config (below) and must move into
   the plugin's `hooks/hooks.json` when packaging.

## Submission gate (built 2026-09-28)

The Associate cannot finish a module with broken numbers. The pieces:

- `.claude/agents/associate.md`: subagent definition. It points at the charter and
  defines the module folder protocol.
- `.claude/hooks/verify_module.py`: runs on `SubagentStop` for `agent_type: associate`
  (registered in `.claude/settings.json`).
- `tests/test_verify_module_hook.py`: 13 tests.

Protocol: each module lives in `engagements/<eng>/modules/<id>/` (`brief.md`, `memo.md`,
optional `sizing.json`). The Associate ends its final message with `MODULE: <that path>`.
The gate blocks (exit 2, with feedback to the Associate) if the line is missing, the path
is not a module folder, `memo.md` is missing, or `sniff_test.py` reports `errors_found`.
Flags do not block; the verdict is saved to `sniff_result.json` for the EM. Escape valve:
an `escalation.md` in the folder lets the Associate stop, handing the problem to the EM,
so the gate can never trap it in a loop.

Decisions: gate on finishing, not on writing `memo.md`, so drafting is never blocked.
Flags stay advisory until the simple gate proves out. `engagements/` is git-ignored
because it will hold client data.

Verified live on 2026-09-28. A real `associate` subagent submitted a sizing with its
estimate outside the method range. The gate blocked it and quoted the error. The
Associate corrected the estimate and resubmitted, and the gate passed it
(`sniff_result.json`: `pass`).

Finding from that run: the Associate's first report reached the parent *before* the gate
ran, and it said nothing had blocked it. The correction arrived later as a separate
message. The gate guarantees the files end up correct, not that the first message is
final. Rule for the EM (to add to its charter): accept a module only by reading its
folder, and treat `sniff_result.json` with status `pass` or `flags_found` as the receipt.
Never act on the Associate's message alone.

The gate only protects sizing modules; other module types have no verifier yet.

## First real run (2026-09-28): US pet insurance, screening grade

The Associate returned $6.5B for 2026 (range $5.8–7.3B), with about 13% CAGR to 2031. The
gate passed it with no flags. It was accepted for screening, but it is not client-ready.
Lessons:

- **Network egress blocks source pages** (NAPHIA, AVMA, dvm360, SEC EDGAR, Trupanion).
  Figures came from search summaries only. The fix is to widen Network access in the
  cloud environment settings, then re-verify.
- **Method independence is not checked.** Two of the three methods both rested on NAPHIA.
  The verifier cannot see shared inputs. Candidate rule: each method records its sources,
  and the gate flags methods that share one.
- **The Associate chose its own `per_capita` anchors,** so the check can be gamed. Anchors
  should come from the EM's brief or the fact base.
- **The curriculum-gap mechanism worked.** The Associate flagged four stub skills it
  needed: `module-memo`, `fact-base-contribution`, `confidentiality-check` and
  `source-vetting`.
- **It caught a scope trap.** "$5.2B" is the North America 2024 figure, not US 2025. This
  is an early candidate for the fact base.

## Open questions (from the brief)

1. Fact-base design: version control for facts (supersede vs. fork, conflicts, locks,
   provenance). This is the biggest unbuilt piece.
2. Brief neutrality: does naming the hypothesis branch steer the agent? The proposed fix
   is paired sighted and blind runs.
3. Who audits the EM? Possibly a fourth role.
4. Compute P&L: who owns the spend on disconfirmation, re-runs, and replications?
5. Autonomy boundary: currently nothing reaches a client without human sign-off.
6. Confidentiality: move it from a skill (advice) to a hook (block) before any
   multi-client use.

## Current direction (2026-10-10)

The user wants a production web app they can use and demo. The plan lives in
`docs/PROJECT_PLAN.md`. Decisions so far: the demo engagement is "What is HubSpot worth
per share?", standalone value only (`docs/engagements/hubspot-value.md`; narrowed
from a buy-side deal question to keep it simple), the user is the only user, data
comes from free sources only, and the runtime is the Claude Agent SDK. Work goes top-down:
engagement first, then the Analyst's workstream, then how the Analyst does the work.

## EDGAR connector (Phase 2, built 2026-10-11)

`connectors/edgar/` is an MCP server (`edgar_mcp`, MCP Python SDK 2.x, registered in
`.mcp.json` as `edgar`) with five read-only tools: `edgar_find_company`,
`edgar_list_filings`, `edgar_search_concepts`, `edgar_get_fact` and `edgar_read_filing`.
Every value carries its filing and a sec.gov link.

- **Setup:** `connectors/edgar/run.sh` creates `.venv/` on first launch. The SEC requires a
  contact in the User-Agent, read from the `SEC_USER_AGENT` environment variable (set in the
  cloud environment's settings, not in the repo). Without it the tools return an error that
  asks for it.
- **Design choice:** XBRL repeats each period in several filings, and a row's `fy` is the
  *filing's* year. `edgar_get_fact` keys on period dates, keeps the latest filing's value,
  and flags `restated` when filings disagree.
- **MCP 2.x notes:** `FastMCP` is now `MCPServer` (`mcp.server.mcpserver`). Only `ToolError`
  messages reach the agent; other exceptions are hidden as "Error executing tool".
- **Verified:** HubSpot FY2025 revenue $3,131,266,000 (10-K filed 2026-02-11). Tests:
  `tests/test_edgar_client.py` (offline).
- `ir.hubspot.com` returns 403 (bot protection on the site). Earnings releases are on
  EDGAR as 8-K exhibits, so this is not a gap.

## Brief 01 fact pack: first run on live data (2026-10-11)

Phase 2 is done. The Associate ran Brief 01 with the EDGAR connector (about 70 tool calls,
6.5 minutes) and passed the gate. The memo is (force-added past the `/engagements/` ignore so it survives)
`engagements/hubspot-value/modules/01-fact-pack/memo.md`. Headline figures: TTM revenue to
June 2026 $3.45B (+21%), GAAP operating margin 3.8%, non-GAAP 20.1%, FCF $658M, $1.38B cash
and investments, no debt, 49.87M shares (2026-07-31).

- **EM check:** headline facts were pulled independently and every derivation recomputed;
  all tie. One wording error was fixed ("~99%" subscription share should be ~98%). The
  Associate's own checks were internally consistent but could not catch a wrong input
  copied in consistently, so the EM's independent re-pull stays part of acceptance.
- **The restatement check worked:** `restated`/`earlier_values` caught the FY2023 revision
  (vendor credits, $7.1M) at once. This is a fact-base candidate.
- **Good judgment unprompted:** it caught the 2025 change in NRR method, the 2026-10-06
  restructuring 8-K ($65–75M, excluded from GAAP guidance), and that guidance implies ~14%
  growth in H2 2026.
- **Gaps:** no fully diluted share count (added to Phase 3); the Analyst Day 2026-09-17
  targets are on IR only; the pack goes stale with Q3 2026 results in early November.
  `company-profile` and the closing trio are still stubs (flagged again).

### Connector backlog (from the Associate's notes, by value)

1. Return exhibit URLs per filing (earnings releases are 8-K Ex. 99.1; it had to guess
   `hubs-ex99_1.htm`).
2. Return 8-K item codes (2.02 results, 2.05 restructuring, 5.02 officers) in `edgar_list_filings`.
3. `edgar_read_filing`: a budget for each keyword (the first keyword used up the whole
   budget) and snippets that include whole tables, not ones cut off before the numbers.
4. `edgar_get_fact`: derived Q4 and a TTM option; `limit` should not let YTD rows push
   out annual history.
5. `edgar_search_concepts`: sort by latest period or hide tags unused since ~2018.
6. Dimensioned facts (subscription vs services split) are not exposed.

## Module 02, what the price implies (2026-10-11)

Phase 3's "done when" is met: module 2 passed the gate on real filing data. Memo:
`engagements/hubspot-value/modules/02-implied-expectations/memo.md`.

- **Answer:** at $228.30 (close 2026-10-09) the market prices in ~9% growth for 10 years
  and a ~17% long-run FCF margin after SBC. That margin is below all four named peers
  (Autodesk 22.5%, Salesforce 26.2%, Intuit 30.6%, Adobe 33.3%). At Autodesk's margin the
  price needs only 5.8% growth. Discount rate 10.5% (CAPM: 5.24% + 1.25 × 4.20%),
  terminal growth 3.0% (cap 4.0%), diluted shares 52.45M, EV $10.66B.
- **This cuts against the working answer** ("price assumes fast growth and rising
  margins"). Escalated to the Partner, who **kept the working answer** (2026-10-11) as the
  hypothesis for Module 3 to test.
  EM note: "undemanding" assumes HubSpot converges to mature peers; Module 3's bear case
  should test non-convergence (for example AI pressure on seat-based software).
- **Built for it:** `implied-expectations` skill with `reverse_dcf.py` (model; implied
  margin is exact because EV is linear in the margin) and `valuation_check.py` (classic
  DCF errors), now run by the gate on `valuation.json`. Closing four skills written.
  Peer set is fixed in the brief, not chosen by the Analyst.
- **EM check:** price, Treasury yield, Adobe peer figures and the model re-run were
  verified independently; all tie.
- **Unverified input:** Analyst Day 2030 targets (30% non-GAAP operating margin, SBC 10%
  of revenue) come from one secondary article; the IR site blocks automated access.

### implied-expectations backlog (from the Associate's notes)

1. Diluted shares fallback order when the 10-Q has no award table: anti-dilutive table +
   dilutive shares, then the 10-K roll-forward, then an estimate.
2. Checker: also flag a margin *below the lowest peer* ("undemanding; check against the
   working answer"), which is the charter's top escalation; check diluted > basic shares;
   ask how the headline growth was chosen.
3. `reverse_dcf.py`: accept a growth path (fade), not only constant growth; produce the
   terminal growth ±0.5 point runs; mention mid-year discounting (~0.8 point lower margins).
4. Skill guidance on debt-like items (leases: don't add; restructuring cash: add) and on
   SBC capitalized into software.
5. Name Damodaran's current ERP page (`New_Home_Page/home.htm`); `implpr.html` stops in 2016.
6. Connector: `edgar_read_filing` missed an exact phrase in the 10-K (likely whitespace).

## Module 03, two stories (2026-10-11)

The Partner replaced bear/base/bull with two stories. Memo:
`engagements/hubspot-value/modules/03-dcf-scenarios/memo.md`.

- **Answer:** Grows up (growth fades 14% → 4%, margin after SBC to 25% by year 7) is worth
  **$343.75**; Squeezed (12% falling to 3% by year 7, margin stalls at 12%) is worth
  **$149.21**. The price of $228.30 sits 41% of the way toward Grows up (25–42% over the
  two-week range). Margin, not growth, separates the stories (swap test: $116–156 vs $39–79).
- **Working answer fails again:** the market accepts ~9% growth but doubts the margin.
  Escalated; the Partner decides at the final checkpoint.
- **Evidence that tells the stories apart:** net adds down (6,988 vs 9,724 a year
  earlier), entry-price cuts, a new FY2025 risk factor on LLMs and vibe coding (verified
  new vs FY2024); against that, seats and credits still growing and NRR ~102% (call,
  unverified). What decides it: Q3 2026 NRR and net adds (early November), gross margin
  vs AI costs, SBC % of revenue.
- **Built:** `valuation-dcf` skill, `dcf.py`, growth paths in the shared model, and the
  `dcf` type in `valuation_check.py` (two sourced evidence items per story, stories-too-
  close and price-outside-both flags). 99 tests.

### valuation-dcf backlog (from the Associate's notes)

1. `dcf.py --write` to merge results into valuation.json (it wrote its own merge script).
2. Print the price's position between stories and a swap test (most useful diagnostic).
3. Optional margin parts (pre-SBC FCF margin, SBC %, capex %) so reinvestment is visible.
4. Say that year 1 starts after the TTM base (H2 2026 + H1 2027), and note mid-year
   discounting (~+5% to values).
5. Evidence grade: require at least one A or B source per story.
6. `dcf` type: optionally carry today's market EV for reference.

## Module 04, peer comparison, and the draft answer (2026-10-11)

All four modules are done. The final answer is `docs/engagements/hubspot-value/answer.md`,
**approved by the Partner on 2026-10-11** (checkpoint 2). Project Hub is complete; next is
Phase 4 (the EM as an agent), which should reproduce this engagement end to end.

- **Module 04:** EM-set rules applied to 20 candidates; 7 peers pass (Autodesk, Workday,
  ServiceNow, DocuSign, Box, Twilio, Okta). On 52.45M shares: $161 (EV/FCF after SBC)
  to $438 (EV/revenue; $324 without Okta and Twilio). Rule-of-40 fit r² 0.05, so the
  range uses the plain medians. HubSpot's FCF gap is before SBC (19% vs 31%), not SBC.
- **The answer:** about $150–$345 per share, hinging on cash conversion; $228 prices in
  roughly a 40% chance HubSpot matures. The DCF and peers, built independently, agree on
  that hinge. The working answer did not survive.
- **EM errors to learn from:** (1) a line on Module 2's result in the engagement doc was
  readable by Module 4 (independent modules should be pointed only at the fact pack);
  (2) Module 4 used 50.6M shares vs 52.45M elsewhere (the fact base, Phase 5, fixes this).
- **Skill loading:** `Skill("benchmarking")` returned "Unknown skill" because associate
  skills live in `agents/associate/skills/`, not a registered skills folder; agents read
  SKILL.md directly. Fix when packaging (Phase 6 or plugin work).

### benchmarking backlog (from the Associate's notes)

1. One rule for the range when r² < 0.3 (skill and checker flag disagree), a
   `--basis methods` option, and a range note field.
2. Compute quartiles and pre-SBC FCF margin and SBC % in `comps.py`.
3. Define the share basis (period-end basic + treasury-stock dilution vs weighted
   diluted) once, engagement-wide.
4. Normalization cases: no capitalized-software line, preferred stock, equity-method
   investments, post-balance-sheet acquisitions, splits, 10-K-latest TTM.
5. Methods-basis check should require the range to equal named method values.
6. Name a free daily-price source (stockanalysis.com and financialcontent.com work);
   document dropping negative-FCF peers from EV/FCF; a field for forward revenue.
7. Brief template: define "cloud software" for usage-based models (Twilio).

## Phase 4: the EM as an agent (built 2026-10-11, test pending)

- **Design:** Claude Code subagents can't launch subagents, so the EM can't be a subagent
  that commissions Associates. The EM is the **main session**, running the `/engagement`
  skill (`.claude/skills/engagement/SKILL.md`). Phase 6's Agent SDK backend can lift this.
- **Playbook:** set up `engagements/<slug>/` (never overwrite) → plan + briefs → Partner
  checkpoint 1 (AskUserQuestion) → commission Associates in dependency order (03 and 04
  in parallel) → receipt check per module → pin shared facts → synthesize `answer.md` →
  Partner checkpoint 2.
- **`engagement.json`:** engagement state plus `pinned` shared facts (shares, cash, debt,
  price and date, discount rate, terminal growth). Facts only, never conclusions, because
  cross-check modules may read it. `log.md` is the EM-only decision log.
- **`em_receipt.py`:** re-runs the gate's verifier, checks the memo's answer and confidence,
  rejects values that differ from the pins, and picks 3 random rows from tables with a
  Source column for the EM to re-pull. Tested (11 tests) and run on the four Project Hub
  modules (all ready_to_review).
- **`module-briefing` skill:** the brief template and the Project Hub lessons (neutral
  questions, EM-set benchmarks, pinned inputs, independence by construction).
- **Test (open):** in a new session, `/engagement What is HubSpot worth per share?`.
  Compare with `docs/engagements/hubspot-value/answer.md` (~$150–$345). Expect a new
  slug such as `hubspot-value-2`.

## Build order (from the brief; superseded by PROJECT_PLAN.md)

1. Fact-base MVP.
2. Hooks for the verifier and for confidentiality.
3. Fill the `interview-synthesis` and `model-build` skill bodies.
4. Package `diligence-pack`.
5. Run a full simulated engagement before any real client data.
