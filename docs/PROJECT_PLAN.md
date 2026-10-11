# Project plan: Analyst Agent app

**Goal:** a production web app, used by one person (the user, acting as Partner), that runs
an engagement end to end and can be demoed. The demo case is
[Project Hub](engagements/hubspot-value.md): what is HubSpot worth per share?

## Decisions (2026-10-10)

| Decision | Choice |
|---|---|
| Demo engagement | What is HubSpot worth per share? Standalone value only (narrowed from a buy-side deal question) |
| Users | The user only, for now |
| Data | Free sources only (SEC EDGAR, company IR, web) |
| Runtime | Claude Agent SDK, self-hosted backend |

## Phases

Each phase ends with something the user can see and test.

### Phase 1: The engagement, top-down
- Engagement document: client, key question, working answer, modules. *(Done.)*
- Briefs for the four modules: fact pack, what the price implies, DCF scenarios, peer
  comparison. *(Done: `docs/engagements/hubspot-value/briefs/`.)*

**Done when:** the user approves the engagement document and the four briefs. ✅ 2026-10-10

### Phase 2: Data access (free sources)
- Open the network to `sec.gov` and `data.sec.gov` (SEC EDGAR filings and XBRL data). *(Done.)*
- An EDGAR connector (MCP server) that fetches filings and XBRL facts and returns them with
  source links. *(Built: `connectors/edgar/`.)*
- `SEC_USER_AGENT` set in the environment, then the Analyst tested in a new session. *(Done.)*
- Brief 01 (fact pack) run by the Analyst on live EDGAR data and accepted by the EM.
  *(Done: `engagements/hubspot-value/modules/01-fact-pack/memo.md`.)*
- Connector fixes from that run (see HANDOVER, "Connector backlog"). *(Open; not blocking.)*

**Done when:** the Analyst quotes HubSpot's latest revenue from the 10-K, with a link. ✅ 2026-10-11

### Phase 3: The Analyst's curriculum for Project Hub
- New skills: `implied-expectations` *(done)*, `valuation-dcf` *(done; module 3 run 2026-10-11)*.
- Finish the stubs: `company-profile` *(open)*, `benchmarking` *(done)*, and the closing four
  (`module-memo`, `fact-base-contribution`, `confidentiality-check`, `source-vetting`)
  *(done)*.
- A valuation checker (like `sniff_test.py`) that catches classic DCF errors, wired into
  the gate. *(Done: `valuation_check.py` handles reverse DCF and two-story DCF.)*
- Skill fixes from the module 2 and 3 runs (HANDOVER backlogs). *(Module 2's mostly done; module 3's open.)*
- Fixes from the first run: benchmark ranges come from the brief, not the Analyst, and
  methods must cite independent sources.
- Add a fully diluted share count to Brief 02. *(Done.)*

**Done when:** module 2 ("what the price implies") passes the gate on real filing data. ✅ 2026-10-11 (remaining items above are
for modules 3 and 4)

### Phase 4: The Engagement Manager as an agent
- The EM turns the key question into modules and briefs.
- It accepts modules only after checking the receipt.
- It pauses for Partner approval of the plan and of the final answer.

**Done when:** the user asks "What is HubSpot worth?", approves a plan, and gets back a
value range built from Analyst modules.

### Phase 5: Fact base MVP
- One record per number: value, definition, source and history. Analysts write to it; the
  EM and the gates read from it.

**Done when:** a HubSpot figure used in two modules comes from one record.

### Phase 6: The app
- Backend on the Claude Agent SDK, running the EM and Analyst with the same charters, skills
  and gate. First step: a small spike to confirm the gate hook works unchanged.
- Storage for engagements and module outputs, replacing the temporary `engagements/` folder.
- Screens: engagement list, engagement page, module page (memo, sources, receipt, flags),
  final answer.
- Login for one user, live progress while agents work, a spending cap per engagement.

**Done when:** the user starts and follows an engagement from a web link, without Claude Code.

### Phase 7: Demo-ready
- A pre-run Project Hub engagement, a 10-minute demo script, a small test set to measure
  quality, and the measured cost per engagement.

**Done when:** the user can demo it to someone new in 10 minutes.

### Later
Plugin packaging, multi-client confidentiality enforcement, more engagement types, more
users, and possibly moving to Managed Agents.
