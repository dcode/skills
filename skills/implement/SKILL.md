---
name: implement
description: Implement a single piece of work described by a spec or one or more tickets, test-first, then review and commit it. Use when the user hands over a spec or ticket and says to build, implement, or code it in the current session.
disable-model-invocation: true
---

# Implement

Implement the work described in the spec or tickets the user gave you.

1. **Load the work.** If the user passed a ticket reference, fetch it as `docs/agents/issue-tracker.md` describes state
   its title, and claim it as the tracker doc's **Claiming** section describes (if it has one) before starting. If the
   reference is ambiguous, ask.
2. **Build test-first** at the seams agreed in the spec: load the `tdd` skill ([../tdd/SKILL.md](../tdd/SKILL.md)) and
   follow its red → green loop. Refactoring waits for the review in step 4.
3. **Keep the loop tight.** Run the project's static checks (type checker, linter) and the single test file you are
   working in after each change; run the full test suite once at the end. Find the commands in the project's own config
   (`pyproject.toml`, `Makefile`, `justfile`, CI workflows) rather than guessing.
4. **Review.** Load the `code-review` skill ([../code-review/SKILL.md](../code-review/SKILL.md)) against the commit you
   started from, and fix what it finds.
5. **Commit** to the current branch.
