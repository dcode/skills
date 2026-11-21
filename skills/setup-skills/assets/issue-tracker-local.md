# Issue tracker: Local TaskNotes Markdown

Issues and specs for this repo live as markdown files in `.scratch/`, each issue a **TaskNote** conforming to the
[TaskNotes specification](https://tasknotes.dev/developers/specification/) with its default configuration.

## Conventions

- One feature per directory: `.scratch/<feature-slug>/`
- The spec is `.scratch/<feature-slug>/spec.md` (plain markdown, not a TaskNote)
- Implementation issues are one TaskNote per ticket at `.scratch/<feature-slug>/issues/<NN>-<slug>.md`, numbered from
  `01` in dependency order (blockers first), never a single combined tickets file
- Comments and conversation history append to the bottom of the issue under a `## Comments` heading

## TaskNote format

```markdown
---
title: "<NN>: <Ticket title>"
status: open
priority: normal
tags: [task, ready-for-agent]
blockedBy:
  - uid: "[[01-add-order-schema]]"
    reltype: FINISHTOSTART
dateCreated: 2026-11-20T09:30:00Z
dateModified: 2026-11-20T09:30:00Z
---

## What to build

The end-to-end behavior this ticket makes work, from the user's perspective, not a layer-by-layer implementation list.

## Acceptance criteria

- [ ] Acceptance criterion 1
- [ ] Acceptance criterion 2
```

Field rules (TaskNotes defaults):

- `tags` must include `task`: that tag is how TaskNotes recognizes a file as a task. Triage state is another tag (see
  `docs/agents/triage-labels.md` for the strings).
- `status`: `open` on create, `in-progress` while claimed, `done` when finished. `done` is the only completed status, so
  it is the only one that unblocks dependents.
- `priority`: one of `none`, `low`, `normal` (default), `high`.
- `blockedBy`: a list of objects, each with `uid` (a wikilink to the blocking ticket's file name, without `.md`) and
  `reltype: FINISHTOSTART`. Use `blockedBy: []` when nothing blocks the ticket. Never list the ticket itself.
- `dateCreated` / `dateModified`: ISO 8601 UTC datetimes; bump `dateModified` on every edit.
- `completedDate`: an ISO date (`YYYY-MM-DD`), required whenever `status: done`.
- `agentSession`: a custom field (TaskNotes preserves unknown fields), present once a session has claimed the ticket;
  see **Claiming**.

## Claiming

A session that starts work on a ticket claims it, as its first write:

- set `status: in-progress`, bump `dateModified`
- set `agentSession` to a string another session could use to find and resume this one: `<client>:<id>`, where `<id>`
  is whatever the client's resume command accepts (e.g. the session name or id for `goose session --resume`, the id for
  `claude --resume`). If the client exposes no id, use `<client>:<hostname>:<UTC start time>`.

Leave `agentSession` in place when the ticket is resolved, so the session that did the work stays traceable. A ticket
that is `in-progress` with an `agentSession` belongs to that session: resume it rather than re-claiming, unless the user
says the session is dead.

## Closing

- **Done**: set `status: done`, set `completedDate`, bump `dateModified`.
- **Won't do** (rejected, duplicate, out of scope): TaskNotes has no default canceled status, so set `status: done`,
  add a `wontfix` tag, and say why under `## Comments`. Then remove its `uid` from every other ticket's `blockedBy`, so
  nothing waits on work that will never happen.

## When a skill says "publish to the issue tracker"

Create a new TaskNote under `.scratch/<feature-slug>/issues/` (creating the directory if needed); a spec goes to
`.scratch/<feature-slug>/spec.md`.

## When a skill says "fetch the relevant ticket"

Read the file at the referenced path. The user will normally pass the path or the issue number directly.

## Wayfinding operations

Used by the `wayfinder` skill. A map is a directory; its tickets are TaskNotes inside it.

- **Map**: `.scratch/<effort>/map.md`, a TaskNote tagged `task` and `wayfinder-map` whose body holds the Destination /
  Notes / Decisions so far / Not yet specified / Out of scope sections.
- **Child ticket**: `.scratch/<effort>/issues/<NN>-<slug>.md`, a TaskNote tagged `task` and `wayfinder-<type>`
  (`research`/`prototype`/`grilling`/`task`). Number in creation order; the number is its id.
- **Blocking**: the ticket's `blockedBy`, referencing other tickets in the same map. A ticket is unblocked when every
  blocker has `status: done`.
- **Frontier query**: list `.scratch/<effort>/issues/*.md` with `status: open` whose blockers are all `done`; lowest
  number wins. `in-progress` tickets are claimed, so skip them.
- **Claim**: as in **Claiming** above (`status: in-progress` plus `agentSession`), as the session's first write.
- **Resolve**: append a `## Resolution` section with the answer, close it as **Done** above, then append a context
  pointer (gist + relative link) to the map's Decisions so far.
- **Out of scope**: close it as **Won't do** above (tagged `wontfix`) and add the line to the map's Out of scope
  section.
