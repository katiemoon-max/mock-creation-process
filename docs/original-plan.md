# Mock Paper Pipeline — Subject-Agnostic Scripted Skills

## Context

The current mock paper creation process is formalised only in parts. Seven skills cover outline → draft → review → diagram → format → feedback, but quality gates (`/spec-check`, `/review-cqi`, the assessment-design-checklist context file) sit outside the formal flow, research is implicit, and there is no subject-agnostic onboarding. The Notion troubleshooting guide enumerates seven recurring failure modes (too-easy questions, repetitive structures, stem-leakage, spec hallucination, AO misclassification, over-academic model answers, constraint drift) that need proactive checks at the right stage — not spot-fixes after the fact.

The goal: adapt this into a cc4e-style numbered pipeline (six scripted skills + a status orchestrator) that any Physics/Biology/Chemistry/Psychology content creator can follow, with a front-loaded setup phase that seeds all downstream constraints and a review phase that enforces every quality gate. Tested end-to-end on a fresh mock exam project in a follow-up session.

## Architecture

**Six numbered skills + one orchestrator**, adopting the cc4e `STOP / USER / ACTION / [Conditional]` script markers plus a new `CHECK` marker for proactive self-reflection logged to `project.json`.

| # | Skill | Purpose |
|---|---|---|
| 0 | `/mock-0-setup` | Subject-agnostic onboarding. Verifies MCPs/spec/past papers/NotebookLM; creates `project.json`, project CLAUDE.md, AO classification guide, misconception bank, exclusion list, difficulty targets. |
| 1 | `/mock-1-research` | NotebookLM research → three catalogues (AO question-type, MCQ, spec-coverage-map). Extends misconception bank with distractor archetypes. |
| 2 | `/mock-2-outline` | Refactor of current `mock-paper-outline`. Research logic removed. Adds command-word+AO+topic duplication gate, per-AO3 litmus test, image-source flag. |
| 3 | `/mock-3-draft` | Refactor of current `draft-questions`. Drafts in batches of 2–3. Stem-only draft → information-leakage + stem-usage audits → solution + MS&G + ET&T → two-pass model-answer self-critique. |
| 4 | `/mock-4-review` | New composite. Runs `/review-questions` → `/spec-check` → assessment-design-checklist → parallel sub-agents (`spec-examiner`, `student-simulator`, `marking-realism-checker`) → `/review-cqi`. Consolidates into `reviews/SUMMARY.md`. |
| 5 | `/mock-5-publish` | Gates on all review pass flags. Applies Cobalt conversion, uploads via SME `createQuestion` MCP (per-question STOP for safety — no update/delete after creation), writes cross-qualification reuse map. |
| – | `/mock` | Thin orchestrator. Reads `project.json`, prints current phase + next command. |

### Script convention

```
STOP: <question to creator>
USER: <expected response shape — author reference only>
ACTION: <tool call / file write / sub-agent invocation>
CHECK: <reflective question Claude must answer and log to project.json>
[Conditional: branch]
```

`CHECK` is the hook that turns "proactive reflection" from hand-wavy into enforced — each one writes a short answer to `project.json.qualityGates[...]`.

### State file: `project.json` (per project)

Machine-readable pipeline state. Schema:

```json
{
  "project": { "board": "...", "qualification": "...", "subject": "...", "paper": "...", "dir": "...", "created": "YYYY-MM-DD" },
  "phase": 0-5,
  "status": "in_progress | complete",
  "gates": { "setup": "pass", "research": "pending", ... },
  "qualityGates": { "specAvailable": true, "pastPaperCount": 6, "notebookLmHealth": "ok", "aoTargetsConfirmed": true, "exclusionListCaptured": true, ... },
  "questions": [ { "id": "Q01", "status": "drafted", "reviewed": false, "cqi": null, "formatted": false, "uploaded": false, "illustrationSource": "claude|creator", "illustrationStatus": "pending|generated|uploaded|linked" } ],
  "reviews": { "notebookLmTypicality": null, "specCheck": null, "assessmentDesign": null, "cqiScore": null, "specExaminer": null, "studentSimulator": null, "markingRealism": null },
  "excludedContexts": [...],
  "notebookLmUrl": "...",
  "nextStep": "/mock-3-draft Q04-Q06"
}
```

The tracker CSV stays (per-question content metadata); `project.json` is separate (pipeline state).

## Proactive-Check Coverage Matrix

Every troubleshooting issue has an explicit enforcement stage:

| Issue | Enforced in | How |
|---|---|---|
| Too easy / weak cognitive demand | `/mock-1-research`, `/mock-3-draft`, `/mock-4-review` | Distractor archetypes from past-paper MCQs → misconception bank → per-distractor named-error requirement → `student-simulator` cross-check |
| Repetitive structures | `/mock-2-outline` | Command-word + AO + topic triple check fails if duplicates found |
| Stem leaks / stem unused | `/mock-3-draft`, `/mock-4-review` | Stem-only draft phase + information-leakage CHECK + stem-usage CHECK + `student-simulator` external read |
| Spec hallucination | `/mock-0-setup`, `/mock-1-research`, `/mock-4-review` | Spec-path hard gate + spec-coverage-map evidence + mandatory `/spec-check` |
| AO misclassification | `/mock-0-setup`, `/mock-2-outline`, `/mock-4-review` | AO classification guide with 3–4 exemplars per AO in CLAUDE.md + per-AO3 litmus-test justification + `spec-examiner` audit |
| Model answer too academic | `/mock-3-draft` | Word-ceiling + reading-level target + two-pass self-critique |
| "Claims compliance" hallucination | `/mock-4-review` | `marking-realism-checker` sub-agent audits MS against command-word demands |
| Constraint drift across session | `/mock-0-setup`, `/mock-3-draft` | CLAUDE.md imports (exclusion list, difficulty targets) reload every skill session; pre-batch STOP reloads verbally |
| Image dependencies block progress | `/mock-2-outline`, `/mock-3-draft` | Tracker columns `illustrationSource` + `illustrationStatus` set at outline; `/generate-diagram` auto-called when Claude can produce |

## Multi-Perspective Sub-Agents

Created at `.claude/agents/[name]/AGENT.md`:

- **`spec-examiner`** (new) — Chief-examiner adversarial review. Audits each SFMA against the spec; flags moderation risks. Writes `reviews/spec-examiner.md`.
- **`student-simulator`** (new) — Reads stems only (no MS access); writes stream-of-consciousness student attempt. Surfaces ambiguity, unused stem info, cross-part answer inference. Writes `reviews/student-simulator.md`.
- **`marking-realism-checker`** (new) — Audits MS against command-word demands, Smart Mark rules (sig figs, ecf chains, alternative equations, multi-point clarity). Writes `reviews/marking-realism.md`.
- **`exam-researcher`** (existing, extended) — Add `mcp__notebooklm__*` tools so `/mock-1-research` can delegate cleanly.
- **`quality-reviewer`** (existing) — Composes aggregate `reviews/SUMMARY.md` inside `/mock-4-review`.

Sonnet for all three new sub-agents (decision deferred; can upgrade `student-simulator` to Opus if simulation proves shallow).

## Templates

New folder `.claude/templates/`:

- `project.json.template`, `project-claude-md.template`
- `sfma.template.md`, `outline-table.template.md`, `tracker.template.csv`
- `misconception-bank.template.md`, `ao-classification-guide.template.md`
- `exclusion-list.template.md`, `difficulty-targets.template.md`
- `review-summary.template.md`, `reuse-map.template.md`

Skills reference via `@../../.claude/templates/X` from inside a project.

## Full Directory Layout

```
Claude/
├── CLAUDE.md                                  [MODIFIED — add pipeline orientation]
├── .claude/
│   ├── agents/
│   │   ├── exam-researcher/AGENT.md           [MODIFIED — add notebooklm tools]
│   │   ├── quality-reviewer/AGENT.md
│   │   ├── spec-examiner/AGENT.md             [NEW]
│   │   ├── student-simulator/AGENT.md         [NEW]
│   │   └── marking-realism-checker/AGENT.md   [NEW]
│   ├── context/
│   │   ├── sme-overview.md
│   │   ├── quality-standards.md
│   │   ├── project-status.md
│   │   └── assessment-design-checklist.md     [actively referenced by /mock-4-review]
│   ├── rules/                                 [unchanged]
│   ├── templates/                             [NEW]
│   ├── skills/
│   │   ├── mock/SKILL.md                      [NEW — orchestrator]
│   │   ├── mock-0-setup/SKILL.md              [NEW]
│   │   ├── mock-1-research/SKILL.md           [NEW]
│   │   ├── mock-2-outline/SKILL.md            [RENAMED from mock-paper-outline, refactored]
│   │   ├── mock-3-draft/SKILL.md              [RENAMED from draft-questions, refactored]
│   │   ├── mock-4-review/SKILL.md             [NEW composite]
│   │   ├── mock-5-publish/SKILL.md            [NEW]
│   │   ├── review-questions/SKILL.md          [unchanged; called by /mock-4-review]
│   │   ├── spec-check/SKILL.md                [unchanged; called by /mock-4-review]
│   │   ├── review-cqi/SKILL.md                [unchanged; called by /mock-4-review]
│   │   ├── cobalt-formatting/SKILL.md         [unchanged reference; read by /mock-5-publish]
│   │   ├── generate-diagram/SKILL.md          [unchanged; called by /mock-3-draft]
│   │   ├── feedback-triage/SKILL.md           [unchanged]
│   │   ├── handover/SKILL.md                  [MODIFIED — reads project.json]
│   │   └── (vault-health, add-skill-to-notion, skills-demo-mode unchanged)
│   └── handovers/
└── 02 - Projects/[Board] [Qual] [Subject]/Paper [X]/
    ├── project.json                           [NEW per project]
    ├── CLAUDE.md                              [NEW per project — imports vault + .project/*]
    ├── .project/
    │   ├── ao-classification-guide.md
    │   ├── ao-targets.md
    │   ├── misconception-bank.md
    │   ├── exclusion-list.md
    │   ├── difficulty-targets.md
    │   ├── command-word-list.md
    │   ├── setup-verification.md
    │   ├── stem-audit.md
    │   └── catalogues/
    │       ├── ao-question-type.md
    │       ├── mcq-catalogue.md
    │       └── spec-coverage-map.md
    ├── Section A/
    ├── diagrams/
    ├── reviews/                               [outputs of /mock-4-review]
    ├── publish/                               [outputs of /mock-5-publish]
    ├── [Project]-Outline.md
    └── [Project]-Tracker.csv
```

## Migration (decided)

- **Hard rename** `mock-paper-outline` → `mock-2-outline`, `draft-questions` → `mock-3-draft`. No aliases. Old commands will fail — forces everyone onto new flow. Documented in next handover entry.
- **Paper 2F** stays on old flow. No retrofit. New pipeline applies from the next project.
- All unchanged skills remain callable standalone AND via the orchestrated flow.

## Critical Files to Modify / Create

- Create: all files in "NEW" rows of the directory layout above (7 skill folders, 3 agent folders, 1 template folder with 11 files).
- Modify: `C:\Users\Katie Moon\Documents\Claude\CLAUDE.md` (add pipeline orientation section pointing creators to `/mock-0-setup`).
- Modify: `C:\Users\Katie Moon\Documents\Claude\.claude\agents\exam-researcher\AGENT.md` (add `mcp__notebooklm__*` to tools).
- Modify: `C:\Users\Katie Moon\Documents\Claude\.claude\skills\handover\SKILL.md` (read `project.json`, surface `nextStep` in handover output).
- Rename: `mock-paper-outline/` folder → `mock-2-outline/`, refactor SKILL.md (remove Step 3 research — now in `/mock-1-research`; add CHECK gates).
- Rename: `draft-questions/` folder → `mock-3-draft/`, refactor SKILL.md (batch-of-3 logic, stem-only phase, information-leakage + stem-usage CHECKs, two-pass model-answer self-critique).

## Reusable Assets (do not reinvent)

- `C:\Users\Katie Moon\Documents\Claude\.claude\context\assessment-design-checklist.md` — 11 per-question/paper validity checks already written. Invoke from `/mock-4-review`.
- `C:\Users\Katie Moon\Documents\Claude\.claude\skills\cobalt-formatting\SKILL.md` — full Cobalt syntax reference. Read (not callable) by `/mock-3-draft` and `/mock-5-publish`, same pattern as today.
- `C:\Users\Katie Moon\Documents\Claude\.claude\skills\generate-diagram\SKILL.md` — matplotlib greyscale, blank+answer PNGs. Called by `/mock-3-draft` when tracker row sets `illustrationSource: claude`.
- `C:\Users\Katie Moon\Documents\cc4e-course\lesson-modules\1.1-introduction\CLAUDE.md` — reference for STOP/USER/ACTION/[Conditional] script cadence.
- Existing `exam-researcher` + `quality-reviewer` agents — extend, don't duplicate.

## Verification Plan

Test on a fresh project (board/level to be captured via `/mock-0-setup`'s own interview — user indicated "a different board/level" pending their choice at runtime). Success criteria:

1. **Setup gate:** `/mock-0-setup` refuses to proceed with intentionally-missing spec; completes cleanly once spec is added.
2. **Constraint persistence:** An exclusion-list item captured at setup is respected in `/mock-3-draft` batch 3 without re-stating.
3. **Research artefacts:** `/mock-1-research` produces 3 catalogues + extends misconception bank.
4. **AO balance gate:** `/mock-2-outline` fails when AO distribution is outside paper-specific target ± 3% and offers a fix.
5. **Stem audit triggers:** `/mock-3-draft` flags a deliberately-seeded information-leakage case (part (c) answerable from part (a) stem).
6. **Multi-agent review value:** `/mock-4-review` produces 5+ review files; `student-simulator` catches at least one issue `spec-examiner` misses (or vice versa).
7. **Publish gate:** `/mock-5-publish` refuses to run when any review gate is pending/fail in `project.json`.
8. **Handover continuity:** Stop mid-pipeline, start fresh session, run `/mock` → correctly reports phase and next command.
9. **Subject-agnostic language:** skim every SKILL.md and template — no Physics-specific content outside explicit "e.g." illustrations.
10. **Usability dry-run:** Role-play a Biology creator running only the numbered slash commands end-to-end — count "what do I do next?" moments. Target: zero.

## Implementation Order (for the next session)

1. Templates folder + all 11 template files (foundation).
2. Three new sub-agents (`spec-examiner`, `student-simulator`, `marking-realism-checker`).
3. `/mock-0-setup` (biggest new skill; unlocks everything downstream).
4. `/mock-1-research` (short skill, three NotebookLM queries + catalogue writes).
5. Rename + refactor `mock-2-outline` and `mock-3-draft`.
6. `/mock-4-review` (composite — wires up existing skills + sub-agents + CQI).
7. `/mock-5-publish`.
8. `/mock` orchestrator.
9. Modify `CLAUDE.md`, `handover` skill, `exam-researcher` agent.
10. Run the verification plan on the test project.
