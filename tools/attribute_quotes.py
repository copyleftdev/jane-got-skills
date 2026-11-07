"""List, for every quotation in a SKILL.md, the corpus file it came from and, for podcast
transcripts (files named snt__<slug>.txt), the speaker whose turn contains it.

usage: python3 -I tools/attribute_quotes.py <corpus_dir> <SKILL.md>
Read the table against the attributions in the skill; this reports, it does not judge.
"""
import glob
import os
import re
import sys

TURN = re.compile(r"(\d{1,2}:\d{2}(?::\d{2})?(?:\.\d+)?) ([a-z]+) ")


def norm(s):
    s = re.sub("[\"'‘’“”]", "'", s.replace("`", "").replace("…", "..."))
    return re.sub(r"\s+", " ", s).strip().lower()


def speaker(text, frag):
    head = text[: text.find(frag)]
    turns = list(TURN.finditer(head))
    return f"{turns[-1].group(2)}@{turns[-1].group(1)}" if turns else "-"


corpus = {os.path.basename(f)[:-4]: norm(open(f, errors="replace").read())
          for f in glob.glob(os.path.join(sys.argv[1], "*.txt"))}
fenced = False
for line in open(sys.argv[2]):
    if line.startswith("```"):
        fenced = not fenced
        continue
    if fenced:
        continue
    for q in (q for q in re.findall(r'"([^"\n]*)"', line) if len(q) >= 25):
        parts = [p.strip(" .,") for p in norm(re.sub(r"\[[^\]]*\]", "...", q)).split("...") if p.strip(" .,")]
        src = [k for k, v in corpus.items() if parts and parts[0] in v]
        who = [speaker(corpus[k], parts[0]) if k.startswith("snt__") else "text" for k in src]
        print(f"{','.join(src) or 'NOT FOUND':40} | {','.join(who):18} | {q[:70]}")
