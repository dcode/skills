# Issue tracker: Local TaskNotes Markdown

Issues and tasks for this repo live as first-class markdown files in `thoughts/` formatted as **TaskNotes** (conforming to the [TaskNotes specification](https://tasknotes.dev/developers/specification/)).

## Conventions

- One feature per directory: `thoughts/<feature-slug>/`
- The spec is `thoughts/<feature-slug>/spec.md`
- Implementation tasks are one file per task at `thoughts/<feature-slug>/issues/<NN>-<slug>.md`, numbered from `01`
- YAML frontmatter includes `title`, `status`, `priority`, `tags`, `blockedBy`, `dateCreated`, and `dateModified`
- Body includes "What to build" and "Acceptance criteria" sections

## When a skill says "publish to the issue tracker"

Create a new TaskNote markdown file under `thoughts/<feature-slug>/issues/` with YAML frontmatter conforming strictly to the TaskNotes specification.

## When a skill says "fetch the relevant ticket/task"

Read the TaskNote file at the referenced path.