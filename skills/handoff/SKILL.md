---
name: handoff
description: Compact the current conversation into a handoff document another agent or session can pick up cold. Use when the user wants to hand off, pause, or continue work in a new session, or the context window is getting full and work must carry over.
disable-model-invocation: true
---

# Handoff

Compact the current conversation into a handoff document for another agent or session. If the user said what the next
session is for, treat that as its focus and weight the document toward it.

## Process

1. **Summarize state**: the goal, what was accomplished, decisions made and why, and the remaining items, so a fresh
   agent can continue without re-deriving anything.
2. **Reference, don't copy**: point at artifacts that already hold content (specs, plans, ADRs, TaskNotes issues,
   commits, diffs) by path or URL instead of duplicating them.
3. **Suggest skills**: add a "Suggested skills" section naming the skills the next agent should load and why.
4. **Redact**: remove secrets and PII (API keys, passwords, tokens, personal data).
5. **Save** to the OS temp directory (`$TMPDIR`, else `/tmp`; `%TEMP%` on Windows), not the workspace, and report the
   full path to the user.
