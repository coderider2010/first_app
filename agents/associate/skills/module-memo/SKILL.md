---
name: module-memo
description: Format any finished module as the firm's answer-first memo with confidence levels and assumptions table. Load at the end of every module before submission.
---

# Module memo

The memo is how the EM, and maybe a client CFO, meets your work. They read the first
paragraph and decide whether to trust the rest.

## Template (in this order)

1. **Header:** engagement, module, from/to, as-of date (and the latest data period),
   confidence.
2. **Answer:** one paragraph, the "so what" first, in the form the brief asked for. A
   reader who stops here has the answer.
3. **Support:** the key exhibit (table or grid), then 3–5 numbered points, each starting
   with its takeaway in bold. Each point is a claim plus the evidence for it.
4. **Escalations to the EM:** conflicts, findings that cut against the storyline, and
   material things the brief didn't ask about. Lead with the most serious.
5. **Assumptions and method:** a table of choice | value | why.
6. **Confidence:** the level, why, and the **top 2 things that would change the answer**.
7. **Open issues and gaps:** what you didn't do and why, including stub or missing skills.
8. **Exhibit A (appendix):** every figure with lineage (see `fact-base-contribution`).

## Confidence: what each level commits you to

- **High:** load-bearing numbers are reported facts or simple arithmetic on them,
  cross-checks tie, and you would defend it to a client CFO today.
- **Medium:** a judgment input moves the answer (a discount rate, a peer set, a growth
  path) or one source is weaker than you'd like. Name the input.
- **Low:** key inputs are estimates or proxies, or methods disagree by more than the
  tolerance. Say what data would raise it.

Don't round up. A medium labelled high costs more trust than it saves.

## Length

Two pages before the appendix. If the body runs long, the answer isn't sharp yet. Move
detail to exhibits; don't cut the lineage.

## Labels

Mark every number **fact** (reported), **estimate** (your calculation or judgment) or
**hypothesis** (untested idea). Mark financial figures GAAP or non-GAAP. Never let an
estimate sit in a table of facts without a label (charter principle 7).

## Red-team pass before submitting

- Does the first sentence answer the brief's question, in the brief's form?
- Can every number be traced to a source in Exhibit A? Spot-check three.
- Do derived numbers recompute? Re-run them, don't re-read them.
- Do the summary numbers match the tables? (Copying slips happen between table and prose.)
- Is anything here pointing against the storyline? If so, is it in Escalations?
- Did the gate's verifier flags all get a sentence in the memo?

## Failure modes

- **Buried answer:** the conclusion arrives on page 2.
- **Prose-table drift:** the summary says one figure, the table another.
- **Confidence inflation:** "high" with a judgment input that moves the answer.
- **Hidden gaps:** a missing figure quietly left out instead of listed.

## Handoff

End with the `MODULE:` line (see `.claude/agents/associate.md`). The EM reads Answer,
Escalations and Confidence first.
