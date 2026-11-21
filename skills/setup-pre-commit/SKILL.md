---
name: setup-pre-commit
description: Set up the Python pre-commit framework (.pre-commit-config.yaml) with hooks tailored to what the repo contains, covering Python (uv, hatch, ruff, pytest, ty), Terraform, Ansible (ansible-lint, molecule), Markdown (rumdl), TOML (taplo), and shell scripts (shellcheck). Use when the user wants pre-commit hooks, git hooks, commit-time linting or formatting, or asks to add or fix a .pre-commit-config.yaml.
compatibility: Requires git, Python with uv (or pip), and network access to fetch hook repositories.
disable-model-invocation: true
---

# Setup Pre-Commit Hooks

Set up the Python `pre-commit` framework in the current repository, with hooks matched to the stacks actually present.

## Tool stack

- **Python**: `uv` for environments, `hatch` builds, `pytest` tests, `ty` type checking (fall back to `mypy`/pyright),
  `ruff` lint + format.
- **Markdown**: `rumdl` check + fmt.
- **TOML**: `taplo` format + lint.
- **Shell**: `shellcheck`.
- **Terraform**: `terraform fmt`, `terraform validate`, native `terraform test`.
- **Ansible**: `ansible-lint`, `molecule`.

## Steps

1. **Detect components.** Enable a stack only when its signal is present:
   - Python: `pyproject.toml`, `uv.lock`, `requirements.txt`, or `.py` files.
   - Terraform: `.tf` files or a `terraform/` directory.
   - Ansible: `playbooks/`, `roles/`, `ansible.cfg`, or `molecule/`.
   - Markdown: `.md` files or `docs/`.
   - TOML: `.toml` files (always true when Python is).
   - Shell: `.sh`/`.bash` files or scripts with a `bash`/`sh` shebang.

2. **Write the config.** Start from [assets/pre-commit-config.yaml](assets/pre-commit-config.yaml). Delete the blocks
   for stacks not detected in step 1. If `.pre-commit-config.yaml` already exists, merge into it rather than
   overwriting.

3. **Install the framework and hooks.**

   ```bash
   uv tool install pre-commit   # or: pip install pre-commit
   pre-commit autoupdate
   pre-commit install
   ```

4. **Verify.** Run `pre-commit run --all-files`. Fix config errors and re-run until every hook passes or only reports
   genuine findings in the user's code. Report those findings; leave fixing them to the user unless asked.

5. **Commit.** Stage `.pre-commit-config.yaml` and any related config, then commit:
   `chore: set up pre-commit hooks for <detected stacks>`

## Gotchas

- The `rev:` pins in the template age quickly. Always run `pre-commit autoupdate` before the first `run`; never
  hand-edit a pin to a version you have not seen in the hook repo's tags.
- Auto-fixing hooks (`ruff-check --fix`, `rumdl-fmt`, `taplo-format`, `end-of-file-fixer`, `trailing-whitespace`) modify
  files and report failure on the first run. Run a second time before concluding a hook is broken.
- `terraform_validate` needs `terraform init` to have run in each module directory; if it fails on missing providers,
  init first.
- `ansible-lint` needs the project's collections installed (`ansible-galaxy install -r requirements.yml`) or it reports
  spurious errors.
- The `ty` hook is a local `uv run ty check`, so it needs `ty` in the project's dev dependencies (`uv add --dev ty`).
- The rumdl hooks live in `rvben/rumdl-pre-commit`, not the main `rvben/rumdl` repo.
