#!/usr/bin/env bash
# Gate for the hardcaml skill: linter tests, examples lint clean and pass under Hardcaml v0.18
# preview, SKILL.md snippets are the compiled code, and a canary mutation is caught.
# usage: scripts/gate.sh [opam-switch]   (default: hardcaml-bleeding)
set -euo pipefail
here=$(cd "$(dirname "$0")/.." && pwd)
switch=${1:-hardcaml-bleeding}
run() { (cd "$1" && nice -n 19 opam exec --switch="$switch" -- dune runtest -j 4 --root . 2>&1); }

echo "== linter tests"
python3 -I -m unittest discover -s "$here/scripts/tests" 2>&1 | tail -1

echo "== lint examples"
python3 -I "$here/scripts/hardcaml_lint.py" "$here/examples"

echo "== examples: dune runtest ($switch: hardcaml $(opam list --switch="$switch" --installed --short --columns=version hardcaml 2>/dev/null))"
run "$here/examples" > /dev/null || { run "$here/examples" | head -60; echo "FAIL: examples"; exit 1; }

echo "== snippets"
python3 -I "$here/../../tools/check_snippets.py" "$here/SKILL.md" "$here/examples"

echo "== canary"
tmp=$(mktemp -d)
cp -r "$here/examples/." "$tmp/"
rm -rf "$tmp/_build"
python3 -I - "$tmp/src/my_module.ml" <<'PY'
import pathlib, sys
p = pathlib.Path(sys.argv[1]); s = p.read_text()
a = "reg spec ~enable:data_in_valid data_in"
if s.count(a) != 1:
    sys.exit(f"canary pattern matched {s.count(a)} times")
p.write_text(s.replace(a, "reg spec data_in"))
PY
if run "$tmp" > "$tmp/out.txt"; then
  echo "FAIL: canary 'register ignores enable' survived"; rm -rf "$tmp"; exit 1
fi
grep -q '\.corrected' "$tmp/out.txt" || { echo "FAIL: canary broke the build instead of a test"; head -20 "$tmp/out.txt"; rm -rf "$tmp"; exit 1; }
echo "canary 'register ignores enable' caught as an expect diff"
rm -rf "$tmp"

echo "gate passed"
