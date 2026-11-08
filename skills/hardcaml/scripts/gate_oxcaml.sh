#!/usr/bin/env bash
# OxCaml half of the hardcaml gate: templates A (Lws) and B (Cyclesim_harness) in
# examples/test_oxcaml must compile and pass on the OxCaml switch, and a canary must be caught.
# usage: scripts/gate_oxcaml.sh [opam-switch]   (default: 5.2.0+ox)
#
# Why the runner is invoked by hand: on 5.2.0+ox (ppxlib 0.33.0+ox2, ppx_expect v0.18~preview.130.106,
# dune 3.24.2) `dune runtest` crashes with Sys_error "./../<file>.ml: No such file or directory",
# because the runner is given -source-tree-root .. while the ppx recorded bare file names. Running it
# from the test directory with -source-tree-root . works. That ppx_expect also writes a .corrected file
# on every run, so "pass" means exit 0 AND every .corrected identical to its source.
set -euo pipefail
here=$(cd "$(dirname "$0")/.." && pwd)
switch=${1:-5.2.0+ox}

check() {
  local root=$1 dir
  (cd "$root" && timeout 900 taskset -c 0-3 nice -n 19 opam exec --switch="$switch" -- \
     dune build -j 4 --root . ./test_oxcaml/.my_design_test_oxcaml.inline-tests/inline-test-runner.exe 2>&1) \
    || return 2
  dir="$root/_build/default/test_oxcaml"
  rm -f "$dir"/*.corrected
  (cd "$dir" && opam exec --switch="$switch" -- ./.my_design_test_oxcaml.inline-tests/inline-test-runner.exe \
     inline-test-runner my_design_test_oxcaml -source-tree-root . -diff-cmd - >/dev/null 2>&1) || return 1
  for c in "$dir"/*.corrected; do
    [ -e "$c" ] || continue
    cmp -s "$c" "${c%.corrected}" || { diff "${c%.corrected}" "$c" | head -8; return 1; }
  done
  return 0
}

echo "== templates A and B on $(opam exec --switch="$switch" -- ocamlopt -version), hardcaml $(opam list --color=never --switch="$switch" --installed --short --columns=version hardcaml 2>/dev/null)"
rc=0; check "$here/examples" || rc=$?
[ $rc -eq 0 ] || { echo "FAIL: templates (rc=$rc)"; exit 1; }
echo "templates A and B pass"

echo "== canary"
tmp=$(mktemp -d); cp -r "$here/examples/." "$tmp/"; rm -rf "$tmp/_build"
python3 -I - "$tmp/test_oxcaml/test_lws.ml" <<'PY'
import pathlib, sys
p = pathlib.Path(sys.argv[1]); s = p.read_text()
a = "inputs.data_in <--. 42;"
if s.count(a) != 1:
    sys.exit("canary pattern not found exactly once")
p.write_text(s.replace(a, "inputs.data_in <--. 41;"))
PY
rc=0; check "$tmp" > "$tmp/out.txt" 2>&1 || rc=$?
case $rc in
  0) echo "FAIL: canary survived"; rm -rf "$tmp"; exit 1 ;;
  1) grep -q "41" "$tmp/out.txt" && echo "canary 'Lws drives 41' caught as an expect diff" || { cat "$tmp/out.txt"; rm -rf "$tmp"; exit 1; } ;;
  *) echo "FAIL: canary broke the build"; rm -rf "$tmp"; exit 1 ;;
esac
rm -rf "$tmp"
echo "gate passed"
