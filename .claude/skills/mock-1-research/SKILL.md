---
name: mock-1-research
description: Phase 1 research. Builds three catalogues (AO question-type, MCQ, spec-coverage-map) using BOTH direct analysis of markdown past papers AND NotebookLM synthesis as independent cross-checks. Also builds an AO breadth map (per-AO palette of command words × task types × contexts) so drafting designs from a menu rather than defaulting to one archetype per AO. Calibrates the course's mark-scheme conventions by drafting a creator-reviewed sample of exemplar SFMAs (hard gate). Extends the misconception bank with distractor archetypes discovered during MCQ cataloguing. Required before /mock-2-outline.
user_invocable: true
arguments: ""
allowed-tools: Read, Glob, Grep, Write, Edit, Bash, Task, mcp__notebooklm__ask_question, mcp__notebooklm__get_health, mcp__notebooklm__select_notebook
---

# Mock Paper Research (Phase 1)

You are running the research phase. Three catalogues and a misconception-bank extension are the outputs. All feed into `/mock-2-outline` as its evidence base.

**Key methodology: use TWO independent sources and cross-check.**

1. **Direct analysis (primary):** Read and Grep the markdown past papers + mark schemes + examiner reports in the Spec Vault. This is authoritative and exhaustive — nothing hedges, nothing is missed due to ingestion gaps.
2. **NotebookLM (secondary, cross-check):** use 2–3 sharp queries per catalogue to validate findings or surface patterns across years that direct analysis might miss.

When the two sources disagree, **record the discrepancy** — it's a useful signal for Phase 2 and Phase 4 review agents.

Markers: `STOP:`, `ACTION:`, `CHECK:`, `[Conditional]`.

## Prerequisites

ACTION: Read `project.json` in the current project directory. Verify `gates.setup == "pass"` and `phase >= 1`.

[Conditional: setup not complete]
> STOP: "Phase 0 (setup) hasn't been completed for this project. Run `/mock-0-setup` first."

ACTION: Read the following fresh:
- `project.json` (paper meta, paperMeta.topicCoverage — what topics are in scope for THIS paper)
- `.project/ao-classification-guide.md` (calibration for AO decisions)
- `.project/misconception-bank.md` (to avoid duplicating IDs when extending)
- `qualityGates.specPath` and `qualityGates.notebookLmUrl` from project.json

ACTION: Identify the markdown past papers for THIS paper (board/qual/subject/paper). Typical location: the same folder as the spec, with filenames like `Paper{N}-Question-{YYYY}.md`, `Paper{N}-MarkScheme-{YYYY}.md`, `Paper{N}-ExaminerReport-{YYYY}.md`. Expect 5–8 years of coverage.

ACTION: The current NotebookLM MCP doesn't require a select step — query tools accept the notebook ID directly via `notebook_id`. Verify auth is live with `mcp__notebooklm__server_info`; if `auth_status` is stale, call `mcp__notebooklm__refresh_auth` and (only if that fails) ask the user to run `nlm login`. Pass the notebook ID from `qualityGates.notebookLmId` to each sub-agent in its briefing.

## Script

The three catalogues can be built in parallel by dispatching three `general-purpose` sub-agents in a single message. Each agent:
- Has Write access (unlike `exam-researcher` which returns findings as text)
- Uses both direct Read/Grep AND NotebookLM MCP tools
- Writes directly to its target file
- Returns a short summary only (keeps main-thread context clean)

### STOP 1 — Confirm paper scope and catalogue plan

> "Running Phase 1 research for {{PROJECT_NAME}}. I'll dispatch three parallel general-purpose agents to build the catalogues — each will cross-reference direct reads of the past papers with NotebookLM synthesis.
>
> Scope confirmed from project.json:
> - Topic coverage for this paper: {{paperMeta.topicCoverage}}
> - Past-paper years available: {{YEAR_RANGE}}
> - MCQ section present: {{yes/no — check paperMeta.sections}}
>
> Each catalogue typically takes 5–10 minutes. Proceed?"

USER: confirm.

### ACTION — Dispatch three parallel agents (single message, three Task tool calls)

All three agents follow this shared briefing pattern. Adapt the specifics per catalogue.

**Shared briefing template (use for all three):**

```
Build the {{CATALOGUE_NAME}} for {{BOARD}} {{QUALIFICATION}} {{SUBJECT}} {{PAPER}}.

Target file: {{PROJECT_DIR}}/.project/catalogues/{{FILENAME}} — write with the Write tool.

Two independent sources — use BOTH and cross-reference:

1. Direct analysis (primary):
   - Past papers: {{PATH}}/Paper{{N}}-Question-{{YYYY}}.md (across available years)
   - Mark schemes: {{PATH}}/Paper{{N}}-MarkScheme-{{YYYY}}.md
   - Examiner reports: {{PATH}}/Paper{{N}}-ExaminerReport-{{YYYY}}.md
   - Spec: {{SPEC_PATH}} (with line ranges for in-scope topics)
   - AO guide: {{PROJECT_DIR}}/.project/ao-classification-guide.md (for calibration)
   - Misconception bank (read-only at this stage): {{PROJECT_DIR}}/.project/misconception-bank.md

2. NotebookLM (secondary, cross-check): notebook is already selected. Use 2–3 sharp queries max
   to validate or fill gaps. Example queries depend on the catalogue (see per-catalogue briefs below).

Rules:
- Every entry cites a real past-paper reference (e.g. "2022 Q11a"). No inventions.
- If the two sources disagree, record the discrepancy in a dedicated section — do not paper over it.
- Flag uncertain classifications with ⚠️ and explain briefly.
- Keep scope to THIS paper's topic coverage only (see project.json.paperMeta.topicCoverage).
```

#### Catalogue 1: AO question-type catalogue

Filename: `ao-question-type.md`. Agent-specific guidance:

- For each structured-question part across every past paper, capture: paper ref, stem quote (short), marks, command word, AO (inferred from AO classification guide if mark schemes don't embed per-mark AO codes — many boards omit these).
- Group by AO (AO1 block, AO2 block, AO3 block).
- For AO3, include the **novel information** the student must engage with.
- Also capture: cross-paper patterns (recurring structures, QWC/starred-question themes, opening-MCQ topic distribution).
- Aim for 40–100+ entries depending on paper format.

**NotebookLM queries (pick 2–3):**
- "Across Paper {N} {YEAR_RANGE}, which structured questions test {TOPIC}? Give refs and brief descriptions."
- "Which AO3 questions across Paper {N} involve evaluating a data-driven claim?"
- "List the 6-mark QWC/starred-question themes across recent sittings."

#### Catalogue 2: MCQ catalogue

Filename: `mcq-catalogue.md`. Skip this catalogue if the paper format has no MCQs (check `paperMeta.sections`).

Agent-specific guidance:

- For each MCQ: paper ref, topic, stem quote, correct answer letter, and **for each of the 3 distractors** what student error leads there.
- Cross-reference each distractor against the misconception bank (IDs M001+ and A001+). Cite by ID.
- Flag any distractor whose rationale doesn't match an existing misconception — these are **candidates for new entries** (propose IDs M{next}+).
- Flag any MCQ whose distractors collapse to a single misconception — those are the "too easy" anti-patterns the pipeline must avoid.
- Include an Appendix listing the new misconception candidates with suggested IDs, short names, descriptions, reasons, and sources.

**NotebookLM queries (pick 1–2):**
- "For Paper {N} MCQs on {TOPIC} across {YEAR_RANGE}, which distractors did students commonly pick and why?"
- Mostly use direct analysis — examiner reports and mark schemes give explicit distractor commentary for many boards.

#### Catalogue 3: Spec coverage map

Filename: `spec-coverage-map.md`.

Agent-specific guidance:

- **Critical:** scope to THIS paper's topic coverage from `project.json.paperMeta.topicCoverage`. Many boards split topics across papers non-contiguously (e.g. Edexcel A Level Physics Paper 1 = Topics 1, 2, 3, 6, 7, 8). Do not assume numerical-range topics.
- Read the spec at the correct line ranges for each in-scope topic. Extract numbered spec points verbatim.
- For each spec point, list which past-paper questions tested it and how (calculation / explanation / MCQ / extended response / not tested).
- Build a coverage analysis section: heavily-tested SPs (candidates to avoid or refresh with novel context), untested SPs (coverage candidates for the mock), tier/subject restrictions flagged.

**NotebookLM queries (pick 1–2):**
- "For each spec point in Topic {X} of the specification, list every Paper {N} past-paper question that tested it from {YEAR} onwards."

### CHECK 1 — All three agents returned

Wait for all three to complete. Read their short summaries.

### CHECK 2 — Catalogue quality (gate)

Reflect on each catalogue:
- Does it cite real past-paper references throughout?
- Does the AO catalogue contain ≥10 examples per AO tier?
- Does the MCQ catalogue cover every MCQ in every available paper?
- Does the spec-coverage map scope to the correct topics (not a naive 1–N range)?

[Conditional: any catalogue is thin or the agent hedged]
Re-dispatch the specific agent with sharper instructions (e.g. name years explicitly, name topic line ranges).

### ACTION — Produce `.project/board-conventions.md`

Dispatch a short `general-purpose` agent to synthesise the board-specific conventions from the three catalogues + past-paper reads + examiner reports. Use the template at `.claude/templates/board-conventions.template.md`.

Target file: `{{PROJECT_DIR}}/.project/board-conventions.md`

Content to extract from research:
- **Stem phrasing conventions:** scan past-paper stems across multiple years to identify the board's habits (figure intros, student-scenario intros, AO3 framing, data-table intros, "Show that" sig-fig convention).
- **Opening-question archetypes:** from the AO catalogue, identify what the first part of each topic's structured questions typically asks (Draw? Describe? Calculate? State?).
- **AO3 distribution pattern:** count AO3 items across the past papers. Are they lumped (single 3-mark final part per question) or spread (AO3 split across multiple parts)? Report N of M observed.
- **MCQ format distribution:** pull percentages directly from the MCQ catalogue.
- **"Show that" frequency:** count per paper across 5+ past papers; report min-max.
- **Question-count norm:** total questions per paper; report typical and range.
- **Mark tariff norms:** for each common cognitive demand, what tariff does the board use?
- **Miscellaneous conventions:** board-specific signatures worth flagging.

This file is the single source of board-specific knowledge. The pipeline skills (`/mock-2-outline`, `/mock-3-draft`, `/mock-4-review`) read from it rather than embedding board-specific examples in their own text. This keeps the skills subject/level/course-agnostic and makes the process replicable for any board.

### ACTION — Produce `.project/catalogues/ao-breadth-map.md`

Dispatch a short `general-purpose` agent to synthesise an **AO breadth map** from `ao-question-type.md` + the past-paper reads + `.project/command-word-list.md`. This is distinct from the AO classification guide (which answers "is this mark AO1/AO2/AO3?"): the breadth map answers "what is the FULL palette of ways this board tests each AO?" — so drafting designs from a menu rather than defaulting to one archetype per AO (the "same-y questions" failure mode: AO1 ≈ State, AO2 ≈ Calculate, AO3 ≈ Deduce).

Target file: `{{PROJECT_DIR}}/.project/catalogues/ao-breadth-map.md`

For each AO (AO1, AO2, AO3), tabulate from the past papers:
- **Command words** used to test it, with rough frequency (e.g. AO1 is not only "State" — also Describe, Give, Label, Complete, Identify, Write-an-equation, Sketch-a-known-diagram).
- **Task archetypes** (e.g. define, recall-a-mechanism, complete-a-diagram, direct calculation, multi-step calculation, resolve-and-apply, graph-read, evaluate-a-claim, compare-data-to-a-model, plan/refine a procedure).
- **Context types** (theoretical, practical/apparatus, data-handling, real-world scenario, historical).
- **Real past-paper examples** (refs) for each — no inventions.

End with a **palette summary per AO**: the complete set of command words and task archetypes observed, plus a one-line "prototype trap" note naming the single most over-used archetype to consciously vary away from (e.g. "AO2 default = 'Calculate'; vary with Show that / Determine / resolve-and-apply / graph-read").

`/mock-2-outline` gates the outline's per-AO variety against this file (CHECK 10); `/mock-4-review` re-checks it on the drafted paper (Review 8).

### ACTION — Merge MCQ catalogue's new misconceptions into the bank

The MCQ catalogue's Appendix flags new misconception candidates (typically 20–60 entries for a Paper with comprehensive MCQ analysis). Dispatch a single short agent to:

- Read the MCQ catalogue's "New misconceptions flagged" / Appendix section.
- Append them to `.project/misconception-bank.md`'s "Subject-specific misconceptions" table with sequential IDs (M{next}+).
- Merge where a new entry duplicates an existing one (add the additional source reference to the existing row rather than creating a new row).
- Update any stale caveats in the bank's header note.

### CHECK 3 — Cross-source discrepancies

For each catalogue, note anywhere direct analysis and NotebookLM disagreed. Typical patterns:
- NotebookLM underreports questions from papers it hasn't fully ingested
- NotebookLM's examiner-report excerpts are partial; direct reads are complete
- Direct analysis may classify a borderline AO3 differently from NotebookLM

Log these to `project.json.research.sourceDiscrepancies` for later reference. They inform how much to trust each source in downstream phases.

### CHECK 4 — Coverage-gap reflection (soft gate)

Read the spec-coverage map's analysis section. Reflect:
- Which untested spec points look interesting for the mock?
- Which heavily-tested spec points could be refreshed with a novel context vs avoided?
- Any spec points flagged as Higher-Tier-Only / HL-Only / Physics-Only that constrain what we can include?

Write these reflections to `project.json.research.coverageGaps` and `research.heavilyTested`.

### ACTION — MS calibration (HARD GATE): course mark-scheme conventions + exemplars

The mark-scheme rules that vary by course are **learned here, not prescribed**. This produces the Layer-2 inputs that the MS pre-flight gate in `/mock-3-draft` and the `marking-realism-checker` depend on. See `.claude/context/mark-scheme-standard.md` for the two-layer model (universal principles + learned course conventions).

1. **Select a calibration sample.** From `ao-question-type.md` + the past papers, pick a small set (typically 4–6) of real past-paper questions that between them span the course's full range of **mark-scheme requirements** — each distinct response mode and marking convention the catalogues reveal. Cover, wherever the course uses them: a multi-step calculation with ecf; a "show that"; a list / "any N from"; an extended-prose or levelled/banded (QWC) part; a graph/data read-off with tolerance; a define/state recall; a diagram/completion mark. Skip modes the course doesn't use.

2. **Draft SME-format SFMAs for the sample.** For each sampled question, write the full SFMA (stem + Model Answer + MS&G + ET&T) in SME house format, using the **real past-paper mark scheme as ground truth** for what earns each mark. Match the house format demonstrated in the **Gold Standard SFMA library** — the four cross-subject exemplar sets (defined-mark closed/open, levelled, MCQ; set IDs in `.claude/context/mark-scheme-standard.md`); pull the closest-matching type via `findQuestion` if a format is unfamiliar. Apply `/cobalt-formatting` and the universal principles in `mark-scheme-standard.md`. Because these calibrate against a *known* question, the official mark scheme is the check on your formatting.

3. **STOP — creator review (mandatory).**
> "MS calibration for {{PROJECT_NAME}}: I've drafted {{N}} SME-format SFMAs spanning the course's mark-scheme types ({{LIST_MODES}}), each formatted from the real past-paper mark scheme. Please review and tweak the mark schemes to the house standard you want — your edits become the reference pattern for drafting the whole paper. What would you change?"

Capture the creator's edits. Approved files → `.project/ms-exemplars/`.

4. **Synthesise `.project/mark-scheme-conventions.md`** from the approved exemplars — the Layer-2 dimensions in `mark-scheme-standard.md` (response modes and their command words, precision convention, "show that" extra-figure count, tolerance idiom, mark-type codes / ecf notation, banding structure + anchoring, list/grouping idiom, accept/reject idiom).

5. **Flag divergences.** Where the course's real mark schemes need a convention that differs from `mark-scheme-standard.md` or `/cobalt-formatting`, record it in a "Divergences from global rules" section of `mark-scheme-conventions.md` and surface it:
> "The {{COURSE}} mark schemes differ from our global rules here: {{LIST}}. Update the global rule, or keep it course-local? (e.g. {{EXAMPLE}})"

Apply the creator's decision — edit `/cobalt-formatting` or `mark-scheme-standard.md` if they choose global; otherwise keep it in the conventions file.

**HARD GATE:** research does not complete without `.project/ms-exemplars/` populated (creator-approved) and `.project/mark-scheme-conventions.md` written.

### ACTION — Update project.json

- Set `gates.research: "pass"`, `phase: 2`, `nextStep: "/mock-2-outline"`.
- Set `gates.msCalibration: "pass"` **only** when `.project/ms-exemplars/` is populated (creator-approved) and `.project/mark-scheme-conventions.md` is written; record their paths under `research.markSchemeCalibration`. Research is NOT complete without this — do not set `gates.research: "pass"` if MS calibration hasn't passed.
- Under `research`: record catalogue file paths, entry counts, coverage gaps, heavily-tested SPs, source discrepancies.

### Final output to user

```
Research complete for {{PROJECT_NAME}}.

Catalogues written:
- .project/catalogues/ao-question-type.md ({{N}} parts · AO1 {{A}} / AO2 {{B}} / AO3 {{C}})
- .project/catalogues/mcq-catalogue.md ({{N}} MCQs · {{M}} distractors tagged to misconceptions)
- .project/catalogues/spec-coverage-map.md ({{N}} spec points across Topics {{SCOPE}})

Board conventions captured: .project/board-conventions.md
(stem phrasings, opening archetypes, AO3 pattern, MCQ format distribution, Show-that frequency, question-count norm, mark tariff norms)

AO breadth map captured: .project/catalogues/ao-breadth-map.md
(per-AO palette of command words × task archetypes × contexts — the design menu that prevents same-y questions)

Misconception bank extended: +{{N}} new entries (now {{TOTAL}} total).

MS calibration: {{N}} exemplar SFMAs approved → .project/ms-exemplars/
Course MS conventions → .project/mark-scheme-conventions.md ({{K}} divergences from global rules flagged)

Coverage flags:
- Heavily-tested spec points (avoid re-running without novel context): {{LIST}}
- Untested spec points (coverage candidates): {{LIST}}
- Cross-source discrepancies noted: {{N}}

Next: /mock-2-outline
```

## Rules

- **Direct analysis is primary.** If you're ever tempted to use NotebookLM alone, don't — it hedges on papers it hasn't fully ingested and its examiner-report excerpts are often partial.
- **NotebookLM for cross-check and synthesis** — 2–3 sharp queries per catalogue is the right dose. Don't burn 20 queries.
- **Scope to this paper's topics.** Many boards split non-contiguously. Check `paperMeta.topicCoverage` — never assume Topics 1–N.
- **Record discrepancies between sources** — disagreement is valuable signal, not noise.
- **Every entry cites a real paper-question ref.** Flag any fabrication hallucinated by NotebookLM.
- If the markdown past papers haven't been converted from PDFs, STOP and tell the user — Phase 1 depends on them.
- **MS calibration is a hard gate.** Research is not complete until the creator has approved the exemplar SFMAs (`.project/ms-exemplars/`) and `.project/mark-scheme-conventions.md` is written. These are the course-specific inputs the `/mock-3-draft` mark-scheme gate audits against — learned from the course's real mark schemes, never guessed.
