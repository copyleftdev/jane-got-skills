#!/usr/bin/env bash
# Gate for the memtrace skill: examples pass under memtrace v0.18 preview, SKILL.md snippets are
# the compiled code, and three canary mutations are each caught as an expect diff.
# usage: scripts/gate.sh [opam-switch]   (default: hardcaml-bleeding, which has memtrace v0.18)
set -euo pipefail
here=$(cd "$(dirname "$0")/.." && pwd)
switch=${1:-hardcaml-bleeding}
run() { (cd "$1" && timeout 600 nice -n 19 opam exec --switch="$switch" -- dune runtest -j 4 --root . 2>&1); }

version=$(opam list --color=never --switch="$switch" --installed --short --columns=version memtrace 2>/dev/null)
case $version in
  v0.18*) ;;
  *) echo "FAIL: switch $switch has memtrace '${version:-none}'; stop_tracing hangs on OCaml >= 5.3 before v0.18"; exit 1 ;;
esac

echo "== examples: dune runtest ($switch: memtrace $version)"
run "$here/examples" > /dev/null || { run "$here/examples" | head -60; echo "FAIL: examples"; exit 1; }

echo "== snippets"
python3 -I "$here/../../tools/check_snippets.py" "$here/SKILL.md" "$here/examples"

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
    echo "FAIL: canary '$name' survived"; rm -rf "$tmp"; exit 1
  fi
  grep -q '\.corrected' "$tmp/out.txt" || { echo "FAIL: canary '$name' broke the build instead of a test"; head -20 "$tmp/out.txt"; rm -rf "$tmp"; exit 1; }
  echo "canary '$name' caught as an expect diff"
  rm -rf "$tmp"
}

echo "== canaries"
mutate "the leak is fixed, so the test must notice" src/workloads.ml \
  "let remember i = Hashtbl.replace cache i (Bytes.create 1024)" \
  "let remember i = ignore (Sys.opaque_identity (i, Bytes.create 1024))"
mutate "live_at_end ranks every allocation" src/memtrace_live.ml \
  "  let survivors, _, _, word_bytes = read filename in
  rank ~word_bytes survivors" \
  "  let survivors, collected, _, word_bytes = read filename in
  rank ~word_bytes (survivors @ List.map fst collected)"
mutate "the pipeline is balanced" src/workloads.ml \
  "let backlogged_pipeline ~ticks = pipeline ~ticks ~produced_per_tick:2" \
  "let backlogged_pipeline ~ticks = pipeline ~ticks ~produced_per_tick:1"

echo "gate passed"
