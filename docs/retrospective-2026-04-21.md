# Pipeline Retrospective — 2026-04-21

First end-to-end run of Phase 3 (`/mock-3-draft`) and Phase 4 (`/mock-4-review`) on Edexcel A Level Physics Paper 1 Mock. Pipeline shipped all 19 SFMAs and all 7 reviews; the CQI gate correctly blocked publication on a Critical-tier failure. Notes below are the pipeline-level improvements that this real-world run surfaced — feed back into the skills/agents on the next revision.

## What worked

- **Phase 3 batch-of-3 rhythm with a per-question review pause only for the first structured question.** The CHECK-1 constraint reload at the start of every batch kept exclusion list / AO targets / misconception bank citations consistent across 19 questions with no drift. After Q11's review, the user explicitly confirmed batch-then-review-at-end was the right cadence.
- **Stem-only phase + information-leakage + stem-usage audits.** Caught 8 genuine defects before model-answer writing: 3 × decorative-values, 2 × info-leakage, 1 × physics-inconsistency (Q13 conical pendulum), 2 × contradictions. Zero of these would have been caught by post-hoc review.
- **Phase 4 multi-agent cross-validation produced genuinely distinct findings.** No echo-chamber pattern. Q13 unused-L caught only by `student-simulator`; Q14d/Q17d missing-ecf caught only by `marking-realism-checker`; Q17 out-of-spec formula caught only by `spec-examiner`. The 3-lens design pays off.
- **CQI Critical-tier gate correctly blocked publication.** Paper scored 43/50 numerically (the historic pass threshold) but failed the Critical-tier rule on Criterion 1 (Specific = 3/5). Without the tier-gate, the paper would have been waved through despite an AQA-native formula embedded in 10 marks of Edexcel content. This gate is load-bearing.

## What needs fixing in the pipeline

### 1. `/spec-check` misses formula-sheet intrusions

**What happened:** Q17 used `C = ε₀A/d`. This is NOT in Edexcel 9PH0's formulae sheet (Appendix 8) or spec content — it belongs to AQA 7408 and Edexcel IAL A2 Physics. The error cascaded through Q17(b), (c), (d) — 10 marks of the paper.

**What reviewer caught it:** `spec-examiner`, by explicitly reading the formulae sheet.

**What missed it:** `/spec-check`, whose prompt focuses on topic-scope (is content within the paper's topic set?) rather than formula-scope (is every equation in the board's formulae sheet or the spec content?).

**Fix:** add to `/spec-check` SKILL.md — a mandatory cross-reference against the board's formulae sheet for every equation used in the paper. The check list item should be: "For every equation a student must use, confirm it appears in (a) the board's formulae sheet, OR (b) the spec content, OR (c) is derivable from (a)+(b) without going outside-spec."

### 2. Sub-agent "no-write" rule conflicts with `/mock-4-review` file expectations

**What happened:** The 5 sub-agents (`spec-examiner`, `student-simulator`, `marking-realism-checker`, `quality-reviewer`, `exam-researcher`) all have a blanket system-level instruction: "Do NOT Write report/summary/findings/analysis .md files. Return findings directly as your final assistant message."

`/mock-4-review` dispatches these sub-agents with explicit file-write instructions in the prompt. Agents consistently prioritised their system-level no-write rule over the prompt's write instruction, returned the full report as text output, and noted they couldn't write the file. The orchestrator (parent agent) had to write the files manually from the returned text.

**Outcome:** Not broken — end-to-end the reviews got written. But 4/5 review files were written by the orchestrator after the fact, adding a round-trip. And in a streaming scenario, the text-outputs count against context more than direct file writes would.

**Fix options:** (a) carve an exception in the sub-agent definitions for "files whose path is explicitly named in the invocation prompt" — rewriting the rule as "do not write files unless the invoking prompt names a specific path"; (b) or document in `/mock-4-review` that text-out + orchestrator-writes is the intended handoff, and simplify the prompts so they're not asking the sub-agents to write. Option (a) is cleaner for Phase 4 ergonomics; option (b) is simpler to implement.

### 3. Recurring centripetal-motion "Describe vs Explain" trap

**What happened:** Two separate questions (Q13b conical pendulum, Q16a banked track) used "Describe how the horizontal component of [tension / normal force] provides the centripetal force" with mark schemes that rewarded causal reasoning ("produces/supplies the centripetal acceleration"). Both are "Explain" demand per Edexcel's command-word definition, not "Describe". Flagged independently by `spec-examiner`, `marking-realism-checker`, CQI, NotebookLM typicality.

**Pattern:** Centripetal-motion narratives are naturally causal ("the [component] **provides** the centripetal force"), so drafters default to "Describe" but the MS ends up rewarding explanation.

**Fix:** Add a named pitfall to `board-conventions.template.md` (under a "Common drafting traps" section): "Centripetal-force questions using 'provides' in the stem are Explain demand, not Describe. Use the 'Explain' command word when the MS rewards causal linkage." Applies across boards, not just Edexcel.

### 4. `/mock-3-draft` lacks a "spec-check-lite" on each drafted question

**What happened:** The out-of-spec `C = ε₀A/d` formula was not caught at Phase 3 drafting time. It was only caught 19 questions later during Phase 4 review. If Phase 3 had a self-check on formulae used per question ("does each equation I've used appear in the formulae sheet or the spec?"), Q17 would have been caught in-place rather than triggering a fix-loop across the whole paper.

**Fix:** Add a per-question CHECK to `/mock-3-draft` (before the model-answer assembly): "For every equation or law used in the model answer, confirm it is on the formulae sheet or in the spec content. If not, stop and flag."

### 5. "Show that" frequency guardrail missing from `/mock-2-outline`

**What happened:** Paper ended with 5 × "Show that" parts (Q11b, Q14b, Q15b, Q17b, Q18b). Edexcel typical range 2017–2024 is 2–4 (mean 2.6). Nothing in `/mock-2-outline` tracked this; the count only surfaced during Phase 4 NotebookLM review.

**Fix:** Add a "Show-that count" check to `/mock-2-outline` CHECK list — cap at the top of the observed board range (value read from `.project/board-conventions.md`).

### 6. Sub-agent review output volumes are high

**What happened:** `spec-examiner` returned ~2,500 tokens; `student-simulator` ~4,500; `marking-realism-checker` ~5,000; CQI scorecard ~4,000. In aggregate Phase 4 returned ~20,000 tokens of text that the orchestrator had to parse to build `SUMMARY.md`.

**Possible fix:** add a structured-output contract to each sub-agent — one section for `CRITICAL`, one for `RECOMMENDED`, one for `MINOR`, one for `ONE_LINE_SUMMARY`, each tagged with the question number. Makes parsing reliable and reduces the orchestrator's synthesis burden. Optional — the current free-form narrative output is also human-readable and useful as a stand-alone review document.

## Counts for this run

| Metric | Value |
|---|---|
| SFMAs drafted | 19 (10 MCQ + 9 structured) |
| Diagrams generated | 11 blank + 3 answer |
| Stem revisions during drafting | 8 |
| New misconceptions added to bank | 4 (M088–M091) |
| Phase 4 sub-agents dispatched | 5 (spec-examiner, student-simulator, marking-realism-checker, general-purpose × 2) |
| Phase 4 reviews written | 7 |
| Critical issues flagged | 9 |
| Recommended issues flagged | 13 |
| Minor issues flagged | 8 |
| CQI score | 43/50 (pass on total, fail on Critical-tier) |
| Publish gate | BLOCKED |

## Single largest-impact pipeline improvement to make first

**Add formula-sheet cross-reference to `/spec-check`.** It's a 3–4 line prompt addition that would have caught the single Critical-tier blocker in this run.
