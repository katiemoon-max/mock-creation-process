---
name: mock-0-setup
description: Initialise a mock paper project with full subject-agnostic onboarding — gathers board/qual/subject/paper, verifies spec and past papers, checks MCPs, captures exclusion list and difficulty targets, generates AO classification guide and seeds misconception bank, and writes project.json + project-level CLAUDE.md. Run once per new paper before any other /mock-* skill.
user_invocable: true
arguments: "[project_dir]"
allowed-tools: Read, Glob, Grep, Write, Edit, Bash, Task, mcp__notebooklm__get_health, mcp__notebooklm__select_notebook, mcp__notebooklm__list_notebooks, mcp__notion__notion-search, mcp__notion__notion-fetch
---

# Mock Paper Setup (Phase 0)

You are running the subject-agnostic onboarding for a new mock paper project. This is the **keystone** of the pipeline — everything downstream relies on what you capture here. Front-load all constraints; don't leave anything to be re-stated during drafting.

This skill uses scripted markers:

- `STOP:` Pause and ask the user the question verbatim.
- `ACTION:` Perform the tool call / file write.
- `CHECK:` Self-reflect and log the answer to `project.json.qualityGates`.
- `[Conditional]:` Branch.

## Prerequisites

None — this is Phase 0. But read the vault CLAUDE.md, `.claude/context/sme-overview.md`, and `.claude/context/quality-standards.md` before starting so the Role, ACE tone, and CQI are loaded.

## Script

### STOP 1 — Project identity

> "Great, let's set up a new mock paper project. I need four things to get started:
> 1. **Exam board** (AQA, OCR, Edexcel, CIE/CAIE, IB, AP, WJEC, Oxford AQA, SQA)
> 2. **Qualification** (e.g. GCSE, IGCSE, A Level, AS Level, IB HL, AP Physics 1, National 5, Higher)
> 3. **Subject** (e.g. Biology, Chemistry, Physics, Psychology, Geography)
> 4. **Paper** (e.g. Paper 1 Higher, Paper 2, Paper 3A)
>
> If this is a tiered paper (Foundation / Higher), I'll plan both tiers together later, but tell me which we're starting with."

USER: board, qualification, subject, paper.

ACTION: Record in a scratch variable. Compute `project_dir` default: `02 - Projects/{{BOARD}} {{QUALIFICATION}} {{SUBJECT}}/{{PAPER}}/`.

### STOP 2 — Project directory

> "I'll create the project at `{{project_dir}}`. Is that right, or do you want a different path?"

USER: confirm or alternative path.

ACTION: Create the project directory plus subfolders: `Section A/`, `diagrams/`, `reviews/`, `publish/`, `.project/`, `.project/catalogues/`.

### CHECK 1 — Spec availability (HARD GATE)

ACTION: Look for the spec markdown file. Expected locations in order:
1. `03 - Resources/Spec Vault/{{BOARD}}/{{QUALIFICATION}}/{{SUBJECT}}/spec.md`
2. `03 - Resources/Spec Vault/{{BOARD}}/{{QUALIFICATION}}/spec.md`
3. Ask the user if neither is found.

[Conditional: if found] Record path in `qualityGates.specPath`.

[Conditional: if not found]
> STOP: "I can't find a local markdown spec at the expected paths. Could you place one at `03 - Resources/Spec Vault/{{BOARD}}/{{QUALIFICATION}}/{{SUBJECT}}/spec.md`? Without a local spec file, the pipeline cannot proceed — this is to prevent Claude from hallucinating spec points from training data. I'll wait."

Do NOT proceed past this gate without a spec file. This addresses the spec-hallucination failure mode.

### CHECK 2 — Past papers and examiner reports

ACTION: Count markdown files in `references/` or the board's past-papers folder (ask user for the path if unclear). Require **≥5 past papers** and **≥2 examiner reports**.

[Conditional: if fewer than required]
> STOP: "I found {{N}} past papers and {{M}} examiner reports, but we need at least 5 papers and 2 reports to calibrate question difficulty, structure, and distractor archetypes. Can you point me to where they live, or add more?"

Record `qualityGates.pastPaperCount` and `qualityGates.examinerReportCount`.

### CHECK 3 — NotebookLM

ACTION: Call `mcp__notebooklm__get_health`. If healthy, call `mcp__notebooklm__list_notebooks`.

STOP 3:
> "Which NotebookLM notebook contains all past papers, the spec, and examiner reports for this paper? Paste the URL or tell me the name."

USER: notebook URL/name.

ACTION: `mcp__notebooklm__select_notebook`. Record URL in `qualityGates.notebookLmUrl`, set `notebookLmHealth: "ok"` if successful.

[Conditional: if health or selection fails] Flag to user, allow them to troubleshoot or skip (but mark gate as failed).

### CHECK 4 — Notion and SME MCPs

ACTION: Quick probe — `mcp__notion__notion-search` with a trivial query. Set `qualityGates.notionReachable` accordingly.

ACTION: Check if SME MCP is configured (look for `mcp__sme__*` tools). If not available, warn user it will block `/mock-5-publish` later but not now.

### STOP 4 — Master Syllabus CSV

> "Do you have a Master Syllabus CSV for this course? It should live in `references/` and map spec points to topic names, tier flags, and combined-science flags. If you have one, tell me the path. If not, I'll generate a stub from the spec markdown and you can confirm it before we proceed."

ACTION: Either record the path or generate a stub CSV from the spec (one row per spec point, blank for tier/combined flags).

Record `qualityGates.masterSyllabusPresent: true` only if the creator confirms the file is accurate.

### STOP 5 — Paper-specific AO targets

> "What are the AO weighting targets for THIS SPECIFIC PAPER (not the overall qualification)? For example, AQA A Level Physics Paper 2 targets AO1=40%, AO2=45%, AO3=15% — even though the overall qualification is different. Check the spec or examiner reports and give me the paper-specific percentages."

USER: AO1, AO2, AO3 percentages.

ACTION: Record in `paperMeta.aoTargets`. If the user is unsure, invoke the `exam-researcher` sub-agent with a clear prompt to find the paper-specific targets from the spec and examiner reports.

### STOP 6 — Difficulty targets (LoD ramp)

> "Let's set the difficulty ramp. For a {{TOTAL_QUESTIONS}}-question paper, the typical ramp is E → E-M → M → M → M-H → M-H → H → H → H → H. Do you want to accept that, or customise? Also confirm:
> - Mean score target (typical: 55–65%)
> - Reading level target (B2 for GCSE / IGCSE, C1 for A Level, B2 for EAL/IB)"

USER: ramp + mean + reading level.

ACTION: Write `.project/difficulty-targets.md` from the template, filling in the per-question LoD, mean score, reading level, year-group register rules, and word ceilings.

### STOP 7 — Exclusion list

> "Any topics, classic contexts, studies, or examples I should NOT use in this paper? Common reasons: 'already tested in Paper 1', 'students over-revise this example', 'sensitive context'. Give me whatever comes to mind — I'll persist these so every drafting batch respects them."

USER: exclusion items.

ACTION: Write `.project/exclusion-list.md` from the template, populating the relevant sections. If the user has a sister paper in the vault, offer to scan it for already-tested command-word + AO + topic triples and add those to the sister-paper section.

### ACTION — AO classification guide

Invoke the `exam-researcher` sub-agent with this prompt:

> "Build an AO classification guide for {{BOARD}} {{QUALIFICATION}} {{SUBJECT}}. Using the past papers and mark schemes in NotebookLM (notebook: {{NOTEBOOK_URL}}) and the spec at {{SPEC_PATH}}:
>
> 1. Extract the AO definitions from the spec.
> 2. Find 3–4 real exemplar questions per AO (AO1, AO2, AO3) from recent past papers. For each, quote the stem and explain in 2–3 sentences why the mark scheme classifies it that AO.
> 3. For AO3 exemplars specifically, identify what novel information the student must engage with (the thing that makes it AO3 not AO1/AO2).
> 4. Compile common AO misclassifications on this board (from examiner report commentary).
>
> Write the output to `.project/ao-classification-guide.md` using the template at `.claude/templates/ao-classification-guide.template.md`. Do not invent examples — if you can't find 3–4 real exemplars for a given AO, return fewer and flag the gap."

### ACTION — Command word list

Invoke `exam-researcher`:

> "List every approved command word for {{BOARD}} {{QUALIFICATION}} {{SUBJECT}} structured questions. Source: the command-word glossary section of the spec (or equivalent on the board's website). For each, give: the official definition, the typical mark count, and the cognitive demand expected. Write to `.project/command-word-list.md`. Do not include command words not on the approved list, even if they appear in adjacent boards."

### ACTION — Misconception bank seed

Invoke `exam-researcher`:

> "Read the examiner reports in the NotebookLM notebook. Extract common misconceptions flagged across reports. For each, give: a short ID (e.g. M012), a short name, a 1-2 sentence description, why students make the error, and the source report. Write to `.project/misconception-bank.md`, appending to the template's 'Subject-specific misconceptions' table. Include the subject-agnostic archetypes (A001–A006) already in the template — do not duplicate them."

### ACTION — AO targets file

Write `.project/ao-targets.md` with the paper-specific AO percentages from STOP 5 and a short reminder that tolerance is ±3%.

### ACTION — Project CLAUDE.md

Write `CLAUDE.md` in the project root using `project-claude-md.template.md`, substituting `{{BOARD}}`, `{{QUALIFICATION}}`, etc. Ensure the imports at the top actually point to files that now exist.

### ACTION — project.json

Write `project.json` using `project.json.template`, populating every field you captured above. Set `phase: 0`, `status: "in_progress"`, `gates.setup: "in_progress"`.

### ACTION — setup-verification.md

Write `.project/setup-verification.md` with a checklist of all gates:

```markdown
# Setup Verification

- [{{X}}] Spec markdown located: {{PATH}}
- [{{X}}] Past papers ≥ 5: found {{N}}
- [{{X}}] Examiner reports ≥ 2: found {{M}}
- [{{X}}] NotebookLM health: {{STATUS}}
- [{{X}}] NotebookLM notebook selected: {{URL}}
- [{{X}}] Notion MCP reachable: {{STATUS}}
- [{{X}}] Master Syllabus present: {{STATUS}}
- [{{X}}] AO targets confirmed: {{AO1}}/{{AO2}}/{{AO3}}
- [{{X}}] Difficulty targets captured
- [{{X}}] Exclusion list captured ({{N}} items)
- [{{X}}] AO classification guide generated
- [{{X}}] Command word list generated
- [{{X}}] Misconception bank seeded ({{N}} subject-specific entries)
```

### CHECK 5 — Setup complete

Reflect on the project.json and setup-verification.md:

> "Are all the critical gates green? If any are yellow or red, say why and offer a remediation path. Do not mark phase 0 complete if any HARD GATE (spec, past papers, NotebookLM) is failed."

[Conditional: all green] Set `project.json.gates.setup: "pass"`, `phase: 1` (ready for Phase 1), `status: "complete"` (for this phase), `nextStep: "/mock-1-research"`.

### Final output to user

Print a concise summary:

```
Setup complete for {{PROJECT_NAME}}.

Created:
- project.json
- CLAUDE.md (project-scoped, imports constraints)
- .project/ao-classification-guide.md ({{N}} exemplars)
- .project/command-word-list.md ({{N}} command words)
- .project/misconception-bank.md ({{N}} misconceptions seeded)
- .project/exclusion-list.md ({{N}} items)
- .project/difficulty-targets.md
- .project/ao-targets.md ({{AO1}}/{{AO2}}/{{AO3}})
- .project/setup-verification.md

Next: /mock-1-research
```

## Rules

- Do not proceed past a failed HARD GATE (spec, past papers, NotebookLM). The whole point of this phase is to front-load these checks.
- Every STOP is a real pause — wait for the user's response. Do not fill in plausible defaults on their behalf.
- If a sub-agent returns empty or suspicious output, surface it to the user — don't paper over gaps.
- The files written here are the single source of truth for all downstream skills. Be precise.
