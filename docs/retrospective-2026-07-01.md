# Retrospective — 2026-07-01: Papers 1–3 process review

After Edexcel A Level Physics Papers 1–3 were completed and archived, we reviewed the whole run — comparing where drafts started against where the published questions ended up — to find where the process worked well and where the manual editing concentrated. Two themes dominated, and both became pipeline changes.

## Finding 1 — the pipeline optimised balance and typicality, but not breadth

A paper could pass every Phase-2 gate (AO balance ±3%, command-word/AO/topic non-duplication) and every Phase-4 gate (CQI 48/50, NotebookLM typicality 5/5) and still be *monotone* — every AO1 mark a "State", every AO2 a "Calculate", MCQ formats repeated, difficulty skewed easy. Paper 1 passed the publish gate and was then substantially re-scoped **by hand** for variety, spec-breadth and difficulty. The gates measured balance and typicality; nothing measured breadth of sampling.

**Changes:**
- **Phase 1** now builds an **AO breadth map** (`.project/catalogues/ao-breadth-map.md`) — the board's full palette of command words × task types × contexts per AO, so drafting designs from a menu rather than the prototype.
- **Phase 2** adds three soft-but-mandatory gates: per-AO variety, difficulty distribution (vs `difficulty-targets.md`), and intra-paper context/format freshness.
- **Phase 3** designs each batch's command words and contexts from the breadth map (and no longer regresses a planned format into the per-AO prototype).
- **Phase 4** adds a **breadth-and-variety re-check** (Review 8) on the *drafted* paper — drafts can regress from a varied outline; a monotone AO or a target-missing difficulty spread is a Critical publish-blocker.

## Finding 2 — mark-scheme construction was the biggest single source of manual edits

The Phase-4 marking-realism audit of the Paper 1 drafts found the manual-edit load concentrated in MS construction: 9 missing significant-figure requirements, 4 command-word ↔ MS-demand mismatches (Describe MS rewarding reasoning; Explain MS rewarding only a number), 2 missing ecf chains, 3 "any reasonable" prose accept clauses Smart Mark can't tag. Almost all of the publish-blocking Critical/Major findings were mark-scheme construction. Root cause: the construction checklist used at drafting was thinner than the audit checklist used at review, and there was **no MS gate at draft time**.

A first attempt at a fix — a comprehensive `mark-scheme-standard.md` — was too prescriptive and quietly Physics-shaped (it embedded an Edexcel-style banding table as if universal). MS conventions vary too much across subjects to enumerate.

**Changes (learned-not-enumerated):**
- New `context/mark-scheme-standard.md` in **two layers**: Layer 1 = universal Smart-Mark-readiness principles + a pre-flight gate; Layer 2 = course conventions that are **learned**, not prescribed.
- **Phase 1** adds an **MS calibration** step (hard gate): sample past-paper questions spanning the MS-requirement range → draft SME-format SFMAs against the real mark schemes → creator reviews/tweaks → `.project/ms-exemplars/` + `.project/mark-scheme-conventions.md`. Divergences from the global rules are flagged for a keep-local-or-update-globally decision.
- **Phase 3** adds a **Smart-Mark pre-flight** hard gate (CHECK 6): every MS&G is audited per marking point before the question is "drafted" — sig-figs, units, ecf-through-the-chain, closed accept-lists, grouping, command-word alignment. If the MS wants a demand the command word doesn't license, the command word is changed, not the MS.
- The `marking-realism-checker` agent now audits against the same two layers, so **construction standard == audit standard** and Phase 4 becomes confirmation rather than defect discovery.
- The definitive format reference is the **SME Gold Standard SFMA library** (Cobalt exemplar sets: defined-mark closed/open, levelled, MCQ). `mark-scheme-standard.md` and `cobalt-formatting` §11 point to it instead of embedding a single subject-flavoured example.

## Finding 3 — "done" drifted from "shipped"

Papers were substantially reworked in Cobalt *after* the publish gate, but the local mirrors and evaluation artefacts didn't track it (session-startup `/cobalt-sync --check` catches only header drift, not content changes). **Phase 5** now carries a discipline rule: run `/cobalt-sync --full` after any post-gate rework.

## Principle reinforced

Every change here follows the pipeline's founding rule — **skills stay generic; course-specific knowledge is learned into `.project/` files.** The AO breadth map, the MS conventions, and the calibration exemplars are all learned per course, exactly like `board-conventions.md`. If a rule can only be stated for one subject, it belongs in Layer 2, not the skill.
