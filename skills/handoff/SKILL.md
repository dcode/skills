---
name: handoff
description: Compact the current conversation into a handoff document for another agent to pick up.
argument-hint: "What will the next session be used for?"
disable-model-invocation: true
---

# Handoff Skill

Compact the current conversation into a handoff document for another agent or session to pick up.

## Process

1. **Summarize state**: Summarize the current conversation, accomplishments, and remaining items so a fresh agent can continue seamlessly.
2. **Save location**: Save to the temporary directory of the user's OS (`$TMPDIR`, else `/tmp`; `%TEMP%` on Windows) — not the current workspace.
3. **Suggested skills**: Include a "suggested skills" section naming which skills the next agent should call.
4. **References**: Do not duplicate content already captured in other artifacts (specs, plans, ADRs, TaskNotes issues, commits, diffs). Reference them by path or URL instead.
5. **Redaction**: Redact any sensitive information (API keys, passwords, PII). If the user passed arguments, treat them as the focus for the next session.