---
name: mock-5-publish
description: Phase 5 publishing. Gates on all review passes, converts SFMAs to Cobalt-ready payloads, uploads via the CMS's createQuestion MCP with batched consent, attaches spec-point IDs via updateQuestion, and writes the cross-qualification reuse map. Final phase of the mock paper pipeline.
user_invocable: true
arguments: ""
allowed-tools: Read, Glob, Grep, Write, Edit, Bash
---

# Mock Paper Publish (Phase 5)

You convert drafted SFMAs into Cobalt-ready payloads and upload them to the CMS. The CMS MCP supports `updateQuestion` for questions in `pending_review` status — corrections remain possible right up until publication. Once a question is moved to **published**, no further update/delete is allowed, so the gate before this phase is still a hard one.

Markers: `STOP:`, `ACTION:`, `CHECK:`, `[Conditional]`.

## Prerequisites

ACTION: Read `project.json`. Verify `gates.review == "pass"` and `phase >= 5`.

[Conditional: review not complete OR any review gate failing]
> STOP: "Phase 4 (review) hasn't passed. Current state: {{GATE_STATUS}}. Run `/mock-4-review` and address Critical issues before publishing. Once questions are moved to `published` they cannot be edited — we must not publish unreviewed content."

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

## Script

ACTION: Read `/cobalt-formatting` as a reference (the Cobalt markdown syntax rules).

### ACTION — Verify CMS connectivity

Check that the CMS MCP exposes the tools this skill needs: `createQuestion`, `updateQuestion`, `getCourseStructure`, `findQuestion`, `getMockExamStructure` (e.g. `mcp__sme-content__*`).

[Conditional: any tool missing]
> STOP: "The CMS MCP isn't fully configured. Need: createQuestion, updateQuestion, getCourseStructure, findQuestion, getMockExamStructure. Can't proceed with publish until these are reachable."

### STOP 1 — Destination identity

Ask the user for:

> "Before I fire anything at the CMS, I need:
>
> 1. **Your CMS user ID** (`cusr_...`) — stamped on every create/update call for audit trail. If you've told me before I'll have it saved in memory.
> 2. **Mock exam section ID(s)** — the `mepsec_...` IDs for each section of this paper (e.g. Section A, Section B). I can call `getMockExamStructure` with board / level / subject to look them up if you don't have them handy.
>
> Confirm both, or tell me to look them up."

USER: user ID + section IDs (or request lookup).

ACTION: Persist the section IDs to `project.json.publish.sectionIds` for re-runs. Save the user ID to memory if not already captured.

### ACTION — Per-question Cobalt conversion (strip and split)

For each SFMA in `Section A/Q*.md` and `Section B/Q*.md`:

1. **Read** the SFMA.
2. **Strip** the following (they don't belong in the Cobalt payload):
   - `# Question NN — Topic` title header
   - Horizontal rules (`---`)
   - `# Part a` / `## Problem` / `## Solution` structural headers (these become part boundaries + `problem`/`solution` fields in the payload)
   - `**Model Answer**` / `**End of Model Answer**` wrappers — **NOT a valid Cobalt callout**; leaving them in renders as plain bold text. They should never be in a well-drafted SFMA in the first place (see `/mock-3-draft` Rules), but strip defensively.
   - `$m{[N mark(s)]}{align=right}` in the Problem section for single-part questions — marks go in Cobalt's per-part `marks` field, not in the problem text.
   - **Keep** `{align=right}[N]` when it labels (i)/(ii) sub-parts inside a single part's problem.
3. **Split MCQ options** out of the problem into the `choices` array:
   - If the option text is a value, expression, or full statement → use that string as `content`
   - If the option is a letter-only reference to a diagram label or table row → pass `"content": ""` — Cobalt auto-renders the A/B/C/D labels; passing the letters as content duplicates them
   - Set `is_correct: true` on the correct choice; positional order determines which letter is which (first choice = A, second = B, etc.)
4. **Structured-question shared stems:** embed the shared question stem in **Part (a)'s `problem` field**. Subsequent parts contain only their own sub-question. Students refer back to part (a) for stem context.
5. **Sub-parts (i)/(ii):** keep as a single Cobalt part with combined marks (e.g. 2+2 = 4) and inline `{align=right}[2]` indicators preserving the split in the problem text.
6. **Image placeholders:** convert local `[IMAGE: …]` references to Cobalt form:
   - If a CDN URL is available → `![alt text](https://cdn.savemyexams.com/uploads/...)`
   - If no CDN URL → `{align=center} **[DIAGRAM: full alt-text]**` — flag for manual attachment post-upload via Cobalt UI or `updateQuestion` once the CDN URL is known
7. **(Optional audit trail)** Write the converted payload preview to `publish/Q{{NN}}-cobalt.md`.

### STOP 2 — Upload consent (batched preview)

Present a consolidated table of every question to be uploaded:

> "Ready to upload {{N}} questions to section {{section_id}} via `createQuestion`. Preview:
>
> | Q | Topic | Parts | Marks | Difficulty | Calc | Image? | Stem preview |
> |---|---|---|---|---|---|---|---|
> | Q01 | … | … | … | … | … | … | "…" |
> | … | … | … | … | … | … | … | "…" |
>
> Conventions applied:
> - Questions are created with status `pending_review` — edits remain possible via `updateQuestion` until publication.
> - {{N_WITH_IMAGES}} questions have `[DIAGRAM: …]` placeholders needing manual attachment post-upload.
> - {{N_CW_OMITTED}} questions have `command_word` omitted because the approved board CW isn't in the MCP enum (e.g. Edexcel's 'Criticise'). The problem text still contains the correct CW so students see it.
> - Distractor explanations are paragraphs (not bullets). `**Model Answer**` wrappers stripped. Letter-only MCQ choices have empty content (Cobalt auto-renders labels).
>
> Fire all {{N}} uploads in parallel? (yes / abort / review-specific-questions)"

USER: yes / abort / partial.

[Conditional: abort] Stop the script.

[Conditional: partial] Loop over user-specified questions with per-question preview and individual consent.

### ACTION — Fire uploads in parallel

For each approved question, call `createQuestion` with:
- `cms_user_id`
- `question_set_id` (the relevant Section mepsec_xxx)
- `difficulty` (easy / medium / hard / very_hard from per-question tracker)
- `style: "exam_whole"` (or as appropriate)
- `comment`: short per-question note (e.g. "Paper 1 Section A Q2 — v-t graph projectile")
- `parts`: array (1 for MCQ, N for multi-part structured)

For each part:
- `question_type`: `multiple_choice` or `structured`
- `marks`: integer
- `problem`: markdown (stem + sub-question; MCQ has stem only, no A/B/C/D options listed)
- `solution`: markdown (model answer + MS&G + ET&T)
- `command_word`: from `.project/command-word-list.md` — **if the approved CW isn't in the MCP enum, omit the field** and keep the word in the problem text
- `calculator`: `allowed` / `not_allowed` / `not_applicable`
- `format`: omit by default; set `extended_response` for starred/QWC extended-response parts
- `choices` (MCQ only): array of `{content, is_correct}` objects
- `source: "original_content"`

Log results to `publish/upload-log.md` and update `project.json.questions[N]` with `uploaded: true`, `uploadedAt`, `cobaltId`.

[Conditional: any upload fails] STOP. Diagnose and ask the user before retrying.

### ACTION — Attach spec-point IDs (updateQuestion pass)

1. Call `getCourseStructure({course_id: <crs_xxx>})` once to retrieve all spec points for the course. Build a name → ID lookup map.
2. For each question, map each part's content to 1–3 spec points using the project's Master Syllabus CSV (`references/{{BOARD}}-Master-Syllabus.csv` or equivalent).
3. Fetch all uploaded questions via `findQuestion({question_ids: [...]})` to get each part's `part_id` (`qstnprt_xxx`). **Note:** this can return a large payload; if it exceeds the tool-call limit, the harness writes it to disk — extract the ID mapping with `python` or `jq`.
4. Fire `updateQuestion` in parallel, one call per question:
   ```
   {
     cms_user_id,
     question_id: "qstn_xxx",
     comment: "Attach spec-point IDs per Master Syllabus",
     update_parts: [
       {id: "qstnprt_xxx", spec_point_ids: ["spcpt_xxx", ...]},
       ...
     ]
   }
   ```
5. Append the spec-point mapping table to `publish/upload-log.md`.

### CHECK 1 — All uploads logged and tagged

After all uploads + spec-point patches, verify:
- Every `questions[N].uploaded` is `true` or `"skipped"`
- Every uploaded question has a `cobaltId`
- `publish/upload-log.md` has a row per question with Cobalt ID + spec-point mapping
- Diagrams awaiting manual attachment are listed in the log under "Post-upload actions required"

### ACTION — Cross-qualification reuse map

For each question, consult the Master Syllabus and tracker CSV's "Suitable for ..." column:
- Identify which sister qualifications could reuse this question
- Identify blockers (spec points unique to this qualification, board-specific command words, etc.)

Write to `publish/reuse-map.md` using `.claude/templates/reuse-map.template.md`.

### ACTION — Update project.json

Set `gates.publish: "pass"`, `phase: 5`, `status: "complete"`, `nextStep: "/handover"`.

### ACTION — Invoke /handover

Trigger the `/handover` skill automatically to capture the session summary.

### Final output

```
Publish complete for {{PROJECT_NAME}}.

Uploaded: {{N}} questions to Cobalt (all pending_review)
Spec-point IDs attached: {{N}} questions / {{M}} parts
Diagram placeholders awaiting manual attachment: {{N}}
Command-word omissions (enum gap): {{N}}

Artefacts:
- publish/upload-log.md      (Cobalt IDs + spec-point mapping + image-attach list)
- publish/reuse-map.md
- publish/Q*-cobalt.md        (converted SFMAs, optional audit)

Next:
- Attach {{N}} diagrams via the Cobalt UI, or supply CDN URLs for an updateQuestion patch
- Content review in Cobalt CMS by the reviewer
- When content is finalised, move questions from pending_review → published
  (no update/delete after that point)
```

## Rules

- **NEVER upload on a failed publish gate.** Published questions cannot be edited or deleted.
- **Batched preview + single consent before upload.** Do not fire `createQuestion` without showing the consolidated table first. For most mock papers this is the efficient default; use per-question STOP only if the user requests it or the content is unusually sensitive.
- **`updateQuestion` is available for `pending_review` questions** — treat upload as a checkpoint, not an irrevocable commit. Fixes after upload are cheap.
- **Strip `**Model Answer**` wrappers during conversion.** They are not a valid Cobalt callout and would render as plain bold text. (They should never be in a well-drafted SFMA anyway — see `/mock-3-draft` Rules.)
- **Log every upload and spec-point patch** to `publish/upload-log.md` — it's the recoverability record if the MCP hiccups.
- **If the CMS MCP is unavailable,** STOP. Do not try to fall back to manual upload; the authoring team needs the Cobalt IDs to route content correctly.
- **`command_word` enum may have gaps** for some board-specific command words (e.g. Edexcel's 'Criticise'). Omit the field rather than force a mismatch; preserve the word in the problem text so students see it.
