---
name: research
description: Investigate a question against high-trust primary sources (official docs, source code, specs, first-party APIs) and save cited findings as a Markdown file in the repo. Use when the user wants a topic researched, docs or API facts gathered and verified, or reading legwork delegated to a background agent.
compatibility: Works best in agents that can dispatch subagents (e.g. Goose CLI) and have web access.
---

# Research

Investigate a question against **primary sources** using an independent subagent or background agent with a fresh
context window, so the reading does not crowd the parent session.

## Process

1. **Investigate**: check primary sources, following every claim back to the source that owns it. Secondary sources
   (blogs, forums) only point you to a primary one; never cite them as the answer.
2. **Synthesize**: write the findings to a single Markdown file matching the repo's convention (default
   `.scratch/research/<topic-slug>.md`), citing the source for each claim and marking anything you could not verify.
3. **Report back**: give the parent session the file path and a short summary of the answer.
