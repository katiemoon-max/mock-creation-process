---
name: skills-demo-mode
description: Demo mode wrapper for any Claude Code skill. Runs any skill in narration mode — ask questions, explain what would happen at each step, describe outputs without executing them. Use for presentations, onboarding, or showing stakeholders how a skill works. Invoke with /skills-demo-mode [skill-name].
allowed-tools: AskUserQuestion,Read,Glob
---

# Skills Demo Mode

You are running a skill in **demo mode**. This is a presentation and walkthrough tool. You are demonstrating how a skill works — you are NOT running it for real.

**Critical distinction:** In demo mode, no real actions are taken. No files are created, no APIs are queried, no spreadsheets are written, no external services are called. Everything is narrated. Make this explicit at the start so the audience understands what they are watching.

## Step 1: Identify the Skill

If the user invoked `/skills-demo-mode [skill-name]`, use that skill name. If no skill was specified, ask:

> "Which skill would you like to demo? Provide the skill name (e.g. `mock-exam-plan-gated`) and I'll walk through it in demo mode."

Once you have the skill name, read its SKILL.md file from `~/.claude/skills/[skill-name]/SKILL.md`.

If the file doesn't exist, tell the user and list available skills from `~/.claude/skills/`.

## Step 2: Opening Frame

Before starting, present a brief framing statement for the audience:

> "We're running **[Skill Display Name]** in demo mode. This is a walkthrough — I'll go through every step of the skill as normal, but instead of taking real actions (creating files, querying databases, calling APIs), I'll narrate what would happen and describe what the output would look like.
>
> If you have existing outputs from a previous live run of this skill, you can share them at any point and I'll pull them up to show the real thing."

## Step 3: Check for Existing Outputs

Before starting the skill walkthrough, ask:

> "Do you have any existing outputs from a previous live run of this skill — for example, a spreadsheet, Notion page, or document — that you'd like to show at relevant points? If yes, have them open and ready to switch to. I'll flag the moments in the demo where it makes sense to show the real thing."

If yes: note what outputs exist and at which point in the walkthrough they are relevant. When you reach that point, say: "This is a good moment to switch to your [spreadsheet/Notion page/etc.] if you'd like to show the real output." Then continue narrating once they're ready.

If no: continue with narration only.

## Step 4: Run the Skill in Demo Mode

**Load the skill's full instructions from its SKILL.md file** (already read in Step 1). Follow them exactly, with these modifications:

### Ask all questions as normal
Run every intake question in sequence. One at a time. Wait for each answer. The user's answers are real — they shape the narration throughout and make the demo feel authentic.

### Narrate instead of execute
At every point where the live skill would take a real action, instead:

1. **"What I'd do:"** — describe the action clearly: which tool would be called, what query would be run, how long it would take, any budget or rate limit considerations.
2. **"What the output would look like:"** — describe the output in concrete terms: structure, layout, what data would appear, what the user would see. Be specific enough that the audience can picture it.

If existing outputs were shared in Step 3, reference them here: "This is a good moment to switch to your [output] if you'd like to show the real thing."

### Honour all confirmation checkpoints
Any confirmation prompt, sign-off step, or pause-and-check built into the skill still fires. Present it as normal. Treat "looks good" or equivalent as sign-off and continue. This is part of what makes the demo authentic — the audience sees that the skill enforces quality at key moments, not just that it produces output.

### Explain the rationale at key checkpoints
At each major checkpoint, briefly explain why it exists — what error it prevents, what would go wrong downstream without it. One or two sentences. The audience should leave understanding the logic, not just the steps.

### Language to use throughout
Use language that makes the demo/live distinction clear at all times:
- "In a live run, I'd now..."
- "This would create..."
- "At this point the user would see..."
- "The output here would be..."

Never use language that implies real actions are happening (e.g. "I've created the tab" or "I've queried the database").

## Step 5: Closing Summary

After the skill walkthrough is complete, present a brief closing summary covering:
- What the full live run would produce (files, tabs, pages, or other outputs)
- Approximate time for a live run
- Any prerequisites or setup needed before running it for real
- Any budget considerations (e.g. API query limits)

Then offer:

> "That's the full walkthrough. To run this for real, invoke `/[skill-name]`."

## Tone

Match the tone of whatever skill is being demoed. If it's a formal, gated pipeline, maintain that rigour. If it's a lightweight utility skill, keep it light. The demo should feel like the real thing — just narrated.
