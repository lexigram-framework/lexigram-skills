"""
prepare-skills.py — Validate and prepare lexigram skills for publishing.

Usage:
    python scripts/prepare-skills.py

Checks:
  - Every skill has valid YAML frontmatter with name + description
  - Description starts with "Use when"
  - Name uses only lowercase letters, numbers, and hyphens
  - Word count under 500 (warning only)
  - No duplicate skill names
  - All SKILL.md files exist in expected locations

Exits with code 0 on success, 1 on failure.
"""

import os
import re
import sys
from pathlib import Path

SKILLS_DIR = Path(__file__).parent.parent


def get_skills() -> list[Path]:
    """Return paths to all SKILL.md files."""
    return sorted(SKILLS_DIR.glob("*/SKILL.md"))


def parse_frontmatter(content: str):
    """Extract YAML frontmatter fields from markdown content."""
    match = re.match(r"^---\n(.+?)\n---", content, re.DOTALL)
    if not match:
        return {}
    fm = {}
    for line in match.group(1).split("\n"):
        colon = line.find(":")
        if colon > 0:
            key = line[:colon].strip()
            value = line[colon + 1 :].strip().strip('"').strip("'")
            fm[key] = value
    return fm


def validate() -> int:
    errors = 0
    warnings = 0
    seen_names: set[str] = set()
    skills = get_skills()

    if not skills:
        print("  ✗ No SKILL.md files found")
        return 1

    for skill_path in skills:
        name = skill_path.parent.name
        content = skill_path.read_text()
        fm = parse_frontmatter(content)

        # Check frontmatter exists
        if not fm:
            print(f"  ✗ {name}: MISSING frontmatter")
            errors += 1
            continue

        # Check required fields
        skill_name = fm.get("name", "")
        description = fm.get("description", "")

        if not skill_name:
            print(f"  ✗ {name}: MISSING 'name' in frontmatter")
            errors += 1
        elif skill_name != name:
            print(f"  ✗ {name}: directory name '{name}' != frontmatter name '{skill_name}'")
            errors += 1
        elif skill_name in seen_names:
            print(f"  ✗ {name}: DUPLICATE name '{skill_name}'")
            errors += 1
        else:
            seen_names.add(skill_name)
            if not re.match(r"^[a-z0-9-]+$", skill_name):
                print(f"  ✗ {name}: name contains invalid characters (lowercase + hyphens only)")
                errors += 1

        if not description:
            print(f"  ✗ {name}: MISSING 'description' in frontmatter")
            errors += 1
        elif not description.startswith("Use when"):
            print(f"  ⚠ {name}: description should start with 'Use when'")
            warnings += 1

        # Word count
        body = re.sub(r"^---\n.*?\n---\n*", "", content, flags=re.DOTALL)
        word_count = len(body.split())
        if word_count > 500:
            print(f"  ⚠ {name}: {word_count} words (recommend <500)")
            warnings += 1

        print(f"  ✓ {name:40s} ({word_count:3d} words)")

    # Summary
    total = len(skills)
    print(f"\n  {'─' * 50}")
    print(f"  Skills:     {total}")
    print(f"  Errors:     {errors}")
    print(f"  Warnings:   {warnings}")
    return errors


if __name__ == "__main__":
    print("=== Preparing lexigram skills for publish ===\n")
    rc = validate()
    print(f"\n{'PASS' if rc == 0 else 'FAIL'}")
    sys.exit(rc)
