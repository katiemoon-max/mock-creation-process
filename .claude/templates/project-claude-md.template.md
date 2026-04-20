# Project: {{BOARD}} {{QUALIFICATION}} {{SUBJECT}} {{PAPER}}

This CLAUDE.md is project-scoped. It is read by every skill that operates on this paper. Its imports carry subject-specific constraints (exclusion list, AO classification guide, difficulty targets) so Claude cannot drift off-brief mid-session.

## Imports

@../../CLAUDE.md
@.project/ao-classification-guide.md
@.project/ao-targets.md
@.project/misconception-bank.md
@.project/exclusion-list.md
@.project/difficulty-targets.md
@.project/command-word-list.md

## Project meta

- **Board:** {{BOARD}}
- **Qualification:** {{QUALIFICATION}}
- **Subject:** {{SUBJECT}}
- **Paper:** {{PAPER}}
- **Total marks:** {{TOTAL_MARKS}}
- **Time allowed:** {{TIME_ALLOWED}}
- **Spec path:** {{SPEC_PATH}}
- **NotebookLM notebook:** {{NOTEBOOK_URL}}
- **Created:** {{CREATED_DATE}}

## Critical constraints (these override everything else)

1. **Only draw content from the spec at `{{SPEC_PATH}}`.** Do not invent spec points from training data.
2. **Respect the exclusion list in `.project/exclusion-list.md`.** Re-read it at the start of every drafting batch.
3. **Paper-specific AO percentages** from `.project/ao-targets.md` — not the overall qualification weighting. Tolerance ±3%.
4. **Difficulty targets** from `.project/difficulty-targets.md` govern word ceilings, reading level, and per-question demand.
5. **Command words** must come from `.project/command-word-list.md` (sourced from the spec, not training data).
6. **House style:** all vault-level formatting and equation rules still apply.
7. **Cobalt limitation:** once a question is uploaded via `createQuestion`, there is no update/delete. Verify before upload.

## Pipeline state

Pipeline state is tracked machine-readably in `project.json`. To see current phase and next step, run `/mock`.

## Do not

- Do not use examples of MCQ distractors that do not correspond to a named misconception in `.project/misconception-bank.md`.
- Do not write model answers above the reading-level / word-count ceiling in `.project/difficulty-targets.md`.
- Do not classify a question as AO3 unless it passes the litmus test in `.project/ao-classification-guide.md`.
- Do not draft solutions before running the stem-only information-leakage and stem-usage CHECKs (enforced in `/mock-3-draft`).
