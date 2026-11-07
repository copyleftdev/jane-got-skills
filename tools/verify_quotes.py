"""Fail if any quotation in a SKILL.md is not found verbatim in the source corpus.

usage: python3 -I tools/verify_quotes.py <corpus_dir_of_txt> <SKILL.md>
Quotes are double-quoted runs on one line, outside code fences. "..." splits a
quote into fragments that must each appear. Bracketed insertions are not
tolerated: rewrite them as fragments or accept the reported miss deliberately.
"""
import glob
import re
import sys


def norm(s):
    for a, b in (("’", "'"), ("‘", "'"), ("“", '"'), ("”", '"'), ("…", "...")):
        s = s.replace(a, b)
    return re.sub(r"\s+", " ", s).strip().lower()


corpus = norm(" ".join(open(f, errors="replace").read() for f in glob.glob(sys.argv[1] + "/*.txt")))
quotes, fenced = [], False
for line in open(sys.argv[2]):
    if line.startswith("```"):
        fenced = not fenced
        continue
    if not fenced:
        quotes += [q for q in re.findall(r'"([^"\n]*)"', line) if len(q) >= 25]

missing = [q for q in quotes
           if not all(p in corpus for p in (x.strip(" .,") for x in norm(re.sub(r"\[[^\]]*\]", "...", q)).split("...")) if p)]
for q in missing:
    print("MISSING:", q)
print(f"{len(quotes)} quotes checked, {len(missing)} missing")
sys.exit(1 if missing else 0)
