---
name: setup-skills
description: Scaffold the per-repo configuration the engineering skills rely on (issue tracker as local TaskNotes markdown under .scratch/ or GitHub issues, triage label vocabulary, and GLOSSARY.md/ADR domain-doc rules) and point AGENTS.md at it. Use when setting up a repo for these skills, when another skill reports the issue tracker or triage labels are not configured, or when the user asks to (re)configure agent skills for a project.
disable-model-invocation: true
---

# Setup Skills

Scaffold the per-repo configuration the engineering skills assume:

- **Issue tracker**: [TaskNotes](https://tasknotes.dev/developers/specification/) markdown files under `.scratch/`
  (default), or GitHub issues via the `gh` CLI.
- **Triage labels**: the label strings for the canonical triage roles.
- **Domain docs**: where `GLOSSARY.md` and ADRs live, and how skills consume them.

## Process

1. **Explore** the repo's starting state: `AGENTS.md` / `CLAUDE.md`, `GLOSSARY.md` / `GLOSSARY-MAP.md`, `docs/adr/`,
   `docs/agents/`, `.scratch/`, and `.out-of-scope/`. Note anything already configured so you extend it rather than
   overwrite it.

2. **Choose the tracker.** Default to local TaskNotes. Offer GitHub issues when the repo has a GitHub remote
   (`git remote -v`) and the user wants a hosted tracker; it needs the `gh` CLI, authenticated.

3. **Write the config files** into `docs/agents/`, copying each seed from this skill's `assets/` and adapting it to what
   step 1 found:

   <!-- rumdl-disable MD013 -->

   | Seed                                                                                                                                                          | Destination                    |
   | ------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------ |
   | [assets/issue-tracker-local.md](assets/issue-tracker-local.md) (local TaskNotes) or [assets/issue-tracker-github.md](assets/issue-tracker-github.md) (GitHub) | `docs/agents/issue-tracker.md` |
   | [assets/triage-labels.md](assets/triage-labels.md)                                                                                                            | `docs/agents/triage-labels.md` |
   | [assets/domain.md](assets/domain.md)                                                                                                                          | `docs/agents/domain.md`        |

   <!-- rumdl-enable MD013 -->

   If a destination file already exists, show the user the diff and ask before replacing it.

4. **Point the agent at them.** Add (or update) this block in `AGENTS.md`, or in `CLAUDE.md` if that is the repo's only
   agent file:

   ```md
   ## Agent skills

   - Issue tracker: read `docs/agents/issue-tracker.md` before publishing or fetching an issue.
   - Triage labels: read `docs/agents/triage-labels.md` before applying a triage label.
   - Domain docs: read `docs/agents/domain.md` before exploring the codebase.
   ```

Done when all three files exist in `docs/agents/` and the agent file contains the block.
