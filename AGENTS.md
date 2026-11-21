# Agent skills repository

## Overview

A personal, curated set of engineering skills packaged per the
[Agent Skills specification](https://agentskills.io/specification), used primarily with **Goose CLI** (Gemini models via
an OpenAI-compatible gateway) and also with Claude Code. The skills cover a workflow from a loose idea to merged code:
interview and design, spec, tickets, test-first implementation, review, and debugging, plus Python project and marimo
notebook tooling.

Several skills are adapted from [mattpocock/skills](https://github.com/mattpocock/skills). When adapting one, keep its
intent, apply the conventions below, and generalize language-specific examples (prefer Python or Bash).

## Skills

`U` marks user-invoked skills (`disable-model-invocation: true`); the rest are model-invoked.

- **Design and planning**: `grilling`, `grill-me` (U), `grill-with-docs` (U), `domain-modeling`, `codebase-design`,
  `improve-codebase-architecture` (U), `wayfinder` (U), `research`, `prototype`
- **Specs and tickets**: `setup-skills` (U), `to-spec` (U), `to-tickets` (U), `triage` (U)
- **Building and fixing**: `implement` (U), `implement-spec` (U), `tdd`, `diagnosing-bugs`, `code-review`
- **Python and notebooks**: `python-project-scaffold`, `setup-pre-commit` (U), `marimo-notebook`, `marimo-batch`,
  `anywidget`
- **Session and meta**: `handoff` (U), `writing-for-agents`

## Skill conventions

- Frontmatter uses only spec keys (`name`, `description`, optional `license`, `compatibility`, `metadata`,
  `allowed-tools`); `name` equals the directory name. The one deliberate exception is `disable-model-invocation: true`
  on user-invoked skills (honored by Claude Code, ignored elsewhere); no other client-specific keys or sidecar files
  (e.g. `agents/openai.yaml`). A skill that other skills load must stay model-invoked.
- Descriptions say what the skill does and then `Use when ...` with its triggers.
- `SKILL.md` stays under 500 lines; disclosed reference lives in `references/`, copyable templates in `assets/`,
  executables in `scripts/`, each linked from `SKILL.md` by a relative path with the condition for loading it. Skills
  point at each other by name plus a relative link (`../grilling/SKILL.md`), so `skills/` stays flat.
- Examples are language-neutral where possible; when one language is needed, use Python (or Bash for shell tasks).
  Prototypes that need a UI are [marimo](https://marimo.io/) notebooks.
- See `skills/writing-for-agents/references/SKILL-MECHANICS.md` for the full rules.

## Packaging

- The repo root is an [Agent Plugins](https://agent-plugins.org/specification) 1.0.0 package: `plugin.json` (portable
  manifest, checked against the published schema by pre-commit) plus `skills/`. Keep `skills/` flat; plugin clients
  only look at its immediate subdirectories.
- `.claude-plugin/marketplace.json` makes the repo a Claude Code marketplace whose one plugin is the repo root. Check
  changes with `claude plugin validate .`.
- Neither manifest sets `version`, so clients that track git treat every commit on `main` as an update. If you add a
  `version`, set the same SemVer value in both files and bump it on every release, or installs stop updating.

## Layout the skills write in a target repo

- Specs and issues: `.scratch/<feature>/spec.md` and `.scratch/<feature>/issues/<NN>-<slug>.md`, issues as
  [TaskNotes](https://tasknotes.dev/developers/specification/) (or GitHub issues, per `setup-skills`)
- Research notes: `.scratch/research/`
- Domain language: `GLOSSARY.md` (or `GLOSSARY-MAP.md`) at the root; ADRs in `docs/adr/`
- Rejected feature requests: `.out-of-scope/<concept>.md`
- Per-repo skill configuration: `docs/agents/` (issue tracker, triage labels, domain-doc rules)

## Working in this repo

- Run `pre-commit run --all-files` before committing (CI runs the same hooks on every PR via
  `.github/workflows/pre-commit.yml`). It runs rumdl (Markdown lint + format), shellcheck, and
  `scripts/validate_skills.py`, which checks every skill's frontmatter, naming, size, and relative links.
- Spelling is American English, enforced by codespell (`en-GB_to_en-US` plus `.codespell-en-us.txt` for words its
  dictionary misses). Exceptions are allowed only for outside names or code that would break; add them to
  `--ignore-words-list` in `.pre-commit-config.yaml`.
- `rumdl fmt` reflows prose to 120 columns. Wrap a table that sits inside a list item in
  `<!-- rumdl-disable MD013 -->` / `<!-- rumdl-enable MD013 -->`, or reflow will flatten it.
- The upstream validator (`skills-ref validate skills/<name>`) reports `disable-model-invocation` as an unexpected
  field; that is expected for the `U` skills above and nothing else should fail it.
