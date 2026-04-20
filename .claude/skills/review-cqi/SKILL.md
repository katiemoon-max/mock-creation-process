---
name: review-cqi
description: Review content against all 10 CQI criteria and produce a quality scorecard
user_invocable: true
arguments: "[content_or_path] [exam_board] [qualification]"
---

# CQI Quality Reviewer

You are reviewing Save My Exams content against the Content Quality Index (CQI) — a 10-criteria quality framework.

## Input

The user provides:
- **Content** (required): Pasted content, or a file path to the content to review
- **Exam board** (optional but recommended): For checking exam-board specificity
- **Qualification** (optional but recommended): For checking pitch and scope

If content is a file path, read it first. If exam board/qualification are not provided, attempt to infer them from the content. If ambiguous, ask.

## Process

Review the content against all 10 CQI criteria. For each criterion, score 1-5 and provide specific evidence.

### Critical Tier (must score 5/5)

**1. Specific**
- Are terms, command words, and definitions correct for the exact exam board?
- Is any content included that is outside the specification scope?
- Is any required specification content missing?
- Does the content use the correct specification codes and paper references?

**2. Accurate**
- Are all equations, formulas, and constants correct?
- Are all facts, figures, and data accurate?
- Are worked solutions correct (check the maths step by step)?
- Are units correct at every step?

**3. Concise**
- Are bullet points effective and minimal?
- Is there any repeated information?
- Are sentences clear and not overly wordy?
- Is there unnecessary context or preamble?

### Standard Tier (must score 4/5 minimum)

**4. Correct**
- Is spelling and grammar correct throughout?
- Is the correct language variant used (UK English, or US for AP)?
- Are proper nouns correctly capitalised?

**5. Consistent**
- Are course-specific elements (terminology, notation, symbols) used consistently?
- Is formatting consistent throughout?
- Are similar concepts explained in similar ways?

**6. Sensitive**
- Apply the PARSNIPS sensitivity filter (defined in `sme-overview.md`)
- Is the content appropriate for a global audience?
- Are examples culturally neutral?

**7. Structured**
- Is the heading hierarchy correct (H1 > H2 > H3 > H4, no skips)?
- Are cross-references and hyperlinks present where needed?
- Is alt text provided for images?
- Is the logical flow sensible?

**8. Formatted**
- Is the layout uncluttered and well-spaced?
- Are bullet points used to highlight key information?
- Are equations in $$...$$ format?
- Does formatting meet house style rules (bold, italics, numbers, ampersands)?

**9. Appropriate Tone**
- Is the tone ACE? (see `sme-overview.md` for definition)
- Is it professional but not intimidating?
- Is it friendly but not jokey or casual?
- Are there any emoji, exclamation marks, or informal language?

**10. Appropriate Pitch**
- Is the content at the right level for the target qualification?
- Is the reading level appropriate (Hemingway level 10-12)?
- Is CEFR level appropriate (C1/C2, or B2 for EAL students)?
- Is unnecessary jargon avoided or explained?

## Output Format

### CQI Scorecard

| # | Criterion | Tier | Score | Status |
|---|-----------|------|-------|--------|
| 1 | Specific | Critical | X/5 | PASS/FAIL |
| 2 | Accurate | Critical | X/5 | PASS/FAIL |
| 3 | Concise | Critical | X/5 | PASS/FAIL |
| 4 | Correct | Standard | X/5 | PASS/FAIL |
| 5 | Consistent | Standard | X/5 | PASS/FAIL |
| 6 | Sensitive | Standard | X/5 | PASS/FAIL |
| 7 | Structured | Standard | X/5 | PASS/FAIL |
| 8 | Formatted | Standard | X/5 | PASS/FAIL |
| 9 | Appropriate Tone | Standard | X/5 | PASS/FAIL |
| 10 | Appropriate Pitch | Standard | X/5 | PASS/FAIL |

**Total: XX/50** (minimum 43 required)

### Issues Found

For each issue, provide:
- **Criterion**: Which CQI criterion it falls under
- **Severity**: Critical / Major / Minor
- **Location**: Where in the content (quote or reference the section)
- **Issue**: What is wrong
- **Suggested Fix**: How to correct it

### Summary

- Overall assessment: PASS (43+/50 with all Critical at 5 and Standard at 4+) or FAIL
- Number of issues by severity
- Priority actions (fix Critical issues first, then Major, then Minor)

## Additional Checks

If Notion MCP is available, fetch the latest CQI definitions from https://www.notion.so/6bbed885ff644045846080e43fee1a23 and the course-specific style sheet from https://www.notion.so/c5fbedbe95884cac9bb0760c42234569 to ensure the review uses the most current criteria.
