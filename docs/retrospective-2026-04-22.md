# Retrospective — 2026-04-22 (Phase 5 end-to-end)

Second end-to-end run of the pipeline, specifically Phase 5 (`/mock-5-publish`), completing what the 2026-04-21 retrospective set up. Uploaded all 19 SFMAs to Cobalt via the SME MCP, attached spec-point IDs to every part using the Master Syllabus CSV, generated the cross-qualification reuse map, and handed off. Notes below are the pipeline-level improvements this run surfaced — the fixes have already been rolled into the skills in this same commit.

## What the pipeline got right

- **Hard publish gate held.** CQI ≥ 43/50 + zero Critical residuals gated the upload, as designed.
- **`/cobalt-formatting` served as the canonical reference.** All 19 questions rendered cleanly on first upload bar one styling issue (see fix #3 below).
- **SME MCP configured and used mid-session.** createQuestion worked on first call once user ID + section IDs were supplied; updateQuestion patched spec-point IDs on all 19 questions in one parallel round.
- **Reuse map auto-generated** from tracker CSV's "Suitable for …" column — a 19 × 5 sister-qualification matrix came out of a single pass.

## Fixes rolled into the skills this run

### 1. Per-question STOP → batched preview + single consent

**Problem:** The skill mandated a STOP before every `createQuestion` call. For a 19-question paper that's 19 explicit approvals, which is high-friction and redundant once the first rendered CMS preview validates the pattern.

**Fix (in `/mock-5-publish`):** consolidated preview table of all questions + single go-ahead, then parallel fire. Per-question STOP remains opt-in for sensitive runs.

### 2. "Cobalt has no update/delete" was outdated

**Problem:** The skill repeated this caveat in three places, creating unnecessary caution. The SME MCP supports `updateQuestion` on `pending_review` status (verified this session).

**Fix (in `/mock-5-publish`):** replaced with the correct framing — *published* questions cannot be edited, but `pending_review` questions can still be patched. Treat upload as a checkpoint, not an irrevocable commit.

### 3. MCQ distractor explanations — paragraphs, not bullets

**Problem:** `/cobalt-formatting` section 6 showed distractor explanations as bullets. The first MCQ upload rendered with correct physics but wrong styling — house convention in Cobalt is paragraphs separated by blank lines.

**Fix (in `/cobalt-formatting` + `/mock-3-draft` Rules):** rewrote section 6 with paragraph distractors; added to drafting rules so the convention is applied at source.

### 4. MCQ ET&T is optional, not mandatory

**Problem:** Section 5.4 of `/cobalt-formatting` required ET&T "on every part". In practice, MCQ distractor explanations often already cover the teaching points — forcing an ET&T creates redundancy.

**Fix (in `/cobalt-formatting` + `/mock-3-draft` Rules):** qualified "every part" to structured parts. MCQ ET&T is optional — include only when it adds genuine new insight beyond distractor commentary.

### 5. Letter-only MCQ choices need empty `content`

**Problem:** For MCQs where options reference a diagram label or table row (the "choice" is just A/B/C/D pointing to something in the problem image), passing the literal letters duplicates Cobalt's rendered labels.

**Fix (in `/cobalt-formatting` + `/mock-5-publish` conversion step):** documented that letter-only choices should pass `"content": ""`. Cobalt auto-renders the labels; `is_correct` still drives the correct-option flag from the array position.

### 6. `**Model Answer**` wrappers stripped during conversion (and prevented at source)

**Problem:** SFMAs sometimes wrap solution content in `**Model Answer**` / `**End of Model Answer**`. This isn't a valid Cobalt callout — it renders as plain bold text.

**Fix (in three places — defence in depth):**
- `/mock-3-draft` Rules now prohibit writing the wrapper in SFMAs (prevent at source)
- `/mock-5-publish` conversion step strips the wrapper defensively if present
- `/cobalt-formatting` section 1.5 flags the wrapper is NOT a valid callout

### 7. Structured-question upload pattern documented

**Problem:** The skill didn't specify how to handle multi-part structured questions with a shared stem — repeat the stem across parts, or embed it in Part (a)?

**Fix (in `/mock-5-publish`):** embed the shared stem in **Part (a)'s `problem` field**; subsequent parts contain only their sub-question. Sub-parts like (c)(i)/(c)(ii) stay as a single Cobalt part with inline `{align=right}[N]` mark indicators preserving the split.

### 8. Mark indicators in the Problem section — marks go in Cobalt's field, not the text

**Problem:** The SFMA template had `$m{[N mark(s)]}{align=right}` in every Problem section. But Cobalt sets part marks via the per-part `marks` field during upload; repeating in the problem text creates duplication, and Cobalt strips the in-text indicator inconsistently.

**Fix (in `sfma.template.md`):** removed the in-problem mark indicator. It's retained only as `{align=right}[N]` for sub-part labelling (e.g. `(i) ... [2]` / `(ii) ... [2]`).

### 9. Spec-point attachment step added to Phase 5

**Problem:** `/mock-5-publish` created questions with no `spec_point_ids`, leaving classification work for manual follow-up.

**Fix (in `/mock-5-publish`):** added a post-upload step that calls `getCourseStructure`, matches each part's content against the Master Syllabus CSV, then fires `updateQuestion` in parallel to attach spec-point IDs. The mapping rationale is logged to `upload-log.md` for review.

## Items surfaced but NOT fixed this run (carry-forward)

### 10. `command_word` enum gap (MCP-side)

**Observation:** The `createQuestion` `command_word` enum doesn't include every approved command word for every board (e.g. Edexcel's "Criticise" from Appendix 7 is missing). Dropped the field for that part; problem text still contains the correct word.

**Suggested action:** Raise with the engineering team to add missing enum entries. If the gap persists, document the allowed fallback (omit + preserve in problem text) in `/cobalt-formatting`. Skill already notes this gracefully.

### 11. Image-attachment workflow has no MCP path

**Observation:** SFMAs have `[IMAGE: description]` placeholders with alt-text but no CDN URLs. The MCP has no image-upload tool — images must be attached via the Cobalt UI after upload, or CDN URLs supplied manually for `updateQuestion` patch.

**Suggested action:** Either add image-upload support to the MCP, or formalise a two-step workflow (upload → attach-images-manually → publish). The skill flags the gap but doesn't automate it.

### 12. Retrospective file count is growing

**Observation:** We now have `retrospective-2026-04-21.md` (Phase 3/4 learnings) and `retrospective-2026-04-22.md` (Phase 5 learnings). After a few more papers this will become hard to navigate.

**Suggested action:** After the third retrospective, consolidate into a single `RETROSPECTIVES.md` with dated sections, or migrate recurring lessons into the skills themselves under a `## Known Issues` block.

## Pipeline shape after this run

Phases 0–5 now tested end-to-end. The full round-trip from "new mock paper" to "questions in CMS, spec-tagged, awaiting reviewer" is green. Suggested next high-value work:

- **Run Phase 5 on a non-Physics subject** (Biology, Chemistry, Psychology) to validate the subject-agnostic claims. The agnostic framing has been tightened in this commit but hasn't yet been stress-tested by a live session outside Physics.
- **Close the image-attachment loop** — either engineer-side (add to MCP) or workflow-side (formalise manual step).
- **Fix the `command_word` enum** — low-priority but cleans up moderation signal.
