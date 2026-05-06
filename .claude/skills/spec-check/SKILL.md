---
name: spec-check
description: Verify content is exam-board specific and aligned to the syllabus specification
user_invocable: true
arguments: "<content_or_path> <exam_board> <qualification> [topic_or_spec_point]"
---

# Specification Compliance Checker

You are verifying that Save My Exams content is correctly aligned to a specific exam board's syllabus specification.

## Input

The user provides:
- **Content** (required): Pasted content or a file path
- **Exam board** (required): AQA, OCR, Edexcel, CIE, IB, AP, WJEC, Oxford AQA, or SQA
- **Qualification** (required): e.g. "A Level", "GCSE", "IGCSE", "IB HL"
- **Topic or spec point** (optional): e.g. "Forces", "4.2.1", "Topic 2"

If content is a file path, read it first.

## Process

### Step 1: Locate the Specification

Check for local specification PDFs in `references/[exam_board]/`. If not available:
- Use NotebookLM MCP tools to query uploaded specifications
- Use web search to find the current specification document
- Use Notion MCP to check course-specific style sheets at https://www.notion.so/c5fbedbe95884cac9bb0760c42234569

### Step 2: Identify Specification Points

Map the content to specific specification points. For each piece of content, determine:
- Which spec point(s) it covers
- Whether the depth of coverage is appropriate
- Whether the content stays within the spec boundaries

### Step 3: Check Terminology

Verify that the content uses the exact terminology from the specification:
- Key terms and definitions must match the exam board's wording
- Command words must be from the exam board's approved list
- Variable symbols and unit conventions must match the formula sheet
- Proper names for laws, principles, and phenomena must match

### Step 4: Spec-Vocabulary Grep (HARD GATE)

Mechanical check that catches off-spec content even when topic-level scope looks fine. This sits before scope-checking because if a named quantity or formula in the question does not appear anywhere in the spec, the question fails outright — there is no need to debate scope.

**Why this gate exists:** Topic-level scope ("is mechanics in scope?") is too coarse. A Mechanics question can still leak in AQA/CIE-only concepts like the coefficient of friction. The 2026-05-05 Edexcel 9PH0 Paper 1 Q3 incident (μ-based friction MCQ on the published paper, redesigned post-publish to KE ratio-scaling) was caused by exactly this gap — every upstream gate passed because friction *as a topic* was plausibly in scope, but the term "coefficient of friction" never appears in the Edexcel spec.

**Procedure:**

1. Locate the spec markdown for the project. For mock-paper projects, read `project.json.project.dir` and resolve `03 - Resources/Spec Vault/[Board]/[Level]/[board-level-subject]-spec.md`. For ad-hoc spec-check calls, ask the user.

2. From the content under review, extract **distinctive physics tokens** — terms that, if present, would be expected to appear in the spec verbatim or as a close paraphrase:
   - **Named quantities and physical concepts:** "coefficient of (kinetic/static) friction", "moment of inertia", "Young modulus", "limit of proportionality", "elastic limit", "specific latent heat", "specific heat capacity", "rest mass energy"
   - **Named laws and principles:** "Hooke's law", "Lenz's law", "Wien's displacement law", "Stefan-Boltzmann law"
   - **Greek-letter symbols paired with non-generic physical meaning:** μ (friction), η (efficiency), σ (Stefan-Boltzmann), κ (thermal conductivity)
   - **Distinctive formulas verbatim:** "F = μN", "τ = RC", "λ_max T = constant"

3. Skip generic high-frequency words ("energy", "force", "mass", "speed", "velocity") — they hit every page and tell you nothing.

4. For each distinctive token, run `Grep` against the spec markdown (case-insensitive). Record hits.

5. **Hard-fail criterion:** if ANY distinctive token returns zero hits in the spec, the question FAILS this gate. Off-spec content cannot be moderated against a spec that does not contain it. The question must be redesigned — surrogate spec-point tagging at upload time is not an acceptable workaround.

6. **Allowed exceptions** (verify before exempting):
   - The token appears only in the formula booklet, not the spec body. The booklet is part of the spec for marking purposes — check `references/[board]/formula-booklet.md` if available, or `03 - Resources/Spec Vault/[Board]/[Level]/[board]-formula-booklet.md`.
   - The token is a synonym the board treats as equivalent (e.g. "p.d." vs "potential difference"). Confirm with the board's glossary or specification appendix; do not assume.

**Output:** a token-by-token table inside the report:

| Token | Hits in spec | Sample line | Verdict |
|---|---|---|---|
| coefficient of kinetic friction | 0 | — | **FAIL — off-spec** |
| Hooke's law | 3 | §29 (Topic 4) | Pass |

### Step 5: Check Scope

Identify:
- **Gaps**: Specification content that should be covered but is missing
- **Extraneous content**: Content included that goes beyond the specification (other exam board's requirements, higher-level content, outdated spec points)
- **Depth mismatches**: Content that is too shallow or too deep for the qualification level

### Step 6: Check Board-Specific Requirements

Different exam boards have specific requirements. Check for:
- **AQA**: Required practicals, mathematical skills requirements
- **OCR**: Practical endorsement skills, mathematical requirements
- **Edexcel**: Core practicals, mathematical skills
- **CIE**: Practical skills, alternative-to-practical paper requirements
- **IB**: Nature of science links, TOK connections, internal assessment links
- **AP**: Science practices, learning objectives, essential knowledge statements
- **WJEC**: Specified practical work, mathematical requirements
- **SQA**: Mandatory course key areas, skills and knowledge requirements

## Output Format

### Specification Compliance Report

**Content**: [title or first line]
**Exam Board**: [board]
**Qualification**: [qualification]
**Specification**: [spec document reference and version]
**Spec Points Covered**: [list of spec point codes]

---

### Aligned Content

| Content Element | Spec Point | Status |
|----------------|------------|--------|
| [topic/concept] | [spec code] | Aligned |

### Gaps (Missing Content)

| Spec Point | Required Content | Severity |
|------------|-----------------|----------|
| [spec code] | [what should be included] | Critical/Minor |

### Extraneous Content

| Content Element | Issue |
|----------------|-------|
| [topic/concept] | [why it's outside spec — e.g. "This is A Level content, not required at GCSE"] |

### Terminology Mismatches

| Content Uses | Specification Uses | Location |
|-------------|-------------------|----------|
| [wrong term] | [correct term] | [where in content] |

---

### Summary

- **Overall alignment**: Strong / Adequate / Weak
- **Spec-vocabulary grep**: PASS / **FAIL** (count of distinctive tokens with zero hits in spec)
- **Critical gaps**: [count] specification points not covered
- **Extraneous items**: [count] items beyond specification scope
- **Terminology issues**: [count] terms that don't match the specification
- **Recommendation**: Ready for publication / Needs revision / Needs significant rework

**Hard-fail rule:** If the spec-vocabulary grep returns FAIL for any token, the overall recommendation is at minimum "Needs revision" regardless of other findings. A FAIL on this gate means the question contains a named concept that does not exist in the specification — moderation against a spec that does not contain the concept is not possible.
