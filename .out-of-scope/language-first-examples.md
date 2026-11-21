# Language-first examples

Skills do not assume a particular application language or stack. Examples are written language-neutrally where
possible, and when a concrete language is needed they use Python (or Bash for shell tasks), not TypeScript/JavaScript.

## Why this is out of scope

Most of the imported skills were written around full-stack TypeScript web apps (`expect(...).toBe(...)`, `jest.mock`,
`performance.now()`, PGLite, `?variant=` routes in a React app). An agent copies the shape of the examples it is given,
so TypeScript examples pull every project toward TypeScript idioms even when the code is Python, Terraform, or Bash.

The behavior each skill teaches (deep modules, testing at seams, mocking only at boundaries, building a feedback loop)
is language-independent; the examples only need to make it concrete. The deliberately language-specific skills
(`python-project-scaffold`, `marimo-*`, `anywidget`) are the exception, and they say so in their descriptions.

Prototypes that need a UI are marimo notebooks rather than single-page web apps, for the same reason.

## Prior requests

- Generalized the `codebase-design`, `tdd`, `diagnosing-bugs`, `triage`, and `prototype` examples during the Agent
  Skills spec migration (November 2026).
