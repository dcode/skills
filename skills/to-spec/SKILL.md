---
name: to-spec
description: Synthesize the current conversation and codebase understanding into a spec (problem, solution, user stories, implementation and testing decisions) and publish it to the project's issue tracker, without interviewing the user. Use when the user wants to turn a discussion into a spec, PRD, or feature write-up, or says "write this up" after a design conversation.
disable-model-invocation: true
---

# To Spec

Turn the current conversation and codebase understanding into a spec. Synthesize what you already know; skip the
interview (use the `grilling` skill first if the design is still open).

Read `docs/agents/issue-tracker.md` and `docs/agents/triage-labels.md` for where specs are published and which labels to
use. If they do not exist, tell the user to run the `setup-skills` skill first.

## Process

1. Explore the repo to understand the current state of the codebase, if you haven't already. Use the project's domain
   glossary vocabulary throughout the spec, and respect any ADRs in the area you're touching.

2. Sketch out the seams at which you're going to test the feature. Existing seams should be preferred to new ones. Use
   the highest seam possible. If new seams are needed, propose them at the highest point you can. The fewer seams across
   the codebase, the better - the ideal number is one.

   Check with the user that these seams match their expectations before writing.

3. Write the spec using the template below, then publish it to the project issue tracker. Apply the `ready-for-agent`
   triage label; no further triage is needed.

<spec-template>

## Problem Statement

The problem that the user is facing, from the user's perspective.

## Solution

The solution to the problem, from the user's perspective.

## User Stories

A LONG, numbered list of user stories. Each user story should be in the format of:

1. As an <actor>, I want a <feature>, so that <benefit>

<user-story-example>
1. As a mobile bank customer, I want to see balance on my accounts, so that I can make better informed decisions about
   my spending
</user-story-example>

This list of user stories should be extremely extensive and cover all aspects of the feature.

## Implementation Decisions

A list of implementation decisions that were made. This can include:

- The modules that will be built/modified
- The interfaces of those modules that will be modified
- Technical clarifications from the developer
- Architectural decisions
- Schema changes
- API contracts
- Specific interactions

Do NOT include specific file paths or code snippets. They may end up being outdated very quickly.

Exception: if a prototype produced a snippet that encodes a decision more precisely than prose can (state machine,
reducer, schema, type shape), inline it within the relevant decision and note briefly that it came from a prototype.
Trim to the decision-rich parts, not a working demo, just the important bits.

## Testing Decisions

A list of testing decisions that were made. Include:

- A description of what makes a good test (only test external behavior, not implementation details)
- Which modules will be tested
- Prior art for the tests (i.e. similar types of tests in the codebase)

## Out of Scope

A description of the things that are out of scope for this spec.

## Further Notes

Any further notes about the feature.

</spec-template>
