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

1. **`market-sizing/scripts/sniff_test.py` is missing.** The brief calls it "runnable and
   tested", but the zip has no scripts. It must be recovered from the original chat or
   rewritten.
2. **Skills live at `agents/associate/skills/`, not a top-level `skills/`.** The plugin
   format expects `skills/` at the plugin root, so they need to move when packaging.
3. **No plugin scaffolding yet:** no `.claude-plugin/plugin.json`, `commands/`,
   `.mcp.json`, or hooks.

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

## Build order (from the brief)

1. Fact-base MVP.
2. Hooks for the verifier and for confidentiality.
3. Fill the `interview-synthesis` and `model-build` skill bodies.
4. Package `diligence-pack`.
5. Run a full simulated engagement before any real client data.
