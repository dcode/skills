# Agent Things

Engineering skills for AI coding agents, packaged per the
[Agent Skills specification](https://agentskills.io/specification) so any compliant client (Goose, Claude Code, and
others) can load them. They take work from a loose idea to merged code: design interviews, specs, tickets, test-first
implementation, review, debugging, and Python / marimo tooling. See [AGENTS.md](AGENTS.md) for the full list and the
conventions they follow.

## Install

To install globally for your user:

```shell
git clone https://github.com/dcode/agents.git ~/.agents
```

or checkout elsewhere and symlink:

```shell
cd ~/Projects/
git clone https://github.com/dcode/agents.git
ln -sf "$(readlink -f agents)" "${HOME}/.agents"
```

The skills live in `~/.agents/skills/<name>/SKILL.md`. If your client looks for skills somewhere else, point that
directory (or a symlink) at `~/.agents/skills`.

## First use in a project

Run the `setup-skills` skill once per repository. It records which issue tracker to use (local TaskNotes files under
`.scratch/` or GitHub issues), the triage labels, and where `GLOSSARY.md` and ADRs live, in `docs/agents/`. The planning
and ticket skills read those files.

## Typical flow

1. `grill-with-docs` or `wayfinder`: settle the design (or map a large, foggy effort).
2. `to-spec`: write the spec. `to-tickets`: split it into dependency-ordered tickets.
3. `implement` (one ticket) or `implement-spec` (the whole graph): build test-first with `tdd`, then `code-review`.
4. `diagnosing-bugs` when something breaks; `triage` to keep the backlog moving.

## Contributing

```shell
uv tool install pre-commit
pre-commit install
pre-commit run --all-files
```

The hooks lint and format Markdown (rumdl), check shell scripts (shellcheck), and validate every skill against the
spec and this repo's conventions (`scripts/validate_skills.py`).
