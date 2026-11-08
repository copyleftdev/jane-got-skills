#!/usr/bin/env bash
# Rebuild the source corpus that verify_quotes.py checks a persona against.
# usage: tools/fetch_corpus.sh <out_dir> <source>...
#   source = blog-slug | https-url | https-url::name
# Always includes the Signals and Threads homepage, which embeds every transcript.
# A bare slug is a blog.janestreet.com post; a URL is fetched as is and named by its last path
# segment unless ::name is given. HTML is reduced to text; PDFs go through pdftotext with words
# hyphenated across line breaks rejoined; .md/.mdx/.mli/.ml/.txt are kept as raw text.
set -euo pipefail
out=$1; shift
raw=$(mktemp -d)
trap 'rm -rf "$raw"' EXIT
mkdir -p "$out"
fetch() { curl -fsSL --retry 3 --retry-delay 2 -A "Mozilla/5.0 research" -o "$1" "$2"; }
fetch "$raw/snt.html" https://signalsandthreads.com/
for arg in "$@"; do
  url=${arg%%::*}
  name=$( [[ $arg == *::* ]] && echo "${arg#*::}" || basename "${url%/}" )
  if [[ $url == https://* ]]; then
    case $url in
      *.pdf)
        fetch "$raw/$name" "$url"
        pdftotext "$raw/$name" - | python3 -I -c 'import re,sys; sys.stdout.write(re.sub(r"(\w)-\n(?=[a-z])", r"\1", sys.stdin.read()))' > "$out/${name%.pdf}.txt" ;;
      *.md|*.mdx|*.mli|*.ml|*.txt)
        fetch "$out/${name%.txt}.txt" "$url" ;;
      *)
        fetch "$raw/${name%.html}.html" "$url" ;;
    esac
  else
    fetch "$raw/$arg.html" "https://blog.janestreet.com/$arg/"
  fi
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
