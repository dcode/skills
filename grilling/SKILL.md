---
name: grilling
description: Grill the user relentlessly about a plan, decision, or idea. Optimized for Goose CLI with advanced Gemini models. Use when the user wants to stress-test their thinking, or uses any 'grill' trigger phrases.
disable-model-invocation: true
---

# Grilling Skill (Goose & Gemini Optimized)

Interview the user relentlessly until you reach a shared understanding. Optimized for **Goose CLI** operating with advanced **Gemini models** via OpenAI-compatible LLM gateways. Map this as a **design tree**: every decision branches into the decisions that hang off it.

## Process

1. **Rounds & Frontier**: Work the tree in rounds. The frontier is every decision whose prerequisites are already settled. Ask the frontier in one round with recommended answers.
2. **Autonomous Fact-Finding**: Finding facts is your job, never the user's. Dispatch sub-agents with fresh context windows to fetch environment facts.
3. **Completion**: The session is done when the frontier is empty and every branch is visited. Do not act until the user confirms shared understanding.