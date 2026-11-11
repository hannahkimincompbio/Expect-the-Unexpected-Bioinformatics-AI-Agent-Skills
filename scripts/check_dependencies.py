#!/usr/bin/env python3
"""check_dependencies.py — validate the `dependencies:` frontmatter of every SKILL.md.

What it does:
  1. Finds every SKILL.md under skills/ in this repo.
  2. Parses the frontmatter and its `dependencies:` list (e.g. [python>=3.7, grounded-citations>=1.4.0]).
  3. Checks each dependency is satisfiable:
     - `python>=X.Y` → the Python running this script must be >= X.Y.
     - `<skill-name>[>=V]` → a sibling skill dir of that name must exist in skills/,
       its SKILL.md `version:` must satisfy >= V when a floor is given.
  4. Errors if a SKILL.md has no `dependencies:` line (header contract of this repo).

Why this is scriptable: frontmatter is a fixed YAML schema, version comparison is a
mechanical tuple comparison, and sibling-skill existence is a filesystem check —
none of it needs judgment. Run: python3 scripts/check_dependencies.py
"""
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO / "skills"

# Matches a dependency spec: optional `>=version` floor after the dependency name.
DEP_RE = re.compile(r"^([A-Za-z0-9_.-]+)(?:>=(\d+(?:\.\d+)*))?$")
# Matches the frontmatter block delimited by `---` lines at the top of the file.
FM_RE = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)
VERSION_RE = re.compile(r"^version:\s*(\d+(?:\.\d+)*)\s*$", re.MULTILINE)


def parse_version(s):
    """Turn '1.4.0' into a comparable tuple (1, 4, 0)."""
    return tuple(int(x) for x in s.split("."))


def check(dep, skills_dir, py_version):
    """Return None if satisfiable, else an error string."""
    m = DEP_RE.match(dep.strip())
    if not m:
        return f"malformed dependency spec {dep!r} (expected name or name>=version)"
    name, floor = m.group(1), m.group(2)
    if name == "python":
        # Python floor is checked against the interpreter running this script.
        if floor and py_version < parse_version(floor):
            return f"python {floor} required, running {sys.version.split()[0]}"
        return None
    # Skill dependency: sibling dir must exist...
    skill_dir = skills_dir / name
    if not (skill_dir / "SKILL.md").is_file():
        return f"skill {name!r} not found under skills/"
    # ...and, when a floor is given, its version must satisfy it.
    if floor:
        ver = VERSION_RE.search((skill_dir / "SKILL.md").read_text(encoding="utf-8"))
        if not ver:
            return f"skill {name!r} has no version: line in frontmatter"
        if parse_version(ver.group(1)) < parse_version(floor):
            return f"skill {name} {ver.group(1)} < required {floor}"
    return None


def main():
    py_version = sys.version_info[:3]
    failures = 0
    for skill_md in sorted(SKILLS_DIR.rglob("SKILL.md")):
        text = skill_md.read_text(encoding="utf-8")
        fm = FM_RE.match(text)
        rel = skill_md.relative_to(REPO)
        if not fm:
            print(f"FAIL {rel}: no frontmatter block")
            failures += 1
            continue
        deps = re.search(r"^dependencies:\s*\[(.*)\]\s*$", fm.group(1), re.MULTILINE)
        if not deps:
            print(f"FAIL {rel}: missing `dependencies:` line in frontmatter")
            failures += 1
            continue
        for dep in deps.group(1).split(","):
            if not dep.strip():
                continue
            err = check(dep, SKILLS_DIR, py_version)
            if err:
                print(f"FAIL {rel}: {err}")
                failures += 1
            else:
                print(f"ok   {rel}: {dep.strip()}")
    if failures:
        print(f"\n{failures} failure(s)")
        return 1
    print("\nall dependencies satisfied")
    return 0


if __name__ == "__main__":
    sys.exit(main())
