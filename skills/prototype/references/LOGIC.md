# Logic Prototype

A marimo notebook (a **shareable demo**) that lets anyone drive a state model by clicking buttons. Use this when the
question is about **business logic, state transitions, or data shape**: the kind of thing that looks reasonable on paper
but only feels wrong once you push it through real cases.

Because it runs as an app (`marimo run`) and exports to a static HTML page, you can hand it to a non-developer (a
designer, a PM, a domain expert) and let them feel the model for themselves. So it speaks their language, not the
code's.

## When this is the right shape

- "I'm not sure if this state machine handles the edge case where X then Y."
- "Does this data model actually let me represent the case where..."
- "I want to feel out what the API should look like before writing it."
- Anything where someone wants to **press buttons and watch state change**.

If the question is "what should this look like," this is the wrong branch. Use [UI.md](UI.md).

## Process

### 1. State the question

Before writing code, write down what state model and what question you're prototyping. One paragraph, as the
notebook's first cell, rendered with `mo.md` (visible in app view, not a code comment). A logic prototype that answers
the wrong question is pure waste, so make the question explicit so it can be checked later, whether the user is watching
now or returning to it AFK.

### 2. Isolate the logic as a liftable function

Put the actual logic (the bit that's answering the question) in top-level `@app.function` / `@app.class_definition`
cells, so it is a plain, importable Python definition that could be lifted into the real codebase later (see
`references/TOP-LEVEL-IMPORTS.md` in the `marimo-notebook` skill). The notebook around it is throwaway; this code isn't.

The right shape depends on the question:

- **A pure reducer**: `reduce(state, action) -> state` over a frozen dataclass. Good when actions are discrete events
  and state is a single value.
- **A state machine**: explicit states and a transition table. Good when "which actions are even legal right now" is
  part of the question.
- **A small set of pure functions** over a plain data type. Good when there's no implicit current state, just
  transformations.
- **A class with a clear method surface** when the logic genuinely owns ongoing internal state.

Pick whichever shape best fits the question being asked, _not_ whichever is easiest to wire to the UI. Keep it pure: no
`mo`, no UI elements, no callbacks reaching inside it. The notebook calls into it; nothing flows the other direction.

```python
@app.class_definition
@dataclass(frozen=True)
class Order:
    status: str = "draft"
    paid: bool = False


@app.function
def reduce(order: Order, action: str) -> Order:
    if action == "submit" and order.status == "draft":
        return replace(order, status="submitted")
    if action == "pay" and order.status == "submitted":
        return replace(order, paid=True)
    return order  # illegal actions leave state unchanged: is that the right call?
```

### 3. Build the notebook UI

Write it for a non-developer. Every label is in **domain language**, not code: buttons and state read like the
business, not the reducer.

The current state is accumulated from button callbacks, which is the case `mo.state()` exists for:

```python
@app.cell
def _(mo):
    get_order, set_order = mo.state(Order())
    return get_order, set_order


@app.cell
def _(mo, set_order):
    def dispatch(action):
        return mo.ui.button(label=action.title(), on_click=lambda _: set_order(lambda o: reduce(o, action)))

    free_play = mo.hstack([dispatch(a) for a in ("submit", "pay")])
    return (free_play,)
```

Lay it out top to bottom:

1. **Title and one-line explanation** of what this demo lets you explore (the question from step 1).
2. **Current state**: the full relevant state as a readable panel (`mo.md` with labeled fields, or `mo.ui.table` for
   collections, not a raw `repr`), re-rendered after every click. Where it helps a non-developer follow, call out what
   just changed.
3. **Free-play buttons**: one per action, always available, so anyone can poke at the model in any order.
4. **Guided walkthroughs**: a set of **scenarios** in `mo.ui.tabs`, one tab each. Each tab holds a short plain-language
   description of the scenario (the situation it sets up and what to watch for) and underneath it the ordered buttons to
   press. Each tab gets a "Start over" button that resets to a known initial state, so the scenario runs the same way
   every time.

Choose scenarios that demonstrate the awkward cases, the ones hard to reason about on paper: the happy path, a tricky
edge case, an attempt at something that should be illegal.

Keep it restrained: default marimo styling, one accent at most. Nothing that competes with the state and the buttons.

### 4. Hand it over

Run `uvx marimo check` on it, then either start it for them (`uv run marimo run prototype_<question>.py`) or export a
static copy they can open with no Python at all:

```bash
uv run marimo export html-wasm prototype_<question>.py -o prototype_<question>/ --mode run
```

They'll click through the walkthroughs and free-play whenever they get to it; the interesting moments are when they say
"wait, that shouldn't be possible" or "huh, I assumed X would be different"; those are the bugs in the _idea_, which is
the whole point. If they want new actions or a new scenario, add them. Prototypes evolve.

### 5. Capture the answer and the prototype

Once the prototype has answered its question, capture the answer, then capture the prototype the way the
[SKILL](../SKILL.md) describes. The logic-specific mapping: the validated reducer / machine / function set lifts into
the real module (the decision, absorbed); the notebook rides along to the throwaway branch that keeps the prototype as a
primary source, and being one self-contained file with inline dependencies, it stays trivially re-runnable there.

## Anti-patterns

- **Don't add tests.** A prototype that needs tests is no longer a prototype.
- **Don't wire it to the real database.** Use in-memory state unless the question is specifically about persistence.
- **Don't generalize.** No "what if we wanted to support X later." The prototype answers one question.
- **Don't blur the logic and the UI together.** If the logic function touches `mo`, UI elements, or callbacks, it's no
  longer liftable. Keep the notebook as a thin shell over pure definitions.
- **Don't reach for a web framework or a server you have to deploy.** The notebook is the app; `marimo run` or a WASM
  export is the whole delivery story.
- **Don't ship the notebook into production.** It is optimized for being clicked through by hand. The logic behind it
  is the bit worth keeping.
