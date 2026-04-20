# Mock Paper Pipeline

A scripted, subject-agnostic pipeline for authoring high-quality mock exam papers with Claude Code. Built for Save My Exams content creators; adaptable to any exam board, qualification, and subject (Biology, Chemistry, Physics, Psychology, Geography, etc.).

## What it does

Turns a blank slate into a fully-drafted, reviewed, and CMS-ready mock paper through six numbered phases. Each phase is a separate Claude Code skill with explicit quality gates; you cannot skip phases. State is tracked machine-readably in a per-project `project.json`.

| # | Skill | Purpose |
|---|-------|---------|
| 0 | `/mock-0-setup` | Subject-agnostic onboarding. Verifies spec, past papers, NotebookLM; captures exclusion list, difficulty targets, AO classification guide, misconception bank, board conventions; writes `project.json` + project CLAUDE.md. |
| 1 | `/mock-1-research` | Builds three catalogues (AO question-type, MCQ, spec-coverage-map) + board-conventions file from direct analysis of past papers AND NotebookLM synthesis. |
| 2 | `/mock-2-outline` | Paper blueprint + tracker CSV. Hard gates: topic scope, CW+AO+Topic duplication, MCQ format variety, MCQ↔Section B non-overlap, AO3 litmus test, AO balance ±3%, exclusion list, image dependencies, paper length, mark tariffs. Mandatory typicality cross-check before advancing. |
| 3 | `/mock-3-draft` | SFMAs in batches of 2-3. Stem-only phase → information-leakage + stem-usage audits → solution → MS&G → ET&T → two-pass self-critique. Every MCQ distractor cites a misconception. |
| 4 | `/mock-4-review` | Composite review: NotebookLM typicality + spec-check + assessment-design-checklist + 3 parallel sub-agents (spec-examiner, student-simulator, marking-realism-checker) + CQI scorecard. Publish gate opens only on CQI ≥ 43/50 with no Critical issues. |
| 5 | `/mock-5-publish` | Cobalt conversion + per-question STOP upload via SME MCP + cross-qualification reuse map. |
| – | `/mock` | Status orchestrator — reads project.json, prints current phase + next command. Run anytime. |

## Key design principles

- **Script markers**: every skill uses `STOP: / USER: / ACTION: / CHECK: / [Conditional:]` — human-readable, no special parser. Inspired by [cc4e-course](https://github.com/csev/cc4e-course).
- **State in JSON, content in Markdown.** `project.json` = pipeline state; tracker CSV = per-question content metadata. They don't overlap.
- **Board-specific knowledge lives in `.project/` files, not in skills.** Every skill reads principles only; board-specific examples (stem phrasings, opening archetypes, AO3 patterns, mark tariff norms) are captured in per-project `.project/board-conventions.md` during Phase 1. Skills stay generic; knowledge stays local.
- **Direct analysis > NotebookLM alone.** The pipeline uses NotebookLM as a cross-check but treats direct Read/Grep of markdown past papers as the authoritative source.
- **Multi-perspective review.** Phase 4 dispatches 3 specialist sub-agents in parallel (adversarial chief-examiner, student simulator reading only stems, mark-scheme realism auditor) alongside NotebookLM typicality and the 10-criterion CQI scorecard.
- **Hard gates at every phase.** Cobalt has no update/delete after upload — the pipeline refuses to publish unreviewed content.

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
│   └── assessment-design-checklist.md  # Board-agnostic AQA-derived checks
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

This pipeline was built and tested end-to-end through Phase 2 on Edexcel A Level Physics Paper 1 in April 2026. See `docs/original-plan.md` for the original design document.

Contributions from future projects (e.g. Paper 2 and Paper 3 of Edexcel A Level Physics, then new subjects) will feed back as pipeline refinements — improvements made while using the pipeline should go back into the skills themselves.

## Licence

SME-internal. Not for external distribution without permission.
