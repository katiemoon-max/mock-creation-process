---
name: mock-5-publish
description: Phase 5 publishing. Gates on all review passes, converts SFMAs to Cobalt format, uploads via SME createQuestion MCP (per-question STOP for safety — no update/delete in Cobalt after creation), and writes the cross-qualification reuse map. Final phase of the mock paper pipeline.
user_invocable: true
arguments: ""
allowed-tools: Read, Glob, Grep, Write, Edit, Bash
---

# Mock Paper Publish (Phase 5)

You convert drafted SFMAs into Cobalt-formatted files and upload them to the CMS. Cobalt has a critical constraint: **no update or delete after creation**. Once uploaded, corrections require manual intervention in the Cobalt UI. This skill is therefore deliberately cautious — per-question STOP before each upload.

Markers: `STOP:`, `ACTION:`, `CHECK:`, `[Conditional]`.

## Prerequisites

ACTION: Read `project.json`. Verify `gates.review == "pass"` and `phase >= 5`.

[Conditional: review not complete OR any review gate failing]
> STOP: "Phase 4 (review) hasn't passed. Current state: {{GATE_STATUS}}. Run `/mock-4-review` and address Critical issues before publishing. Cobalt has no update/delete — we must not publish unreviewed content."

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

> "All {{N}} questions converted to Cobalt format. Ready to upload via SME `createQuestion` MCP. **Reminder: once uploaded, Cobalt has no update/delete — corrections must be made manually in the Cobalt UI.** I'll STOP before each upload so you can approve each one. Proceed?"

USER: confirm.

### For each question, upload with per-question STOP:

#### STOP (per question) — Upload confirmation

> "Uploading Q{{NN}}: {{TOPIC}}, {{MARKS}} marks.
>
> Preview: {{STEM_FIRST_LINE}}...
>
> Confirm upload? (yes / skip / abort)"

USER: yes / skip / abort.

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

- **NEVER upload on a failed publish gate.** This is the single most important rule in this skill. Better to ship late than ship bad content that cannot be corrected.
- **Per-question STOP before upload is mandatory.** Do not batch upload silently.
- **Log every action to `publish/upload-log.md`** — if something goes wrong with the MCP, the log is the only recoverability path.
- **If the SME MCP is unavailable,** STOP and tell the user — do not skip to "manual upload".
