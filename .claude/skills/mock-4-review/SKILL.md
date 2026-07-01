---
name: mock-4-review
description: Phase 4 composite review. Runs NotebookLM typicality, spec-check, assessment-design-checklist, three sub-agent reviews (spec-examiner, student-simulator, marking-realism-checker) in parallel, the CQI scorecard, and a breadth-and-variety re-check on the drafted paper. Consolidates into reviews/SUMMARY.md. Mandatory before /mock-5-publish.
user_invocable: true
arguments: ""
allowed-tools: Read, Glob, Grep, Write, Edit, Bash, Task
---

# Mock Paper Review (Phase 4)

You orchestrate every quality gate. Today these skills exist in isolation (`/spec-check`, `/review-cqi`, the assessment-design-checklist context file) — this skill wires them into a single mandatory review flow so nothing sits orphaned.

## Success Criteria

The publish gate (`gates.review: "pass"`) opens only when every review below verifies. Log each outcome to `project.json.reviews.*` as named. Do not advance `phase` to 5 if any Critical issue is open.

**Publish-gate criteria (all must verify):**
1. NotebookLM typicality → verify: Review 1 (`/review-questions` → `reviews/notebooklm-review.md`)
2. Spec alignment → verify: Review 2 (`/spec-check` → `reviews/spec-check.md`)
3. Assessment design checklist (8 per-question + 3 paper-level) → verify: Review 3 (`reviews/assessment-design.md`)
4. spec-examiner: no Critical → verify: Review 4a (`reviews/spec-examiner.md`)
5. student-simulator: no Critical → verify: Review 4b (`reviews/student-simulator.md`)
6. marking-realism-checker: no Critical → verify: Review 4c (`reviews/marking-realism.md`)
7. CQI total ≥ 43/50 with no Critical-tier criterion below 5 → verify: Review 7 (`reviews/cqi-scorecard.md`)
8. Breadth & variety re-verified on the drafted questions (per-AO command-word/task spread, difficulty distribution, context freshness) → verify: Review 8 (`reviews/breadth-variety.md`)

**Consolidation:** `reviews/SUMMARY.md` ticks each gate pass/pass-with-issues/fail and aggregates Critical/Recommended/Minor deduplicated across reviewers. Publish gate is OPEN only if every numbered criterion above passes AND no Critical issue remains in the consolidated list.

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
> 6. Breadth & variety audit — re-checks per-AO variety, difficulty distribution and context freshness on the drafted questions (drafts can regress from a varied outline)
>
> Everything writes to `reviews/`. This will take a while — roughly 10-15 minutes of tool calls. OK to proceed?"

USER: confirm.

### ACTION — Review 1: NotebookLM typicality (word-for-word, one question at a time)

This is a **permanent fixture** of `/mock-4-review`. Every drafted question goes to NotebookLM verbatim, one at a time — no batching, no summarising, no skipping.

Invoke `/review-questions` via the Skill tool. That skill enforces:

1. **Word-for-word submission** — extract each question's `## Problem` sections (stem + every part) verbatim, preserving all markdown, equations, alignment tags, image placeholders, mark indicators, and sub-part numbering. Do not paraphrase, summarise, abbreviate, or rewrite.
2. **Section-appropriate batching** — Section A (MCQs) is submitted as a **single batched prompt** covering the whole section, because the cohesion verdict on format variety only works at section level. Section B (SQs) is submitted **one question at a time**, sequentially. See `/review-questions` Step 3 for the canonical prompt templates (Section A MCQ batched, Section B SQ per-question, whole-paper). These templates are the refined versions from the 2026-05-06 Paper 2 review — they specify the 1–5 rating scale, demand a named past-paper parallel, and enumerate what counts as a flag.
3. **Whole-paper prompt last** — after Section A's batched response and every Section B SQ response have been captured, submit the whole-paper review prompt to assess topic coverage, balance, and overall paper-level typicality.
4. **Verbatim capture** — record each NotebookLM response unedited in `reviews/notebooklm-review.md`. Do not summarise the response before logging.

[Conditional: NotebookLM MCP unavailable / auth expired]
> ACTION: Run `nlm login` via Bash to refresh authentication. If the MCP is genuinely unavailable, fall back to Playwright as `/review-questions` Step 4 describes — but DO NOT skip this review and DO NOT batch the questions to save time.

Output: `reviews/notebooklm-review.md`. Log to `project.json.reviews.notebookLmTypicality = {"status": "...", "file": "...", "questionsSubmitted": N, "wholePaperPromptSubmitted": true}`.

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

### ACTION — Review 8: Breadth & variety audit

The outline gates variety, breadth and difficulty (`/mock-2-outline` CHECK 10/11/12), but **drafts can regress from a varied outline** — a planned format collapses into a repeated archetype, or a part drifts easier. Re-verify on the ACTUAL drafted questions. This is the lens that would have caught Paper 1's biggest process gap: a paper that passed every other gate (CQI 48/50, typicality 5/5) was still re-scoped by hand afterwards for variety, breadth and difficulty.

Read the drafted stems + command words, `.project/catalogues/ao-breadth-map.md`, `.project/difficulty-targets.md`, and the approved outline. Check:

1. **Per-AO variety** — the command words / task types actually used per AO. Flag any AO where a single command word exceeds ~50% of its marks, or fewer than 3 distinct command words/task types are used, or the drafts have regressed from the outline's planned spread.
2. **Difficulty distribution** — the drafted LoD spread vs `difficulty-targets.md` (≥ target hard parts, ≥ target accessible openers, overall mix). Flag softening/hardening away from target.
3. **Context/format freshness** — each question's context archetype + distinctive format (MCQ format + Section B context/graph type). Flag any two questions sharing a context archetype or format unless intended.

Write to `reviews/breadth-variety.md`. **Severity:** a **monotone AO** (one command word > ~60% of an AO's marks) or a **difficulty distribution that misses the `difficulty-targets.md` minimums** is a **Critical** publish-blocker — this was the dominant reason Paper 1 needed a large post-gate rework. Lesser variety/freshness concerns are Recommended.

Log to `project.json.reviews.breadthVariety = {"status": "...", "file": "reviews/breadth-variety.md", "critical": [...]}`.

### CHECK 1 — Aggregate & consolidate

Read all 8 review files. Build the consolidated summary at `reviews/SUMMARY.md` using `.claude/templates/review-summary.template.md`:

- Tick each gate as pass / pass with issues / fail
- Aggregate Critical issues (would-block-publish), Recommended, Minor — deduplicated across reviews
- Flag the publish gate as OPEN only if: CQI ≥ 43/50, all sub-reviews ≥ pass, no Critical issues

#### Triple-consensus elevation rule

When deduplicating issues across reviewers, count how many distinct reviewers flagged each issue (NotebookLM, spec-check, assessment-design, spec-examiner, student-simulator, marking-realism, CQI, breadth-variety). Then apply:

- **≥ 3 reviewers flagged the same issue** (even at different severities — e.g. one Major + two Minor) → **auto-elevate to Critical**. Reviewer agreement across independent lenses is strong evidence that the issue is real, regardless of how each individual reviewer rated severity.
- **2 reviewers flagged the same issue** → keep at the highest-rated severity of the two.
- **1 reviewer** → keep at the original severity.

Add a `Reviewers` column to the Critical / Recommended / Minor issue tables in SUMMARY.md showing the count and the reviewer names. Example:

| # | Issue | Q | Original max severity | Reviewers | Elevated? | Final severity |
|---|---|---|---|---|---|---|
| 1 | Q15(c) ET&T duplicates MS&G | 15 | Major (spec-examiner) | 3 (spec-examiner Major, student-simulator Minor, marking-realism Recommended) | **Yes** | **Critical** |
| 2 | Q8 stem ambiguity | 8 | Major (student-simulator) | 1 | No | Major |

**Why this rule exists:** During the 2026-04-21 Paper 1 re-review, Q15(c) duplicate ET&T was flagged independently by all three sub-agents at different severities. The orchestrator merged findings without weighting by reviewer agreement, so the issue ended up listed as Major rather than Critical. Triple-lens consensus on the same root cause is a strong signal — if three independent reviewers using different lenses converge on the same issue, treat it as Critical even if no individual reviewer used that word.

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

- **Do not mark `gates.review: "pass"` unless CQI ≥ 43/50 AND all sub-reviews have no Critical issues.** Cobalt has no update/delete on published questions — bad questions published cannot be retracted (questions in `pending_review` can still be patched via `updateQuestion`).
- **Run sub-agents in parallel.** Single message, three Task calls.
- **NotebookLM Review 1 is non-skippable and word-for-word.** Every question's stem is submitted verbatim via `/review-questions`. Section A MCQs are sent as a single batched prompt for the whole section (cohesion verdict needs section-level scope); Section B SQs are sent one at a time. No summarising, no shortcut "I already know this question is fine", no skipping the whole-paper prompt at the end. The per-section + per-SQ + whole-paper sequence catches typicality and cohesion issues that no other gate in the pipeline finds. Two re-review passes on Paper 2 (2026-05-06) showed that NotebookLM and the sub-agents catch different issue classes — both are required.
- **Do not summarise away issues.** If a sub-agent or NotebookLM flags something, surface it — even if another reviewer disagrees. Disagreement is useful signal.
- **Re-runs are cheap.** Prefer running the review again after fixes over declaring a borderline paper "done".
