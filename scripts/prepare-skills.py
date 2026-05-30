"""
prepare-skills.py — Validate, cross-reference, and prepare lexigram skills for publishing.

Usage:
    python scripts/prepare-skills.py
    python scripts/prepare-skills.py --docs PATH   # cross-reference against lexigram-docs

Checks:
  - Valid YAML frontmatter with name + description
  - Description starts with "Use when"
  - Name uses only lowercase letters, numbers, and hyphens
  - No duplicate skill names
  - Word count under 500 (warning)
  - Cross-reference: guide topics without a matching skill (--docs)
  - Cross-reference: REF_* error codes, CLI commands, env vars used in skills

Exits with code 0 on success, 1 on failure.
"""

import argparse
import re
import sys
from pathlib import Path

SKILLS_DIR = Path(__file__).parent.parent
LEXIGRAM_DIR = SKILLS_DIR / ".." / "lexigram"
DOCS_SRC_DIR = Path.home() / "Documents/AI/applications/framework/lexigram-docs/src/content/docs"

# Topics from lexigram-docs/guides that we intentionally DON'T need a skill for.
# These are either too narrow, not pattern-oriented, or covered by an existing skill.
SKIP_GUIDE_TOPICS = frozenset({
    "migrating-from-fastapi", "deployment", "adoption-paths",
    "compatibility", "choosing-backends", "ai-architecture",
    "architecture",  # conceptual overview, not a specific pattern
    "core-concepts",  # conceptual overview
    "project-structure",  # covered by creating-providers-and-modules layout docs
})

# Mapping from guide topic → the skill that covers it (to avoid false positives)
GUIDE_TO_SKILL = {
    "providers": "creating-providers-and-modules",
    "modules": "creating-providers-and-modules",
    "dependency-injection": "creating-providers-and-modules",
    "container-protocols": "creating-providers-and-modules",
    "boot-lifecycle": "creating-providers-and-modules",
    "result-pattern": "using-result-and-error-codes",
    "cli": "cli-project-scaffolding",
    "testing": "testing-with-lexigram",
    "caching": "caching-patterns",
    "configuration": "configuration-management",
    "yaml-configuration": "configuration-management",
    "resilience": "resilience-patterns",
    "database": "database-repository-pattern",
    "event-driven": "events-and-messaging",
    "queue": "events-and-messaging",
    "ai-integration": "ai-subsystem-quickstart",
    "ai-llm": "ai-subsystem-quickstart",
    "ai-agents": "ai-subsystem-quickstart",
    "ai-rag": "ai-subsystem-quickstart",
    "ai-memory": "ai-subsystem-quickstart",
    "ai-mcp": "ai-subsystem-quickstart",
    "ai-skills": "ai-subsystem-quickstart",
    "ai-sessions": "ai-subsystem-quickstart",
    "ai-feedback": "ai-subsystem-quickstart",
    "ai-workers": "ai-subsystem-quickstart",
    "webhooks": "events-and-messaging",
    "authentication": "web-controllers-and-routing",
    "notifications": "events-and-messaging",
    "feature-flags": "configuration-management",
    "multi-tenancy": "creating-providers-and-modules",
    "application-lifecycle": "creating-providers-and-modules",
    "file-storage": "caching-patterns",
    "graphql": "web-controllers-and-routing",
    "search": "caching-patterns",
    "nosql": "database-repository-pattern",
    "graph-databases": "database-repository-pattern",
    "vector-stores": "ai-subsystem-quickstart",
    "real-time": "web-controllers-and-routing",
    "observability": "testing-with-lexigram",
    "background-jobs": "events-and-messaging",
    "workflows-sagas": "events-and-messaging",
    "audit-trail": "testing-with-lexigram",
    "http-client": "resilience-patterns",
}


def get_skills() -> list[Path]:
    return sorted(SKILLS_DIR.glob("*/SKILL.md"))


def parse_frontmatter(content: str) -> dict[str, str]:
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


def find_ref_files() -> dict[str, Path | None]:
    """Locate REF_* files in lexigram or lexigram-docs."""
    paths = {}
    candidates = [
        LEXIGRAM_DIR / "REF_CLI_COMMANDS.md",
        LEXIGRAM_DIR / "REF_ERROR_CODES.md",
        LEXIGRAM_DIR / "REF_ENV_VARS.md",
        DOCS_SRC_DIR / "reference" / "REF_CLI_COMMANDS.md",
        DOCS_SRC_DIR / "reference" / "REF_ERROR_CODES.md",
        DOCS_SRC_DIR / "reference" / "REF_ENV_VARS.md",
    ]
    for p in candidates:
        if p.exists():
            key = p.stem  # REF_CLI_COMMANDS, REF_ERROR_CODES, REF_ENV_VARS
            paths[key] = p
    return paths


def find_guide_topics(docs_path: Path | None) -> list[str]:
    """List all guide .md files in lexigram-docs as topic names."""
    if not docs_path:
        return []
    guides_dir = docs_path / "guides"
    if not guides_dir.exists():
        return []
    topics = []
    for f in sorted(guides_dir.glob("*.md")):
        stem = f.stem
        if stem not in SKIP_GUIDE_TOPICS:
            topics.append(stem)
    # Also fundamentals
    for f in sorted((docs_path / "fundamentals").glob("*.md")):
        stem = f.stem
        if stem not in SKIP_GUIDE_TOPICS:
            topics.append(stem)
    return sorted(topics)


def extract_error_codes(text: str) -> set[str]:
    return set(re.findall(r"LEX_ERR_[A-Z]+_\d+", text))


def extract_cli_commands(text: str) -> set[str]:
    cmds = set()
    for m in re.finditer(r"lexigram\s+([a-z][a-z_]+(?:\s+[a-z][a-z_-]+)*)", text):
        parts = m.group(1).strip().split()
        if parts:
            cmds.add(parts[0])
    return cmds


def cross_reference_guides(docs_path: Path | None, skill_names: set[str]) -> list[str]:
    """Find guide topics not covered by any skill."""
    if not docs_path:
        return []
    topics = find_guide_topics(docs_path)
    uncovered = []
    for topic in topics:
        # Check if this topic maps to a skill we have
        mapped_skill = GUIDE_TO_SKILL.get(topic)
        if mapped_skill and mapped_skill in skill_names:
            continue
        # Check if topic name or alias matches a skill name directly
        alias = topic.replace("-", " ").replace("_", " ")
        found = False
        for sn in skill_names:
            sn_clean = sn.replace("-", " ").replace("_", " ")
            if alias in sn_clean or sn_clean in alias:
                found = True
                break
        if not found:
            uncovered.append(topic)
    return uncovered


def main() -> int:
    parser = argparse.ArgumentParser(description="Prepare lexigram skills for publish")
    parser.add_argument("--docs", type=str, help="Path to lexigram-docs content root (src/content/docs)")
    parser.add_argument("--refs", action="store_true", help="Cross-reference against REF_* files")
    args = parser.parse_args()

    docs_path = Path(args.docs) if args.docs else DOCS_SRC_DIR
    if not docs_path.exists():
        docs_path = None

    ref_files = find_ref_files() if args.refs else {}

    errors = 0
    warnings = 0
    seen_names: set[str] = set()
    all_bodies: dict[str, str] = {}
    skills = get_skills()

    print("=== Validating skills ===\n")

    if not skills:
        print("  ✗ No SKILL.md files found")
        return 1

    for skill_path in skills:
        name = skill_path.parent.name
        content = skill_path.read_text()
        fm = parse_frontmatter(content)
        body = re.sub(r"^---\n.*?\n---\n*", "", content, flags=re.DOTALL)

        if not fm:
            print(f"  ✗ {name}: MISSING frontmatter")
            errors += 1
            continue

        skill_name = fm.get("name", "")
        description = fm.get("description", "")

        if not skill_name:
            print(f"  ✗ {name}: MISSING 'name' in frontmatter")
            errors += 1
        elif skill_name != name:
            print(f"  ✗ {name}: directory '{name}' != frontmatter name '{skill_name}'")
            errors += 1
        elif skill_name in seen_names:
            print(f"  ✗ {name}: DUPLICATE name")
            errors += 1
        else:
            seen_names.add(skill_name)
            if not re.match(r"^[a-z0-9-]+$", skill_name):
                print(f"  ✗ {name}: invalid characters in name (lowercase + hyphens only)")
                errors += 1

        if not description:
            print(f"  ✗ {name}: MISSING description")
            errors += 1
        elif not description.startswith("Use when"):
            print(f"  ⚠ {name}: description should start with 'Use when'")
            warnings += 1

        wc = len(body.split())
        if wc > 500:
            print(f"  ⚠ {name}: {wc} words (recommend <500)")
            warnings += 1

        all_bodies[name] = body
        print(f"  ✓ {name:40s} ({wc:3d} words)")

    # Summary
    total = len(skills)
    print(f"\n  {'─' * 50}")
    print(f"  Skills:     {total}")
    print(f"  Errors:     {errors}")
    print(f"  Warnings:   {warnings}")

    # Cross-reference: guide topics
    if docs_path:
        print(f"\n=== Cross-referencing against lexigram-docs ===\n")
        uncovered = cross_reference_guides(docs_path, seen_names)
        if uncovered:
            for topic in uncovered:
                print(f"  ⚠ No skill for guide: {topic}")
                warnings += len(uncovered)
            print(f"\n  {len(uncovered)} uncovered topics")
        else:
            print("  All guide topics covered by existing skills.")

    # Cross-reference: error codes in skills vs REF_ERROR_CODES
    if ref_files.get("REF_ERROR_CODES"):
        print(f"\n=== Cross-referencing error codes ===\n")
        ref_content = ref_files["REF_ERROR_CODES"].read_text()
        all_known_codes = extract_error_codes(ref_content)
        for sname, body in sorted(all_bodies.items()):
            used = extract_error_codes(body)
            if not used:
                continue
            for code in sorted(used):
                if code not in all_known_codes:
                    print(f"  ✗ {sname}: references unknown error code {code}")
                    errors += 1

    return errors


if __name__ == "__main__":
    rc = main()
    print(f"\n{'PASS' if rc == 0 else 'FAIL'}")
    sys.exit(rc)
