# Scope

This repo is the set of skills I use every day with Goose CLI and Claude Code. It is a personal, curated collection: a
change earns its place by fixing something that went wrong in real use, not by being a good idea in the abstract. Issues
track changes to the skills; ideas are welcome, and each is judged against the bar below.

## The bar for changing a skill

A change lands only if it clears **both** parts:

1. **Observed failure.** It describes something that went wrong in a real session: what was asked, what the skill did,
   what should have happened. A hypothetical improvement ("it would be better if...") does not clear this part.
2. **Fits the conventions.** It follows [AGENTS.md](AGENTS.md) (Agent Skills spec frontmatter, `references/` / `assets/`
   / `scripts/` layout, language-neutral examples with Python or Bash where one is needed), and it does not match
   anything already rejected in [`.out-of-scope/`](.out-of-scope/).

Size is irrelevant: a one-word fix and a rewrite face the same bar.

## New skills

Before adding a skill, ask one question: **does this behavior compose from skills that already exist?** If it does,
improve or point at those skills instead (a router skill like `grill-with-docs` is the cheapest way to compose). A new
skill is justified only when it has its own trigger that should fire on its own, or other skills need to reach it.

A skill imported from elsewhere (for example [mattpocock/skills](https://github.com/mattpocock/skills)) is adapted
before it lands: conventions applied, client-specific files removed, language-specific examples generalized, and
references to skills this repo doesn't have resolved. `pre-commit run --all-files` must pass.

## By group

The groups below match the skill list in [AGENTS.md](AGENTS.md). All of them face the same bar; what differs is what to
watch for.

- **Design and planning** (`grilling`, `domain-modeling`, `codebase-design`, `wayfinder`, `prototype`, ...): changes
  must keep the agent finding facts itself and asking the user only for decisions.
- **Specs and tickets** (`setup-skills`, `to-spec`, `to-tickets`, `triage`): changes must work for every tracker
  `setup-skills` offers (local TaskNotes and GitHub), and local tickets must stay valid against the
  [TaskNotes specification](https://tasknotes.dev/developers/specification/).
- **Building and fixing** (`implement`, `implement-spec`, `tdd`, `diagnosing-bugs`, `code-review`): changes must keep
  the test-first loop and the separation between implementation and review.
- **Python and notebooks** (`python-project-scaffold`, `setup-pre-commit`, `marimo-*`, `anywidget`): these are the
  deliberately language-specific skills. Keep tool versions current via `pre-commit autoupdate` rather than hand edits.
- **Session and meta** (`handoff`, `writing-for-agents`): `writing-for-agents` holds the rules every other skill
  follows; change it first when a convention changes.

## Already decided

Each file in [`.out-of-scope/`](.out-of-scope/) records one rejected concept and why. Read them before proposing a
change:

- [Client-specific sidecar files and keys](.out-of-scope/client-specific-sidecars.md)
- [Language-first examples](.out-of-scope/language-first-examples.md)
- [Nested skill folders](.out-of-scope/nested-skill-folders.md)
- [A `thoughts/` directory for skill artifacts](.out-of-scope/thoughts-directory.md)

## Unclear issues

An issue that can't be judged against the bar gets one round of questions and the `needs-info` label. With no reply in
14 days, it is closed. Rejections close as "not planned" and, when the concept could come back, get a file in
`.out-of-scope/`.
