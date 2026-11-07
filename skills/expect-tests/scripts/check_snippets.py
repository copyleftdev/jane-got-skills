"""Fail unless every ```ocaml block in SKILL.md appears verbatim (modulo whitespace) in examples/.

usage: python3 -I check_snippets.py <SKILL.md> <examples_dir>
A snippet that only lives in prose can drift from what compiles; this keeps them the same text.
"""

import pathlib
import re
import sys


def squash(s):
    return re.sub(r"\s+", " ", s).strip()


def main(skill, examples):
    blocks = re.findall(r"```ocaml\n(.*?)```", pathlib.Path(skill).read_text(), re.S)
    sources = squash(" ".join(p.read_text() for p in sorted(pathlib.Path(examples).rglob("*.ml*"))
                               if "_build" not in p.parts))
    missing = [b for b in blocks if squash(b) not in sources]
    for b in missing:
        print("NOT IN examples/:\n" + b)
    print(f"{len(blocks)} ocaml blocks checked, {len(missing)} not found in {examples}")
    return 1 if missing or not blocks else 0


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:3]) if len(sys.argv) == 3 else (print(__doc__.strip()) or 2))
