"""Fail unless every ```ocaml block in a SKILL.md appears verbatim (modulo whitespace) in a compiled project.

usage: python3 -I tools/check_snippets.py <SKILL.md> <examples_dir>
A snippet that only lives in prose can drift from what compiles; this keeps them the same text.
A block preceded by `<!-- snippet: uncompiled <reason> -->` is skipped and reported, never silently.
"""

import pathlib
import re
import sys

BLOCK = re.compile(r"(<!-- snippet: uncompiled ([^>]*?) -->\s*)?```ocaml\n(.*?)```", re.S)


def squash(s):
    return re.sub(r"\s+", " ", s).strip()


def main(skill, examples):
    sources = squash(" ".join(p.read_text() for p in sorted(pathlib.Path(examples).rglob("*.ml*"))
                               if "_build" not in p.parts))
    checked, skipped, missing = 0, [], []
    for m in BLOCK.finditer(pathlib.Path(skill).read_text()):
        if m.group(1):
            skipped.append(m.group(2))
            continue
        checked += 1
        if squash(m.group(3)) not in sources:
            missing.append(m.group(3))
    for b in missing:
        print("NOT IN examples/:\n" + b)
    for reason in skipped:
        print("skipped (uncompiled):", reason)
    print(f"{checked} ocaml blocks checked, {len(missing)} not found in {examples}, {len(skipped)} marked uncompiled")
    return 1 if missing or not checked else 0


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:3]) if len(sys.argv) == 3 else (print(__doc__.strip()) or 2))
