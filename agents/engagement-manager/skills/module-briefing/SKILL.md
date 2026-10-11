---
name: module-briefing
description: Write a module brief for an Associate: the question, the branch it tests, the limits the EM sets, what the Associate may read, and the output the gate checks. Use for every module you commission.
---

# Module briefing

A brief is the EM's code; the Associate executes it. Most rework traces back to a brief
that left a choice open that the EM should have made. Worked examples: the four Project
Hub briefs in `docs/engagements/hubspot-value/briefs/`.

## Template

```
# Brief NN: <title>

**Engagement:** <name> · **From:** EM
**Skill:** `<associate skill>`
**Depends on:** <modules>. **May read:** <exact folders>. **Must not read:** <folders>.

## Question
<One question, phrased so either answer is equally reportable.>

## Why it matters
<The branch of the hypothesis tree it tests, and what decision hangs on it.>

## Method
<The approach, at the level of "reverse DCF" or "peer multiples"; not the answer.>

## Limits set by the EM
<Every judgment call that would otherwise let the result be steered: benchmarks, peer
sets, caps, definitions, pinned inputs. See the rules below.>

## Sources
<Allowed sources; how to date and cite them.>

## Output
<memo.md answer-first sentence form; valuation.json / sizing.json if the gate checks one.>
```

## Rules (each one learned the hard way on Project Hub)

1. **Neutral questions.** State what the module must *test*, never what you hope it
   finds. "What growth does the price imply?", not "Show the price is demanding."
   Share the working answer as context, labelled as a hypothesis.
2. **The EM sets the benchmarks.** Peer sets, comparison ranges and selection rules
   go in the brief, decided before anyone sees the numbers they produce. For a peer
   valuation, give the selection rules *and* a candidate list; the Associate applies
   them and records every decision. (The peer set is the answer.)
3. **Pin shared inputs.** Any quantity two modules use (diluted shares, cash, debt,
   share price and its date, discount rate, terminal growth) is pinned once in
   `engagement.json` and quoted in each brief. The receipt check rejects a module that
   uses a different value. (Project Hub's module 4 used 50.6M shares against 52.45M
   elsewhere.)
4. **Independence by construction.** For a module meant to cross-check another,
   list exactly what it may read: usually only the fact pack and `engagement.json`.
   Keep conclusions out of anything it may read, including the engagement document
   and `engagement.json`. (On Project Hub the EM leaked Module 2's result to Module 4
   through a note in the engagement document.)
5. **Name the gate's file.** If the module's skill has a verifier (`valuation.json`,
   `sizing.json`), the Output section must require that file, so the gate can check it.
6. **Say what to do when a rule can't be met.** "If fewer than 5 peers pass, escalate
   rather than loosening a rule." Otherwise the Associate improvises.
7. **Ask for skill notes.** End the commissioning message (not the brief) with a request
   for a short "Skill notes" section; that is how the curriculum improves.

## Before sending, check the brief against these questions

- Could a motivated Associate steer the answer through any choice this brief leaves open?
- Does any file it may read contain another module's conclusion?
- Is every shared input pinned, with its value in the brief?
- Would either answer to the question be equally easy to report?

## Failure modes

- **The leading brief:** the question presumes its answer.
- **The open benchmark:** "compare with peers" without naming them.
- **The leaky dependency:** a cross-check that can read what it is checking.
- **The unpinned input:** two modules, two share counts.
