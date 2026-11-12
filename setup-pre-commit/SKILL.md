---
name: setup-pre-commit
description: Set up Python pre-commit framework hooks, tailored for repos containing Python (uv, hatch, pytest, ty type checking), Terraform (native tests), Ansible (molecule), and Markdown docs (rumdl).
disable-model-invocation: true
---

# Setup Pre-Commit Hooks (Python Framework & Multi-Tool Edition)

Set up the **Python pre-commit framework** (`pre-commit`) in the current repository, adapted for our standard multi-tool tech stacks: **Python**, **Terraform**, **Ansible**, and **Markdown docs**.

## Preferences & Tool Stack

- **Framework**: Python `pre-commit` (`.pre-commit-config.yaml`)
- **Python**: Managed with `uv`, builds with `hatch`, unit testing with `pytest`, type checking with `ty` (or standard `mypy`/pyright fallback), formatting/linting via ruff/black as appropriate.
- **Markdown Docs**: `rumdl` (or standard markdownlint/prettier).
- **Terraform**: Native terraform validation, formatting (`terraform fmt`), and native terraform testing (`test`).
- **Ansible**: Linting via `ansible-lint`, testing via `molecule`.

---

## Steps

### 1. Detect Repository Components

Inspect the repository structure to determine which hooks to enable:
- **Python**: Presence of `pyproject.toml`, `uv.toml`, `requirements.txt`, or `.py` files. (Check for `hatch` build system, `pytest`, and `ty` type checker).
- **Terraform**: Presence of `.tf` files or `terraform/` directories.
- **Ansible**: Presence of `playbooks/`, `roles/`, `ansible.cfg`, or `molecule/` directories.
- **Markdown Docs**: Presence of `.md` files or `docs/` directories (configure `rumdl`).

### 2. Install & Configure pre-commit

Ensure `pre-commit` is available (via `uv pip install pre-commit` or `pip install pre-commit`).

Create or update `.pre-commit-config.yaml` at the repo root with standard hooks tailored to the detected tech stack:

<pre-commit-template>
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v5.0.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
      - id: check-toml

  # Python / uv / ty / pytest / hatch
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.8.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  # Markdown linting via rumdl (or standard markdown linter)
  - repo: https://github.com/rumdl/rumdl
    rev: v0.1.0 # (or latest stable)
    hooks:
      - id: rumdl

  # Terraform validation & formatting
  - repo: https://github.com/antonbabenko/pre-commit-terraform
    rev: v1.96.2
    hooks:
      - id: terraform_fmt
      - id: terraform_validate

  # Ansible linting
  - repo: https://github.com/ansible/ansible-lint
    rev: v25.1.0
    hooks:
      - id: ansible-lint
</pre-commit-template>

*(Note: Prune or adjust hooks based on what was actually detected in Step 1).*

### 3. Install Git Hooks

Run:
```bash
pre-commit install
```

### 4. Verify & Test

Run pre-commit across all files to verify everything is working smoothly:
```bash
pre-commit run --all-files
```

### 5. Commit

Stage the `.pre-commit-config.yaml` and any related configuration files, then commit with message (adapt as needed):
`chore: set up pre-commit hooks for python, terraform, ansible, and markdown`
