# Skill mechanics

The skill-specific branch of [`writing-for-agents`](../SKILL.md): what changes when the document is a skill (packaging,
frontmatter, invocation, router skills). Everything else about writing it is the universal reference in `SKILL.md`.

Skills in this repo follow the [Agent Skills specification](https://agentskills.io/specification) so they load in any
compliant client (Goose, Claude Code, Gemini CLI, and others).

## Packaging

```text
skill-name/
├── SKILL.md          # required: frontmatter + body
├── references/       # disclosed reference, loaded when a pointer fires
├── scripts/          # executable code the agent runs instead of reinventing
└── assets/           # templates and static files the agent copies or fills in
```

- Keep `SKILL.md` under 500 lines / ~5,000 tokens. Past that, disclose reference into `references/`.
- Reference bundled files by relative path from the skill root (`references/FOO.md`), one level deep. A reference file
  that points at another reference file is a chain the agent may never finish walking.
- Write each pointer with its condition: "Read `references/api-errors.md` if the API returns a non-200 status", not "see
  `references/`".
- Keep **gotchas** in `SKILL.md` itself: they are the highest-value lines and must be in context when the mistake is
  about to happen.

## Frontmatter

These keys are the portable set defined by the spec:

| Key             | Required | Rule                                                                                                        |
| --------------- | -------- | ----------------------------------------------------------------------------------------------------------- |
| `name`          | yes      | 1–64 chars, `a-z0-9-`, no leading/trailing/double hyphen, **must equal the directory name**                  |
| `description`   | yes      | 1–1024 chars: what it does **and** when to use it                                                            |
| `license`       | no       | short license name or pointer to a bundled license file                                                     |
| `compatibility` | no       | ≤500 chars; only when the skill has real environment needs (tools, network, target client)                   |
| `metadata`      | no       | string→string map for anything else (`author`, `version`); use distinctive key names                         |
| `allowed-tools` | no       | experimental, space-separated pre-approved tools; support varies by client                                  |

**Deliberate exception:** this repo also uses `disable-model-invocation: true`, which is not in the spec. Clients that
support it (Claude Code) hide the skill from autonomous activation; clients that do not (Goose and most others) ignore
it, so the skill still behaves as model-invoked there. Strict validators such as `skills-ref validate` flag it as an
unexpected key; that is expected. Add no other client-specific keys (`argument-hint`,...), and no client-specific
sidecar files (such as `agents/openai.yaml`).

## Invocation

Two choices, trading the two loads:

- A **model-invoked** skill (the spec default): its `name` and `description` load at startup for every session, and the
  agent activates the skill when a task matches. A user can still ask for it by name. The description is the skill's
  top-level context pointer: permanent context load in exchange for discoverability, so the pointer-writing rules in
  `SKILL.md` apply in full.
- A **user-invoked** skill sets `disable-model-invocation: true`: in clients that honor the key, only the human naming
  it invokes it, so it costs no context load but spends cognitive load (you are the index that must remember it).
  Because clients that ignore the key still treat it as model-invoked, keep its description written as a trigger anyway.

Pick model-invocation only when the agent must reach the skill on its own, or another skill must.

Write the description as a trigger, not a summary:

- Lead with the action, then `Use when ...` listing each distinct branch that should fire it.
- Name the user's intent, including phrasings where they never say the domain word.
- Be a little pushy: under-triggering is the common failure. A few sentences is usually right.
- Leave out implementation detail and marketing ("optimized for X"): every word costs on every turn.

A model-invoked skill whose content is all reference is also a home for shared reference: other skills can tell the
agent to load it, so reference needed by several skills lives in one place.

## Splitting by invocation

The invocation cut of splitting (the sequence cut lives in `SKILL.md`): split off a skill when you have a distinct
leading word that should trigger it on its own (a trigger word you actually use in your prompts), or another skill must
reach it. You pay context load for the new always-loaded description, so that independent reach has to be worth it.

## Router skills

A **router skill** names other skills and tells the agent to load them, so the human has one name to remember instead of
several. Point at siblings by name and by relative path (`../grilling/SKILL.md`) so the router works whether the client
loads skills by name or by file.
