#!/usr/bin/env bash
# Rebuild the source corpus that verify_quotes.py checks a persona against.
# usage: tools/fetch_corpus.sh <out_dir> <blog-slug>...
# Always includes the Signals and Threads homepage, which embeds every transcript.
set -euo pipefail
out=$1; shift
raw=$(mktemp -d)
mkdir -p "$out"
curl -fsSL -A "Mozilla/5.0 research" -o "$raw/snt.html" https://signalsandthreads.com/
for slug in "$@"; do
  curl -fsSL -A "Mozilla/5.0 research" -o "$raw/$slug.html" "https://blog.janestreet.com/$slug/"
done
python3 -I - "$raw" "$out" <<'PY'
import html, pathlib, re, sys
src, dst = map(pathlib.Path, sys.argv[1:])
for f in src.glob("*.html"):
    t = f.read_text(errors="replace")
    t = re.sub(r"\\u([0-9a-fA-F]{4})", lambda m: chr(int(m.group(1), 16)), t)
    t = t.replace("\\n", " ").replace('\\"', '"')
    t = re.sub(r"(?is)<(script|style)\b.*?</\1>", " ", t) if f.stem != "snt" else t
    t = re.sub(r"(?i)</?(code|a|em|strong|span|i|b|tt)\b[^>]*>", "", t)
    (dst / f"{f.stem}.txt").write_text(html.unescape(re.sub(r"<[^>]+>", " ", t)))
PY
rm -rf "$raw"
