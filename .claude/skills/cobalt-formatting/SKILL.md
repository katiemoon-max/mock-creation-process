---
name: cobalt-formatting
description: Format exam questions and solutions for the Cobalt CMS. Use when writing SFMAs, MCQ solutions, or any content destined for Cobalt. Covers TipTap markdown syntax, SFMA structure, mark indicators, equation formatting, callout blocks, and course-dependent rules.
allowed-tools: Read
---

# Cobalt CMS Formatting Skill

> **Purpose**: This file teaches Claude how to write Cobalt-ready exam questions and solutions. Drop it into your `.claude/rules/` directory or paste it into your system prompt.

---

## 1. Supported Markdown Syntax

Cobalt uses a TipTap-based markdown parser. Only the syntax below is supported — anything else will be ignored or break.

### 1.1 Block Elements

#### Headings (H1–H4 only)

```
# Heading 1
## Heading 2
### Heading 3
#### Heading 4
```

H5 and below are **not supported**. Never skip heading levels.

#### Paragraphs

Any line that doesn't match another block rule is a paragraph. Empty lines are skipped.

#### Bullet Lists

```
- First item
- Second item
- Third item
```

#### Ordered Lists

```
1. First item
2. Second item
3. Third item
```

The output always starts at 1 regardless of the numbers used in the source.

#### Tables

Standard GitHub-flavoured markdown tables with colon alignment:

```
| Left | Centre | Right |
| --- | :---: | ---: |
| a | b | c |
```

- First row becomes header cells
- Inline formatting (bold, italic, equations) works inside cells

#### Code Blocks

````
```
const x = 1;
```
````

Language specifiers are ignored.

#### Images

```
![Descriptive alt text](https://cdn.savemyexams.com/uploads/...)
```

- Must be the only content on the line
- Auto-centres with empty caption
- Alt text is **required** and must be descriptive
- Diagrams must follow the colour rules in `.claude/rules/formatting.md`

### 1.2 Inline Formatting

| Syntax | Result |
| --- | --- |
| `**bold**` | **bold** |
| `*italic*` | *italic* |
| `***bold italic***` | ***bold italic*** |
| `~~strikethrough~~` | ~~strikethrough~~ |
| `^superscript^` | superscript (e.g. `10^-6^`) |
| `~subscript~` | subscript (e.g. `H~2~O`) |
| `_underline_` | underline (NOT italic — use `*` for italic) |
| `` `inline code` `` | inline code |
| `[text](url)` | hyperlink |

**Critical rule — superscript and subscript in plain text**: When writing quantities outside of LaTeX, always use caret-wrap for superscripts (`10^-6^`) and tilde-wrap for subscripts (`v~rms~`). Never use Unicode superscript/subscript characters (like ⁻⁶ or ₂). Prefer LaTeX (`$$10^{-6}$$`) where possible, but when plain text is needed (e.g. inside table cells or inline references), use the `^…^` and `~…~` syntax.

### 1.3 Text Alignment

Prefix any paragraph or list item with `{align=left|center|right}`:

```
{align=center} This text is centred.
{align=right} This text is right-aligned.
```

Works inside list items too:

```
- {align=center} Centred list item
1. {align=right} Right-aligned list item
```

### 1.4 Equations (LaTeX)

All equations use **double dollar signs** — never single:

```
The area is $$A = \pi r^2$$ for a circle.
```

Display equations on their own line with blank lines above and below. Centre them:

```
{align=center} $$v = u + at$$
```

**LaTeX spacing note**: Use standard LaTeX when drafting — `\text{ N}` and `8.0`. The CMS may render these with artefacts like `\textrm{ }\text{N}` and `8 . 0` in its exports, but you should NOT replicate these artefacts when writing content.

#### Equation Emphasis Tags

Wrap equations in a prefix to apply colour/emphasis:

| Syntax | Meaning | Use for |
| --- | --- | --- |
| `$m{$$x = 5$$}` | Exam mark (blue) | Inline mark indicators |
| `$w{$$x = 5$$}` | Working (grey) | Intermediate working steps |
| `$f{$$x = 5$$}` | Final answer (green) | Final calculated answers |
| `$c{$$x = 5$$}` | Commentary (orange) | Explanatory annotations |

These also work **without LaTeX** for plain text emphasis:

```
$f{The correct answer is B}
$m{[1 mark]}
```

### 1.5 Callout Blocks

Wrapped in bold markers with a matching end marker. Use "and" not "&".

| Markdown Name | Variant | Typical Use |
| --- | --- | --- |
| `Mark Scheme and Guidance` | Mark scheme | Marking points and examiner guidance |
| `Examiner Tips and Tricks` | Exam tip | Actionable exam advice |
| `Worked Example` | Worked example | Question + answer demonstration |
| `Case Study` | Case study | Real-world context |
| `Blockquote` | Blockquote | Quoted material |

**Syntax:**

```
**Mark Scheme and Guidance**
Content here — paragraphs, bullets, tables, ordered lists, code blocks allowed.
**End of Mark Scheme and Guidance**
```

Only these node types survive inside callouts: paragraph, bullet list, ordered list, table, code block. Images and headings inside callouts are stripped.

### 1.6 Spec Points

```
**Spec Point: 1.2.3**
Content inside the spec point section.
**End of Spec Point: 1.2.3**
```

The name must match exactly between start and end markers.

### 1.7 Extracts

```
**Extract**
Paragraph content, images, bullet lists, and ordered lists allowed.
**End of Extract**
```

---

## 2. SFMA File Structure

Each question is one file. The top-level structure uses H1 for parts:

```
# Part a
## Problem
[Question text, figures, context]
## Solution
[Model answer with inline marks]
[MS&G callout]
[ET&T callout]

# Part b
## Problem
...
## Solution
...
```

### Rules

- `# Part [letter]` as H1 for each part (a, b, c, etc.)
- `## Problem` contains the question text
- `## Solution` contains the model answer, MS&G, and ET&T together
- No horizontal rules (`---`) between sections
- Total marks are NOT shown in headings

---

## 3. Mark Indicators

- No checkmarks (✓) anywhere in the content
- **Inline marks**: Place `$m{[1 mark]}` on the **same line** as the equation or statement it awards:

```
{align=center} $$v = \frac{s}{t}$$ $m{[1 mark]}
```

- **Mark allocation in the Problem section**: The total marks for each part are set via Cobalt's "Marks" field, so do **not** show marks in the question text for parts without sub-parts. When a part has sub-parts (i), (ii) etc., show the mark allocation for each sub-part using plain square brackets WITHOUT the `$m{}` tag:

```
{align=right}[2]
```

This distinguishes sub-part mark allocations (which appear in the question paper) from solution mark indicators (which use `$m{}`).

- **Right-aligned marks in the Solution section**: Use `{align=right} $m{[N marks]}` when marks cannot sit inline — e.g. for graphs, diagrams, extended prose answers, or multi-mark blocks where individual marking points are not shown in the model answer:

```
{align=right} $m{[3 marks]}
```

- Inside MS&G callouts, marks sit inline at the end of each bullet:

```
- The resultant force on the object is zero $m{[1 mark]}
```

---

## 4. Figure Labels

```
{align=center} **Figure N**

![Descriptive alt text](https://cdn.savemyexams.com/uploads/...)
```

Figure label on its own line, centred and bold, followed by the image.

---

## 5. Structured Question Solutions

### 5.1 Calculation Solutions

Solution scaffold steps are **bullet points**. Open with a scaffold, then show step-by-step working:

```
## Solution

To calculate the velocity:

- List the known quantities:

- $$s = 120 \text{ m}$$
- $$t = 8.0 \text{ s}$$

- Write down the equation:

{align=center} $$v = \frac{s}{t}$$ $m{[1 mark]}

- Substitute the known values:

{align=center} $$v = \frac{120}{8.0}$$ $m{[1 mark]}

- Calculate the answer:

{align=center} $$v =$$ $f{$$15 \text{ m s}^{-1}$$} $m{[1 mark]}
```

**Rules:**

- Scaffold steps ("List the known quantities:", "Write down the equation:", "Substitute the known values:", "Calculate the answer:") are bullet points (`- `)
- Open with "List the known quantities:" followed by a bulleted list of symbols and values
- Show an explicit rearrangement step before substitution (when applicable)
- Intermediate steps use plain `{align=center}` equations
- **Final answer**: Only the numerical answer and unit are green — the variable and = sign stay black. Write `$$R_{L} =$$ $f{$$210 \text{ N}$$} $m{[1 mark]}` (not `$f{$$R_{L} = 210 \text{ N}$$}`)
- `$m{[1 mark]}` goes on the same `{align=center}` line as the step it marks
- Include units at every step, not just the final answer
- When multiple valid methods exist, label as **Method 1** / **Method 2** with full working
- **Sub-parts with separate calculations**: When a part has sub-parts (i), (ii) etc. that each have their own calculation, place the MS&G callout immediately after the working for each sub-part — not one combined MS&G at the end. This keeps marking guidance next to the relevant working

### 5.2 Short-Answer / Recall Parts

For simple define/state/recall parts (typically 1–2 marks), put the answer inside the MS&G callout directly — no separate model answer above it. Marks go inline at the end of each bullet:

```
## Solution

**Mark Scheme and Guidance**
- The resultant force on the object is zero $m{[1 mark]}
- The resultant moment about any point is zero $m{[1 mark]}

For the first mark, accept: net force = 0, no unbalanced force, or equivalent

For the second mark, accept: net torque = 0, sum of clockwise moments = sum of anticlockwise moments, or equivalent
**End of Mark Scheme and Guidance**
```

Accept/reject criteria go in **separate paragraphs** below the marking point bullets, not embedded within them.

### 5.3 MS&G Style

```
**Mark Scheme and Guidance**
1 mark for correct substitution into $$v = u + at$$ (accept $$v = 0 + 9.81 \times 3.0$$)

1 mark for correct answer of $$v = 29 \text{ m s}^{-1}$$ (accept 29.4)
- ecf from incorrect substitution
- Must have correct unit for this mark

1 mark for correct substitution **OR** correct intermediate answer of $$t = 4.2 \text{ s}$$
**End of Mark Scheme and Guidance**
```

- Use "1 mark for..." paragraph style for each marking point
- Accept/reject criteria as sub-bullets beneath the relevant marking point
- Use ecf notation where appropriate
- Group marks with **OR** where substitution and intermediate answer earn the same mark

### 5.4 ET&T

```
**Examiner Tips and Tricks**
A common mistake is to forget to convert the diameter to a radius before substituting into the area equation. Always halve the diameter first.
**End of Examiner Tips and Tricks**
```

- Include on **every part**, even 1-mark recall parts
- Focus on common misconceptions and actionable advice
- Never repeat the solution — provide new insight
- Use second person voice ("you", "your")

---

## 6. MCQ Solutions

```
## Solution

$f{The correct answer is B}

- A proton has a charge of $$+1.6 \times 10^{-19} \text{ C}$$ and a mass of $$1.67 \times 10^{-27} \text{ kg}$$

{align=center} $$\text{specific charge} = \frac{q}{m} = \frac{1.6 \times 10^{-19}}{1.67 \times 10^{-27}}$$

{align=center} $$= 9.6 \times 10^{7} \text{ C kg}^{-1}$$

**A** is incorrect because it uses the mass of an electron instead of a proton

**C** is incorrect because it inverts the fraction (mass divided by charge)

**D** is incorrect because it uses the elementary charge without converting units
```

**Rules:**

- Correct answer uses `$f{The correct answer is X}` — NOT bold
- Positive-derivation steps use bullet points (`-`) for text, `{align=center}` for equations
- Label each calculation step on its own `{align=center}` line
- **Distractor explanations are paragraphs, NOT bullets.** Write each "**A** is incorrect because…", "**B** is incorrect because…" etc. as a separate paragraph separated by blank lines
- Distractor explanations use `**B**`, `**C**`, `**D**` only — do NOT include the option value in parentheses
- No MS&G callout for MCQs — use free text explanation only
- No marks shown in MCQ solutions
- **ET&T is optional on MCQs.** Include one only when it adds genuine new insight beyond the distractor explanations. If the A/B/D commentary has already covered the teaching points, omit the ET&T
- When the question asks to derive a compound unit in SI base units, prefer the shortest equation chain to reach the target (e.g. use $$E_k = \frac{1}{2}mv^2$$ to get 1 J in base units, not $$W = Fs$$ combined with $$F = ma$$)
- **When options are letter-only references** (e.g. points on a diagram, rows of a table, graphs labelled A–D), pass an empty string as the choice content — Cobalt renders the A/B/C/D labels automatically, so including "A"/"B"/"C"/"D" as content duplicates them

---

## 7. Number & Unit Formatting

| Rule | Correct | Incorrect |
| --- | --- | --- |
| Quantities in LaTeX | $$300 \text{ K}$$ | 300 K |
| Scientific notation | $$1.5 \times 10^5 \text{ Pa}$$ | 1.5 × 10⁵ Pa |
| Units with exponents | $$\text{m s}^{-1}$$ | m/s or ms⁻¹ |
| Ranges with units | $$480\text{–}484 \text{ m s}^{-1}$$ | 480–484 m s⁻¹ |
| Space between number and unit | $$5 \text{ m}$$ | $$5\text{m}$$ |
| Plain text superscript | 10^-6^ | 10⁻⁶ or 10^-6 |
| Plain text subscript | v~rms~ | v_rms or vᵣₘₛ |

- Use en dashes (–) for ranges, not hyphens
- Tabular data may remain as plain text; all other quantities use `$$...$$`

---

## 8. Course & Subject-Dependent Rules

Some formatting choices depend on the exam board, qualification level, and subject. The rules in this skill are **universal Cobalt formatting** unless noted below. Always check the relevant specification and house style for your course.

### 8.1 STEM-Specific (not applicable to non-STEM subjects)

The following sections apply only to Physics, Chemistry, Maths, and other STEM subjects:

- **Calculation scaffold** (section 5.1): "List known quantities" → equation → substitute → calculate. Non-STEM subjects will not use this pattern
- **`$f{$$...$$}` for final calculated answers**: Only relevant when solutions involve numerical calculations
- **`$w{$$...$$}` for working steps**: Only relevant for multi-step mathematical working
- **All LaTeX/equation formatting** (section 1.4): Non-STEM subjects rarely need equations
- **Scientific notation formatting**: STEM only
- **Greek letter conventions**: STEM only
- **Unit formatting rules** (spacing, exponents): STEM only
- **Figure numbering** ("Figure N"): More common in STEM; other subjects may use different labelling conventions
- **Diagram colour restriction** (black/grey/white only): Primarily a STEM diagram rule

### 8.2 Exam Board & Level-Dependent

These rules vary and should be adapted to your specific course:

- **Unit notation**: A Level Physics uses negative exponents ($$\text{m s}^{-1}$$). GCSE and IGCSE Physics typically uses fraction notation ($$\text{m/s}$$). Always match the convention used in the exam board's specification and formula sheet
- **Equation complexity**: A Level solutions show full rearrangement steps; GCSE may not need explicit rearrangement as a separate step
- **Command words**: Vary by exam board. AQA uses "State", "Determine", "Explain"; CIE also uses "Give", "Suggest"; IB has its own set. Always use the exact command words from your board's specification
- **Assessment objective (AO) framework**: AQA has 3 AOs; CIE theory papers test only 2 (no AO3); IB uses different objectives entirely. AO classifications in MS&G must match the board's framework
- **Mark types**: AQA does not label mark types in the mark scheme. CIE uses explicit mark type codes: A (final answer), B (independent), C (compensatory), M (method), with ecf (error carried forward) notation
- **Language**: UK English for all UK and international boards; American English for AP courses only

---

## 9. General Style Rules

> For general house style (punctuation, capitalisation, bullet formatting, numbers, spelling), see `.claude/rules/formatting.md`. For equation conventions (display equations, units, Greek letters), see `.claude/rules/equations.md`. The rules below are Cobalt-specific additions only.

- Use the exam board's own command words and terminology — never generic alternatives
- Callout names use "and" not "&" (e.g. "Mark Scheme and Guidance")

---

## 10. Quick Reference — Parsing Priority

The parser processes each line top-to-bottom. First match wins:

1. Heading (`# ...`)
2. Bullet list (`- ...`)
3. Ordered list (`1. ...`)
4. Spec point start (`**Spec Point: ...**`)
5. Extract start (`**Extract**`)
6. Callout start (`**Callout Name**`)
7. Code block (`` ``` ``)
8. Table (line contains `|`)
9. Image (`![...](...)`)
10. Paragraph (everything else)

Inline marks applied in order: links → bold+italic → bold → italic → strikethrough → superscript → subscript → underline → inline code → emphasis markers (`$m{}`, `$w{}`, `$f{}`, `$c{}`)

---

## 11. Complete Worked Example

Below is a complete 2-part structured question formatted for Cobalt:

```markdown
# Part a

## Problem

State the two conditions required for an object to be in equilibrium.

## Solution

**Mark Scheme and Guidance**
- The resultant force on the object is zero $m{[1 mark]}
- The resultant moment about any point is zero $m{[1 mark]}

For the first mark, accept: net force = 0, no unbalanced force, or equivalent

For the second mark, accept: net torque = 0, sum of clockwise moments = sum of anticlockwise moments, or equivalent
**End of Mark Scheme and Guidance**

**Examiner Tips and Tricks**
Many students only state the force condition and forget about moments. Remember: equilibrium requires BOTH conditions — forces AND moments.
**End of Examiner Tips and Tricks**

# Part b

## Problem

A uniform beam of weight $$120 \text{ N}$$ and length $$4.0 \text{ m}$$ is supported at both ends. A $$200 \text{ N}$$ load is placed $$1.0 \text{ m}$$ from the left support.

Calculate the reaction force at the left support.

## Solution

To calculate the reaction force at the left support:

- List the known quantities:

- Weight of beam, $$W = 120 \text{ N}$$ (acts at centre, $$2.0 \text{ m}$$ from left)
- Load, $$F = 200 \text{ N}$$ (acts $$1.0 \text{ m}$$ from left)
- Length of beam, $$L = 4.0 \text{ m}$$

- Determine the clockwise and anticlockwise moments about the right support:

{align=center} Clockwise moments = $$R_{L} \times 4.0$$ $m{[1 mark]}

{align=center} Anticlockwise moments = $$\left(120 \times 2.0\right) + \left(200 \times 3.0\right)$$

- Apply the principle of moments to calculate $$R_{L}$$:

{align=center} Clockwise moments = Anticlockwise moments

{align=center} $$R_{L} \times 4.0 = \left(120 \times 2.0\right) + \left(200 \times 3.0\right)$$ $m{[1 mark]}

{align=center} $$R_{L} \times 4.0 = 240 + 600$$

{align=center} $$R_{L} = \frac{840}{4.0}$$

{align=center} $$R_{L} =$$ $f{$$210 \text{ N}$$} $m{[1 mark]}

**Mark Scheme and Guidance**
1 mark for correct calculation of anticlockwise moments **OR** clockwise moments

1 mark for correct substitution of all values with consistent distances

1 mark for a correct final answer of $$210 \text{ N}$$
- ecf from incorrect moment equation
- Must include unit for this mark
- Accept 210 N or 2.1 × 10^2^ N
**End of Mark Scheme and Guidance**

**Examiner Tips and Tricks**
Taking moments about one of the supports eliminates that support's reaction force from the equation, making the algebra simpler. Choose the support you are NOT asked about as your pivot point.
**End of Examiner Tips and Tricks**
```
