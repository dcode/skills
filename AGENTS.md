# Repository Context: AI Engineering Skills for Goose CLI & Gemini

## Overview
This repository contains a collection of modular engineering skills designed specifically for **Goose CLI** interacting with advanced **Gemini models** via OpenAI-compatible LLM gateways.

## Goals
1. **TaskNotes Integration**: Standardize all task and issue tracking around **TaskNotes** (individual markdown files with YAML frontmatter conforming to the [TaskNotes specification](https://tasknotes.dev/developers/specification/)).
2. **Goose CLI & Gemini Optimization**: Adapt workflow skills, planning instructions, and scaffolding to leverage the capabilities of advanced Gemini models operating within Goose CLI.
3. **Structured Engineering Workflow**: Provide clean, prompt-driven setup and issue-breaking skills (`setup-skills`, `to-tasknotes`) to guide AI agents in breaking plans/specs into verifiable, dependency-ordered vertical slices.

## Key Components & Skills
- **`setup-skills/`**: Scaffolds per-repo configuration, establishing local TaskNotes markdown tracking in `thoughts/`, triage label vocabularies, and domain documentation rules (`GLOSSARY.md`, ADRs).
- **`to-tasknotes/`**: Breaks plans, specs, or conversations into tracer-bullet vertical slices formatted strictly as TaskNotes files (`thoughts/<feature>/issues/<NN>-<slug>.md`) with blocking edges.
