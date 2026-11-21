#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml>=6"]
# ///
"""Validate every skill under a directory against the Agent Skills spec and this repo's conventions.

Checks, per skill directory:
  - SKILL.md exists and starts with YAML frontmatter that parses
  - only spec keys (plus this repo's one exception, disable-model-invocation)
  - name: 1-64 chars of a-z0-9 and single hyphens, equal to the directory name
  - description: 1-1024 chars; compatibility: at most 500 chars
  - SKILL.md body under 500 lines
  - every relative Markdown link in the skill's .md files resolves (links inside code are ignored)

Usage: uv run scripts/validate_skills.py [SKILLS_DIR]   (default: skills)
Exit status is 1 if any skill fails.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

SPEC_KEYS = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
REPO_EXCEPTIONS = {"disable-model-invocation"}
NAME_RE = re.compile(r"[a-z0-9]+(-[a-z0-9]+)*")
FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n", re.S)
FENCE_RE = re.compile(r"^\s*(`{3,}|~{3,})")
INLINE_CODE_RE = re.compile(r"`+[^`]*`+")
LINK_RE = re.compile(r"\]\(([^)\s#]+)(?:#[^)]*)?\)")
MAX_BODY_LINES = 500


def prose_lines(text: str) -> list[str]:
    """Return the lines outside fenced code blocks, with inline code removed."""
    out: list[str] = []
    fence: str | None = None
    for line in text.splitlines():
        match = FENCE_RE.match(line)
        if fence is None and match:
            fence = match.group(1)
            continue
        if fence is not None:
            if line.strip().startswith(fence[0] * len(fence)) and not line.strip().strip(fence[0]):
                fence = None
            continue
        out.append(INLINE_CODE_RE.sub("", line))
    return out


def broken_links(md_file: Path) -> list[str]:
    errors = []
    for line in prose_lines(md_file.read_text(encoding="utf-8")):
        for target in LINK_RE.findall(line):
            if re.match(r"^[a-z][a-z0-9+.-]*:", target) or target.startswith("<"):
                continue  # URL schemes (http:, mailto:) and placeholders
            if not (md_file.parent / target).exists():
                errors.append(f"broken link in {md_file.name}: {target}")
    return errors


def check_skill(skill_dir: Path) -> list[str]:
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        return ["missing SKILL.md"]
    text = skill_md.read_text(encoding="utf-8")
    match = FRONTMATTER_RE.match(text)
    if not match:
        return ["SKILL.md does not start with --- frontmatter ---"]
    try:
        meta = yaml.safe_load(match.group(1))
    except yaml.YAMLError as exc:
        return [f"frontmatter is not valid YAML: {exc}".replace("\n", " ")]
    if not isinstance(meta, dict):
        return ["frontmatter is not a mapping"]

    errors: list[str] = []
    unexpected = set(meta) - SPEC_KEYS - REPO_EXCEPTIONS
    if unexpected:
        errors.append(f"unexpected frontmatter keys: {sorted(unexpected)}")

    name = meta.get("name")
    if not isinstance(name, str) or not NAME_RE.fullmatch(name) or len(name) > 64:
        errors.append(f"invalid name: {name!r}")
    elif name != skill_dir.name:
        errors.append(f"name {name!r} does not match directory {skill_dir.name!r}")

    description = meta.get("description")
    if not isinstance(description, str) or not 0 < len(description) <= 1024:
        errors.append("description must be a 1-1024 character string")

    compatibility = meta.get("compatibility")
    if compatibility is not None and (not isinstance(compatibility, str) or len(compatibility) > 500):
        errors.append("compatibility must be a string of at most 500 characters")

    body_lines = text[match.end() :].count("\n")
    if body_lines > MAX_BODY_LINES:
        errors.append(f"SKILL.md body is {body_lines} lines (limit {MAX_BODY_LINES})")

    for md_file in sorted(skill_dir.rglob("*.md")):
        if "templates" in md_file.relative_to(skill_dir).parts:
            continue  # scaffold templates link to files that exist only once rendered
        errors.extend(broken_links(md_file))
    return errors


def main(argv: list[str]) -> int:
    root = Path(argv[1] if len(argv) > 1 else "skills")
    if not root.is_dir():
        print(f"error: {root} is not a directory", file=sys.stderr)
        return 2
    failed = 0
    for skill_dir in sorted(p for p in root.iterdir() if p.is_dir() and not p.name.startswith(".")):
        errors = check_skill(skill_dir)
        if errors:
            failed += 1
            for error in errors:
                print(f"{skill_dir.name}: {error}", file=sys.stderr)
    total = sum(1 for p in root.iterdir() if p.is_dir() and not p.name.startswith("."))
    print(f"{total - failed}/{total} skills valid")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
