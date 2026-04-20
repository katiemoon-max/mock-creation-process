# Assessment Design Review Checklist

> Derived from AQA's Principles of Assessment professional development materials (2024), adapted to be subject/course/level-agnostic. Apply to every mock exam question and paper as a complement to CQI scoring.

Where a check references a specific value (reading age, AO target, mark limits, tier structure), **it should come from the project's `.project/*` files** — not be hardcoded here. This file is the set of principles; the project CLAUDE.md imports carry the board-specific numbers.

## Per-Question Checks

### 1. Validity & Command Word Alignment
- [ ] Command word matches what the MS actually rewards (e.g. "Explain" MS must not only reward "State")
- [ ] Command word is on the board's approved list (check `.project/command-word-list.md`)
- [ ] No hidden marking rules — student can infer what's expected from the question alone
- [ ] Question assesses the intended spec point, not something adjacent
- [ ] Mark scheme constructed *with* the question — MS reflects the actual cognitive demand

### 2. Construct Irrelevant Variance (CIV)

**CIV-Difficulty** (barriers unrelated to subject knowledge):
- [ ] No propositionally dense sentences (one idea per sentence)
- [ ] No ambiguous phrasing (check "only", "that", unclear referents)
- [ ] Cognitive load is minimised — only information needed to answer is given
- [ ] Reading level matches the target in `.project/difficulty-targets.md` (CEFR / Hemingway level)
- [ ] No context that requires specific cultural/socioeconomic knowledge

**CIV-Easiness** (unintended clues):
- [ ] No grammatical cues in MCQ options (e.g. "an" revealing vowel-starting answer)
- [ ] No verbal association between stem and key in MCQs
- [ ] Later parts do not give away earlier answers (information leakage — enforced also in `/mock-3-draft`)
- [ ] Images do not narrow or misdirect student responses
- [ ] Question stem does not name the answer to its own MCQ

### 3. Differentiation & Demand Ramping
- [ ] Demand ramps within the question (easy opening part → harder closing part)
- [ ] Multi-mark parts would yield a spread of scores (not clustering at 0 or full marks)
- [ ] Levelled responses (if the board uses them) have clear daylight between levels and sensible progression
- [ ] The question contributes to the paper's overall difficulty ramp (see `.project/difficulty-targets.md`)

### 4. Cognitive Load & Working Memory
- [ ] Question contains minimum information required to answer
- [ ] Students do not need to hold >5 values/concepts simultaneously without scaffolding
- [ ] Information is given where it's needed (not buried in an earlier part they must hunt for)
- [ ] Multi-step calculations have appropriate scaffolding for the level
- [ ] "Show that" values are provided where earlier answers feed into later parts (preventing ecf cascades)

### 5. Language & Accessibility
- [ ] Sentence length reasonable (typically <20 words)
- [ ] Familiar vocabulary used (could a simpler synonym replace any word?)
- [ ] Technical subject vocabulary retained where the spec requires it — do not dumb down
- [ ] One command word per sentence
- [ ] Command word at start of question line (or close to it)
- [ ] Question sentence is the last before answer lines / mark tariff
- [ ] Bold prompts for key instructions (e.g. **two**, **one**)
- [ ] Figures referenced only after they appear

### 6. Context, Bias & Sensitivity
- [ ] Context accessible to all students regardless of background (global audience)
- [ ] No distressing scenarios (PARSNIPS filter applied)
- [ ] Images activate the right expectations (not misleading)
- [ ] Context is authentic — reflects how the subject is used in real life or in a laboratory/field setting
- [ ] No systematic bias towards/against particular student groups
- [ ] Exclusion list respected (`.project/exclusion-list.md`)

### 7. Mark Scheme Quality
- [ ] MS type matches question type (objective / points-based / levels of response)
- [ ] Levelled responses: clear progression across levels, qualitatively distinct descriptors
- [ ] Points-based: no mismatch between command word demand and what earns marks
- [ ] Acceptance criteria are explicit and comprehensive (Accept / Do not accept for list-style questions — Smart Mark requirement)
- [ ] Significant figures specified where the answer is numerical
- [ ] ecf chains correctly specified and clearly labelled
- [ ] "Show that" MS gives unrounded answer to 2 extra s.f. beyond the stem's stated value
- [ ] No mark scheme overlap between parts (same knowledge rewarded twice)

### 8. Question Structure
- [ ] Overarching stem links all parts thematically
- [ ] Parts cascade logically (each builds on or follows from the previous)
- [ ] No abrupt context shifts mid-question (or if there is one, it's signposted)
- [ ] Mark tariffs visible to students
- [ ] Scaffolding appropriate for the level/tier per `.project/difficulty-targets.md`
- [ ] Stem-usage audit: every piece of information in the stem is used by at least one part

## Paper-Level Checks

### Differentiation
- [ ] Difficulty ramps across the paper (opening question most accessible → closing most demanding)
- [ ] Each question contains parts at different demand levels
- [ ] Mark distribution would approximate a normal curve across the cohort
- [ ] LoD ramp matches the plan in `.project/difficulty-targets.md`

### Construct Coverage
- [ ] All in-scope topics represented (see `project.json.paperMeta.topicCoverage` — this varies per paper per board; do NOT assume a contiguous range)
- [ ] AO weightings within tolerance of target in `.project/ao-targets.md` (typically ±3%)
- [ ] Required practicals / core practicals / fieldwork represented where the board requires it (board-specific — check spec)
- [ ] Mathematical / quantitative skills tested at appropriate demand levels where the board requires it
- [ ] Extension / stretch content present if the paper is a Higher-tier or HL variant

### Paper Structure
- [ ] Extended-response count and format match the board's convention (check past papers; e.g. QWC / starred questions)
- [ ] MCQ marks within the board's regulatory limits (check spec — some boards cap closed-response marks)
- [ ] Extended response questions are ≥4 marks each, totalling a meaningful % of the paper (typically ≥15%)
- [ ] Paper timing is realistic (~1 mark per minute for most boards; check past papers for exceptions)
- [ ] Section structure (e.g. Section A MCQs + Section B structured) matches past papers

### Tiered-Paper / HL-SL Overlap Quality (conditional — only if the board has tiers or HL/SL split)

Apply these only when `project.json.project.paper` indicates a tier (Foundation / Higher) or level variant (HL / SL) with a paired counterpart:

- [ ] Common questions across tiers test the same construct at comparable demand
- [ ] Higher / HL versions are not easier than Foundation / SL versions of the same content
- [ ] Higher-only / HL-only extensions genuinely extend the demand (not just "more of the same")
- [ ] Shared-mark overlap matches the board's convention (e.g. Edexcel GCSE Physics typically ~27 shared marks)

### Cross-Qualification Reuse (conditional — where applicable)

For qualifications with co-ordinated / combined science variants (e.g. GCSE Combined, IGCSE Co-ordinated), or HL papers that source SL content:

- [ ] Spec points flagged as "Physics Only" / "HL Only" / "Higher Tier Only" identified
- [ ] Reusable questions flagged in the tracker (`Suitable for Combined?` / `Suitable for Co-ordinated?` / `Suitable for SL?` column)

## How this checklist is used in the pipeline

- **`/mock-2-outline` (Phase 2):** Section 8 (question structure) and the paper-level differentiation/construct-coverage checks inform outline design before drafting.
- **`/mock-3-draft` (Phase 3):** Per-question checks 1, 2, 4, 5, 6, 7 inform drafting decisions in each batch.
- **`/mock-4-review` (Phase 4):** The whole checklist is applied automatically to every drafted question and written to `reviews/assessment-design.md`.
