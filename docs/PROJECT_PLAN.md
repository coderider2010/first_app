# Project plan: Analyst Agent app

**Goal:** a production web app, used by one person (the user, acting as Partner), that runs
an engagement end to end and can be demoed. The demo case is
[Project Hub](engagements/hubspot-acquisition.md): should a client buy HubSpot, and at
what price?

## Decisions (2026-10-10)

| Decision | Choice |
|---|---|
| Demo engagement | Buy-side: should the client acquire HubSpot, and what is the walk-away price? |
| Users | The user only, for now |
| Data | Free sources only (SEC EDGAR, company IR, web) |
| Runtime | Claude Agent SDK, self-hosted backend |

## Phases

Each phase ends with something the user can see and test.

### Phase 1: The engagement, top-down
- Engagement document: client, key question, working answer, workstreams. *(Drafted.)*
- Briefs for the Analyst's first workstream (WS1, standalone value).

**Done when:** the user approves the engagement document and the WS1 briefs.

### Phase 2: Data access (free sources)
- Open the network to `sec.gov` and `data.sec.gov` (SEC EDGAR filings and XBRL data), plus
  HubSpot's investor relations site.
- An EDGAR connector (MCP server) that fetches filings and XBRL facts and returns them with
  source links.

**Done when:** the Analyst quotes HubSpot's latest revenue from the 10-K, with a link.

### Phase 3: The Analyst's curriculum for WS1
- New skills: `implied-expectations`, `valuation-dcf`, `precedent-transactions`.
- Finish the stubs: `company-profile`, `benchmarking`, and the closing four
  (`module-memo`, `fact-base-contribution`, `confidentiality-check`, `source-vetting`).
- A valuation checker (like `sniff_test.py`) that catches classic DCF errors, wired into
  the gate.
- Fixes from the first run: benchmark ranges come from the brief, not the Analyst, and
  methods must cite independent sources.

**Done when:** module 1b ("what the price implies") passes the gate on real filing data.

### Phase 4: The Engagement Manager as an agent
- The EM turns the key question into a hypothesis tree, workstreams and briefs.
- It accepts modules only after checking the receipt.
- It pauses for Partner approval of the plan and of the recommendation.

**Done when:** the user asks the key question, approves a plan, and gets back a draft
recommendation built from Analyst modules.

### Phase 5: Fact base MVP
- One record per number: value, definition, source and history. Analysts write to it; the
  EM and the gates read from it.

**Done when:** a HubSpot figure used in two modules comes from one record.

### Phase 6: The app
- Backend on the Claude Agent SDK, running the EM and Analyst with the same charters, skills
  and gate. First step: a small spike to confirm the gate hook works unchanged.
- Storage for engagements and module outputs, replacing the temporary `engagements/` folder.
- Screens: engagement list, engagement page, module page (memo, sources, receipt, flags),
  recommendation.
- Login for one user, live progress while agents work, a spending cap per engagement.

**Done when:** the user starts and follows an engagement from a web link, without Claude Code.

### Phase 7: Demo-ready
- A pre-run Project Hub engagement, a 10-minute demo script, a small test set to measure
  quality, and the measured cost per engagement.

**Done when:** the user can demo it to someone new in 10 minutes.

### Later
Plugin packaging, multi-client confidentiality enforcement, more engagement types, more
users, and possibly moving to Managed Agents.
