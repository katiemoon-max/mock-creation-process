# Mark Scheme Standard — Smart Mark-ready MS&G

A reliable mark scheme needs two things: it follows the **house SFMA format** (learned from real exemplars — not prescribed here), and every marking point is **Smart-Mark-ready** (the universal principles and gate in this file). This file holds only the second part; it does not re-invent the format.

## Where the format guidance lives — the Gold Standard SFMA library

The definitive, cross-subject exemplars of SFMA and MS&G *structure* are the **SME Gold Standard SFMA library** in Cobalt — four sets covering the whole SFMA taxonomy (pull any via `findQuestion` with the set ID):

- **Defined mark — closed:** `tqst_y47V8W9YsPkTCKdC` — fixed-answer point-marked: recall, define/state, describe, explain/justify, calculation (single/multi-step and with alternative methods), graph/data, table/list, diagram completion — with before/after "original vs gold standard" pairs.
- **Defined mark — open:** `tqst_hTnJnWfxV3jdxcp7` — open-response point-marked, where marks turn on an accept-list rather than a single fixed answer.
- **Levelled response:** `tqst_BRC4pXkf3BVy9nnt` — the Level 3/2/1 descriptor + indicative-content structure (Evaluate, Plan, extended Describe).
- **MCQ:** `tqst_ptq6pZp3h474X24B` — free-text explanation format (bold-green correct answer, paragraph distractor explanations, no MS&G callout).

These span subjects and boards (Physics, Chemistry, Biology, Geography, Maths, AP, CIE), so they show *what a gold-standard SFMA of each type looks like* far more definitively than any prose rule could. **Do not duplicate them here.** Per project, the calibration step in `/mock-1-research` draws on this library plus the course's real mark schemes to produce `.project/ms-exemplars/` and `.project/mark-scheme-conventions.md`.

## Two layers

- **Layer 1 — universal principles (below):** what makes any marking point reliably auto-markable, on any course.
- **Layer 2 — course conventions** (`.project/mark-scheme-conventions.md` + `.project/ms-exemplars/`, learned in `/mock-1-research`): the course's format and idioms — precision convention, whether/how it uses levelled marking, tolerance style, mark-type codes. Whenever a Layer-1 principle needs a concrete value, it comes from Layer 2 (or the library).

Consumers: `/mock-3-draft` builds against both layers + the library format, then self-audits with the gate (§ below); `marking-realism-checker` audits against the same; `/cobalt-formatting` supplies the Cobalt syntax.

---

## Layer 1 — universal Smart-Mark principles

Smart Mark awards a mark by matching a response against an explicit, closed criterion. It cannot interpret open prose, infer intent, or "award on spirit". Therefore, on every course:

1. **Tag-ability.** Every marking point is a discrete, closed, unambiguous criterion.
2. **MS demand == command-word demand.** Credit neither more nor less than the command word asks. The Describe/Explain conflation — crediting reasoning under "Describe", or a bare number under "Explain" — is the most common Critical defect. If the MS you want to write demands *more* than the command word licenses, **change the command word, not the MS**. (Authoritative command words and their demands: `.project/command-word-list.md`.)
3. **Closed accept-lists.** Every `Accept:` is a finite, enumerated list of specific alternatives. Never "any reasonable / or similar / words to that effect / etc."
4. **ecf explicit.** Wherever a part uses a value produced earlier, name the source and trace ecf through the whole chain (b → c → d), not just the first hop.
5. **Grouping explicit.** State "Any N from:"; say when one statement earns two marks; never bundle two distinct checks into one mark silently.
6. **Precision, tolerance and units are stated.** The *principle* is universal; the *values and idioms* (s.f. vs d.p., the "show that" extra-figure count, the read-off tolerance) are course-specific → Layer 2.
7. **Alternatives enumerated.** List every valid method or phrasing a student might use that Smart Mark would otherwise reject.
8. **MS&G holds marking content only.** Marking points, accept/reject, credit guidance, alternatives — nothing else. No commentary or teaching (that is ET&T); not a duplicate of a Model Answer that already shows every pathway.

**Demand families (map the course's command words onto these — the mapping is Layer 2):** recall (fact only) · account/Describe (linked points, no causal link) · reasoning/Explain (the causal link) · quantitative/Calculate (working + answer as separable marks) · judgement/Evaluate·Deduce (the weighing behind the verdict, not the verdict alone).

## Levelled / extended responses

Do **not** point-mark. Use the house levelled structure demonstrated in the levelled library set (`tqst_BRC4pXkf3BVy9nnt`): an up-front "this is a levelled response question — each point does not equal one mark", a **Mark allocation** block placing answers into Levels (e.g. 3/2/1 with mark ranges and prose descriptors covering coverage, quality and logical progression), and an **Indicative content** block organised by stage/section with the creditable key points in **bold**. Take the exact level count and descriptor wording from the course's real levelled mark schemes (Layer 2) — the library shows the SME format; the board sets the specifics.

## Layer 2 dimensions (learned, not prescribed)

Captured in `.project/mark-scheme-conventions.md` during calibration: response modes and which command words map to which; precision convention (s.f./d.p., "show that" extra-figure count); read-off tolerance idiom; mark-type codes and ecf-notation style; whether the course uses levelled marking and its level structure; list/grouping idiom; accept/reject idiom; units and notation (defer to `/cobalt-formatting` §8 and `.project/board-conventions.md`).

---

## Common mistakes (universal anti-patterns)

- MS&G that duplicates a Model Answer already showing all pathways
- commentary / teaching / strategy inside MS&G (belongs in ET&T)
- "any reasonable" / prose-only accept clauses Smart Mark cannot tag
- point-marking a levelled response, or bundling two distinct checks into one mark
- bare "correct answer" with no precision/unit expectation
- ecf implicit, or specified only for the first hop of a multi-part chain
- MS demand ≠ command-word demand (Describe/Explain conflation)
- ambiguous accept-range notation — a dash between a rounded value and a more-precise one reads ambiguously (a range, or "either of these two"?); write an explicit interval, or list the discrete accepted values
- **"claims-compliance" hallucination** — the MS *says* a rule is applied ("significant figures specified") but the value is missing or ambiguous. Verify the rule is really implemented, not just named.

---

## §9 — MS&G pre-flight gate (per marking point)

Run before a question is marked "drafted". `/mock-3-draft` gates on it (hard); `marking-realism-checker` audits against it.

**Universal checks (every course)**
- [ ] discrete, closed, tag-able marking point
- [ ] MS demand == the command word's demand (else the command word is flagged for change)
- [ ] every Accept is an enumerated, closed list (no "any reasonable")
- [ ] explicit ecf line for every cross-part dependency, traced through the whole chain
- [ ] grouping explicit; no two distinct checks silently bundled; levelled parts not point-marked
- [ ] required precision, tolerance and units stated (not left implicit)
- [ ] alternative valid responses/methods enumerated
- [ ] no commentary inside MS&G; not a duplicate of a complete Model Answer; no claims-compliance gap

**Course-convention checks (per `.project/mark-scheme-conventions.md` + `.project/ms-exemplars/` + the Gold Standard library)**
- [ ] precision stated in the course's convention (correct s.f./d.p.; correct "show that" extra-figure count)
- [ ] tolerance expressed in the course's idiom
- [ ] mark-type codes / ecf notation in the course's style
- [ ] levelled parts built in the house Level/indicative-content structure with the course's level wording
- [ ] overall format matches the approved `.project/ms-exemplars/` and the Gold Standard library
