#!/usr/bin/env bash
# Gate for the expect-tests skill: examples pass, SKILL.md snippets are the compiled code,
# and two canary mutations are caught by the tests.
# usage: scripts/gate.sh [opam-switch]   (default: jane-skills)
set -euo pipefail
here=$(cd "$(dirname "$0")/.." && pwd)
switch=${1:-jane-skills}
run() { (cd "$1" && nice -n 19 opam exec --switch="$switch" -- dune runtest -j 4 --root . 2>&1); }

echo "== examples: dune runtest"
run "$here/examples" > /dev/null || { run "$here/examples" | head -60; echo "FAIL: examples"; exit 1; }

echo "== snippets"
python3 -I "$here/scripts/check_snippets.py" "$here/SKILL.md" "$here/examples"

mutate() {
  local name=$1 file=$2 from=$3 to=$4 tmp
  tmp=$(mktemp -d)
  cp -r "$here/examples/." "$tmp/"
  rm -rf "$tmp/_build"
  python3 -I - "$tmp/$file" "$from" "$to" <<'PY'
import pathlib, sys
p, a, b = pathlib.Path(sys.argv[1]), sys.argv[2], sys.argv[3]
s = p.read_text()
if s.count(a) != 1:
    sys.exit(f"canary pattern matched {s.count(a)} times, expected 1: {a!r}")
p.write_text(s.replace(a, b))
PY
  if run "$tmp" > "$tmp/out.txt"; then
    echo "FAIL: canary '$name' survived: the tests did not notice the mutation"
    rm -rf "$tmp"; exit 1
  fi
  if ! grep -q '\.corrected' "$tmp/out.txt"; then
    echo "FAIL: canary '$name' broke the build instead of failing an expect test:"
    head -20 "$tmp/out.txt"; rm -rf "$tmp"; exit 1
  fi
  echo "canary '$name' caught as an expect diff ($(grep -c '^+ ' "$tmp/out.txt" || true) new output lines)"
  rm -rf "$tmp"
}

echo "== canaries"
mutate "size mangled on rest" src/book.ml \
  "ahead @ (order :: behind)" "ahead @ ({ order with size = order.size * 100 } :: behind)"
mutate "time priority broken" src/book.ml \
  "| Sell -> a <= b" "| Sell -> a < b"

mutate "buy at the offer does not trade" src/book.ml \
  "| Buy -> incoming.price >= resting.price" "| Buy -> incoming.price > resting.price"

echo "gate passed"
