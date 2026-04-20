---
name: mock-4-review
description: Phase 4 composite review. Runs NotebookLM typicality, spec-check, assessment-design-checklist, three sub-agent reviews (spec-examiner, student-simulator, marking-realism-checker) in parallel, and the CQI scorecard. Consolidates into reviews/SUMMARY.md. Mandatory before /mock-5-publish.
user_invocable: true
arguments: ""
allowed-tools: Read, Glob, Grep, Write, Edit, Bash, Task
---

# Mock Paper Review (Phase 4)

You orchestrate every quality gate. Today these skills exist in isolation (`/spec-check`, `/review-cqi`, the assessment-design-checklist context file) — this skill wires them into a single mandatory review flow so nothing sits orphaned.

Markers: `STOP:`, `ACTION:`, `CHECK:`, `[Conditional]`.

## Prerequisites

ACTION: Read `project.json`. Verify `gates.draft == "pass"` and `phase >= 4`.

[Conditional: not all questions drafted]
> STOP: "Not all questions are drafted. Current status: {{STATUS_TABLE}}. Run `/mock-3-draft` for the remaining questions first."

## Script

### STOP 1 — Review scope confirmation

> "Running the full Phase 4 review for {{PROJECT_NAME}}. This will run:
>
> 1. `/review-questions` (NotebookLM typicality, one question at a time)
> 2. `/spec-check` across all drafted questions
> 3. Assessment design checklist (`.claude/context/assessment-design-checklist.md` applied per-question)
> 4. Three sub-agents in parallel: `spec-examiner`, `student-simulator`, `marking-realism-checker`
> 5. `/review-cqi` for CQI scorecard
>
> Everything writes to `reviews/`. This will take a while — roughly 10-15 minutes of tool calls. OK to proceed?"

USER: confirm.

### ACTION — Review 1: NotebookLM typicality

Invoke `/review-questions` via Skill tool. Output expected at `reviews/notebooklm-review.md` (or wherever `/review-questions` writes — ensure it's inside `reviews/`).

Log to `project.json.reviews.notebookLmTypicality = {"status": "...", "file": "..."}`.

### ACTION — Review 2: Spec-check

Invoke `/spec-check` with all drafted SFMAs as input. Write consolidated output to `reviews/spec-check.md`.

Log to `project.json.reviews.specCheck`.

### ACTION — Review 3: Assessment design checklist

Read `.claude/context/assessment-design-checklist.md`. For each of its 11 checks (8 per-question, 3 paper-level), apply them to every drafted SFMA and produce a report at `reviews/assessment-design.md`.

Format:

```markdown
# Assessment Design Review — {{PROJECT_NAME}}

## Per-question audits

### Q1
- [ ] Validity: every mark tests the intended construct
- [ ] CIV-Difficulty: no marks lost to reading comprehension / handwriting
- [ ] CIV-Easiness: context doesn't advantage particular backgrounds
- [ ] Differentiation: distinguishes across the ability range
- [ ] Cognitive load: matches LoD target
- [ ] Language: accessible at CEFR {{TARGET}}
- [ ] Context: culturally neutral
- [ ] MS quality: markers agree independently

### Paper-level

- [ ] Comparable demand vs past papers
- [ ] Accessible entry points
- [ ] Coherent paper narrative
```

Log to `project.json.reviews.assessmentDesign`.

### ACTION — Review 4, 5, 6: Sub-agents (parallel)

Dispatch three sub-agents in parallel (single message, three Task tool calls):

**Task 4a — spec-examiner**
> "Run an adversarial chief-examiner review on all drafted SFMAs in {{PROJECT_DIR}}/Section A/. Read .project/ao-classification-guide.md, .project/command-word-list.md, and the spec at {{SPEC_PATH}}. Write verdict to reviews/spec-examiner.md per your AGENT.md spec."

**Task 4b — student-simulator**
> "Read only the Problem sections of all SFMAs in {{PROJECT_DIR}}/Section A/. Simulate a strong-but-not-exceptional {{YEAR_GROUP}} student's stream-of-consciousness attempt. Flag ambiguity, unused stem info, cross-part leakage, and blocked dependencies. Write to reviews/student-simulator.md per your AGENT.md spec."

**Task 4c — marking-realism-checker**
> "Audit mark schemes for Smart Mark readiness and command-word-demand alignment across all SFMAs in {{PROJECT_DIR}}/Section A/. Apply every Smart Mark rule. Write to reviews/marking-realism.md per your AGENT.md spec."

Wait for all three to return, then log each to `project.json.reviews.*`.

### ACTION — Review 7: CQI scorecard

Invoke `/review-cqi` on the whole paper. Expected output at `reviews/cqi-scorecard.md` with 10-criterion scorecard.

Log to `project.json.reviews.cqiScore = {"total": N, "pass": true/false, "critical": [...], "file": "..."}`.

### CHECK 1 — Aggregate & consolidate

Read all 7 review files. Build the consolidated summary at `reviews/SUMMARY.md` using `.claude/templates/review-summary.template.md`:

- Tick each gate as pass / pass with issues / fail
- Aggregate Critical issues (would-block-publish), Recommended, Minor — deduplicated across reviews
- Flag the publish gate as OPEN only if: CQI ≥ 43/50, all sub-reviews ≥ pass, no Critical issues

### CHECK 2 — Multi-agent cross-validation

Reflect:
- Did the student-simulator catch issues the spec-examiner missed (or vice versa)?
- If all three sub-agents produced identical flags, they may be pattern-matching rather than offering distinct lenses — flag this to the creator.

Write a brief "Review meta" section in SUMMARY.md noting which reviewer caught each Critical issue.

### STOP 2 — Present to creator

Show:
- Gate table (all 7 reviews)
- Top 5 Critical issues
- Count of Recommended / Minor
- Publish-gate status (OPEN / BLOCKED)

> "Review complete. Publish gate is {{OPEN / BLOCKED}}.
>
> - Critical issues: {{N}}
> - Recommended: {{N}}
> - Minor: {{N}}
>
> Options:
> 1. Apply all Critical fixes now — I'll re-run `/mock-3-draft --fix Q{{N}}` for each, then re-run this review.
> 2. Apply Critical + Recommended — same process, broader scope.
> 3. Defer and proceed to publish (only possible if gate is OPEN).
>
> Which?"

USER: choose.

### ACTION — Update project.json

- If all gates pass and creator chose to proceed: `gates.review: "pass"`, `phase: 5`, `nextStep: "/mock-5-publish"`.
- If fixes requested: set `nextStep: "/mock-3-draft --fix Q{{N}}"` for each; do not advance phase.

## Rules

- **Do not mark `gates.review: "pass"` unless CQI ≥ 43/50 AND all sub-reviews have no Critical issues.** Cobalt has no update/delete — bad questions published cannot be retracted.
- **Run sub-agents in parallel.** Single message, three Task calls.
- **Do not summarise away issues.** If a sub-agent flags something, surface it — even if another sub-agent disagrees. Disagreement is useful signal.
- **Re-runs are cheap.** Prefer running the review again after fixes over declaring a borderline paper "done".
