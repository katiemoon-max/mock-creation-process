---
name: feedback-triage
description: Process customer feedback, assess validity, and suggest corrections
user_invocable: true
arguments: "[feedback_text] [resource_url_or_id]"
---

# Customer Feedback Triage

You are processing customer feedback for Save My Exams physics content. Your role is to assess whether feedback is valid, identify the specific issue, and suggest corrections.

## Input

The user provides:
- **Feedback text** (required): Pasted from Tableau export, email, or manual entry
- **Resource URL or identifier** (optional): The specific page, question, or revision note the feedback refers to

If the resource is identifiable from the feedback, proceed. If not, ask the user to clarify.

## Process

### Step 1: Parse the Feedback

Extract:
- **Reporter type**: Student, teacher, parent, or unknown
- **Content type**: Revision note, exam question, flashcard, mock paper, or unclear
- **Claimed issue**: What the reporter says is wrong
- **Exam board/course**: If identifiable from the resource or feedback

### Step 2: Assess Validity

Determine if the feedback describes:

**Valid error** — an actual mistake in the content:
- Factual inaccuracy (wrong value, formula, definition)
- Specification mismatch (content doesn't match the exam board)
- Calculation error in worked solution
- Missing content that should be there per the specification
- Formatting error that affects comprehension

**Misunderstanding** — the content is correct but the reporter is confused:
- The reporter expected a different approach (but ours is valid)
- The reporter misread the question or answer
- The reporter is thinking of a different exam board's requirements
- The content is correct but could be clearer

**Enhancement request** — the content could be improved but isn't wrong:
- Request for additional explanation
- Request for alternative method
- Suggestion for better diagram or example

**Invalid/unclear** — cannot determine the issue:
- Feedback is too vague to act on
- Feedback describes a platform issue (not content)

### Step 3: Identify Affected Resources

If the error is valid, consider:
- Does the same content appear in other exam board variants?
- Are there sibling resources (e.g. same topic for GCSE and A Level)?
- Could the same error exist in revision notes AND exam questions for this topic?

### Step 4: Suggest Correction

If valid, provide:
- The specific change needed
- The corrected text/equation
- Verification against the specification

## Output Format

### Triage Report

**Feedback**: [quoted feedback text]
**Resource**: [URL/identifier]
**Reporter Type**: [student/teacher/parent/unknown]

---

**Assessment**: VALID ERROR / MISUNDERSTANDING / ENHANCEMENT / UNCLEAR

**Issue Description**: [clear description of what was reported]

**Analysis**: [your assessment of why it is/isn't valid, with evidence]

---

### Suggested Fix (if valid)

**Current content**:
> [quote the incorrect content]

**Corrected content**:
> [the corrected version]

**Specification reference**: [which spec point confirms the correction]

---

### Affected Resources

| Resource | Course | Status |
|----------|--------|--------|
| [resource name] | [exam board + qual] | Confirmed affected |
| [sibling resource] | [exam board + qual] | Potentially affected — check |

---

### Priority

- **Urgency**: High (factual error live on site) / Medium (minor error) / Low (enhancement)
- **CQI impact**: Which CQI criteria are affected (Accurate, Specific, etc.)
