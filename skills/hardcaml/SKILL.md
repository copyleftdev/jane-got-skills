---
name: hardcaml-design
description: Design, simulate, and test FPGA/ASIC hardware in Hardcaml, Jane Street's OCaml hardware construction library, following Jane Street's own published agent guidelines. Covers module structure (I/O interfaces, Config functors, hierarchical instantiation), the Signal vs Always API split, signal naming with let%hw, operator precedence and signedness traps, constants and resizing, muxing idioms, and testbenches (Lws or Cyclesim_harness on OxCaml, plain Cyclesim on stock OCaml, chosen by an explicit toolchain check) with expect tests and ASCII waveforms. Ships a linter for the patterns the guidelines ban. Use when writing or reviewing Hardcaml, porting Verilog/VHDL designs to Hardcaml, writing Hardcaml testbenches, or generating RTL from OCaml.
---

# Hardcaml Design

## Overview

Hardcaml is an OCaml library for describing hardware. A Hardcaml design is an OCaml program which, when run, builds a circuit data structure. That structure can then be simulated, printed as a waveform inside an expect test, or converted to Verilog/VHDL for vendor tools. Jane Street uses it for its FPGA work and publishes the library, about 25 companion repos, and, since May 2026, a set of prompts written specifically for AI agents.

This skill is built on those prompts. They are vendored verbatim, under MIT, in `references/`:

| Reference | Read it when |
|---|---|
| `references/design_guideline.md` | Writing or reviewing any design code |
| `references/simulation_guideline.md` | Writing any testbench |
| `references/variant_interfaces.md` | A module must support several interface *shapes* chosen at build time |

This file condenses those prompts into a workflow. It adds the toolchain check they assume, corrections where they contradict themselves, and a linter (`scripts/hardcaml_lint.py`) that enforces the mechanical rules. When this file and a reference disagree on a rule, the reference wins, except where this file says it is correcting the reference.

## Step 0: Identify the Toolchain

The guidelines track the newest Hardcaml (v0.18 preview) on Jane Street's OxCaml compiler. Which APIs exist depends entirely on the toolchain, so find it first: `opam switch show`, `opam list hardcaml`, and whether existing code uses `@ local` / `let%hw`.

| Toolchain | Hardcaml | Guideline APIs (`let%hw`, `of_unsigned_int`, `to_unsigned_int`, `uextend`, `cut_through_reg`) | `hardcaml_test_harness` | `hardcaml_lws` | Testbench to write |
|---|---|---|---|---|---|
| **OxCaml**: switch `5.2.0+ox`, packages from `oxcaml/opam-repository` (Jane Street's recommended setup) | v0.18 preview | yes | yes | yes | **Lws** via `Lws_harness`, with `(h @ local)` and `[@nontail]` as the guideline shows |
| **Stock OCaml + `janestreet-bleeding`** (`opam repo add janestreet-bleeding https://github.com/janestreet/opam-repository.git`), on an opam-built `ocaml-base-compiler` 5.4 | v0.18 preview | yes | **no** | **no** | Plain `Cyclesim.With_interface` + `Cyclesim.Waveform` (template C below), with no mode annotations |
| **Stock OCaml, default opam** | v0.17.1 | **no**: `of_int`, `--` naming, no `let%hw` | no | no | Plain Cyclesim. The guideline's API rules don't apply, so lint with `--skip H002,H004` |

Verified 2026-11-07 against the three opam repositories and the v0.17.1 source:

- `hardcaml_template_project` itself requires the first row. Its tests use `hardcaml_test_harness`, and its README says to install OxCaml.
- On GitHub, the OxCaml version of each Hardcaml repo lives on the `oxcaml` branch. `hardcaml_lws`'s `master` is a README stub.
- The second row was built and run on 2026-11-07, with Hardcaml `v0.18~preview.133.03+642` on `ocaml-base-compiler.5.4.0`. `examples/` passes there, and `scripts/gate.sh` re-checks it. Two traps came up while setting it up:
  - **Stale package lists.** The preview needs `ppxlib >= 0.39.0`, released 2026-10-07. With stale opam metadata, the solver either fails or silently falls back to v0.17.1. Run `opam update` first, and check that `opam list hardcaml` says `v0.18~preview`.
  - **`ocaml-system` on Ubuntu.** On an `ocaml-system` switch, `odoc-parser` (pulled in by `ppx_js_style`) fails with `Unbound module Stream`. The build picks up Ubuntu's `libcamlp-streams-ocaml` from `/usr/lib/ocaml`, which ships no `.cmi` files. Use `ocaml-base-compiler`, which does not see the system's OCaml libraries.

If the project is on v0.17.1, tell the user that the guidelines target a newer Hardcaml, and recommend OxCaml before writing much code. Porting later means touching every constant, conversion, and signal name.

## Step 1: Project Layout

Follow `janestreet/hardcaml_template_project`:

```
src/dune   (library (name my_design) (libraries core hardcaml)
             (preprocess (pps ppx_hardcaml ppx_jane)))
test/dune  (library (name my_design_test)
             (libraries core hardcaml my_design hardcaml_test_harness hardcaml_waveterm)
             (preprocess (pps ppx_hardcaml ppx_jane)) (inline_tests))
bin/       RTL generation executable
```

Every design file opens:

```ocaml
open! Core
open! Hardcaml
open! Signal
```

Test files open `Hardcaml_waveterm` and `Hardcaml_test_harness`, but not `Signal`.

## Step 2: Module Skeleton

Every module has an `I` and an `O` interface, a `create`, and a `hierarchical`. Parameterize with a `Config` functor when widths or latencies vary.

```ocaml
module type Config = sig
  val data_bits : int

  (** Cycles from [start] to [result.valid]. *)
  val latency : int
end

module Make (Config : Config) = struct
  module I = struct
    type 'a t =
      { clocking : 'a Clocking.t
      ; data_in : 'a [@bits Config.data_bits]
      ; data_in_valid : 'a
      }
    [@@deriving hardcaml]
  end

  module O = struct
    type 'a t = { result : 'a With_valid.t [@bits Config.data_bits] }
    [@@deriving hardcaml]
  end

  let create scope ({ clocking; data_in; data_in_valid } : _ I.t) : _ O.t =
    let spec = Clocking.to_spec clocking in
    let%hw data_q = reg spec ~enable:data_in_valid data_in in
    let%hw valid_q = reg spec data_in_valid in
    { O.result = { valid = valid_q; value = data_q } }
  ;;

  let hierarchical ?instance scope i =
    let module H = Hierarchy.In_scope (I) (O) in
    H.hierarchical ?instance ~scope ~name:"my_module" create i
  ;;
end
```

- `[@@deriving hardcaml]` already includes `sexp_of`. Never write `[@@deriving sexp_of, hardcaml]`.
- Callers instantiate children with `Child.hierarchical ~scope`, not `create`, to get a separate RTL module.
- Use the OCaml field name as the RTL port name. Override it (`[@rtlname]`, `[@rtlprefix]`, `[@rtlmangle]`) only for an I/O name collision or for external IP that expects specific names.
- For simulation, elaborate with `flatten_design` enabled. A retained instance without a simulation model makes Cyclesim raise `Instantiation not supported in simulation`.

## Step 3: Design Rules

### Signal API or Always API?

| Logic | Use |
|---|---|
| Ordinary combinational logic | Inline Signal: `let%hw x = mux2 cond a b in` |
| A register fed by a next-value signal | `Signal.reg` / `reg_fb`, **not** `Always.Variable.reg` |
| A counter independent of FSM state | `reg_fb spec ~width ~enable ~f:(fun fb -> fb +:. 1)` |
| A value driven only in particular FSM states | `Always.Variable.wire ~default` assigned inside `sm.switch` |
| State machines | `Always.State_machine.create (module State) spec` named with `let%hw.Always.State_machine` |

An `Always.Variable.t` is not a `Signal.t`. Read it through `.value` (`a +: foo_reg.value`).

### Naming

Named signals appear in waveforms and in generated RTL, while unnamed ones become `_T_123`. Name as much as possible.

- `let%hw` for `Signal.t`, `let%hw_var` for `Always.Variable.t`, `let%hw.Foo.Of_signal` for interface records, and `_list` / `_array` / `_option` variants for collections. These need a `Scope.t` called `scope` in context.
- Helper functions that create named signals use `let%subscope` to avoid name collisions across instances.
- **Never use the `--` naming operator.** The guideline calls it dangerous.

### Operators: Always Parenthesize

Hardcaml's operator precedence is not Verilog's. "`&:` and `|:` have equal precedence and are left-associative, so `a |: b &: c` parses as `(a |: b) &: c`." The rule is absolute: parenthesize every mixed expression.

```ocaml
let%hw sum = (a +: b) -: d in               (* not  a +: b -: d        *)
let%hw ok = (a <: b) &: (e >: f) in         (* not  a <: b &: e >: f   *)
```

Signedness lives in the operator: `*:`, `<:`, `>:` are unsigned, while `*+`, `<+`, `>+` are signed. Pick deliberately when comparing two's-complement values.

Unary operators go in operator form with the argument parenthesized: `~:(foo)`, never `(~:) foo`.

### Constants, Conversions, Widths

- OCaml int to signal: `of_unsigned_int ~width:8 10` or `of_signed_int ~width:8 (-128)`. **Never `of_int_trunc`**, which the guideline calls broken and dangerous because it silently truncates.
- Bits to OCaml int (in tests): `Bits.to_unsigned_int` or `Bits.to_signed_int`. Never `to_int` / `to_int_trunc`.
- Widen with `uextend` / `sextend` and narrow with `sel_bottom`. Use `uresize` / `sresize` only with a comment justifying it.
- Bit select with `x.:(i)` and range select with `x.:[hi, lo]` (`foo.:[10, 0]` is 11 bits wide).
- Concatenate with `concat_msb [hi; lo]` or `hi @: lo`, and split with `split_lsb ~part_width`.

### Muxing

| Situation | Idiom |
|---|---|
| 2 choices | `mux2 cond a b` |
| A 2–4 deep priority chain | `mux2 c1 a @@ mux2 c2 b @@ mux2 c3 c @@ default`. Use `@@` to stop the indentation growing, and never `@@` on a single non-chained `mux2` |
| 5 or more priority cases | `priority_select_with_default [ { valid; value }; ... ] ~default` |
| Exactly one condition guaranteed high | `onehot_select` |
| A few selector values with a default | `cases ~default selector [ (v, r); ... ]` (plural, explicit selector) |

### Registers and Clocking

- Build one `Reg_spec` (or `Clocking.t`) at the top of `create` and reuse it.
- `~enable` defaults to `vdd`, so omit it. Never write `~enable:vdd`.
- `cut_through_reg spec ~enable d` forwards `d` with zero latency while enabled, and holds otherwise.

### Hygiene

No unused values (`let _special_code_1 = 1`). No dead wires. Keep handshake signals as `With_valid.t`.

## Step 4: Test With Expect Tests and Waveforms

Hardcaml testbenches are expect tests. Print values as sexps (`Bits.Hex.t`, `Bits.Unsigned_int.t`, `Bits.Signed_int.t`) and, for small designs, print an ASCII waveform inline so reviewers see behavior change as a diff.

**Sampling:** outputs come as `Before_and_after_edge.t`. Use `after_edge` for registered outputs and `before_edge` for combinational or handshake checks, such as `before_edge.valid &: before_edge.tready` to detect a completed transfer.

**A. OxCaml (Lws, the guideline default):**

```ocaml
module Harness = Hardcaml_test_harness.Lws_harness.Make (Dut.I) (Dut.O)

let%expect_test "accumulates" =
  Harness.run ~create:Dut.hierarchical (fun (h @ local) ~inputs ~outputs ->
    let open Bits in
    inputs.data_in <--. 42;
    inputs.data_in_valid := vdd;
    Lws.step h;
    print_s [%message (!(outputs.after_edge.result.value) : Bits.Unsigned_int.t)]);
  [%expect {| ("!(((outputs.after_edge).result).value)" 16'd42) |}]
;;
```

Use `Lws.spawn` for concurrent drivers and monitors, and `Lws.step_until_some` to wait on a condition. Prefer `List.iter` / `List.map` with `[@nontail]` over hand-rolled loops.

**B. OxCaml, Cyclesim_harness (as in the template project, for direct port poking):**

```ocaml
module Harness = Cyclesim_harness.Make (Dut.I) (Dut.O)

let ( <--. ) = Bits.( <--. )

let%expect_test "accumulates" =
  Harness.run_advanced ~create:Dut.hierarchical (fun sim ->
    let inputs = Cyclesim.inputs sim in
    let outputs = Cyclesim.outputs ~clock_edge:After sim in
    inputs.clocking.clear := Bits.vdd;
    Cyclesim.cycle sim;
    inputs.clocking.clear := Bits.gnd;
    inputs.data_in <--. 42;
    inputs.data_in_valid := Bits.vdd;
    Cyclesim.cycle sim;
    print_s [%message (Bits.to_unsigned_int !(outputs.result.value) : int)]);
  [%expect {| ("Bits.to_unsigned_int (!((outputs.result).value))" 42) |}]
;;
```

**C. Stock OCaml without the harness packages** (pattern from Hardcaml's `docs/fibonacci_example.md`):

```ocaml
let%expect_test "accumulates" =
  let module Sim = Cyclesim.With_interface (Dut.I) (Dut.O) in
  let scope = Scope.create ~flatten_design:true () in
  let sim = Sim.create ~config:Cyclesim.Config.trace_all (Dut.create scope) in
  let waves, sim = Cyclesim.Waveform.create sim in
  let display_rules =
    [ Hardcaml_waveterm.Display_rule.port_name_matches
        ~wave_format:(Bit_or Unsigned_int) (Glob "*")
    ]
  in
  let inputs = Cyclesim.inputs sim in
  let outputs = Cyclesim.outputs sim in
  inputs.data_in := Bits.of_unsigned_int ~width:16 42;
  inputs.data_in_valid := Bits.vdd;
  Cyclesim.cycle sim;
  print_s [%message (Bits.to_unsigned_int !(outputs.result.value) : int)];
  Hardcaml_waveterm.Waveform.print ~display_rules waves;
  [%expect {|
    ("Bits.to_unsigned_int (!((outputs.result).value))" 42)
    ┌Signals────────┐┌Waves──────────────────────────────────────────────┐
    │clear          ││                                                   │
    │               ││────────                                           │
    │clock          ││────┐                                              │
    │               ││    └───                                           │
    │               ││────────                                           │
    │data_in        ││ 42                                                │
    │               ││────────                                           │
    │data_in_valid  ││────────                                           │
    │               ││                                                   │
    │result$valid   ││                                                   │
    │               ││────────                                           │
    │               ││────────                                           │
    │result$value   ││ 0                                                 │
    │               ││────────                                           │
    │               ││────────                                           │
    │data_q         ││ 0                                                 │
    │               ││────────                                           │
    │valid_q        ││                                                   │
    │               ││────────                                           │
    └───────────────┘└───────────────────────────────────────────────────┘
    |}]
;;
```

**Before or after the edge.** In this test, the `print_s` reports 42 while the waveform shows `result$value` as 0 in the same cycle, and both are right. `Cyclesim.outputs` defaults to `~clock_edge:After` (`cyclesim.ml`), so it reads the register after it loaded. The waveform samples the cycle before the edge. When a printed value and a wave disagree by exactly one cycle, check which edge each one read before you suspect the design.

Testbench rules for all three:

- **Waveforms:** pass `~print_waves_after_test:(fun w -> Waveform.print ~display_rules w)`, always with `display_rules` limiting output to the relevant signals. Use `~trace:\`All_named`.
- **Debugging:** switch to `Waves_config.to_test_directory ()` and `~trace:\`Everything`, then open the file in the waveterm viewer.
- **Robustness:** `~random_initial_state:\`All` catches logic that silently relies on zeroed registers.
- **Configurations:** functorize the test over `Config` and instantiate it with `module%test Test_foo = Make (Foo_config)` for each configuration that matters.
- **Backends:** don't use the event-driven backend unless existing code does or the user asks. The legacy `Hardcaml_step_testbench` is for reading old tests, so don't write new ones with it.
- **Verilator:** reset discards the foreign model, so reacquire memory views after every reset.

## Step 5: Gate Before Handing Back

```sh
python3 -I <skill-dir>/scripts/hardcaml_lint.py src test   # exit 1 on any error-severity finding
dune build @fmt && dune build
dune runtest            # inspect the diff, then:
dune promote            # only after reading every changed expectation and waveform
```

The linter is line-based, so it is a floor, not a proof. Its rules and what each one catches:

| Rule | Severity | Catches |
|---|---|---|
| H001 | error | `~enable:vdd` |
| H002 | error | `--` signal naming |
| H003 | error | `of_int_trunc` |
| H004 | error | `Bits` / `Cyclesim` `to_int`, `to_int_trunc` |
| H005 | error | `[@@deriving sexp_of, hardcaml]` |
| H006 | error | prefix unary `(~:) x` |
| H008 | error | 2+ distinct Hardcaml binary operators at one paren level on one line |
| H007 | warning | `uresize` / `sresize` with no comment on that line or the one above |
| H009 | warning | event-driven simulation backend |
| H010 | warning | `let _unused = ...` |

It ignores strings and nested multi-line comments. It cannot see operator mixing that spans lines, `@@` on a lone `mux2`, or Signal-vs-Always placement, so review those by hand against the table in Step 3.

**Calibration (2026-11-07):** `hardcaml_template_project` → 0 findings. `hardcaml_circuits`, which predates the agent guidelines → 174 findings across 159 files, including 92 `of_int_trunc`. Every H008 hit was inspected and is a real unparenthesized mix, such as `x &: y |: (x &: z)` in `add.ml`. Expect findings when linting older Hardcaml code. Fix them in code you are changing, and don't mass-rewrite code you aren't.

**This skill's own gates.**

`scripts/gate_oxcaml.sh [switch]` (default `5.2.0+ox`) compiles and runs templates A and B on OxCaml with Hardcaml `v0.18~preview.130.106`. Both print 42 after one cycle. A canary that drives 41 must be caught. Two OxCaml-switch findings are behind how it works:
- **The runner is invoked by hand.** There, `dune runtest` crashes with `Sys_error "./../<file>.ml"`, because the runner gets `-source-tree-root ..` while the ppx recorded bare file names. The script runs the runner from the test directory with `-source-tree-root .`. That ppx_expect writes a `.corrected` file on every run, so a pass means exit 0 *and* every `.corrected` identical to its source.
- **Waveform text depends on the Hardcaml version.** The same one-cycle test draws the clock across the whole display on `130.106`, but as a single cycle on `133.03`. Keep expect files with waveforms on one toolchain, and don't share them between switches.

`scripts/gate.sh [switch]` (default `hardcaml-bleeding`) runs four checks:
- the linter's tests;
- the linter over `examples/`;
- `dune runtest` in `examples/`;
- `tools/check_snippets.py`, which confirms every `ocaml` block in this file is the compiled code.

Templates A and B are verified by `gate_oxcaml.sh` instead, because they need OxCaml. A canary that removes the register's `~enable` must fail the hold test as an expect diff.

## Corrections to the Upstream Guidelines

The vendored guideline is authoritative but not error-free. Known slips as of commit `869a1fb`:

- Its own `Hierarchy.In_scope` example writes `reg spec ~enable:vdd data_in`, the pattern it bans a few sections earlier. Follow the rule, not the example.
- Its "good practice" Always example misspells `Always` as `Alway.Variable.wire` and calls `Always.State_machine.create (module State)` without `spec`. Neither compiles as written.
- `default_resut` in the mux2 chain example is a typo.
- The Lws templates assume OxCaml (see Step 0).

## Porting From Verilog

- One Verilog module becomes one OCaml module with `I` / `O` / `create` / `hierarchical`.
- Parameters become a `Config` functor. `generate` loops become ordinary OCaml `List.init` / `Array.init` at elaboration time.
- `always @(posedge clk)` with a next-value expression becomes `reg` / `reg_fb`. A `case` FSM becomes an `Always.State_machine`.
- Re-derive every expression's precedence, because a Verilog `a | b & c` becomes `a |: (b &: c)` in Hardcaml.
- Check signedness on every comparison and multiply (`<:` vs `<+`).
- `hardcaml_of_verilog` exists for mechanical conversion. Treat its output as a starting point to rewrite into these idioms.

## Sources

- Hardcaml: https://github.com/janestreet/hardcaml (docs in `docs/`, including `why.md`, `using_ai.md`, `waveforms.md`)
- Agent prompts (vendored in `references/`): https://github.com/janestreet/hardcaml_agents_docs
- Template project: https://github.com/janestreet/hardcaml_template_project
- Lws scheduler (code on the `oxcaml` branch): https://github.com/janestreet/hardcaml_lws
- Jane Street blog, *Using ASCII waveforms to test hardware designs*: https://blog.janestreet.com/using-ascii-waveforms-to-test-hardware-designs/
