---
name: review-questions
description: Review drafted mock exam questions by submitting them one at a time to NotebookLM for typicality and improvement feedback, then collate feedback and summarise key fixes. Use after /draft-questions has generated SFMAs.
allowed-tools: Read, Glob, Grep, Write, Edit, Bash, mcp__notebooklm__ask_question, mcp__notebooklm__select_notebook, mcp__notebooklm__list_notebooks, mcp__notebooklm__list_sessions, mcp__notebooklm__get_health, mcp__notebooklm__setup_auth, mcp__playwright__browser_navigate, mcp__playwright__browser_snapshot, mcp__playwright__browser_click, mcp__playwright__browser_fill_form, mcp__playwright__browser_type, mcp__playwright__browser_press_key, mcp__playwright__browser_wait_for, mcp__playwright__browser_take_screenshot
user_invocable: true
arguments: "paper-directory"
---

# Review Questions via NotebookLM

> **Purpose**: Submit drafted mock exam questions to NotebookLM for expert review of typicality and improvement suggestions, then collate the feedback and summarise the key fixes required.

---

## When to Use

After `/draft-questions` has generated SFMA files in a `Section A/` (and optionally `Section B/`) directory. This skill:

1. Reads each SFMA file and extracts the **Problem sections only** (not solutions)
2. Formats each question for NotebookLM review
3. Submits questions **one at a time** to NotebookLM
4. Submits a whole-paper review prompt after all individual questions
5. Collates all feedback into a single review file
6. Summarises the key fixes and suggests changes

---

## Inputs Required

Before starting, confirm these with the user:

| Input | How to obtain |
|---|---|
| **Paper directory** | The directory containing the SFMA files (e.g. `02 - Projects/{{BOARD}} {{QUALIFICATION}} {{SUBJECT}}/{{PAPER}}/`). May be provided as an argument |
| **Paper name** | The short paper identifier used in prompts (e.g. "Paper 2F", "Paper 1", "Paper 3A"). Infer from the directory name or outline file |
| **NotebookLM notebook URL** | The URL of the NotebookLM notebook loaded with past papers for this exam board. Ask the user if not known. Check MEMORY.md for saved notebook URLs |
| **SFMA subdirectory** | Usually `Section A\` — confirm if `Section B\` also exists and needs reviewing |

---

## Step 1: Locate and Read SFMA Files

1. Glob for `Section A/*.md` (and `Section B/*.md` if applicable) in the paper directory
2. Sort files by question number (Q01, Q02, ... Q10 etc.)
3. Read each SFMA file in full
4. Count the total number of questions — this is needed for the whole-paper review prompt

---

## Step 2: Extract Problem Sections

For each SFMA file, extract **only the Problem content** — never include Solution, MS&G, or ET&T content. The extraction rules are:

### Structured questions (multi-part)

For each `# Part [letter]` section, extract everything under `## Problem` up to (but not including) `## Solution`. Format as:

```
(a) [Problem text for Part a]

---

(b) [Problem text for Part b]

---
```

### Important formatting rules

- **Preserve all markdown formatting** exactly: bold, italic, LaTeX equations (`$$...$$`), alignment tags (`{align=center}`), superscripts (`^...^`), subscripts (`~...~`)
- **Preserve image placeholders** in full: `[IMAGE: description]`
- **Preserve figure labels**: `{align=center} **Figure N**`
- **Preserve mark allocations**: `{align=right}[N]` for sub-parts
- **Include the total marks** for each part. If a part has no sub-parts, add `[N]` at the end based on the mark count from the Solution section (count `$m{` occurrences)
- **Preserve sub-part numbering**: (i), (ii), etc. exactly as written
- **Preserve MCQ options**: A, B, C, D on separate lines
- **Separate parts with `---`** (horizontal rule) on its own line between parts
- **Include any stem/context text** that appears before Part a (e.g. "This question is about magnets and magnetic fields.") — place it before part (a)

### MCQ-only questions

If the entire question is a single MCQ (1 mark, 4 options), format as a single block with no `---` separators.

---

## Step 3: Format the Review Prompts

### Per-question prompt

For each question, format exactly as:

```
## Question N
How typical is the following question N for Paper [NAME], and what can be done to improve it:

[extracted problem content with parts separated by ---]
```

Where:
- `N` = the question number (1, 2, 3, ...)
- `[NAME]` = the paper name (e.g. "2F", "1", "3A")

### Whole-paper prompt

After all individual questions have been submitted and responses received:

```
## Overall feedback
Please could you review the suitability of the [TOTAL] questions as a whole mock paper - do they reflect a true Paper [NAME] in terms of topic coverage, skills tested, question types etc. Is anything missing or overrepresented?
```

Where:
- `[TOTAL]` = the total number of questions
- `[NAME]` = the paper name

---

## Step 4: Submit to NotebookLM

### Primary method: NotebookLM MCP

If the `mcp__notebooklm__*` tools are available:

1. Check health: `mcp__notebooklm__get_health`
2. If no active session, run `mcp__notebooklm__setup_auth` and follow prompts
3. List notebooks: `mcp__notebooklm__list_notebooks`
4. Select the correct notebook: `mcp__notebooklm__select_notebook` with the notebook URL/ID
5. Submit each question prompt via `mcp__notebooklm__ask_question` — **one at a time, sequentially**
6. Wait for each response before submitting the next question
7. After all individual questions, submit the whole-paper review prompt

### Fallback method: Playwright MCP

If NotebookLM MCP tools are not available or fail:

1. Ask the user for the NotebookLM notebook URL
2. Navigate to the URL using `mcp__playwright__browser_navigate`
3. Wait for the page to load and take a snapshot
4. For each question:
   - Find the chat input field and click it
   - Type/fill the formatted question prompt
   - Press Enter to submit
   - Wait for the response to appear (look for response completion indicators)
   - Take a snapshot to capture the response
5. After all individual questions, submit the whole-paper review prompt

### Critical submission rules

- **One question at a time**: Never batch multiple questions into a single prompt
- **Sequential order**: Submit Q1, wait for response, then Q2, etc.
- **Capture each response**: Record the full text of each NotebookLM response before moving to the next question
- **Do not modify the question text**: Submit the exact extracted problem content — do not paraphrase, summarise, or add commentary

---

## Step 5: Collate Feedback

Save all feedback to a single file in the paper directory:

**Filename**: `[Paper Name] - NotebookLM Review.md`
(e.g. `Paper 2F - NotebookLM Review.md`)

**Format**:

```markdown
## Question 1

[Full NotebookLM response for Question 1]

## Question 2

[Full NotebookLM response for Question 2]

...

## Whole Paper Review

[Full NotebookLM response for the whole-paper review prompt]
```

### Rules

- Reproduce NotebookLM's responses **verbatim** — do not edit, summarise, or reformat them
- Use `## Question N` headings to separate each response
- Use `## Whole Paper Review` for the final review response
- If a file with this name already exists, ask the user whether to overwrite or create a new version (e.g. `Paper 2F - NotebookLM Review (2).md`)

---

## Step 6: Summarise Key Fixes

After collating the feedback, produce a summary of actionable changes. Present this directly to the user (not saved to a file unless requested).

### Summary format

```
# NotebookLM Review Summary — Paper [NAME]

## Critical fixes (must change)
- [Question N, Part X]: [specific fix required]
- ...

## Recommended improvements (should change)
- [Question N, Part X]: [specific improvement]
- ...

## Minor suggestions (could change)
- [Question N, Part X]: [minor suggestion]
- ...

## Whole-paper adjustments
- [Any structural, coverage, or balance changes recommended]
```

### Classification rules

- **Critical**: Factual errors, specification violations, question types that never appear on this paper, incorrect mark allocations, missing required elements (e.g. missing data/source material referenced in the question)
- **Recommended**: Structural improvements, mark scheme refinements, better alignment with past paper patterns, combining/splitting parts
- **Minor**: Phrasing tweaks, alternative contexts, additional marking points

### After presenting the summary

Ask the user:
> "Would you like me to implement any of these changes? I can work through them systematically, starting with the critical fixes."

---

## Error Handling

| Scenario | Action |
|---|---|
| NotebookLM MCP not available AND Playwright fails | Save the formatted prompts to `[Paper Name] - NotebookLM Questions.md` so the user can submit them manually. Inform the user |
| NotebookLM returns an error or empty response | Retry once. If it fails again, note the failure in the review file and move to the next question |
| SFMA file has no `## Problem` section | Skip the file and warn the user |
| Mixed MCQ and structured questions | Handle each question according to its type (see Step 2) |
| User provides notebook URL mid-workflow | Use it immediately — do not restart from the beginning |

---

## Complete Example

> **Note**: The example below uses a Physics paper for illustration, but the workflow applies identically to any subject — just substitute the relevant question content and paper name.

For a Paper 2F with 10 questions, the workflow produces:

1. **10 individual prompts** submitted sequentially to NotebookLM
2. **1 whole-paper prompt** submitted after all individual responses received
3. **1 review file**: `Paper 2F - NotebookLM Review.md` containing all 11 responses
4. **1 summary** presented to the user with fixes categorised by priority

### Example per-question prompt (Q1):

```
## Question 1
How typical is the following question 1 for Paper 2F, and what can be done to improve it:

(a) This question is about magnets and magnetic fields.

A student has four different objects made from different materials.

Which of these materials is magnetic? [1]

A copper
B iron
C plastic
D wood

---

(b) Describe one **similarity** and one **difference** between a permanent magnet and an induced magnet. [2]

---

(c) Figure 1 shows a bar magnet.

[IMAGE: A horizontal bar magnet with the north pole labelled N on the left and the south pole labelled S on the right. No field lines are drawn. Black, grey and white only]

{align=center} **Figure 1**

(i) Complete the magnetic field line diagram around the bar magnet in Figure 1. Draw at least three field lines.

{align=right}[1]

(ii) Add arrows to your field lines to show the direction of the magnetic field.

{align=right}[1]

---

(d) Figure 2 shows two bar magnets placed near each other on a table. A compass is placed at point X between the magnets.

[IMAGE: Two horizontal bar magnets on a table. The left magnet has N on the right side (facing point X). The right magnet has N on the left side (also facing point X). Point X is marked midway between the two north poles. A small compass is shown at point X with no needle direction indicated. Black, grey and white only]

{align=center} **Figure 2**

Predict the direction the compass needle at point X will point. Explain your answer. [2]
```

### Example whole-paper prompt:

```
## Overall feedback
Please could you review the suitability of the 10 questions as a whole mock paper - do they reflect a true Paper 2F in terms of topic coverage, skills tested, question types etc. Is anything missing or overrepresented?
```
