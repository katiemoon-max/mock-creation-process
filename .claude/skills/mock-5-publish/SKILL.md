---
name: mock-5-publish
description: Phase 5 publishing. Gates on all review passes, converts SFMAs to Cobalt format, uploads via SME createQuestion MCP (per-question STOP for safety — questions in `pending_review` can still be patched via `updateQuestion`, but no update/delete is possible once published), and writes the cross-qualification reuse map. Final phase of the mock paper pipeline.
user_invocable: true
arguments: ""
allowed-tools: Read, Glob, Grep, Write, Edit, Bash
---

# Mock Paper Publish (Phase 5)

You convert drafted SFMAs into Cobalt-formatted files and upload them to the CMS. Cobalt has a critical constraint: **once a question is published, no update or delete is possible**. Questions in `pending_review` can still be patched via `updateQuestion` (so review-fix sweeps after upload are supported), but once they move to `published` the only recourse is manual intervention in the Cobalt UI. This skill is therefore deliberately cautious — per-question STOP before each upload.

Markers: `STOP:`, `ACTION:`, `CHECK:`, `[Conditional]`.

## Prerequisites

ACTION: Read `project.json`. Verify `gates.review == "pass"` and `phase >= 5`.

[Conditional: review not complete OR any review gate failing]
> STOP: "Phase 4 (review) hasn't passed. Current state: {{GATE_STATUS}}. Run `/mock-4-review` and address Critical issues before publishing. Once a question moves from `pending_review` to `published`, no update or delete is possible — we must not publish unreviewed content."

### CHECK 0 — Publish gate (HARD GATE)

Verify ALL of:
- `project.json.reviews.cqiScore.pass == true` (CQI ≥ 43/50)
- `project.json.reviews.notebookLmTypicality.status == "pass"`
- `project.json.reviews.specCheck.status == "pass"`
- `project.json.reviews.specExaminer.status == "pass"`
- `project.json.reviews.studentSimulator.status == "pass"`
- `project.json.reviews.markingRealism.status == "pass"`
- `project.json.reviews.assessmentDesign.status == "pass"`
- Zero unresolved Critical issues in `reviews/SUMMARY.md`

[Conditional: any gate fails]
> STOP: "Publish gate is BLOCKED: {{FAILED_GATES}}. Do not proceed. Go back to `/mock-3-draft` to fix, then re-run `/mock-4-review`."

### CHECK 0.5 — Spec-point matching pre-flight (HARD GATE)

Every question part must be cleanly mappable to one or more **specific** specification points BEFORE upload. "Cleanly mappable" means:

- The named quantities, formulas, and concepts in the part appear verbatim or as a close paraphrase in the spec point's stated learning objective
- No "judgement-call" surrogate tagging — the pattern "the closest spec point is X but the question actually tests Y, which isn't named anywhere in the spec" is FORBIDDEN
- For multi-tag parts, at least ONE tag must be a clean primary match (supporting tags are allowed)

**Why this gate exists:** Surrogate tagging at upload time is how off-spec content slipped past the pipeline before. The 2026-05-05 Edexcel 9PH0 Paper 1 Q3 incident — μ-based friction MCQ uploaded under surrogate tags 2.9 (Newton's 2nd Law) + 2.10 (Mass/Weight), then redesigned post-publish — was caused by treating spec-point matching as a soft flag rather than a hard gate. From now on: no clean match → no upload.

**Procedure:**

1. ACTION: Read the project's Master Syllabus CSV (path in `project.json.qualityGates.masterSyllabusPath`) and call `mcp__sme-content__getCourseStructure` for the project's course to retrieve the live `spcpt_` ID list.

2. For each question part, identify the candidate spec point(s). Record a one-line **match rationale** stating exactly which spec-point learning objective the part tests, citing the spec-point name verbatim.

3. CHECK each part's match rationale against this rubric:
   - ✓ The rationale names a concept that appears in the spec point's stated objective.
   - ✗ The rationale uses hedging language: "closest match", "approximate", "the part tests Y, which is similar to spec point X", "judgement call", "no exact match — using nearest neighbour".

4. [Conditional: any part has no clean match — i.e. every candidate spec point requires hedging]
> STOP: "Spec-point matching FAILED for {{PARTS}}. The following parts cannot be cleanly mapped to a specification point:
>
> {{PART_LIST_WITH_RATIONALES}}
>
> This is evidence of off-spec content. Do NOT upload.
>
> Route the part(s) back to `/spec-check` (use the Spec-Vocabulary Grep gate) or to `/mock-3-draft` for redesign. The 2026-05-05 Q3 friction incident on Edexcel 9PH0 Paper 1 was caught here, too late: surrogate-tagged with N2L+Mass/Weight when the actual content (coefficient of kinetic friction) was not in the Edexcel spec at all. We do not surrogate-tag any more."

5. [Conditional: every part has a clean primary match]
   - Record `spec_point_ids` and the match rationale per part in `publish/upload-log.md` BEFORE conversion begins (so the rationale is auditable even if upload is later abandoned).
   - Proceed to Cobalt conversion.

## Script

ACTION: Read `/cobalt-formatting` as a reference (the Cobalt markdown syntax rules).

### ACTION — Per-question Cobalt conversion

For each question file in `Section A/Q*.md`:

1. Read the SFMA
2. Apply Cobalt conversion:
   - Ensure `# Part a` / `## Problem` / `## Solution` structure
   - Verify `$m{[N mark(s)]}{align=right}` on every part
   - Verify `$f{...}` wraps final answers, `$w{...}` working, `$c{...}` commentary
   - Verify `**Mark Scheme and Guidance**` ... `**End of Mark Scheme and Guidance**` callout blocks (not headings)
   - Verify `**Examiner Tips and Tricks**` ... `**End of Examiner Tips and Tricks**` callouts
   - Verify all equations use `$$...$$` (never `$...$`)
   - Verify `^…^` / `~…~` for superscript/subscript (never Unicode)
   - Verify no `---` horizontal rules, no emoji, no checkmarks
3. Write the converted file to `publish/Q{{NN}}-cobalt.md`
4. Log conversion to `project.json.questions[N].formatted = true`

### STOP 1 — First file review

> "Q01 converted to Cobalt format at `publish/Q01-cobalt.md`. Please skim it — does the format look right? If you spot any issue, I'll fix before converting the rest."

USER: confirm or request fixes.

[Conditional: issues] Fix the conversion logic, re-run Q01, ask again.

### ACTION — Convert remaining questions

After Q01 is approved, convert Q02–QN to `publish/Q{{NN}}-cobalt.md`.

### STOP 2 — Upload consent

> "All {{N}} questions converted to Cobalt format. Ready to upload via SME `createQuestion` MCP.
>
> **Reminder on Cobalt edit window:** questions land in `pending_review` and can still be patched via `updateQuestion` while in that state. Once Katie moves them to `published` via the Cobalt UI, no update or delete is possible.
>
> Two options for STOP cadence:
> 1. **Per-question STOP** (default for sensitive papers — fewer than 6 questions, or unusual content): I'll STOP before each upload so you can approve each one. Safer, slower.
> 2. **Consolidated preview + batch fire** (default for routine papers — 10+ questions, all gates passed cleanly): I'll show you a single preview table (Q#, topic, difficulty, marks, stem first line) and fire all uploads in parallel after one approval. Validated on the 2026-04-22 Paper 1 publish.
>
> Which cadence?"

USER: choose cadence + confirm.

### Upload — branch by cadence chosen at STOP 2

[Conditional: per-question cadence]

For each question, upload with per-question STOP:

#### STOP (per question) — Upload confirmation

> "Uploading Q{{NN}}: {{TOPIC}}, {{MARKS}} marks.
>
> Preview: {{STEM_FIRST_LINE}}...
>
> Confirm upload? (yes / skip / abort)"

USER: yes / skip / abort.

[Conditional: consolidated cadence]

Present a single preview table covering every question:

```
| Q  | Topic              | AO    | Marks | Difficulty | Stem first line                        |
|----|--------------------|-------|-------|------------|-----------------------------------------|
| 01 | Photoelectric MCQ  | AO1   | 1     | M          | Monochromatic light is incident on...   |
| 02 | ...                | ...   | ...   | ...        | ...                                     |
```

#### STOP — Batch upload confirmation

> "Preview table above shows all {{N}} questions ready for upload. Fire all in parallel? (yes / abort / drop-back-to-per-question)"

USER: yes / abort / drop-back.

[Conditional: yes] Fire all `createQuestion` calls in parallel (single message, N tool calls). Report Cobalt IDs in a table.

[Conditional: drop-back] Resume the per-question cadence above starting from Q01.

[Conditional: skip] Move to next question; log `project.json.questions[N].uploaded = "skipped"`.

[Conditional: abort] Stop the script entirely; log whichever questions have uploaded so far.

[Conditional: yes]

#### ACTION — Upload via SME MCP

Call the SME `createQuestion` MCP tool (exact tool name depends on the SME MCP; check available `mcp__sme__*` tools).

Log result to `publish/upload-log.md`:
```markdown
- {{DATETIME}} — Q{{NN}}: {{RESULT}} (Cobalt ID: {{ID}})
```

Update `project.json.questions[N].uploaded: true`, `uploadedAt: "{{DATETIME}}"`, `cobaltId: "{{ID}}"`.

[Conditional: upload failed] STOP — do NOT proceed to next question. Diagnose the failure.

### CHECK 1 — All uploads logged

After all questions processed, verify:
- Every `questions[N].uploaded` is `true` or `"skipped"` (not `false`/`null`)
- Every uploaded question has a `cobaltId`
- `publish/upload-log.md` has a line per question

### ACTION — Cross-qualification reuse map

For each question, consult the Master Syllabus and tracker CSV's "Suitable for ..." column:
- Identify which sister qualifications could reuse this question
- Identify blockers (spec points that are unique to this qualification)

Write the reuse map to `publish/reuse-map.md` using `.claude/templates/reuse-map.template.md`.

### ACTION — Update project.json

Set `gates.publish: "pass"`, `phase: 5`, `status: "complete"`, `nextStep: "/handover"`.

### ACTION — Invoke /handover

Trigger the `/handover` skill automatically to capture the session summary and back up the vault.

### Final output to user

```
Publish complete for {{PROJECT_NAME}}.

Uploaded: {{N}} questions to Cobalt
Skipped: {{N}}
Failed: {{N}} (see publish/upload-log.md)

Artefacts:
- publish/Q*-cobalt.md (converted files)
- publish/upload-log.md
- publish/reuse-map.md

Reuse potential:
- {{TARGET_QUAL_1}}: {{N}} questions reusable
- {{TARGET_QUAL_2}}: {{N}} questions reusable

The project is complete. /handover has been triggered to checkpoint the session.
```

## Rules

- **NEVER upload on a failed publish gate.** This is the single most important rule in this skill. Better to ship late than ship bad content that needs Cobalt-UI patching after publish.
- **NEVER upload without a clean spec-point match.** Surrogate spec-point tagging is forbidden — if the closest spec point requires hedging language ("approximately", "judgement call", "nearest neighbour"), the question is off-spec and must be redesigned, not tagged-and-uploaded. CHECK 0.5 enforces this.
- **Upload cadence is creator's choice at STOP 2.** Per-question STOP for sensitive content (few questions, novel formats); consolidated preview + batch fire for routine papers with all gates passed cleanly. Default to per-question only when creator does not specify.
- **`updateQuestion` is available while a question is in `pending_review`** — so fix sweeps after upload are supported, but only inside that edit window. Plan review-fix sweeps before Katie moves anything to `published` in the Cobalt UI.
- **After any post-gate rework in Cobalt, run `/cobalt-sync --full`.** If questions are edited or re-scoped in the Cobalt UI after upload — whether a fix sweep in `pending_review` or a later content rework — the local SFMA files, tracker and project.json drift from the shipped paper. Session-startup `--check` only catches header drift (marks, parts, status); it does NOT catch content changes such as a changed context, stem or command word. Run `/cobalt-sync --full` after the rework so the local mirror and any evaluation artefacts track what actually shipped. (Paper 1's local Section B mirror drifted for weeks after a 2026-05-22 rework because only `--check` ever ran — the local files still showed a conical pendulum long after Cobalt had moved to a washing-machine-drum question.)
- **Log every action to `publish/upload-log.md`** — if something goes wrong with the MCP, the log is the only recoverability path.
- **If the SME MCP is unavailable,** STOP and tell the user — do not skip to "manual upload".
