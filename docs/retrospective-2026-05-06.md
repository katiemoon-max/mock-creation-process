# Retrospective — 2026-05-06: Paper 2 end-to-end (Edexcel A Level Physics 9PH0/02)

> Pipeline's second full end-to-end run. Followed Paper 1 (April 2026, 19/19) with Paper 2 (May 2026, 20/20 published to Cobalt). This retrospective focuses on what was new vs Paper 1: the multi-iteration review pattern, mass-conserving fix sweeps, second-paper Cobalt format gaps, and skill-improvement candidates surfaced for Phase 3 + Phase 4.

## What worked well (carried forward from Paper 1)

- **Hard gates at every phase** caught issues early. Phase 4 typicality check (NotebookLM word-for-word per question + Section B cohesion) surfaced 3 Criticals on the post-fix paper that the SFMA-stage review had missed.
- **Phase 5 spec-point matching pre-flight (CHECK 0.5)** — added after the 2026-05-05 Paper 1 Q3 friction incident — passed cleanly for all 20 Paper 2 parts. No surrogate-tagging flagged. Confirms the gate is doing its job.
- **Subject-agnostic skills + per-project `.project/` knowledge** held up across the second paper. The `board-conventions.md` from Phase 1 captured Paper 2-specific stem phrasings (Edexcel "named-object" scaffolding, "Show that … is about X" cascade pattern, AO3 "Deduce/Determine whether…" lump) that informed every drafting batch.
- **Multi-perspective Phase 4 review.** The three sub-agents (`spec-examiner`, `student-simulator`, `marking-realism-checker`) caught complementary issue classes: spec-examiner found out-of-spec content (Q18(a) dark matter, Q14(d) photosynthesis biology drift); student-simulator caught wording ambiguity (Q16(c) "single BMMD measurement"); marking-realism flagged Smart Mark anchoring gaps (ecf misallocation, MS&G table gaps, rounding-noise boundaries). NotebookLM macro/cohesion review added a fourth orthogonal lens.

## What was new (specific to Paper 2)

### Two re-review passes were needed before publish

- **Rerun #1** closed the 3 word-for-word Criticals NotebookLM raised + the deferred C9 from initial review.
- **Rerun #2** then surfaced 3 NEW spec-examiner Criticals (Q16(c) sketch tariff persisted, Q18(a) "describe three observations" drifted to out-of-spec dark-matter content, Q14(c) under-tariff vs precedent) + 3 marking-realism Smart Mark blockers (Q13(c) needed formal MS&G table, Q15(d) ecf misallocation, Q16(d) rounding noise blocked discriminator).
- Insight: NotebookLM's typicality lens and the sub-agents' Smart-Mark / spec-vocab lens find different issue classes. Both rounds were necessary. Future runs should plan for two re-review passes by default after large fix sweeps.

### Mass-conserving "Path A" fix sweep

- Edexcel papers are rigorously 90 marks. NotebookLM's tariff-up recommendations (sketches 1→2, definitions 1→2, etc.) collectively would have pushed the paper to ~100 marks.
- Solution: paired tariff-up with tariff-down using same-question or different-question swaps that net to zero (e.g. Q14(c) +1 marked AO2 / Q14(d) −1 AO1 within the same question; Q16(c) +1 / Q18(a) −1 across questions).
- AO balance maintained at 34/40/16 = 37.8/44.4/16.7% (within ±3% of 40/43/17 targets).
- Pattern is reusable: if rerun review proposes additive tariff changes, prioritise those with paired downgrades NotebookLM also flagged (over-tariffed parts, out-of-spec content that should be cut). Document the deferred recommendations explicitly so peer review can swap-and-balance later.

### Spec-vocabulary leak in model answer (not stem)

- Q13(c) model answer used "acoustic impedance" — not in the Edexcel 9PH0 spec markdown.
- The Spec-Vocabulary Grep gate (added 2026-05-05) is currently scoped to QUESTION STEMS. The leak slipped through to publish-readiness only because spec-examiner also audits model-answer text in its own Smart Mark checks.
- **Skill-improvement candidate**: extend `/spec-check` Step 4 grep to cover MS&G + ET&T + model-answer text, not just stems.

### Cobalt format gap between Phase 3 drafts and Phase 5 published format

- `/mock-3-draft` emits a Paper-2-specific draft format that differs from the Cobalt-canonical published format (`# Question N — Topic` H1 missing, no `---` between parts, `$m{[N marks]}{align=right}` instead of `{align=right}[N]`, table-format MS&G instead of paragraph-style, missing inline `$m{[N mark]}` markers in working).
- Paper 2 publish required substantial reformatting of all 10 structured questions (Q11–Q20) at Phase 5. Paper 1 SFMAs (already in canonical form from earlier work) needed no rework.
- **Skill-improvement candidate**: update `/mock-3-draft` to emit Cobalt-canonical format from the start. Add a structural template referencing Paper 1 Q19 (RC emergency lighting) as the canonical example. Saves ~30–60 minutes per publish run.

### Two-pass NotebookLM macro queries are reliable

- The combined query covering Q13/Q15/Q16/Q19 + Section B cohesion in one request (after starting a fresh conversation) worked cleanly. The earlier rejection in the session was caused by an expired conversation_id from yesterday, NOT query length.
- Per-question queries are safer for first-pass reviews (one Critical per response is easier to act on); combined queries are fine for verification re-reviews where you've already triaged.

### `updateQuestion` enables in-section patches

- Reconfirmed today: `mcp__sme-content__updateQuestion` works for questions in `pending_review`. Paper 1's Q3 friction patch (2026-05-05) used it; Paper 2 has the same patch path available.
- The hard "no update/delete" rule applies only AFTER a question moves out of `pending_review` (i.e. published).
- **Skill-improvement candidate**: update `/mock-5-publish` skill text to reflect this. Currently says "Cobalt has no update/delete after creation" in three places — accurate as a long-term truth but misleading at the publish step where `updateQuestion` is still available.

### Per-question STOP vs batched fire-all

- Paper 1 used per-question STOP (19 separate approvals) and Katie noted it was high-friction. Paper 2 used "single go-ahead, fire all 20 in parallel" after a consolidated preview table. Worked smoothly.
- Recommendation: change the `/mock-5-publish` default from per-question STOP to consolidated-preview + single-fire. Retain per-question STOP as an opt-in flag for content sensitive to manual approval.

## What's now broken and not yet fixed

- **`/mock-3-draft` Cobalt format gap** — drafted SFMAs require reformatting at publish time (see above).
- **`/spec-check` Step 4 grep is stem-only** — model-answer leaks slip through (see above).
- **`/mock-5-publish` skill text outdated on update/delete** — misrepresents the `updateQuestion` capability (see above).
- **`/mock-5-publish` per-question STOP default high-friction** for 20-question batches.
- **4 sub-agent AGENT.md files lack Write/Edit** — `spec-examiner`, `student-simulator`, `marking-realism-checker`, `quality-reviewer` still return text and require the orchestrator to persist. Same root cause as the `exam-researcher` patch (2026-05-05); affected `/mock-4-review` runs today and yesterday.
- **`/mock-4-review` doesn't auto-elevate triple-sub-agent consensus findings** — Q19(c) banding overlap was flagged by all three reviewers but at different severities; the orchestrator merged without weighting by reviewer agreement.
- **`/spec-check` skill prompt misses formula-sheet audit** — caught Q17 out-of-spec capacitance equation only because spec-examiner ran Appendix 8 cross-reference separately.
- **SME MCP `command_word` enum missing "criticise"** — Edexcel approved CW. Q19(e) workaround was to omit the field; classification gap downstream.

## What's working well, no change needed

- **Direct analysis > NotebookLM alone** — the dual approach in Phase 1 catalogues continued to deliver. Catalogues from Paper 1 + Paper 2 are now significant enough to inform Paper 3 (synoptic) outline planning.
- **Phase 0 capture of `.project/exclusion-list.md`** — Paper 2 inherited the "coefficient of friction (μ)" guard from Paper 1's 2026-05-05 fix; no μ-based content slipped into drafts.
- **Spec-grep hard gate at /spec-check Step 4** — caught 0 violations on Paper 2 stems. Confirms the gate is calibrated correctly (no false positives, but model-answer scope gap noted).
- **Cross-qualification reuse map at Phase 5** — useful for downstream conversion work. Paper 2 reuse map shows 19/20 reusable for Edexcel IAL, 16+/20 for AQA/OCR/CIE A Level.

## Counts & metrics

| Metric | Paper 1 (2026-04) | Paper 2 (2026-05) |
|---|---|---|
| Total marks | 90 | 90 |
| Questions | 19 | 20 |
| MCQs | 10 | 10 |
| Structured | 9 | 10 |
| AO balance (final) | 40/43/17 | 37.8/44.4/16.7 |
| Critical issues raised at review | 12 | 4 (rerun #1) + 3 (rerun #2) |
| Critical fixes applied | 11 + Q3 post-publish | 4 + 3 (all Path A) |
| Final CQI | 48/50 | 48/50 |
| Re-review passes needed | 0 (single review) | 2 (rerun #1 + rerun #2) |
| Cobalt upload outcome | 19/19 ✓ | 20/20 ✓ |
| Post-publish patches | 1 (Q3 friction → updateQuestion) | TBD (Katie's UI review pending) |

## Action items for pipeline maintenance

Priority order for next pipeline-improvement session:

1. **Patch four sub-agent AGENT.md files** (`spec-examiner`, `student-simulator`, `marking-realism-checker`, `quality-reviewer`) to add `Write` + `Edit` tools. Mirrors the 2026-05-05 `exam-researcher` patch. Saves orchestrator time + context window on every Phase 4 run.

2. **Update `/mock-3-draft` to emit Cobalt-canonical format from the start.** Reference Paper 1 Q19 as the canonical structural template. Eliminates ~30–60 minutes of reformatting per publish run.

3. **Extend `/spec-check` Step 4 spec-vocabulary grep to cover model answers + MS&G + ET&T**, not just stems. Catches model-answer leaks like Q13(c) "acoustic impedance".

4. **Replace `/mock-5-publish` "no update/delete after creation" wording** in three places with accurate "no update/delete after a question is **published**; questions in `pending_review` can still be patched via `updateQuestion`".

5. **Change `/mock-5-publish` default from per-question STOP to consolidated-preview + single-fire.** Retain per-question STOP as an opt-in flag.

6. **Add aggregation rule in `/mock-4-review`**: if ≥ 3 sub-agents flag the same issue (any severity), auto-elevate to Critical in `SUMMARY.md`. Prevents triple-consensus findings being diluted by orchestrator merging.

7. **Add formula-sheet audit step to `/spec-check`** — enumerate every formula in every SFMA part and cross-reference against the relevant board's data/formulae sheet. Catches out-of-spec equations like Q17 capacitance leak.

8. **Raise SME MCP enum gap with eng team** — `command_word` enum missing "criticise" (Edexcel) and likely other board-specific command words.
