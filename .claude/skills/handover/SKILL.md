---
name: handover
description: Create a session handover summary capturing key insights, decisions, and next steps so the next conversation can pick up where this one left off. Also backs up the vault to GitHub.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
user_invocable: true
---

# Session Handover

> **Purpose**: Write a concise handover document at the end of a session so the next conversation starts with full context. Emphasise insights and decisions, not a granular activity log.

---

## Process

1. **Check for active mock paper pipeline state** — look for `project.json` files in `02 - Projects/**/`. For each, read `phase`, `gates`, `nextStep`, and the question-level progress. If any project is mid-pipeline, include its current phase and suggested next command at the top of the handover so the next session can resume without re-orienting.

2. **Review the conversation** — mentally walk through the session and identify:
   - **What was worked on**: which project(s), paper(s), or task(s)
   - **Key decisions made**: design choices, approach changes, things confirmed or ruled out
   - **Important insights**: anything learned that would be non-obvious to a fresh session (e.g. exam board quirks, formatting discoveries, tool behaviours)
   - **Current state**: what's done, what's in progress, what's blocked
   - **Next steps**: concrete actions to pick up from, in priority order. If a `project.json` exists, lead with its `nextStep` command verbatim.

2. **Write the handover file** to `C:\Users\kjmoo\Documents\Claude\.claude\handovers` with the filename format `YYYY-MM-DD.md` (use today's date). If a file for today already exists, append a letter suffix: `YYYY-MM-DD-b.md`, `YYYY-MM-DD-c.md`, etc.

3. **Use this template**:

```markdown
# Session Handover — YYYY-MM-DD

## What we worked on
<!-- 1-3 sentences: project context and scope of the session -->

## Key decisions & insights
<!-- Bullet list of the important things learned or decided. These should be non-obvious — don't state things that are already in memory or derivable from the files. -->

## Current state
<!-- Where things stand right now. What's complete, what's in progress, any blockers. -->

## Next steps
<!-- Numbered list, priority order. Be specific enough that the next session can start immediately. -->
```

4. **Keep it concise** — a good handover is typically 15-30 lines. It's a briefing, not a transcript. If something is important enough to persist beyond the next session, it should go into memory instead.

5. **Check memory** — if any insights from the session should be saved as permanent memories (feedback corrections, project status changes, new reference locations), flag these to the user and offer to save them before closing out. Don't save them silently — the user should confirm.

6. **Update project status** — read `.claude/context/project-status.md` and update the relevant row(s) to reflect the current state of whatever was worked on. Change the Status, Next Action, and Last Updated columns. If a new project or paper was started, add a row.

7. **Log vault issues** — if any vault issues were noticed during the session (missing context, stale references, duplication found, broken paths), append them to `.claude/vault-health-log.md` under "Open Issues" using the format: `### [YYYY-MM-DD] Issue title` with Category, Severity, Description, and Suggested fix fields. Skip this step if no issues were noticed.

8. **Back up to GitHub** — after writing the handover and any memory updates, commit and push all changes:
   ```
   git add -A
   git commit -m "Session handover — YYYY-MM-DD"
   git push
   ```
   If the push fails (e.g. no internet), tell the user — the local commit is still safe and can be pushed later.

---

## Guidelines

- **Tone**: Write as a briefing to a colleague picking up the work. Direct, specific, no filler.
- **Don't duplicate memory**: If something is already captured in a memory file, don't repeat it in the handover — just reference it.
- **Don't log tool calls**: The handover captures *what matters*, not *what happened mechanically*.
- **Date awareness**: Always use the actual current date, not a placeholder.
