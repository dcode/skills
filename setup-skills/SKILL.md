---
name: setup-skills
description: "Configure this repo for the engineering skills, specializing in TaskNotes formatted markdown files as the issue tracker, domain docs, and triage labels."
disable-model-invocation: true
---

# Setup Skills (TaskNotes Edition)

Scaffold the per-repo configuration assumed by the engineering skills:

- **Issue tracker**: TaskNotes-formatted local markdown files under `thoughts/` (fully conforming to [TaskNotes specification](https://tasknotes.dev/developers/specification/))
- **Triage labels**: The strings used for canonical triage roles
- **Domain docs**: Where `GLOSSARY.md` and ADRs live, and consumer rules for reading them

This is a prompt-driven skill.

## Process

### 1. Explore

Look at the current repo to understand its starting state:
- `AGENTS.md` and `CLAUDE.md` at the repo root
- `GLOSSARY.md` and `GLOSSARY-MAP.md` at the repo root
- `docs/adr/` and `docs/agents/`
- `thoughts/` directory

### 2. Configure TaskNotes Issue Tracker & Domain Docs

- Set the issue tracker to **Local TaskNotes markdown files** under `thoughts/<feature>/issues/<NN>-<slug>.md` complying with the TaskNotes specification.
- Set up domain docs (`GLOSSARY.md` and `docs/adr/`).

### 3. Write Configuration Files

Write the configuration files using the seed templates in this skill folder:
- [issue-tracker-local.md](./issue-tracker-local.md): Local TaskNotes-conforming issue tracker
- [triage-labels.md](./triage-labels.md): Label mapping for triage
- [domain.md](./domain.md): Domain doc consumer rules + layout

Update `AGENTS.md` or `CLAUDE.md` to include the `## Agent skills` block pointing to these files.
