---
name: mock
description: Status orchestrator for the mock paper pipeline. Reads project.json in the current directory (or asks which project), prints the current phase, gate status, and the next slash command to run. Use at any point to re-orient — especially across sessions or after /handover.
user_invocable: true
arguments: "[project_dir]"
allowed-tools: Read, Glob, Bash
---

# Mock Pipeline Orchestrator

You are the status helper for the mock paper pipeline. This skill does not write files — it reads `project.json` and tells the creator where they are.

## Script

### ACTION — Locate project.json

If the user passed a `project_dir`, look for `project.json` there.

Otherwise:
1. Check current working directory
2. Check `02 - Projects/**/project.json` — list all that exist
3. If multiple, ask the user which

[Conditional: no project.json found]
> "I can't find a `project.json` in the current directory or any active project. Either run `/mock-0-setup` to start a new project, or `cd` into an existing project directory."

### ACTION — Parse project.json

Extract:
- `project.board`, `qualification`, `subject`, `paper`
- `phase`, `status`
- `gates.*`
- `qualityGates.*` (setup-phase gate status)
- `questions[]` (count drafted / reviewed / formatted / uploaded)
- `reviews.*` (review gate status)
- `nextStep`

### ACTION — Print status report

Format:

```
Project: {{BOARD}} {{QUAL}} {{SUBJECT}} {{PAPER}}
Phase: {{N}} / 5 — {{PHASE_NAME}}
Status: {{STATUS}}

Pipeline gates:
  Phase 0 setup:    {{✓/✗/pending}}
  Phase 1 research: {{✓/✗/pending}}
  Phase 2 outline:  {{✓/✗/pending}}
  Phase 3 draft:    {{✓/✗/pending}}  ({{N}}/{{TOTAL}} questions drafted)
  Phase 4 review:   {{✓/✗/pending}}
  Phase 5 publish:  {{✓/✗/pending}}  ({{N}}/{{TOTAL}} uploaded)

Next step: {{nextStep}}
```

[Conditional: phase == 3 and drafting partial]
> Add a breakdown:
> ```
> Draft status:
>   Q01 - {{TOPIC}} - drafted
>   Q02 - {{TOPIC}} - drafted
>   Q03 - {{TOPIC}} - planned
>   Q04 - {{TOPIC}} - planned
>   ...
> Recommended next batch: Q03-Q05 (max 3 per batch)
> ```

[Conditional: phase == 4 and reviews mixed]
> Add review summary:
> ```
> Review status:
>   NotebookLM typicality: {{STATUS}}
>   Spec-check:            {{STATUS}}
>   Assessment design:     {{STATUS}}
>   Spec-examiner:         {{STATUS}}
>   Student-simulator:     {{STATUS}}
>   Marking-realism:       {{STATUS}}
>   CQI scorecard:         {{SCORE}}/50 ({{PASS/FAIL}})
> Critical issues open: {{N}}
> Publish gate: {{OPEN/BLOCKED}}
> ```

[Conditional: phase == 0 and qualityGates has failures]
> Add gate breakdown:
> ```
> Setup blockers:
>   Spec markdown:          {{path if found, else 'MISSING'}}
>   Past papers (≥5):       {{N}} found
>   Examiner reports (≥2):  {{M}} found
>   NotebookLM:             {{STATUS}}
>   Notion MCP:             {{STATUS}}
>   SME MCP:                {{STATUS}}
> ```

## Rules

- Do not write to any file. This is a read-only skill.
- Do not advance phases. That's the job of the numbered skills.
- If the project.json is missing fields the schema expects, flag them — likely corrupted state.
- If `nextStep` contradicts the gate status (e.g. says `/mock-5-publish` but a review gate is pending), trust the gates and recompute a sensible next step.
