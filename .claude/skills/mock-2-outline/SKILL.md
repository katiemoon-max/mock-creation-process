---
name: mock-2-outline
description: Phase 2 outline. Produces the paper blueprint (outline markdown + tracker CSV) from Phase 1 catalogues. Enforces command-word+AO+topic duplication gate, per-AO3 litmus test, image-source flag, paper-specific AO balance tolerance, and per-AO variety / difficulty-distribution / context-freshness checks. Required before /mock-3-draft.
user_invocable: true
arguments: ""
allowed-tools: Read, Glob, Grep, Write, Edit, Bash, Task, mcp__notion__notion-fetch
---

# Mock Paper Outline (Phase 2)

You are blueprinting the paper before any drafting. Everything here is subject-agnostic — Biology, Chemistry, Physics, Psychology, Geography all route through this same script. Board-specific detail comes from `.project/*` files, not from this skill.

## Success Criteria

This phase is complete only when every hard gate verifies. Log each outcome to `project.json.qualityGates.*` as named. Do not advance `phase` to 3 on any hard-gate failure.

**Hard gates (must verify before STOP 2):**
1. Planned topics within paper scope → verify: CHECK 0 (topicScopeCheck)
2. No repeated (command-word, AO, topic) triples → verify: CHECK 1A (duplicationCheck)
3. No MCQ ↔ Section B topic overlap → verify: CHECK 1B (mcqOverlapCheck)
4. MCQ format variety ≥ 4 categories, no single format over cap → verify: CHECK 1C (mcqFormatVariety)
5. Every AO3 mark passes the 3-part litmus → verify: CHECK 2 (ao3LitmusCheck)
6. AO balance within ±3% of `ao-targets.md` → verify: CHECK 3 (aoBalanceCheck)
7. No exclusion-list violations → verify: CHECK 4 (exclusionListCheck)
8. Image dependencies surfaced with source assigned → verify: CHECK 5 (imageDependencyCheck)
9. Typicality cross-check predicts ≥ 4.0/5 with no Critical flags → verify: CHECK 7 (typicalityCheck)

**Soft gates (logged, non-blocking):** stem-usage pre-plan (CHECK 6), paper length norm (CHECK 8), mark tariff norms (CHECK 9), per-AO variety (CHECK 10), difficulty distribution (CHECK 11), intra-paper context freshness (CHECK 12).

Markers: `STOP:`, `ACTION:`, `CHECK:`, `[Conditional]`.

## Prerequisites

ACTION: Read `project.json`. Verify `gates.research == "pass"` and `phase >= 2`.

[Conditional: research not complete]
> STOP: "Phase 1 (research) hasn't been completed. Run `/mock-1-research` first — the outline needs the three catalogues as evidence base."

ACTION: Load:
- `project.json` (paper meta, AO targets, exclusion list, topicCoverage)
- `.project/ao-classification-guide.md`
- `.project/ao-targets.md`
- `.project/command-word-list.md`
- `.project/difficulty-targets.md`
- `.project/exclusion-list.md`
- `.project/catalogues/ao-question-type.md`
- `.project/catalogues/ao-breadth-map.md`
- `.project/catalogues/mcq-catalogue.md`
- `.project/catalogues/spec-coverage-map.md`

### CHECK 0 — Topic scope verification (HARD GATE — runs first)

Before designing any question, build the planned-topic list (from any preliminary design in mind OR from the spec-coverage map's untested/heavily-tested analysis) and verify every topic/subtopic is within `project.json.paperMeta.topicCoverage`.

Common failure mode: planning synoptic questions that accidentally include out-of-scope topics (e.g. satellite orbits are Topic 9 / Paper 2 on Edexcel A Level Physics, but a creator might casually plan one for Paper 1).

[Conditional: any planned topic out of scope]
> STOP: "Planned content includes {{OUT_OF_SCOPE_TOPIC}} which is not in this paper's scope ({{paperMeta.topicCoverage}}). Swap for an in-scope alternative."

Log outcome to `project.json.qualityGates.topicScopeCheck`.

## Script

### STOP 1 — Confirm paper parameters

> "Confirming paper parameters from `project.json`:
> - Total marks: {{TOTAL}}
> - Time: {{TIME}}
> - AO targets (paper-specific): AO1 {{A1}}% · AO2 {{A2}}% · AO3 {{A3}}% (±3%)
> - Section structure: {{SECTIONS}}
> - Topic focus: {{FOCUS or 'full syllabus'}}
>
> Any changes before I start building the outline?"

USER: confirm or adjust.

### ACTION — Section structure

ACTION: Fetch SME Mock Exams Guidance from Notion (`notion-fetch` on https://www.notion.so/19d847b30a5f80c185abc52e886e19a1) for any board/subject-specific mock requirements.

ACTION: Determine section breakdown based on past papers. E.g. Section A = structured, Section B = MCQs; or mixed; or extended-response essays for essay-based subjects.

### ACTION — Plan topic coverage

Using `spec-coverage-map.md`:
- Prioritise spec points flagged as **untested** in recent papers (coverage breadth)
- Consider spec points **heavily tested** for REFRESH with a new context (not repetition)
- Respect tier/subject restrictions (e.g. Higher-Tier-only, HL-only, Physics-Only)
- Check `.project/exclusion-list.md` — do not plan topics or contexts on it

### ACTION — Design question flow

For each structured/extended question, design a cascading narrative arc:

- **Opening part:** low-demand entry (definition, recall, simple calculation / simple identification)
- **Building parts:** use the opening concept; produce values/ideas needed later; include "show that" safety nets where a later part depends on a derivation
- **Concluding part:** higher-demand calculation using earlier results OR qualitative analysis that interprets the scenario

For essay-based subjects (Psychology, Sociology, Geography case studies):
- Opening: state / outline
- Middle: describe / apply to a study or case
- Conclusion: evaluate / judge — with a novel claim or scenario for AO3

### ACTION — Assign AO with evidence

For every AO3 mark, write the **AO3 justification** in the outline's AO3 justification log:
- What novel information must the student interpret?
- Why can't this be answered from memorised content?

Use `.project/ao-classification-guide.md` exemplars as calibration.

### ACTION — Assign command words

Every command word must come from `.project/command-word-list.md`. Do not use command words from adjacent boards (e.g. AQA's "Describe" does not mean the same thing as CIE's "Describe").

### ACTION — Commit concrete numerical values in stems

Every structured-question stem must include concrete numerical values at outline stage — not placeholders like "given values" or "for a suitable mass". Mass, length, time, voltage, etc. must be committed so drafting (Phase 3) and review (Phase 4) can verify the numbers work.

Committed values go in the stem's `Suggested stem` / `Context` line, e.g. "A cyclist of mass 75 kg cycles up an incline at 8.0° at 4.5 m s⁻¹ against 25 N of resistive force" — not "A cyclist on a slope against resistive force".

### ACTION — Match opening-part to board archetype

For each structured question, consult `.project/board-conventions.md` ("Opening-question archetypes by in-scope topic") for the board's typical opening move for that topic. Use it to shape the first part of each structured question.

**Principle:** Generic decontextualised openers ("State the definition of X") are typical of MCQs, NOT structured-question openings. Structured openers are usually scenario-led (Draw / Describe / Show that / Calculate something concrete given the stem). If `board-conventions.md` isn't yet populated for a topic, check the `ao-question-type.md` catalogue's AO1 block for that topic and use the dominant opening pattern observed in past papers.

### ACTION — Use board-specific stem phrasing

Apply the phrasing conventions captured in `.project/board-conventions.md` ("Stem phrasing conventions"). These vary — some boards use numbered figures, others simple descriptors, others nested numbering. Also check AO3 framing conventions (e.g. "Deduce whether..." vs "Evaluate this claim..." vs "Criticise the statement...") — boards differ markedly here.

**Principle:** Applying the wrong board's convention is a small but noticeable typicality drag — students feel the paper "doesn't sound right". The phrasing fingerprint is more important than any individual word choice.

### ACTION — "Show that" safety-net frequency

Use the typical count recorded in `.project/board-conventions.md` ("'Show that' safety-net frequency"). "Show that" parts are cascade safety-nets — a student who can't complete part (b) can still access parts (c)-(e) using the given value.

**Principle:** Fewer than the board's typical count under-supports cascade dependencies; more over-scaffolds. Match the observed frequency.

### ACTION — Flag illustrations

For every row, set `Illustration required: Y/N`.
- If Y, set `Illustration source:` `claude` (matplotlib-generatable: graphs, circuits, ray diagrams, force diagrams) or `creator` (photos, micrographs, technical illustrations).
- Status starts as `pending`.

### ACTION — Write outline and tracker

Write the outline to `{{ProjectRoot}}/{{BOARD}}-{{QUAL}}-{{SUBJECT}}-{{PAPER}}-Mock-Outline.md` using `.claude/templates/outline-table.template.md`.

Write the tracker to `{{ProjectRoot}}/{{BOARD}}-{{QUAL}}-{{SUBJECT}}-{{PAPER}}-Mock-Tracker.csv` using `.claude/templates/tracker.template.csv`. One row per question part (a, b, c — consolidate sub-parts i/ii with notes).

For GCSE/IGCSE only: include the "Suitable for Combined?" / "Suitable for Co-ordinated?" column per board convention. For IB HL: include "Suitable for SL?". For A Level / AP / Higher: omit.

### CHECK 1A — Command-word + AO + topic duplication (HARD GATE)

Build the set of every (command-word, AO, topic) triple across all parts. Check:
- Any duplicates? Each triple should appear at most once across the paper (otherwise the paper is testing the same thing twice).

[Conditional: duplicates found]
> STOP: "I found duplicate command-word + AO + topic combinations: {{LIST}}. This violates the 'no repeated testing' rule. Rewrite the outline to remove duplicates, or justify the overlap."

Log outcome to `project.json.qualityGates.duplicationCheck`.

### CHECK 1B — MCQ ↔ Section B topic non-overlap (HARD GATE)

For each MCQ, check whether its topic/subtopic substantively duplicates a structured-question focus. Example failure: if Section B Q14 is an AO3 inverse-square-law verification, Section A should not have an MCQ asking "Which graph shows an inverse-square field?" — both test the same construct.

Build a list of MCQ subtopics and structured-question subtopics. Flag overlaps.

[Conditional: overlaps found]
> STOP: "MCQ{{N}} (subtopic: {{X}}) overlaps with Q{{M}} (focus: {{Y}}). Replace MCQ{{N}} with a different subtopic from the same topic area."

Log to `project.json.qualityGates.mcqOverlapCheck`.

### CHECK 1C — MCQ format variety (HARD GATE)

Classify every MCQ into a format category using the taxonomy in `.project/catalogues/mcq-catalogue.md` (produced by `/mock-1-research`). Categories vary by subject but commonly include: direct-calculation, multi-step-calculation, ratio/scaling, graph-interpretation, graph+calculation, table/row-identification, "Which is NOT" (negative framing), properties-table-matching, concept-deduction, unit/identity-analysis, algebraic-expression-selection, direct-recall/identification.

**Rules (principles — the specific numbers come from `.project/board-conventions.md`):**
- No single format may exceed the cap defined for this board (typically 30-40% of the MCQ section; e.g. for 10 MCQs, cap any one format at 3-4)
- At least 4 distinct format categories represented across the section
- Format distribution should broadly match the real-paper distribution recorded in the MCQ catalogue (if a format appears in ~10% of real MCQs, include at least one)

[Conditional: single format exceeds cap OR fewer than 4 categories]
> STOP: "MCQ section is format-monotone: {{DISTRIBUTION}}. Redesign {{N}} MCQs to add variety. Priority gaps: {{MISSING_FORMATS}}."

Log to `project.json.qualityGates.mcqFormatVariety`.

### CHECK 2 — AO3 litmus test (HARD GATE)

For every AO3 mark in the outline, apply the litmus test from `ao-classification-guide.md`:
1. Novelty — is there information the student must interpret that they haven't seen?
2. Engagement — does answering *require* that information?
3. Judgement — synthesis/evaluation, not just procedure?

[Conditional: any AO3 mark fails the litmus test]
> STOP: "Q{{N}}.{{P}} is classified AO3 but doesn't pass the litmus test. Specifically: {{REASON}}. Re-classify as AO1 or AO2, or add genuine novel content."

Log to `project.json.qualityGates.ao3LitmusCheck`.

### CHECK 3 — AO balance (HARD GATE)

Sum marks by AO. Compute percentages.

Compare against `.project/ao-targets.md` with tolerance ±3%.

[Conditional: outside tolerance]
> STOP: "AO balance is out: AO1 {{actual}}% (target {{target}}%), AO2 {{actual}}% (target {{target}}%), AO3 {{actual}}% (target {{target}}%). Adjust mark tariffs on specific parts — I can suggest candidates (parts where AO could plausibly shift up/down by 1). Would you like me to propose shifts?"

Log to `project.json.qualityGates.aoBalanceCheck`.

### CHECK 4 — Exclusion-list compliance

Verify:
- No planned topic appears in `.project/exclusion-list.md`'s excluded topics
- No planned context appears in the excluded contexts list
- No planned question uses an excluded command-word + AO + topic triple (from sister-paper analysis)

[Conditional: any violation]
> STOP: "Q{{N}}.{{P}} uses {{VIOLATION}} which is on the exclusion list. Replace it."

Log to `project.json.qualityGates.exclusionListCheck`.

### CHECK 5 — Image dependencies surfaced

Count `Illustration required: Y` rows. For each:
- Is `Illustration source` set (claude or creator)?
- Is the description in Notes specific enough for Claude/creator to build from?

[Conditional: creator-provided images present]
> STOP: "This paper depends on {{N}} creator-provided images: {{LIST}}. Flagging now so these don't block drafting later. Tracker status marked `pending creator upload`."

Log to `project.json.qualityGates.imageDependencyCheck`.

### CHECK 6 — Stem-usage plan (soft gate)

For each multi-part question, write a brief stem-usage plan in the outline's appendix:
- What information will the stem carry?
- Which parts will use that information?
- Are there any pieces of information that would be *unused*? (If yes, either remove from stem or add a part that uses it.)

This is soft — the hard stem-usage audit happens in `/mock-3-draft` once the full stems exist. Here we just pre-plan.

### CHECK 7 — Typicality cross-check (soft gate, mandatory)

Before finalising the outline, run a paired typicality cross-check. Dispatch two `general-purpose` agents in parallel:

**Agent A — NotebookLM typicality review:**
- 3-5 sharp NotebookLM queries rating each structured question 1-5 for typicality vs real past papers
- Named stem-level past-paper parallels (not just topic-level)
- Opening-archetype alignment per topic
- Stem-phrasing convention check
- Write findings to `reviews/outline-typicality-notebooklm.md`

**Agent B — Direct-analysis typicality review:**
- Read the outline + catalogues + real past-paper markdown files
- Apply: MCQ format variety check, MCQ↔Section B overlap check, opening archetype comparison, stem concreteness audit, paper-length check, AO3 distribution pattern (spread vs lumped — varies by board)
- Write findings to `reviews/outline-typicality-direct.md`

Both agents predict a student-perception score on "How well does this match your actual exam?" (1-5).

[Conditional: predicted score < 4.0 OR any Critical flag raised]
> STOP: "Typicality cross-check predicts {{X}}/5 student-perception score. Critical flags: {{LIST}}. Revise before advancing to Phase 3."

Log to `project.json.qualityGates.typicalityCheck` with the predicted score and reviewer file paths.

### CHECK 8 — Paper length (soft gate)

Total question count should match the board's observed norm captured in `.project/board-conventions.md` ("Question-count norm"). Expect variation by qualification and board — some boards run 18-20 questions on A Level papers, others 25-30, others fewer.

[Conditional: count outside ±1 of the board's observed norm]
> "Paper has {{N}} questions; this board's observed norm is {{M}} ± 1. Recommend adjusting — fewer questions if over, or slightly more if under."

Log to `project.json.qualityGates.paperLengthCheck`.

### CHECK 9 — Mark tariff alignment (soft gate)

For each structured-question part, compare the assigned mark tariff against the board's typical tariffs for that cognitive demand (recorded in `.project/board-conventions.md` → "Mark tariff norms by cognitive demand").

**Principle:** boards have characteristic tariffs for specific demands. A 2-mark "State" where the board typically awards 1 mark, or a 6-mark "Calculate" where the board typically caps at 4, will feel atypical to students even if the physics is correct.

[Conditional: any part's tariff deviates by >1 from the board's typical tariff for that demand]
> "Q{{N}}.{{P}} has tariff {{X}} for a {{COMMAND}} demand; board typical is {{Y}}. Consider adjusting or justify the deviation."

Log to `project.json.qualityGates.markTariffCheck`.

### CHECK 10 — Per-AO variety / breadth (soft gate, mandatory)

The anti-"same-y" gate. AO balance (CHECK 3) fixes the *proportion* of each AO; this fixes the *spread* — each AO tested through a range of command words and task types, not one archetype.

Using `.project/catalogues/ao-breadth-map.md` (the board's observed palette per AO), for each AO list the command words and task-type categories used across every mark of that AO in the outline. Check:
- No single command word accounts for more than ~50% of an AO's marks
- Each AO is tested through at least 3 distinct command words / task types (exempt an AO that carries only 1–2 parts in this paper)
- The outline draws from the breadth map's palette rather than clustering on the prototype (AO1 ≈ State, AO2 ≈ Calculate, AO3 ≈ Deduce)

**Why this gate exists:** a paper can pass AO balance, duplication and typicality while every AO1 mark is "State" and every AO2 is "Calculate" — balanced but monotone, under-sampling the spec's breadth. This is the failure mode that drove a large by-hand rework of Paper 1 *after* every other gate had passed.

[Conditional: an AO is monotone]
> "AO{{N}} is testing narrowly: {{DISTRIBUTION}} (e.g. {{X}}% via '{{COMMAND}}'). Under-used options from the breadth map: {{LIST}}. Recommend diversifying {{K}} parts before drafting."

Log to `project.json.qualityGates.aoVarietyCheck`.

### CHECK 11 — Difficulty distribution (soft gate, mandatory)

Compare the outline's LoD ramp against `.project/difficulty-targets.md`. Check:
- At least the target number of high-demand parts only the top ~20% should get (default ≥ 3)
- At least the target number of accessible entry points all candidates can attempt (default ≥ 3)
- The overall easy / medium / hard mix (MCQs + structured parts) is not skewed away from the targets

**Why this gate exists:** a paper can pass AO balance and typicality while sitting too easy — several Paper 1 MCQs reached review "too easy for the paper" and were hardened by hand. Catch the skew at outline.

[Conditional: distribution misses the targets]
> "Difficulty distribution is off target: {{SUMMARY}}. difficulty-targets.md asks for {{TARGETS}}. Recommend hardening/softening these parts: {{LIST}}."

Log to `project.json.qualityGates.difficultyDistributionCheck`.

### CHECK 12 — Intra-paper context/format freshness (soft gate)

CHECK 1C covers MCQ format variety; this covers Section B contexts. List each structured question's **context archetype** (e.g. "vertical circular motion", "potential divider", "capacitor discharge") and its distinctive diagram/graph type. Flag any two questions sharing a context archetype or a distinctive format unless the overlap is intended.

**Why this gate exists:** the drafted Paper 1 carried two circular-motion contexts and reused the four-graph MCQ format twice; both were caught by hand after the fact. A fresh context per construct widens the range of scenarios the paper samples.

[Conditional: repeated context archetype]
> "Q{{N}} and Q{{M}} share the {{ARCHETYPE}} context. Recommend refreshing one for breadth, unless the repeat is deliberate."

Log to `project.json.qualityGates.contextFreshnessCheck`.

### STOP 2 — Present outline for approval

Show the creator:
- The outline table
- AO balance
- Topic coverage
- Command word distribution
- LoD ramp
- Illustration sources
- AO3 justifications
- Duplication audit result
- Per-AO variety, difficulty distribution and context-freshness results (CHECK 10–12)
- Past-paper parallels for each structured question

> "Outline complete. All hard gates passed. Would you like to make any changes before we move to drafting, or shall I mark Phase 2 complete?"

USER: approve or request edits.

### ACTION — Update project.json

On approval:
- Set `gates.outline: "pass"`, `phase: 3`.
- Write one `questions[]` entry per part, with `status: "planned"`, `illustrationSource`, `illustrationStatus: "pending"`.
- Set `nextStep: "/mock-3-draft Q01-Q03"` (recommending a first batch of 3).

### Final output to user

```
Outline complete for {{PROJECT_NAME}}.

- Total marks: {{SUM}} (target {{TARGET}})
- AO balance: AO1 {{A1}}% · AO2 {{A2}}% · AO3 {{A3}}% — PASS (tolerance ±3%)
- Duplication check: PASS (no repeated command-word+AO+topic)
- AO3 litmus: PASS ({{N}} AO3 marks all justified)
- Exclusion list: PASS ({{N}} items checked)
- Variety & difficulty (soft): per-AO spread {{OK/flags}} · difficulty distribution {{OK/flags}} · context freshness {{OK/flags}}
- Illustrations: {{N}} Claude-generatable, {{M}} creator-provided

Files:
- {{OUTLINE_PATH}}
- {{TRACKER_PATH}}

Next: /mock-3-draft Q01-Q03 (drafting in batches of 2–3)
```

## Rules

- HARD GATES fail-closed: do not update project.json phase on a hard-gate failure. Return to the user.
- Do not invent past-paper parallels. Every "cf. June 2023 Q4" must come from `.project/catalogues/`.
- Do not exceed tolerance on AO balance by "rounding" — a 4% gap is a fail, fix it before proceeding.
- Call the `exam-researcher` sub-agent for past-paper parallels if the catalogues are thin on a specific topic.
