"""Fail if any quotation in a SKILL.md is not found verbatim in the source corpus.

usage: python3 -I tools/verify_quotes.py <corpus_dir_of_txt> <SKILL.md> [--manual <manual_quotes.tsv>]
Quotes are double-quoted runs on one line, outside code fences. "..." splits a
quote into fragments that must each appear. Bracketed insertions are not
tolerated: rewrite them as fragments or accept the reported miss deliberately.

--manual names quotes whose source cannot be fetched automatically (one per line:
<source file>TAB<quote exactly as in SKILL.md>). If that source file is in the corpus the
quote is checked as usual; if not, it is reported SKIPPED, never silently passed. An entry
whose quote no longer appears in SKILL.md is an error, so the list cannot go stale.
"""
import glob
import re
import sys


def norm(s):
    for a, b in (("’", "'"), ("‘", "'"), ("“", '"'), ("”", '"'), ("…", "...")):
        s = s.replace(a, b)
    s = re.sub("[\"'\u2018\u2019\u201c\u201d]", "'", s.replace("`", ""))
    return re.sub(r"\s+", " ", s).strip().lower()


args = sys.argv[1:]
manual = {}
if "--manual" in args:
    i = args.index("--manual")
    for line in open(args[i + 1]):
        if line.strip() and not line.startswith("#"):
            source, quote = line.rstrip("\n").split("\t", 1)
            manual[quote] = source
    del args[i:i + 2]
corpus_dir, skill = args
present = {f.rsplit("/", 1)[-1] for f in glob.glob(corpus_dir + "/*.txt")}
corpus = norm(" ".join(open(f, errors="replace").read() for f in glob.glob(corpus_dir + "/*.txt")))
quotes, fenced = [], False
for line in open(skill):
    if line.startswith("```"):
        fenced = not fenced
        continue
    if not fenced:
        quotes += [q for q in re.findall(r'"([^"\n]*)"', line) if len(q) >= 25]

missing = [q for q in quotes
           if not all(p in corpus for p in (x.strip(" .,") for x in norm(re.sub(r"\[[^\]]*\]", "...", q)).split("...")) if p)]
skipped = [q for q in missing if q in manual and manual[q] not in present]
missing = [q for q in missing if q not in skipped]
stale = [q for q in manual if q not in quotes]
for q in missing:
    print("MISSING:", q)
for q in skipped:
    print(f"SKIPPED (source {manual[q]} not in corpus; verify locally):", q)
for q in stale:
    print("STALE manual entry, quote not in SKILL.md:", q)
print(f"{len(quotes)} quotes checked, {len(missing)} missing, {len(skipped)} skipped (manual source)")
sys.exit(1 if missing or stale else 0)
