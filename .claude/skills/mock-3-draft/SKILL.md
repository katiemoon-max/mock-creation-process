---
name: mock-3-draft
description: Phase 3 drafting. Drafts SFMAs in batches of 2–3 with stem-only phase, information-leakage audit, stem-usage audit, misconception-tagged MCQ distractors, and two-pass model-answer self-critique. Respects the project's exclusion list, difficulty targets, and command-word list via CLAUDE.md imports.
user_invocable: true
arguments: "[question_range]"
allowed-tools: Read, Glob, Grep, Write, Edit, Bash, Task
---

# Mock Paper Drafting (Phase 3)

You are drafting full Student Friendly Model Answers (SFMAs) in small batches. The pipeline deliberately forces batch sizes of 2–3 to keep constraints close in context — this addresses the "Claude ignores constraints stated once" failure mode.

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

#### ACTION — Stem only (draft with NO solution yet)

Draft ONLY the question stem and each part's prompt — no model answer, no MS&G, no ET&T. Write to a scratch buffer (not yet the final SFMA file).

- Use the command word approved for this part
- Mark allocation in `$m{[N mark(s)]}{align=right}` at the end of each part
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

Apply the Smart Mark rules (from the existing draft-questions spec):
- **Lists:** Accept / Do not accept for each listed item; "Any N from:" grouping
- **Calculations:** specify sig figs in stem or MS; final answer on its own line; ecf noted where applicable
- **Show that:** MS shows unrounded answer to 2 extra s.f. beyond the stem's rounded value
- **Definitions:** precise language, run through NotebookLM for consistency if unsure
- **Multi-point:** explicit when one statement earns multiple marks
- **Graph/data:** state ±½ small square tolerance
- **Alternatives:** list any valid equations Smart Mark might reject

Skip MS&G for MCQs.

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

#### ACTION — Assemble SFMA

Write to `Section A/Q{{NN}}-{{TopicSlug}}.md` using `.claude/templates/sfma.template.md`. Remove the HTML comment block from the template before committing.

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
- **Do not invent past-paper parallels.** Use the catalogues from `.project/catalogues/`.
- **Respect the exclusion list verbatim.** If a topic or context on the exclusion list starts creeping in, STOP and ask the user.
