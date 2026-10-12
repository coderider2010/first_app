# CLAUDE.md

This repo builds the **Analyst Agent** ("Associate") for an AI-native professional-services
firm. Read `docs/HANDOVER.md` first: it holds the goal, architecture, decisions, known gaps,
and build order. The current plan is `docs/PROJECT_PLAN.md`; the demo engagement is
`docs/engagements/hubspot-value.md`.

- Charters: `agents/associate/AGENTS.md` (Analyst) and `agents/engagement-manager/AGENTS.md` (EM).
- To run an engagement end to end, the main session acts as the EM via the `/engagement` skill
  (`.claude/skills/engagement/SKILL.md`); subagents can't launch subagents, so the EM can't be one.
- Skills: `agents/associate/skills/*/SKILL.md`. Stubs are marked `STATUS: STUB`.
- Keep `docs/HANDOVER.md` current when decisions change, so the next session starts with context.

The user is here to learn: explain reasoning, prefer more explanation over less, and use analogies.
