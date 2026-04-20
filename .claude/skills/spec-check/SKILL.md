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

### Step 4: Check Scope

Identify:
- **Gaps**: Specification content that should be covered but is missing
- **Extraneous content**: Content included that goes beyond the specification (other exam board's requirements, higher-level content, outdated spec points)
- **Depth mismatches**: Content that is too shallow or too deep for the qualification level

### Step 5: Check Board-Specific Requirements

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
- **Critical gaps**: [count] specification points not covered
- **Extraneous items**: [count] items beyond specification scope
- **Terminology issues**: [count] terms that don't match the specification
- **Recommendation**: Ready for publication / Needs revision / Needs significant rework
