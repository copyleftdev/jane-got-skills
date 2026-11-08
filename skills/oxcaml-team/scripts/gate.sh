#!/usr/bin/env bash
# Gate for the oxcaml-team skill's "OxCaml Toolkit" table: examples/ uses every shape in the table and
# must compile on OxCaml; four canaries must each FAIL to compile with the checker's own error.
# usage: scripts/gate.sh [opam-switch]   (default: 5.2.0+ox)
set -euo pipefail
here=$(cd "$(dirname "$0")/.." && pwd)
switch=${1:-5.2.0+ox}
build() { (cd "$1" && timeout 900 taskset -c 0-3 nice -n 19 opam exec --switch="$switch" -- dune build -j 4 --root . 2>&1); }

echo "== examples compile on $(opam exec --switch="$switch" -- ocamlopt -version)"
build "$here/examples" > /dev/null || { build "$here/examples" | head -40; echo "FAIL: examples"; exit 1; }

canary() {
  local name=$1 expect=$2 from=$3 to=$4 tmp
  tmp=$(mktemp -d)
  cp -r "$here/examples/." "$tmp/"
  rm -rf "$tmp/_build"
  python3 -I - "$tmp/src/toolkit.ml" "$from" "$to" <<'PY'
import pathlib, sys
p, a, b = pathlib.Path(sys.argv[1]), sys.argv[2], sys.argv[3]
s = p.read_text()
if s.count(a) != 1:
    sys.exit(f"canary pattern matched {s.count(a)} times, expected 1: {a!r}")
p.write_text(s.replace(a, b))
PY
  if build "$tmp" > "$tmp/out.txt"; then
    echo "FAIL: canary '$name' compiled; the checker did not fire"; rm -rf "$tmp"; exit 1
  fi
  grep -q -- "$expect" "$tmp/out.txt" || { echo "FAIL: canary '$name' failed for another reason:"; head -15 "$tmp/out.txt"; rm -rf "$tmp"; exit 1; }
  echo "canary '$name' rejected: $(grep -m1 -o -- "$expect.\{0,60\}" "$tmp/out.txt")"
  rm -rf "$tmp"
}

echo "== canaries"
canary "zero_alloc function that allocates" "Annotation check for zero_alloc failed" \
  "let[@zero_alloc] add_scaled a b k = a + (b * k)" \
  "let[@zero_alloc] add_scaled a b k = ignore (Sys.opaque_identity [ a ]); a + (b * k)"
canary "mutable array shared across fork_join2" "nonportable" \
  "let parallel_sum par (xs : int iarray) =
  let n = Base.Iarray.length xs in
  let half = n / 2 in
  let sum lo hi =
    let s = ref 0 in
    for i = lo to hi - 1 do
      s := !s + Base.Iarray.get xs i" \
  "let parallel_sum par (xs : int array) =
  let n = Array.length xs in
  let half = n / 2 in
  let sum lo hi =
    let s = ref 0 in
    for i = lo to hi - 1 do
      s := !s + xs.(i)"
canary "stack value in tail position" "tail call" \
  "  manhattan p [@nontail]" "  manhattan p"
canary "int64_u is not a type" "Unbound type constructor" \
  "let sum_and_diff (a : int64#)" "let sum_and_diff (a : int64_u)"

echo "gate passed"
