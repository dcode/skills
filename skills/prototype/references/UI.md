# UI Prototype

Generate **several radically different variants** of one view in a marimo notebook, switchable from a single control.
The user flips between variants, picks one (or steals bits from each), then throws the rest away.

If the question is about logic/state rather than what something looks like, this is the wrong branch. Use
[LOGIC.md](LOGIC.md).

## When this is the right shape

- "What should this report / dashboard / summary look like?"
- "I want to see a few options for presenting this data before committing."
- "Try a different layout for the results view."
- Any time the user would otherwise spend a day picking between three vague mockups in their head.

## Real data, not a vacuum

A UI prototype is much easier to judge when it shows **real data at real density**: actual records, actual edge cases,
actual volume. Every variant looks fine on three hand-written rows. So the notebook's first cells load data through the
project's own code (import its loader, query a fixture or a local copy of the data), and every variant renders that same
data. Only the presentation differs.

If the project has its own web frontend and the question is how one of _its_ pages should look, see **Variants inside
an existing web app** below instead.

## Process

### 1. State the question and pick N

Default to **3 variants**. More than 5 stops being radically different and starts being noise, so cap there.

Write the plan in one line as the notebook's first `mo.md` cell:

> "Three variants of the weekly usage report, switchable from the dropdown, on last month's real data."

This works whether the user is here to push back or not.

### 2. Generate radically different variants

Write each variant as one function that takes the data and returns a marimo element:
`variant_a(data) -> mo.Html`, `variant_b(data)`, `variant_c(data)`. Hold each one to:

- The view's purpose and the data it has access to.
- marimo's built-in building blocks first (`mo.md`, `mo.hstack`/`mo.vstack`, `mo.ui.table`, `mo.stat`, charts via
  altair or plotly); reach for an anywidget only when a visual genuinely needs custom drawing.
- A short human name per variant, e.g. `"B (Sidebar summary)"`.

Variants must be **structurally different**: different layout, different information hierarchy, different primary
affordance, not just different colors. Three slightly-tweaked tables isn't a UI prototype, it's wallpaper. If two
drafts come out too similar, redo one with explicit "do not use a table" guidance.

### 3. Wire up the switcher

One dropdown, seeded from the URL so a variant is shareable and reload-stable:

```python
@app.cell
def _(mo):
    variants = {"A (Table)": variant_a, "B (Sidebar summary)": variant_b, "C (Cards)": variant_c}
    choice = mo.ui.dropdown(
        options=list(variants),
        value=mo.query_params().get("variant") or "A (Table)",
        label="Variant",
    )
    return choice, variants


@app.cell
def _(choice, data, mo, variants):
    mo.vstack([choice, variants[choice.value](data)])
    return
```

Keep the data loading above the switcher; only the rendered output changes per variant. Use `mo.ui.tabs` instead of a
dropdown when the user wants to flip back and forth quickly rather than share links to one variant.

### 4. Hand it over

Run `uvx marimo check`, then start it (`uv run marimo run prototype_<question>.py`) and surface the URL plus the variant
names, or export a static copy with `uv run marimo export html-wasm ... --mode run` if the data can travel with it. The
interesting feedback is usually **"I want the header from B with the chart from C"**, which is the actual design they
want.

### 5. Capture the answer and clean up

Once a variant has won, capture the answer (which variant and why), then capture the prototype the way the
[SKILL](../SKILL.md) describes. Build the winner properly in the real code; the notebook with every variant goes to the
throwaway branch as the primary source, not into main.

## Variants inside an existing web app

When the view being prototyped is a page of the project's own web frontend, judge it in place: real header, real
navigation, real density. Render the variants on the existing route (or, only if nothing could host it, a throwaway
route whose path says `prototype`), switched by a `?variant=` URL parameter and a small floating switcher bar (previous
/ label / next, arrow-key support, hidden in production builds). Follow the app's own framework, routing, and component
conventions; the rest of this file (N, radical difference, real data, capture) applies unchanged.

## Anti-patterns

- **Variants that differ only in color or copy.** That's a tweak, not a prototype. Real variants disagree about
  structure.
- **Sharing too much code between variants.** A shared data-loading cell is the point; a shared layout helper defeats
  it. Each variant should be free to throw out the layout.
- **Wiring variants to real mutations.** Read-only prototypes are fine. If a variant needs to mutate, point it at a
  stub: the question is "what should this look like", not "does the backend work".
- **Promoting the prototype directly to production.** The variant code was written under prototype constraints (no
  tests, minimal error handling). Rewrite it properly when you fold it in.
