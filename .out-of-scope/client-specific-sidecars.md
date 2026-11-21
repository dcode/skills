# Client-specific sidecar files and keys

Skills here carry no files or frontmatter keys that only one agent client understands, such as `agents/openai.yaml`
(Codex display and invocation settings) or `argument-hint` (a Claude Code slash-command hint).

This rule is about the skills. At the repo root, a client's distribution file is allowed when no portable equivalent
exists: `.claude-plugin/marketplace.json` lets Claude Code install and update the plugin, because the Agent Plugins
spec standardizes the package (`plugin.json`, `skills/`) but not how clients fetch or update it.

## Why this is out of scope

The skills are meant to load unchanged in any client that implements the
[Agent Skills specification](https://agentskills.io/specification), and Goose CLI is the primary one. A sidecar file or
key that one client reads is dead weight everywhere else, drifts out of sync with `SKILL.md` because nothing validates
it, and invites a parallel set of per-client settings for every skill.

The one deliberate exception is `disable-model-invocation: true`. Clients that honor it (Claude Code) keep user-invoked
skills out of autonomous activation; clients that don't simply ignore it, so the skill still works. It is the only key
`scripts/validate_skills.py` allows beyond the spec, and `skills-ref validate` flagging it is expected.

## Prior requests

- Removed the `agents/openai.yaml` files and `argument-hint` keys from skills imported from mattpocock/skills during the
  Agent Skills spec migration (November 2026).
