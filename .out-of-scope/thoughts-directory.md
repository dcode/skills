# A `thoughts/` directory for skill artifacts

Skills do not write specs, tickets, research, or rejected requests under a `thoughts/` directory in the target repo.

## Why this is out of scope

An earlier version of these skills kept everything under `thoughts/`. It was replaced by the layout the upstream skills
use, so that artifacts land where people and other tools already look:

- specs and issues in `.scratch/<feature>/` (`spec.md`, `issues/<NN>-<slug>.md` as TaskNotes)
- research notes in `.scratch/research/`
- `GLOSSARY.md` (or `GLOSSARY-MAP.md`) at the repo root, ADRs in `docs/adr/`
- rejected feature requests in `.out-of-scope/`
- per-repo skill configuration in `docs/agents/`

One shared layout also keeps skills adapted from elsewhere close to their source, which makes future updates cheap.

## Prior requests

- Moved off `thoughts/` during the Agent Skills spec migration (November 2026).
