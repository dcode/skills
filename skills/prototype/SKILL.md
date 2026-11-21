---
name: prototype
description: Build a throwaway prototype, usually a marimo notebook, that answers one design question. Use when the user wants to check whether a state model, business rule, or data shape feels right by pushing it through cases, or to see several alternative layouts for a view, dashboard, or report before committing, or when a wayfinder prototype ticket needs a concrete artifact to react to.
compatibility: Requires Python with uv; marimo is pulled in per notebook via PEP 723 inline dependencies.
---

# Prototype

A prototype is **throwaway code that answers a question**. The question decides the shape.

Whenever the prototype needs a UI to experiment with or demonstrate, build it as a [marimo](https://marimo.io/)
notebook: a plain Python file that runs as an interactive app, is reactive by default, and exports to a static,
shareable HTML page. Load the `marimo-notebook` skill ([../marimo-notebook/SKILL.md](../marimo-notebook/SKILL.md))
before writing one, and the `anywidget` skill ([../anywidget/SKILL.md](../anywidget/SKILL.md)) only if a visual needs
something marimo's built-in UI elements cannot draw.

## Pick a branch

Identify which question is being answered, using the user's prompt, the surrounding code, or by asking if the user is
around:

- **"Does this logic / state model feel right?"** → read [references/LOGIC.md](references/LOGIC.md). A notebook with
  the logic as a pure, liftable function, free-play buttons, and tabbed guided walkthroughs that push it through the
  cases hard to reason about on paper, drivable by a non-developer.
- **"What should this look like?"** → read [references/UI.md](references/UI.md). Several radically different variants
  of one view in a notebook, switchable from a single control, fed by the project's real data.

The two branches produce very different artifacts, so getting this wrong wastes the whole prototype. If the question is
genuinely ambiguous and the user isn't reachable, default to whichever branch better matches the surrounding code (a
backend module → logic; a report, dashboard, or page → UI) and state the assumption at the top of the prototype.

## Rules that apply to both

1. **Throwaway from day one, and clearly marked as such.** Put the prototype next to the module it's prototyping for so
   the context is obvious, and name it so a casual reader can see it's not production: `prototype_<question>.py`.
2. **Trivial to run.** One command, no setup: `uv run marimo edit prototype_<question>.py` (or `marimo run` for the
   app view). Declare every dependency in the notebook's PEP 723 header so nothing needs installing first.
3. **No persistence by default.** State lives in memory. Persistence is the thing the prototype is _checking_, not
   something it should depend on. If the question explicitly involves a database, hit a scratch DB or a local file with
   a clear "PROTOTYPE, wipe me" name.
4. **Skip the polish.** No tests, no error handling beyond what makes the prototype _runnable_, no abstractions. The
   point is to learn something fast.
5. **Surface the state.** After every action (logic) or on every variant switch (UI), render the full relevant state so
   the user can see what changed.
6. **Check it runs.** Run `uvx marimo check <notebook.py>` and fix what it reports before handing it over.
7. **Capture it when done.** Fold any validated decision into the real code, then capture the prototype itself as a
   **primary source**: commit it to a throwaway branch, out of main, and leave a context pointer to that branch on the
   implementation issue. Capture the answer too (the verdict and the question it settled) in the issue or a commit. The
   main branch keeps only the validated decision.
