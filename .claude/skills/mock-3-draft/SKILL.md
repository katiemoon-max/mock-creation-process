---
name: mock-3-draft
description: Phase 3 drafting. Drafts SFMAs in batches of 2–3 with stem-only phase, information-leakage audit, stem-usage audit, misconception-tagged MCQ distractors, and two-pass model-answer self-critique. Respects the project's exclusion list, difficulty targets, and command-word list via CLAUDE.md imports.
user_invocable: true
arguments: "[question_range]"
allowed-tools: Read, Glob, Grep, Write, Edit, Bash, Task
---

# Mock Paper Drafting (Phase 3)

You are drafting full Student Friendly Model Answers (SFMAs) in small batches. The pipeline deliberately forces batch sizes of 2–3 to keep constraints close in context — this addresses the "Claude ignores constraints stated once" failure mode.

## Success Criteria

A question is "drafted" only when every per-question hard gate verifies. Log each outcome to `project.json.questions[N].*` as named.

**Per question (must verify before moving to the next):**
1. No information leakage between parts → verify: CHECK 2 (infoLeakageAudit)
2. Every stem fact is required by at least one part → verify: CHECK 3 (stemUsageAudit)
3. Model answer at target CEFR level, within word ceiling → verify: CHECK 4 (modelAnswerTwoPass)
4. Every MCQ distractor cites a named misconception by ID → verify: CHECK 5 (MCQ only)
5. Every MS&G marking point is Smart-Mark-ready → verify: CHECK 6 (markSchemeAudit; structured parts)

**Per batch:**
5. Batch size ≤ 3 (constraint-drift guard) → verify: STOP 1
6. Constraints repeated back verbatim before drafting starts → verify: CHECK 1
7. All questions in batch have `status: "drafted"` and all gate flags set → verify: inner-loop end

**Phase advance (to Phase 4):** only when every question in the outline is drafted. Then set `gates.draft: "pass"`, `phase: 4`.

Markers: `STOP:`, `ACTION:`, `CHECK:`, `[Conditional]`.

## Prerequisites

ACTION: Read `project.json`. Verify `gates.outline == "pass"` and `phase >= 3`.

[Conditional: outline not complete]
> STOP: "Phase 2 (outline) hasn't been completed. Run `/mock-2-outline` first — drafting needs the approved outline as input."

ACTION: Read the following files fresh at the start of every batch (even if you've read them before):
- `project.json` (current question statuses, excluded contexts)
- The project root `CLAUDE.md` (which imports the full set of project-scoped constraints)
- `.project/exclusion-list.md`
- `.project/difficulty-targets.md`
- `.project/command-word-list.md`
- `.project/misconception-bank.md`
- `.project/ao-classification-guide.md`
- `.project/catalogues/ao-breadth-map.md`
- `.claude/context/mark-scheme-standard.md` (universal MS principles + pre-flight gate)
- `.project/mark-scheme-conventions.md` (this course's learned MS conventions)
- `.project/ms-exemplars/` (creator-approved MS format exemplars for this course)
- The outline file for the question range specified
- The tracker CSV for illustration sources

ACTION: Read `/cobalt-formatting` as a reference (it's not callable — it's the markdown syntax reference for Cobalt CMS output).

## Script

### STOP 1 — Batch selection

If the user provided a question range (e.g. `Q03-Q05`), use it. Otherwise:

> "Which questions should I draft in this batch? I recommend batches of 2–3 to keep constraints in context — larger batches tend to drift. Options based on `project.json`: {{PLANNED_QUESTIONS}}."

USER: question range.

[Conditional: batch size > 3]
> STOP: "That's {{N}} questions — larger batches lead to constraint drift. I strongly recommend splitting into two batches. Proceed anyway, or split?"

### CHECK 1 — Pre-batch constraint reload (STOP and repeat back)

Before writing anything, repeat the constraints verbatim so they're in the immediate context:

> "Before I draft Q{{N1}}–Q{{Nk}}, confirming the constraints I'll respect:
>
> - **Exclusion list:** {{SHORT_LIST}}
> - **Difficulty targets:** reading level {{CEFR}}, word ceiling {{N}} for {{MARK}} marks
> - **AO targets:** AO1 {{A1}}% · AO2 {{A2}}% · AO3 {{A3}}% (±3%)
> - **Command words approved:** {{TOP_5_FROM_LIST}}
> - **Misconception bank has:** {{N}} entries — every MCQ distractor must cite one
>
> Ready to start with Q{{N1}}."

This is deliberately verbose. It's the cheapest way to keep constraints load-bearing.

### For each question in the batch, run this inner loop:

#### ACTION — Research precedent

Read `.project/catalogues/ao-question-type.md` for parallels to the question's topic + command word + AO. Note 1–2 past-paper references to cite in the outline's "Notes" column.

Also check `.project/catalogues/ao-breadth-map.md` for the AO's command-word / task-type palette. Draft each part with the command word and task type the outline assigned — do NOT collapse a planned format into the per-AO prototype (AO1 ≈ State, AO2 ≈ Calculate, AO3 ≈ Deduce). Where the outline leaves phrasing open, pick from the breadth map's palette and prefer a command word / task archetype not already used elsewhere in the paper. This is the drafting-time guard against the "same-y questions" regression that CHECK 10 gates at outline and Review 8 re-checks at review.

#### ACTION — Stem only (draft with NO solution yet)

Draft ONLY the question stem and each part's prompt — no model answer, no MS&G, no ET&T. Write to a scratch buffer (not yet the final SFMA file).

- Use the command word approved for this part
- Mark allocation in `{align=right}[N]` at the end of each part stem (Cobalt-canonical syntax — NOT `$m{[N mark(s)]}{align=right}`, which is the inline-working syntax)
- Image placeholder where required: `[IMAGE: {{DESCRIPTION}}]`

#### CHECK 2 — Information-leakage audit (HARD GATE, pre-solution)

Read the stem-only draft. For each part, ask:

> "Can part ({{P}}) be answered using information given in the stem of any other part? Can the answer to part ({{P}}) be inferred from another part's wording?"

[Conditional: any leakage found]
Fix the stems before writing solutions. Typical fix: move information from a later part's stem into the main question stem, or remove the answer-revealing wording.

Log to `project.json.questions[N].infoLeakageAudit = "pass"`.

#### CHECK 3 — Stem-usage audit (HARD GATE, pre-solution)

For every piece of information in every stem, identify which part requires it:

> "For the stem of Q{{N}}, I listed {{LIST_OF_FACTS}}. Each of these is required by: {{FACT_1}} → part ({{P1}}); {{FACT_2}} → part ({{P2}}); ..."

[Conditional: any fact unused]
Either remove the unused fact from the stem, or add a part that requires it. Do not leave decorative information — it confuses students.

Log to `project.json.questions[N].stemUsageAudit = "pass"` and write the mapping to `.project/stem-audit.md`.

#### ACTION — Model answer

Draft the Model Answer for each part:

- Full worked solution earning all marks
- Show every step for calculations; include units at every step
- Reference values from earlier parts explicitly ("Using the {{QUANTITY}} = {{VALUE}} from part ({{P}})...")
- Use `$$...$$` for equations
- Use `$f{...}` for final answers, `$w{...}` for working, `$c{...}` for commentary
- Respect the word ceiling from `.project/difficulty-targets.md`

#### CHECK 4 — Two-pass model-answer self-critique

After drafting the model answer, reflect:

> "Is this answer at {{CEFR}} reading level for a strong {{YEAR_GROUP}} student, or did I drift to academic/postgraduate register? Word count: {{N}} vs ceiling {{CEILING}}. Any vocabulary a student wouldn't use? Would removing marks-irrelevant content tighten it?"

[Conditional: over ceiling / too academic]
Rewrite the answer:
- Simplify vocabulary
- Cut content that doesn't earn marks
- Use plain phrasing over academic register

Log to `project.json.questions[N].modelAnswerTwoPass = "pass"`.

#### ACTION — Mark Scheme and Guidance (MS&G)

Only include if the Model Answer doesn't already show every mark-earning pathway.

Build the MS&G against **both layers** of `.claude/context/mark-scheme-standard.md`:
- **Universal principles (Layer 1):** every marking point discrete and closed; MS demand == the command word's demand; closed accept-lists (no "any reasonable"); explicit ecf for every cross-part dependency, traced through the whole chain; grouping explicit; precision, tolerance and units stated; alternative valid responses enumerated; no commentary inside MS&G.
- **This course's conventions (Layer 2):** apply `.project/mark-scheme-conventions.md` for the course's precision convention, "show that" extra-figure count, tolerance idiom, mark-type codes and banding style; match the format of the creator-approved `.project/ms-exemplars/`.

Skip MS&G for MCQs.

#### CHECK 6 — Mark-scheme Smart-Mark pre-flight (HARD GATE, structured parts)

Run the pre-flight gate (§9 of `mark-scheme-standard.md`) on every marking point of this question's MS&G before moving on. Confirm, per marking point:

- discrete, closed, tag-able; **MS demand == the command word's demand** (if the natural MS demand doesn't match, change the command word — do not bend the MS)
- accept-lists enumerated (no "any reasonable"); ecf explicit through the whole chain; grouping explicit, no silent bundling
- precision, tolerance and units stated **in this course's convention** (`.project/mark-scheme-conventions.md`)
- alternative valid responses enumerated; no commentary inside MS&G; not a duplicate of a complete Model Answer; no claims-compliance gap
- levelled parts built in the course's banding style; overall format matches `.project/ms-exemplars/`

[Conditional: any marking point fails]
Fix the MS&G before drafting continues. If the fix is a command-word change, update the outline's command-word plan for that part too.

Log to `project.json.questions[N].markSchemeAudit = "pass"`. (MCQs have no MS&G — skip this gate for them; MCQ distractor rigour is covered by CHECK 5.)

#### ACTION — MCQ distractors (if MCQ)

For each distractor (B, C, D):

> "Which misconception from `.project/misconception-bank.md` does this distractor target? Cite the ID."

[Conditional: no existing misconception fits]
Append a new entry to the misconception bank with a new ID, then cite it.

Log the distractor-to-misconception mapping to the misconception bank's per-paper log.

#### CHECK 5 — Per-distractor misconception check (HARD GATE, MCQ only)

For every distractor across every MCQ in this batch:
- Does it cite a misconception by ID?
- Would a student making that error realistically select that option?

[Conditional: any distractor fails]
Rewrite — do not leave distractors that don't correspond to a named misconception (this creates MCQs where wrong answers are implausible, which is the "too easy" failure mode).

#### ACTION — Examiner Tips and Tricks (ET&T)

Actionable exam advice, not a repeat of the solution:
- Common student errors (can draw from misconception bank)
- Patterns from examiner reports
- Strategic tips (time management, working-out conventions)
- 2nd person voice
- Cross-reference to other parts where relevant

#### ACTION — Diagrams

If the tracker row has `Illustration required: Y` and `Illustration source: claude`:
- Invoke `/generate-diagram` with a clear description
- Update tracker: `illustrationStatus: generated`

If `Illustration source: creator`:
- Write a clear `[IMAGE: {{DESCRIPTION}}]` placeholder
- Update tracker: `illustrationStatus: pending creator upload`

#### ACTION — Assemble SFMA (Cobalt-canonical from the start)

Write to `Section A/Q{{NN}}-{{TopicSlug}}.md` using `.claude/templates/sfma.template.md`. Remove the HTML comment block from the template before committing.

**The output MUST match the course's canonical Cobalt format.** Reference: the creator-approved exemplars in `.project/ms-exemplars/` (produced by the MS calibration step in `/mock-1-research`), which are seeded from the SME Gold Standard SFMA library (four sets — defined-mark closed/open, levelled, MCQ; set IDs in `.claude/context/mark-scheme-standard.md`) — read these before drafting if the format is unfamiliar. Eliminating reformatting at publish time is the whole point of this gate.

**Cobalt-canonical structural checklist (every SFMA must satisfy):**

1. Single H1 `# Question N — Topic` at the top of the file only.
2. Common-context stem (shared scenario for all parts) sits directly under that H1, BEFORE the first `---`. Stem-level image placeholders go here.
3. Each part opens with `# Part a` / `# Part b` H1, then `## Problem` and `## Solution` H2s.
4. Horizontal rule `---` between every part.
5. Tariff at end of each part stem: `{align=right}[N]` (NOT `$m{[N mark(s)]}{align=right}` — that syntax is for inline-working markers only).
6. Inline mark markers in working steps: `$m{[1 mark]}` placed at the end of the line that earns the mark. Centre-aligned working: `{align=center} $$equation$$ $m{[1 mark]}` on one line.
7. MS&G uses paragraph-style points with inline `$m{[N mark]}` markers, plus explicit `Accept` and `Do not accept` paragraph clauses where the command word's mark scheme distinguishes them.
8. Multi-mark "Explain" parts use **MP1 / MP2 / MP3 (key-term anchors: ...)** prefix per mark for Smart-Mark anchoring.
9. ecf chains stated explicitly: which mark carries ecf, from which earlier part.
10. Model-answer content sits directly under `## Solution` — NO `**Model Answer**` / `**End of Model Answer**` wrappers (not a valid Cobalt callout). MS&G + ET&T wrappers ARE valid and required.

#### ACTION — Update project.json

Set `questions[N].status: "drafted"` and all per-question quality-gate flags to `"pass"`.

### END inner loop (next question in batch)

### STOP 2 — Batch complete

> "Batch complete: Q{{N1}}–Q{{Nk}} drafted. Next batch? Options: {{REMAINING_QUESTIONS}}. Or run `/mock-4-review` when all questions are drafted."

### ACTION — Final batch handling

[Conditional: all questions in the outline are drafted]
Set `gates.draft: "pass"`, `phase: 4`, `nextStep: "/mock-4-review"`.

## Rules

- **Batches of 2–3 maximum.** Not a suggestion — the whole point is to keep constraints in context.
- **Stem-only phase is mandatory.** Do NOT draft the solution in the same pass as the stem — the audits must happen on the stem alone.
- **Every MCQ distractor cites a misconception.** No exceptions.
- **Two-pass model answer.** The first draft is expected to be too academic — the second pass is where it becomes student-appropriate.
- **Cobalt formatting is not optional.** Every SFMA goes through Cobalt; violations cost time to fix post-hoc.
- **Cobalt-canonical format from the start — do NOT defer to publish phase.** Drafted SFMAs must match the published Paper 1 format exactly: `# Question N — Topic` H1, common stem before first `---`, `# Part a` H1 per part, `## Problem` + `## Solution` H2s, `---` between parts, `{align=right}[N]` tariffs, inline `$m{[N mark]}` markers in working, paragraph-style MS&G with explicit `Accept` / `Do not accept` clauses. Reference: the creator-approved `.project/ms-exemplars/`. Reformatting at `/mock-5-publish` time is a 30–60 minute cost per paper — absorb it here.
- **Design command words and contexts from the breadth map.** Consult `.project/catalogues/ao-breadth-map.md` when drafting; honour the outline's planned variety and don't regress a planned format into the per-AO prototype. Enforced upstream by CHECK 10 (outline) and downstream by Review 8 (review).
- **Every MS&G passes the Smart-Mark pre-flight (CHECK 6) before a question is marked "drafted".** Build against `.claude/context/mark-scheme-standard.md` (universal) plus `.project/mark-scheme-conventions.md` and `.project/ms-exemplars/` (this course, learned in `/mock-1-research`). If the mark scheme wants a demand the command word doesn't license, change the command word — not the mark scheme.
- **Do not invent past-paper parallels.** Use the catalogues from `.project/catalogues/`.
- **Respect the exclusion list verbatim.** If a topic or context on the exclusion list starts creeping in, STOP and ask the user.
- **Do NOT wrap the model answer in `**Model Answer**` / `**End of Model Answer**`.** It is not a valid Cobalt callout (only MS&G, ET&T, Worked Example, Case Study, Blockquote are). Write the solution content directly under the `## Solution` heading — no wrapper. Phase 5 publish strips these defensively, but they shouldn't be in the SFMA to begin with.
- **MCQ distractor explanations are paragraphs, not bullets.** Write each "**A** is incorrect because…", "**B** is incorrect because…" as a separate paragraph separated by blank lines. Bullets (`- `) stay for positive-derivation steps only.
- **MCQ ET&T is optional.** Include one only when it adds genuine new insight beyond the distractor commentary. If the distractor explanations already cover the teaching points, omit it. (For structured parts, ET&T is still recommended on every part.)
