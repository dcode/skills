---
name: research
description: Investigate a question against high-trust primary sources and capture the findings as a Markdown file in the repo. Use when the user wants a topic researched, docs or API facts gathered, or reading legwork delegated to a background agent.
disable-model-invocation: true
---

# Research Skill

Investigate a question against **primary sources** (official docs, source code, specs, first-party APIs) using an independent background agent or subagent with a fresh context window.

## Process

1. **Investigate**: Check primary sources, following every claim back to the source that owns it.
2. **Synthesize**: Write findings to a single Markdown file matching the repository's convention (e.g. under `thoughts/research/`), citing each claim's source.
3. **Handoff**: Report the completed research path back to the parent session.