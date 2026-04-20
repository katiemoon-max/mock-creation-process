# Exclusion List — {{BOARD}} {{QUALIFICATION}} {{SUBJECT}} {{PAPER}}

Explicit "do NOT use" items captured at `/mock-0-setup`. Every skill re-reads this file at the start of every drafting batch via the project CLAUDE.md imports, addressing the "Claude ignores constraints stated once" failure mode.

## Why this file exists

Stating a constraint once at planning does not guarantee Claude respects it during drafting. This file is imported by the project CLAUDE.md so it is in context at every turn.

## Excluded topics

<!-- Topics the creator does NOT want to appear in this paper, e.g. "pendulums covered in Paper 1", "radioactive decay already tested in Q2 of sister paper". -->

- {{TOPIC}}

## Excluded contexts / scenarios

<!-- E.g. "the Milgram experiment", "COVID-19 scenarios", "Stanford Prison Experiment", "pendulums as context". -->

- {{CONTEXT}}

## Excluded command-word + AO + topic combinations

<!-- If `/mock-2-outline` detects a duplicate command-word + AO + topic across questions, it logs here so `/mock-3-draft` avoids re-using it when rewriting. -->

- {{CW}} + AO{{N}} + {{TOPIC}}

## Studies / classic examples to avoid (if essay-based subject)

<!-- E.g. for Psychology: "Bandura 1961 (Bobo doll) — already in student revision", "Loftus and Palmer (1974)". -->

- {{STUDY_OR_EXAMPLE}}

## Sister-paper usage (cross-reference)

<!-- Topics already tested in Paper 1 / previous sittings — not necessarily excluded, but flagged for creator attention. -->

- {{TOPIC}} — tested in {{SISTER_PAPER}}
