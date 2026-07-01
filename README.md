# Mock Paper Pipeline

A scripted, subject-agnostic pipeline for authoring high-quality mock exam papers with Claude Code. Built for Save My Exams content creators; adaptable to any exam board, qualification, and subject (Biology, Chemistry, Physics, Psychology, Geography, etc.).

## What it does

Turns a blank slate into a fully-drafted, reviewed, and CMS-ready mock paper through six numbered phases. Each phase is a separate Claude Code skill with explicit quality gates; you cannot skip phases. State is tracked machine-readably in a per-project `project.json`.

| # | Skill | Purpose |
|---|-------|---------|
| 0 | `/mock-0-setup` | Subject-agnostic onboarding. Verifies spec, past papers, NotebookLM; captures exclusion list, difficulty targets, AO classification guide, misconception bank, board conventions; writes `project.json` + project CLAUDE.md. |
| 1 | `/mock-1-research` | Builds three catalogues (AO question-type, MCQ, spec-coverage-map) + board-conventions + an **AO breadth map** from direct analysis of past papers AND NotebookLM synthesis. Runs a creator-reviewed **MS calibration** sample → `.project/ms-exemplars/` + `mark-scheme-conventions.md` (hard gate). |
| 2 | `/mock-2-outline` | Paper blueprint + tracker CSV. Hard gates: topic scope, CW+AO+Topic duplication, MCQ format variety, MCQ↔Section B non-overlap, AO3 litmus test, AO balance ±3%, exclusion list, image dependencies, paper length, mark tariffs. Soft gates: per-AO variety, difficulty distribution, intra-paper context freshness. Mandatory typicality cross-check before advancing. |
| 3 | `/mock-3-draft` | SFMAs in batches of 2-3. Stem-only phase → information-leakage + stem-usage audits → solution → MS&G (**Smart-Mark pre-flight** hard gate) → ET&T → two-pass self-critique. Command words/contexts designed from the AO breadth map; every MCQ distractor cites a misconception. |
| 4 | `/mock-4-review` | Composite review: NotebookLM typicality + spec-check + assessment-design-checklist + 3 parallel sub-agents (spec-examiner, student-simulator, marking-realism-checker) + CQI scorecard + a **breadth-and-variety** re-check. Publish gate opens only on CQI ≥ 43/50 with no Critical issues. |
| 5 | `/mock-5-publish` | Cobalt conversion + per-question STOP upload via SME MCP + cross-qualification reuse map. Run `/cobalt-sync --full` after any post-gate Cobalt rework. |
| – | `/mock` | Status orchestrator — reads project.json, prints current phase + next command. Run anytime. |

## Key design principles

- **Script markers**: every skill uses `STOP: / USER: / ACTION: / CHECK: / [Conditional:]` — human-readable, no special parser. Inspired by [cc4e-course](https://github.com/csev/cc4e-course).
- **State in JSON, content in Markdown.** `project.json` = pipeline state; tracker CSV = per-question content metadata. They don't overlap.
- **Board-specific knowledge lives in `.project/` files, not in skills.** Every skill reads principles only; board-specific examples (stem phrasings, opening archetypes, AO3 patterns, mark tariff norms) are captured in per-project `.project/board-conventions.md` during Phase 1. Skills stay generic; knowledge stays local.
- **Conventions are learned, not enumerated.** The same empirical approach extends to mark schemes and assessment breadth: a generic `context/mark-scheme-standard.md` holds only the universal Smart-Mark-readiness principles + a pre-flight gate, while each course's MS format is learned in Phase 1 (the MS calibration sample, drawn from real past-paper mark schemes and the SME Gold Standard SFMA library) and captured in `.project/mark-scheme-conventions.md` + `.project/ms-exemplars/`. Phase 1 likewise builds an **AO breadth map** so drafting tests each AO through a variety of command words and contexts rather than one archetype.
- **Direct analysis > NotebookLM alone.** The pipeline uses NotebookLM as a cross-check but treats direct Read/Grep of markdown past papers as the authoritative source.
- **Multi-perspective review.** Phase 4 dispatches 3 specialist sub-agents in parallel (adversarial chief-examiner, student simulator reading only stems, mark-scheme realism auditor) alongside NotebookLM typicality, the 10-criterion CQI scorecard, and a breadth-and-variety re-check.
- **Hard gates at every phase.** Cobalt has no update/delete once a question is published — the pipeline refuses to publish unreviewed content.

## Installation

Copy the `.claude/` directory contents into your own Claude Code configuration directory:

```bash
# If you already have a .claude/ directory at your working root:
cp -r .claude/* /path/to/your/working-directory/.claude/

# If not:
cp -r .claude/ /path/to/your/working-directory/
```

Tools needed:
- [Claude Code](https://claude.ai/download) (CLI or desktop)
- [NotebookLM MCP](https://notebooklm.google.com) authenticated (for Phase 1 research)
- Python 3.11+ with `pymupdf4llm` for PDF conversion (`pip install pymupdf4llm`)
- Optional: `pdftotext` (Poppler) for OCR'd scanned PDFs
- Optional: Notion MCP for workspace integration
- Optional: SME Cobalt MCP for Phase 5 publishing

## Usage

From a working directory where you want to create a mock paper project:

```
/mock-0-setup
```

The skill interviews you for board/qualification/subject/paper and walks you through spec and past-paper verification. Each subsequent phase is run via its slash command — the `project.json` enforces phase ordering.

At any point: run `/mock` to see where you are and what comes next.

## File structure

```
.claude/
├── skills/
│   ├── mock/                      # Status orchestrator
│   ├── mock-0-setup/              # Phase 0
│   ├── mock-1-research/           # Phase 1
│   ├── mock-2-outline/            # Phase 2
│   ├── mock-3-draft/              # Phase 3
│   ├── mock-4-review/             # Phase 4
│   ├── mock-5-publish/            # Phase 5
│   ├── review-questions/          # Called by Phase 4
│   ├── review-cqi/                # Called by Phase 4
│   ├── spec-check/                # Called by Phase 4
│   ├── cobalt-formatting/         # Reference for Phase 3 + 5
│   ├── generate-diagram/          # Called by Phase 3
│   ├── feedback-triage/           # Post-publication feedback
│   ├── handover/                  # Session checkpointing
│   └── skills-demo-mode/          # Demo wrapper for any skill
├── agents/
│   ├── exam-researcher/           # Deep past-paper + spec research
│   ├── quality-reviewer/          # Aggregates Phase 4 outputs
│   ├── spec-examiner/             # Adversarial chief-examiner review
│   ├── student-simulator/         # Reads stems as a student
│   └── marking-realism-checker/   # Smart Mark readiness audit
├── templates/                     # Reusable project templates (12 files)
│   ├── project.json.template
│   ├── project-claude-md.template.md
│   ├── sfma.template.md
│   ├── outline-table.template.md
│   ├── tracker.template.csv
│   ├── board-conventions.template.md
│   ├── ao-classification-guide.template.md
│   ├── misconception-bank.template.md
│   ├── exclusion-list.template.md
│   ├── difficulty-targets.template.md
│   ├── review-summary.template.md
│   └── reuse-map.template.md
├── context/                       # Shared knowledge (generic — no project data)
│   ├── sme-overview.md            # Role, exam boards, ACE tone, PARSNIPS
│   ├── quality-standards.md       # CQI criteria, Gold Standard SFMA
│   ├── assessment-design-checklist.md  # Board-agnostic AQA-derived checks
│   └── mark-scheme-standard.md    # Universal Smart-Mark-readiness principles + pre-flight gate
├── rules/                         # Auto-loaded formatting + equation rules
│   ├── formatting.md
│   └── equations.md
└── tools/
    └── pdf_to_md.py               # Batch convert past-paper PDFs to markdown
```

## Running this pipeline on a new subject

Adaptation is one-shot — `/mock-0-setup` handles everything subject-agnostic. The only board/subject-specific content is in per-project `.project/` files that Phase 1 produces. The skills themselves never mention a specific board or topic.

When starting a new paper:
1. Put the board's spec in `03 - Resources/Spec Vault/{{BOARD}}/{{QUAL}}/{{SUBJECT}}/spec.md` (markdown, convertible from PDF via `pdf_to_md.py`)
2. Put ≥5 past papers + ≥2 examiner reports in the same folder
3. Create a NotebookLM notebook with all of the above as sources
4. Run `/mock-0-setup`

## Status

All six phases (0–5) now tested end-to-end on real papers:
- **Edexcel A Level Physics Paper 1** (April 2026) — 19/19 SFMAs drafted, reviewed, and uploaded to Cobalt with spec-point IDs attached via the SME content MCP. Consolidated to 18 questions in a later creator rework.
- **Edexcel A Level Physics Paper 2** (May 2026) — 20/20 SFMAs drafted, reviewed across two re-review passes, and uploaded to Cobalt. CHECK 0.5 spec-point matching pre-flight passed cleanly. Cross-qualification reuse map shows 19/20 questions reusable for Edexcel IAL and 16+/20 for AQA/OCR/CIE A Level.
- **Edexcel A Level Physics Paper 3** — completed, archived alongside Papers 1–2.

The July 2026 post-project review of Papers 1–3 fed back the AO breadth map, the Phase-2 variety/difficulty/freshness gates, the Phase-4 breadth-and-variety lens, and the two-layer mark-scheme standard + MS calibration gate — all now in the pipeline.

See:
- `docs/original-plan.md` — original design document
- `docs/retrospective-2026-04-21.md` — Phase 3/4 learnings from the first end-to-end run (Paper 1)
- `docs/retrospective-2026-04-22.md` — Phase 5 learnings (CMS upload + spec-point attachment)
- `docs/retrospective-2026-05-06.md` — Paper 2 second-time learnings (two-pass re-review pattern, mass-conserving fix sweeps, Cobalt format gap in Phase 3, `updateQuestion` for `pending_review`)
- `docs/retrospective-2026-07-01.md` — Papers 1–3 process review (AO variety, mark-scheme construction, learned-not-enumerated conventions)

Contributions from future projects (new papers, subjects, boards) should feed back as pipeline refinements — improvements made while using the pipeline should go back into the skills themselves. The pipeline is subject/level/course-agnostic by design; if you find board- or subject-specific content leaking into a skill, that's a bug.

## Licence

SME-internal. Not for external distribution without permission.
