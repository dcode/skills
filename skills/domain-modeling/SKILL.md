---
name: domain-modeling
description: Build and sharpen a project's domain model by challenging terminology, probing edge cases, and recording settled terms in GLOSSARY.md and decisions as ADRs. Use when pinning down domain language or a ubiquitous language, resolving what a term means, writing or editing GLOSSARY.md, or recording or editing an architectural decision record.
---

# Domain Modeling

Actively build and sharpen the project's domain model as you design: challenge terms, invent edge-case scenarios, and
write the glossary and decisions down the moment they crystallize. Merely *reading* `GLOSSARY.md` for vocabulary is a
one-line habit any skill can do; this skill is for *changing* the model.

## File structure

Most repos have a single context:

```text
/
├── GLOSSARY.md
├── docs/
│   └── adr/
│       ├── 0001-event-sourced-orders.md
│       └── 0002-postgres-for-write-model.md
└── src/
```

If a `GLOSSARY-MAP.md` exists at the root, the repo has multiple contexts. The map points to where each one lives:

```text
/
├── GLOSSARY-MAP.md
├── docs/
│   └── adr/                          ← system-wide decisions
├── src/
│   ├── ordering/
│   │   ├── GLOSSARY.md
│   │   └── docs/adr/                 ← context-specific decisions
│   └── billing/
│       ├── GLOSSARY.md
│       └── docs/adr/
```

Create files lazily: a `GLOSSARY.md` when the first term is resolved, `docs/adr/` when the first ADR is needed.

## During the session

### Challenge against the glossary

When the user uses a term that conflicts with the existing language in `GLOSSARY.md`, call it out immediately: "Your
glossary defines 'cancellation' as X, but you seem to mean Y. Which is it?"

### Sharpen fuzzy language

When the user uses vague or overloaded terms, propose a precise canonical term: "You're saying 'account': do you mean
the Customer or the User? Those are different things."

### Discuss concrete scenarios

Stress-test domain relationships with specific scenarios. Invent ones that probe edge cases and force precision about
the boundaries between concepts.

### Cross-reference with code

When the user states how something works, check whether the code agrees. Surface contradictions: "Your code cancels
entire Orders, but you just said partial cancellation is possible. Which is right?"

### Update GLOSSARY.md inline

When a term is resolved, update `GLOSSARY.md` right then; capture each term as it happens. Before the first write in a
session, read [references/GLOSSARY-FORMAT.md](references/GLOSSARY-FORMAT.md) for the entry format and the single- vs
multi-context rules.

`GLOSSARY.md` holds definitions only: keep implementation details, specs, and scratch notes elsewhere.

### Offer ADRs sparingly

Offer an ADR only when all three are true:

1. **Hard to reverse**: changing your mind later has a meaningful cost
2. **Surprising without context**: a future reader will wonder "why did they do it this way?"
3. **The result of a real trade-off**: there were genuine alternatives and you picked one for specific reasons

If any is missing, skip the ADR. When writing one, read [references/ADR-FORMAT.md](references/ADR-FORMAT.md) for the
template and numbering.
