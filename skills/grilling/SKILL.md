---
name: grilling
description: Interview the user relentlessly about a plan, decision, or idea until every branch of the design is settled and both sides share one understanding. Use when the user wants to stress-test their thinking, poke holes in a plan, be asked hard questions before building, or uses any "grill" phrasing.
compatibility: Works best in agents that can dispatch subagents (e.g. Goose CLI) for fact-finding.
---

# Grilling

Interview the user relentlessly until you reach a shared understanding. Map the topic as a **design tree**: every
decision branches into the decisions that hang off it.

## Process

1. **Work the frontier in rounds.** The frontier is every decision whose prerequisites are already settled. Ask the
   whole frontier in one round, each question with your recommended answer, then recompute the frontier from the
   answers.
2. **Find facts yourself.** Anything the environment can answer (code, config, docs, git history) is your job, never the
   user's. Dispatch subagents with fresh context windows to fetch those facts, and ask the user only for decisions and
   intent.
3. **Finish at an empty frontier.** The session is done when every branch is visited and no decision is open. Summarize
   the settled tree and get the user's explicit confirmation before acting on any of it.
