# Nested skill folders

`skills/` stays flat: every skill is `skills/<name>/SKILL.md`. There are no group folders such as `skills/engineering/`
or `skills/productivity/`.

## Why this is out of scope

Agent clients discover skills one level below the skills directory, so a nested layout only works with an installer that
flattens it again. The skills also point at each other by relative path (`../grilling/SKILL.md`), which assumes they
are siblings; nesting would break those links or force them to know the grouping.

Grouping is still useful for humans, so it lives in the skill list in `AGENTS.md` and the groups in `SCOPE.md`, where it
costs nothing at load time.

## Prior requests

- Considered when importing mattpocock/skills, which groups skills into `engineering/`, `productivity/`, `misc/`, and
  `in-progress/` (November 2026).
