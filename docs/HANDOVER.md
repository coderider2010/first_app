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

## Build order (from the brief; superseded by PROJECT_PLAN.md)

1. Fact-base MVP.
2. Hooks for the verifier and for confidentiality.
3. Fill the `interview-synthesis` and `model-build` skill bodies.
4. Package `diligence-pack`.
5. Run a full simulated engagement before any real client data.
