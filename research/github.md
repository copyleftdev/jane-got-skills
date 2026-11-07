# Jane Street open source: GitHub footprint, as source material for agent skills

Snapshot taken 2026-11-07. Sources:
- `gh api orgs/janestreet/repos`: 446 public repos. The raw list is in [`repos.json`](repos.json).
- `gh api orgs/oxcaml/repos`: 17 repos.
- Shallow clones of about 30 key repos.
- The Wayback copy of opensource.janestreet.com.

## 1. Shape of the org

- **446 repos.** 373 are OCaml. 20 are forks: emacs, spacemacs, perfetto, ppxlib, ocaml, ocaml-jst, utop, tuareg, ocp-indent and others. 8 are archived: jenga, pythonlib, ocaml_plugin, install-ocaml, ppx_python, krb, core_compat, memtrace_viewer_with_deps.
- **Almost everything moves in one batch.** 337 repos were pushed on 2026-11-03, the same `public-release` export. 387 were pushed during 2026, and 48 have not been pushed since before 2024.
- **Few repos stand on their own.** The exceptions are magic-trace, the editor forks (spacemacs, emacs, ttyd, evil, company-mode) and asic-puzzle-2026.
- **The org pins** base, magic-trace, core, hardcaml, bonsai and async.

## 2. Top 40 by stars

| # | Repo | Stars | Lang | Last push | Archived | Description |
|---|---|---|---|---|---|---|
| 1 | [magic-trace](https://github.com/janestreet/magic-trace) | 6347 | OCaml | 2026-10-19 |  | magic-trace collects and displays high-resolution traces of what a process is doing |
| 2 | [incremental](https://github.com/janestreet/incremental) | 1539 | OCaml | 2026-11-03 |  | A library for incremental computations |
| 3 | [bonsai](https://github.com/janestreet/bonsai) | 1424 | OCaml | 2026-11-03 |  | A library for building dynamic webapps, using Js_of_ocaml |
| 4 | [core](https://github.com/janestreet/core) | 1347 | OCaml | 2026-11-03 |  | Jane Street Capital's standard library overlay |
| 5 | [hardcaml](https://github.com/janestreet/hardcaml) | 1167 | OCaml | 2026-11-03 |  | Hardcaml is an OCaml library for designing hardware. |
| 6 | [base](https://github.com/janestreet/base) | 1098 | OCaml | 2026-11-03 |  | Standard library for OCaml |
| 7 | [learn-ocaml-workshop](https://github.com/janestreet/learn-ocaml-workshop) | 723 | OCaml | 2022-04-04 |  | Exercises and projects for Jane Street's OCaml Workshop |
| 8 | [incr_dom](https://github.com/janestreet/incr_dom) | 403 | OCaml | 2026-11-03 |  | A library for building dynamic webapps, using Js_of_ocaml. |
| 9 | [asic-puzzle-2026](https://github.com/janestreet/asic-puzzle-2026) | 338 | Verilog | 2026-08-05 |  |  |
| 10 | [async](https://github.com/janestreet/async) | 291 | OCaml | 2026-11-03 |  | Jane Street Capital's asynchronous execution library |
| 11 | [ecaml](https://github.com/janestreet/ecaml) | 291 | OCaml | 2026-11-03 |  | Writing Emacs plugin in OCaml |
| 12 | [patdiff](https://github.com/janestreet/patdiff) | 254 | OCaml | 2026-11-03 |  | File Diff using the Patience Diff algorithm. https://opensource.janestreet.com/patdiff/ |
| 13 | [bonsai_term](https://github.com/janestreet/bonsai_term) | 231 | OCaml | 2026-11-03 |  | A library for building dynamic terminal apps, using bonsai |
| 14 | [core_kernel](https://github.com/janestreet/core_kernel) | 229 | OCaml | 2026-11-03 |  | Jane Street's standard library overlay (kernel) |
| 15 | [sexplib](https://github.com/janestreet/sexplib) | 199 | OCaml | 2026-11-03 |  | Automated S-expression conversion |
| 16 | [ppx_expect](https://github.com/janestreet/ppx_expect) | 198 | OCaml | 2026-11-03 |  | Cram like framework for OCaml |
| 17 | [iron](https://github.com/janestreet/iron) | 192 | - | 2020-01-14 |  | Jane Street code review system |
| 18 | [vcaml](https://github.com/janestreet/vcaml) | 182 | OCaml | 2026-11-03 |  | OCaml bindings for the Neovim API |
| 19 | [torch](https://github.com/janestreet/torch) | 168 | OCaml | 2026-11-03 |  |  |
| 20 | [shexp](https://github.com/janestreet/shexp) | 146 | OCaml | 2026-11-03 |  | Process library and s-expression based shell |
| 21 | [ppx_inline_test](https://github.com/janestreet/ppx_inline_test) | 144 | OCaml | 2026-11-03 |  | Syntax extension for writing in-line tests in ocaml code |
| 22 | [opam-repository](https://github.com/janestreet/opam-repository) | 140 | - | 2026-11-03 |  | Opam repository for the development version of Jane Street packages |
| 23 | [ppx_let](https://github.com/janestreet/ppx_let) | 132 | OCaml | 2026-11-03 |  | Monadic let-bindings |
| 24 | [strace_ui](https://github.com/janestreet/strace_ui) | 131 | OCaml | 2026-11-03 |  | A Bonsai_term application for interactively viewing strace output |
| 25 | [install-ocaml](https://github.com/janestreet/install-ocaml) | 98 | OCaml | 2019-12-20 | yes | Instructions for setting up an OCaml development environment |
| 26 | [pythonlib](https://github.com/janestreet/pythonlib) | 98 | OCaml | 2024-07-30 | yes | A library to help writing wrappers around ocaml code for python |
| 27 | [ppx_sexp_conv](https://github.com/janestreet/ppx_sexp_conv) | 93 | OCaml | 2026-11-03 |  | Generation of S-expression conversion functions from type definitions |
| 28 | [jenga](https://github.com/janestreet/jenga) | 90 | - | 2018-09-19 | yes | Build system |
| 29 | [bin_prot](https://github.com/janestreet/bin_prot) | 88 | OCaml | 2026-11-03 |  | Binary protocol generator |
| 30 | [memtrace](https://github.com/janestreet/memtrace) | 88 | OCaml | 2026-11-03 |  | Streaming client for OCaml's Memprof |
| 31 | [spawn](https://github.com/janestreet/spawn) | 71 | C | 2024-11-11 |  | Spawning sub-processes |
| 32 | [ppx_yojson_conv](https://github.com/janestreet/ppx_yojson_conv) | 70 | OCaml | 2026-11-03 |  | [@@​deriving] plugin to generate Yojson conversion functions |
| 33 | [ppx_optcomp](https://github.com/janestreet/ppx_optcomp) | 67 | OCaml | 2026-11-03 |  | Optional compilation for OCaml |
| 34 | [ppx_fields_conv](https://github.com/janestreet/ppx_fields_conv) | 64 | OCaml | 2026-11-03 |  | Generation of accessor and iteration functions for ocaml records |
| 35 | [accessor](https://github.com/janestreet/accessor) | 62 | OCaml | 2026-11-03 |  | A library that makes it nicer to work with nested functional data structures |
| 36 | [async_kernel](https://github.com/janestreet/async_kernel) | 60 | OCaml | 2026-11-03 |  | Jane Street Capital's asynchronous execution library (core) |
| 37 | [ocaml_plugin](https://github.com/janestreet/ocaml_plugin) | 59 | OCaml | 2023-10-16 | yes | (Archived) Automatically build and dynlink ocaml source files |
| 38 | [virtual_dom](https://github.com/janestreet/virtual_dom) | 59 | OCaml | 2026-11-03 |  | OCaml bindings for the virtual-dom library  |
| 39 | [core_bench](https://github.com/janestreet/core_bench) | 58 | OCaml | 2026-11-03 |  | Micro-benchmarking library for OCaml |
| 40 | [sexp](https://github.com/janestreet/sexp) | 56 | OCaml | 2026-11-03 |  | S-expression swiss knife |

## 3. Clusters

Counts are name-pattern matches over `repos.json`. Star totals are summed, so the bigger repos dominate them.

| Cluster | Repos | Stars | Anchors |
|---|---|---|---|
| Perf tooling | 9 | 6,602 | magic-trace (6347), memtrace (88), tracing (41), ocaml_intrinsics (40), memtrace_viewer (35), perfetto fork (33) |
| Incremental / Bonsai UI | 25 | 3,885 | incremental (1539), bonsai (1424), incr_dom (403), bonsai_term (231), virtual_dom, bonsai_web (holds the docs), incr_map, ppx_html |
| Stdlib (Base/Core) | 18 | 2,877 | core (1347), base (1098), core_kernel (229, now a shim), stdio, core_unix, core_extended, base_quickcheck |
| ppx_* family | 89 | 1,391 | ppx_expect, ppx_inline_test, ppx_let, ppx_sexp_conv, ppx_fields_conv, ppx_variants_conv, ppx_jane (the bundle), ppx_js_style (style linter), ppx_template, ppx_stable |
| Hardcaml | 28 | 1,384 | hardcaml (1167), hardcaml_template_project, hardcaml_circuits, hardcaml_verify, hardcaml_waveterm, hardcaml_step_testbench, ppx_hardcaml, **hardcaml_agents_docs** |
| Async | 21 | 604 | async (291), async_kernel, async_unix, async_rpc_kernel, rpc_parallel, async_smtp |
| Sexp | 24 | 494 | sexplib (199), ppx_sexp_conv, sexp, parsexp, sexp_pretty, ppx_sexp_message |
| Testing | 16 | 487 | ppx_expect (198), ppx_inline_test (144), core_bench, base_quickcheck, ppx_assert, expect_test_helpers_{base,core,async} |
| Editor integration | 11 | 482 | ecaml (291, Emacs plugins in OCaml), vcaml (182, Neovim), plus forks of spacemacs, emacs, evil, tuareg, ocp-indent, utop |
| OxCaml runtime libraries | 11 | 106 | parallel (44), handled_effect (37), portable, ppx_template, await, concurrent, basement, unique |
| Other notable | – | – | patdiff (254), shexp (146), torch (168, PyTorch bindings), learn-ocaml-workshop (723, last push 2022), asic-puzzle-2026 (338, Verilog), accessor, iron (192, code review, last push 2020) |

**OxCaml lives in its own org.** [github.com/oxcaml](https://github.com/oxcaml) has 17 repos. The compiler is [oxcaml/oxcaml](https://github.com/oxcaml/oxcaml) (932 stars, pushed 2026-11-07). `ocaml-flambda/flambda-backend` now redirects there. The org also holds forks of `merlin`, `ocamlformat`, `ocaml-lsp`, `odoc`, `utop`, `dune`, `eio` and `mdx`, plus [tutorial-icfp25](https://github.com/oxcaml/tutorial-icfp25), [playground](https://github.com/oxcaml/playground) and [stylo](https://github.com/oxcaml/stylo), a new Wadler-style CST pretty-printer for OxCaml (the `stylo-jane` opam package). The site is https://oxcaml.org. Its docs are generated from `oxcaml/oxcaml:jane/doc/extensions/`. `janestreet/ocaml-jst` is the dead predecessor (fork, last push 2023-01).

**Important: the OxCaml edition of each library is on the `oxcaml` branch.** The default `master` branch of `base`, `core`, `bonsai`, `hardcaml` and others is the upstream-compatible build. On it, modes are erased to attributes such as `('a array[@local_opt])` or written in the legacy `local_` syntax. The `oxcaml` branch has the real mode and kind annotations, for example in `base/src/list.mli@oxcaml`:

```ocaml
val iter : ('a : k). 'a t @ l -> f:('a @ l -> unit) @ local -> unit
```

and `option.mli@oxcaml` begins with `@@ portable` and uses `[%%template ...]` with `[@@deriving compare ~localize, equal ~localize, sexp ~stackify]`. The hardcaml_template_project README says this outright: *"when looking at Hardcaml GitHub repositories, the OxCaml version is in a branch named `oxcaml`."* An OxCaml skill should cite `oxcaml`-branch sources, not `master`.

## 4. Per-cluster idioms (agent-ready rules)

### 4.1 "Write OCaml the Jane Street way" (base / core / ppx_js_style / style guide)

The primary source is the **Jane Street Style Guide**, formerly at `opensource.janestreet.com/standards/`. That domain now 301-redirects to github.com/janestreet, so the page survives only in the Wayback Machine ([snapshot 2025-11-16](http://web.archive.org/web/20251116120403/https://opensource.janestreet.com/standards/)). It describes itself as the "house style" used in Base, Core, Async and Incremental. Rules taken from it:

- **Formatting:** ocamlformat with the `janestreet` profile, ocp-indent rules, 90-column maximum. (OxCaml's AGENTS.md says to keep lines under 80 in the compiler.)
- **Naming:** `snake_case` / `Snake_case`, never CamelCase. Short names for short scopes and descriptive names for long ones. Boolean functions are predicates (`is_valid`, not `check_validity`). `unsafe_` means memory-unsafe only; use `_unchecked` for "unspecified result but memory-safe" (`Int.of_float_unchecked`).
- **Signatures:** most modules have one main type `t`. Functions take `t` first, except that optional arguments come before a sole positional `t` so they can be erased. Prefer `include Comparable.S with type t := t` over hand-written signatures. Comments go in the `.mli`, above the item.
- **Errors:** return `option` / `Or_error.t` / a variant. A function that raises gets an `_exn` suffix (`val create : string -> t option` / `val create_exn : string -> t`). **Never declare or match on exceptions.** If callers need to tell errors apart, return a variant. Raise with `raise_s [%message "something bad happened" (t : t)]`.
- **Defensive programming:** always type-annotate ignored values (`ignore (Unix.wait `Any : Pid.t)`). Label same-typed arguments (`val send : source:User.t -> dest:User.t -> unit`). **No catch-all `_` in matches** on variants you own, so adding a constructor breaks the build. Use optional arguments only for widely-called, exported functions.
- **Let-syntax:** use `let%bind` / `let%map` (ppx_let) when binding variables. Infix `>>=` / `>>|` only point-free. Open only standard modules (`open! Core`, `open Async`), at the top. Keep local opens small: `Time.(now () < lockout_time)`.
- **Docs:** odoc `(** ... *)` comments in mli, with `[x]` for inline code and `{[ ]}` for blocks. Don't restate the type (`(** [compare x y] Compares two strings lexicographically *)`).
- **Tests:** in a separate test library, against the public API. "Expect tests are the preferred way of writing tests". Quickcheck runs inside `let%expect_test`. `Private` submodules are only for tests and benchmarks of the module itself.
- **Directories:** dash-separated (`trader-tools/`).

**Rules enforced by the linter** ([ppx_js_style](https://github.com/janestreet/ppx_js_style) README):
- `[@@deprecated "[since MM-YYYY] ..."]` must carry a date.
- Ignores must be annotated: `ignore (e : t)` / `let (_ : t) = e`.
- `.mli` comments must be doc comments `(** *)` or explicitly ignored `(*_ *)`.
- Underscores in numeric literals go in groups of 3 (decimal) or 2 (hex).
- **Binding operators (`let*`, `let+`) are forbidden internally.** Use ppx_let.

**Base README rules:**
- Polymorphic compare is hidden. Use type-specific `compare` (`List.compare String.compare x y` or `[%compare: string list]`), and reach for `Poly` only when necessary.
- `open Base` deprecates the stdlib's names. Reach them through `Stdlib.Foo` and never `open Stdlib`.
- Core = Base + `bin_io` + `Stable` + Unix-y modules. Start files with `open! Core`.

**Usage frequency in the base+core source** (this is what the code looks like):

| Pattern | base | core |
|---|---|---|
| `[@@deriving ...]` | 367 | 1,179 |
| `_exn :` vals | 201 | 158 |
| `Or_error` | 101 | 90 |
| `raise_s` | 53 | 62 |
| `[@zero_alloc` | 56 | 132 |
| `Stable` | 1 | 1,083 |

The most common derivers are `sexp_of`, `bin_io`, `sexp`, `compare`, `[compare, equal, hash, sexp_of, sexp_grammar]`, `quickcheck` and `stable_witness`. Versioned wire types use `module Stable = struct module V1 = struct type t = ... [@@deriving bin_io, compare, sexp, stable_witness] end end`.

**Contents of `ppx_jane`** ([src/dune](https://github.com/janestreet/ppx_jane)): ppx_assert, ppx_base (compare/equal/hash/sexp/enumerate/globalize), ppx_bench, ppx_bin_prot, ppx_custom_printf, ppx_expect, ppx_fields_conv, ppx_here, ppx_inline_test, ppx_let, ppx_log, ppx_optional, ppx_pipebang, ppx_quickcheck, ppx_sexp_message, ppx_sexp_value, ppx_stable, ppx_stable_witness, ppx_string, ppx_template, ppx_typed_fields, ppx_variants_conv, and others.

### 4.2 "Expect-test driven development" (ppx_expect / ppx_inline_test / expect_test_helpers)

Source: [ppx_expect/README.mdx](https://github.com/janestreet/ppx_expect/blob/master/README.mdx) (813 lines).

- The test is `let%expect_test "name" = <print things>; [%expect {| output |}]`. The runner writes `foo.ml.corrected` and shows a diff. You **promote** (`dune promote`) instead of hand-writing expected values. The workflow is: write a test with an empty `[%expect {| |}]`, run it, inspect the diff, promote.
- Each `[%expect]` matches all output since the previous one. Interleave them to show which code produced which output. Trailing unmatched output gets a new `[%expect]` appended automatically.
- Whitespace is normalized: indentation is aligned to the block and blank lines are trimmed. Use `[%expect_exact]` for byte-exact output.
- Use `[%expect.unreachable]` for code paths that must not run. An uncaught exception is recorded as `[@@expect.uncaught_exn {| ... |}]`.
- Print values as sexps: `print_s [%sexp (x : T.t)]` or `print_s [%message "label" (x : int) (y : string)]`.
- Helpers in [expect_test_helpers_base](https://github.com/janestreet/expect_test_helpers_base) / `_core`:
  - `require cond` and `require_equal (module M) a b` print a CR instead of raising. `print_cr` is documented as "an expect-test-friendly version of `assert false`".
  - `show_raise` and `require_does_raise (fun () -> ...)` cover raising code. `require_does_raise` "additionally prints a CR if the function does not raise".
  - `print_and_check_round_trip` is for serializers. There is also a quickcheck integration.
- `ppx_inline_test` is the underlying `let%test` / `let%test_unit` framework. The contribute page asks that new tests "typically be done using ppx_inline_test" (expect tests are built on it).
- Library-level dune stanza: `(inline_tests) (preprocess (pps ppx_jane))`. The same idiom appears in Hardcaml (`Waveform.print` in expect tests) and Bonsai (`Handle.show` renders vdom as HTML in expect tests).

### 4.3 Incremental / Bonsai UI

Sources: [incremental/doc/part1–8](https://github.com/janestreet/incremental/tree/master/doc), [bonsai_web/docs/](https://github.com/janestreet/bonsai_web/tree/master/docs) (including `bonsai_best_practices.md`, 590 lines, written as Bad/Good pairs), and [bonsai/README.md](https://github.com/janestreet/bonsai). The bonsai repo itself has no docs; they live in **bonsai_web**.

Incremental rules (part1, part4-pitfalls):
- It is "an optimization tool. If you're not trying to solve a performance problem, you probably shouldn't be using it". It costs extra from scratch and "isn't super fast": it is "largely not compatible with zero-alloc approaches".
- The model has three parts: `Var` (inputs), incrementals, and `Observer`s.
- Pitfalls: don't over-incrementalize, and don't use mutable state, especially for capturing history. "Be wary of `bind` (and especially `return`)". Bind makes sense only in two cases, and "using `bind` in other cases is almost always a mistake".

Bonsai rules (bonsai_best_practices.md, verbatim headings):
- **Always use `let%arr` over `let%map` / `Bonsai.map`.** It adds an incremental cutoff.
- **Always destructure in a `let%arr`** (`let%arr { foo; _ } = my_thing in ...`).
- **Prefer `ppx_html`** (`{%html|<div class="c">%{x#Int}</div>|}`) over `Vdom.Node` constructors.
- **Avoid duplicate state** and derive values instead. **Don't sync states with `Bonsai.Edge.on_change`.** Use `Bonsai_kernel_mirror` for external state such as the URL or localStorage.
- **Never have side effects in `let%arr` bodies.** Use `Bonsai.Edge.on_change`.
- Time sources: `Vdom_time_ago`, `Bonsai.Clock.at` → `Before_or_after.t`, `Bonsai.Clock.get_current_time` inside effects, and the time source in `Apply_action_context`. Avoid `Clock.Expert.now`, which runs every frame.
- **Always call the graph param `graph` and label it `@ local`**: `let component (graph @ local) = ...`. Pass it explicitly.
- Also: avoid mutable values in `Bonsai.t`, avoid `>>|`, prefer `Bonsai_web.Effect.t` over `Ui_effect.t`, don't do expensive work to build an `Effect.t`, use `[%lazy]` with `match%sub` for routing, put reusable views and components in modules, avoid CSS resets, and **never use exceptions** (they are expensive in JS/WASM).
- State primitives: `Bonsai.state`, `Bonsai.state_machine ~default_model ~apply_action`, and `match%sub` for dynamic structure. `Bonsai.t` has no `bind` by design (thinking_in_bonsai.md).
- Testing (how_to/testing.md): use `Bonsai_web_test.Handle` with `Handle.show`, `Handle.click_on`, `Handle.input_text` and `Handle.do_actions`, run as js_of_ocaml expect tests (`(inline_tests ((native dont_build_dont_run) (javascript build_and_run)))`). It also covers diffs, mocking time, and "Avoid Async Testing".
- bonsai_term (231 stars) applies the same model to terminal UIs. strace_ui (131) is a real app built on it.

### 4.4 Hardcaml hardware design

Sources: [hardcaml/docs/](https://github.com/janestreet/hardcaml/tree/master/docs) (~70 pages, from combinational logic to FFT and quicksort examples) and **[janestreet/hardcaml_agents_docs](https://github.com/janestreet/hardcaml_agents_docs)** (created 2026-05-15). The second is Jane Street's own set of **prompts written for AI agents**. `hardcaml/docs/using_ai.md` says these prompts "can be provided to AI models (e.g. via AGENTS.md files or context bundles)", and that Jane Street finds models "able to write testbenches quite well when given a few hand-crafted prompts". Files: `hardcaml_design_guideline.md` (575 lines), `hardcaml_simulation_guideline.md` (380), `hardcaml_variant_interfaces.md` (158). This is almost a ready-made skill (MIT-licensed).

Design rules (hardcaml_design_guideline.md):
- Module shape: `module type Config`, then `module Make (Config : Config)` containing `module I` / `module O` (`type 'a t = {...} [@@deriving hardcaml]`, `[@bits n]`), `let create (scope : Scope.t) (i : Signal.t I.t)`, and `let hierarchical ?instance scope i` via `Hierarchy.In_scope (I) (O)`.
- `[@@deriving hardcaml]` already includes sexp_of. **Never write `[@@deriving sexp_of, hardcaml]`.**
- Name signals with `let%hw x = ...`, `let%hw_var`, `let%hw.Always.State_machine sm = ...` and `let%subscope helper scope ...`. **Never use the `--` naming operator.**
- Use `of_unsigned_int ~width` / `of_signed_int ~width`. **Never `of_int_trunc`.** In sim, use `Bits.to_unsigned_int` / `to_signed_int`, never `to_int`.
- Omit `~enable:vdd` (it is the default). Registers driven by a next signal should use `Signal.reg`, not `Always.Variable.reg`. Combinational logic should be inline `mux2`, not `if_` inside Always, unless it is state-dependent.
- **Always parenthesize Hardcaml operators.** `&:` and `|:` have equal precedence and are left-associative, unlike Verilog. `*:` / `<:` are unsigned and `*+` / `<+` are signed.
- Chain 2–4 `mux2`s with `@@`. With 5 or more cases use `priority_select_with_default`. Use `Signal.cases ~default sel [...]` and `onehot_select`.
- Prefer `uextend` / `sextend` / `sel_bottom` over `uresize` / `sresize`. Index with `x.:(i)` and `x.:[hi, lo]`. Write unary operators as `~:(x)`, not `(~:) x`.
- Use `Reg_spec.create ~clock ~clear ()` or `Clocking.t`, `cut_through_reg`, `with_valid`, and the `Of_signal` / `Of_always` interface helpers.

Simulation rules (hardcaml_simulation_guideline.md):
- New tests should use **Hardcaml_lws** (effects-based cooperative tasks) on the cyclesim backend, through `Hardcaml_test_harness.Lws_harness.Make (Dut.I) (Dut.O)`.
- `Before_and_after_edge.t` distinguishes combinational outputs (`before_edge`) from registered ones (`after_edge`).
- Print `Bits.Hex.t` etc. in `[%message]`, and print waveforms inline in expect tests.

```ocaml
let%expect_test "my test" =
  Harness.run ~create:Dut.create (fun (h @ local) ~inputs ~outputs ->
    let open Bits in
    inputs.data <--. 42;
    Lws.step h;
    printf "result = %d\n" (to_unsigned_int !(outputs.after_edge.result)));
  [%expect {| result = ... |}]
```

The starter is [hardcaml_template_project](https://github.com/janestreet/hardcaml_template_project). It recommends the OxCaml switch (`opam switch 5.2.0+ox`). Related: [asic-puzzle-2026](https://github.com/janestreet/asic-puzzle-2026) (338 stars, a GDS reverse-engineering puzzle) has hardware-culture value but is not Hardcaml.

### 4.5 magic-trace / memtrace performance debugging

magic-trace ([README](https://github.com/janestreet/magic-trace), plus a [wiki](https://github.com/janestreet/magic-trace/wiki)) is the org's most-starred repo at 6,347 stars. It is the one repo that is not part of the batch-release flow: it was pushed 2026-10-19, has a Discord and real issues, and has a separate maintainer set.
- **Method:** Intel PT ring buffer → snapshot on a trigger → reconstruct every call, ~40ns resolution, with 2–10% overhead. Requires Linux on Intel (Skylake or later). VMs are mostly unsupported.
- **Commands:** `magic-trace attach -pid <pid>`, then Ctrl+C, which writes `trace.fxt.gz`. Open it at magic-trace.org, a Perfetto fork; keys are W/S zoom and A/D pan. `magic-trace run ./exe`. `-trigger '?'` gives a fuzzy symbol picker, `-trigger SYMBOL` names a symbol, and `-trigger .` uses `magic_trace_stop_indicator`. Pass `-trace-include-kernel` (root) to see kernel frames such as page faults.
- **Philosophy:** "In contrast to traditional perf workflows, magic-trace excels at hypothesis generation." Put stop-indicator functions in production code where interesting events happen: long scheduler cycles, slow requests, after a GC. They cost ~10µs only when a snapshot fires. It complements perf: perf samples, while magic-trace shows "all the function calls that a 70ns function was performing."

memtrace ([README](https://github.com/janestreet/memtrace), [docs/internal.md](https://github.com/janestreet/memtrace/blob/master/docs/internal.md)): link `memtrace` and call `Memtrace.trace_if_requested ()` at startup. Set `MEMTRACE=trace.ctf` and analyze with memtrace_viewer. It samples allocations via Memprof and knows when, if ever, each sample was collected, which makes it the tool for leaks.

Related: `core_bench` / `ppx_bench` (`let%bench "name" = ...`, run via `Inline_benchmarks_public.Runner.main` with `-linkall`); `tracing` (fxt writer); `ocaml_intrinsics` (rdtsc, popcnt and other instructions).

### 4.6 OxCaml: modes, locals, unboxed types, parallelism

Sources (all in [oxcaml/oxcaml:jane/doc/extensions/](https://github.com/oxcaml/oxcaml/tree/main/jane/doc/extensions), rendered at oxcaml.org/documentation): `_05-modes/{intro,syntax,reference}`, `_02-stack-allocation/{intro,reference,pitfalls}`, `_03-unboxed-types/{01-intro,02-or-null,03-block-indices,04-c-abi}`, `_04-parallelism/{01-intro,02-capsules}`, `_06-kinds/*`, `_07-uniqueness/*`, `_10-templates/*`, `_09-simd`, `_08-comprehensions`, `_11-miscellaneous-extensions/{zero_alloc_check,let-mutable,labeled-tuples,immutable-arrays,include-functor,...}`, `_01-tutorials/intro-to-parallelism-part-{1,2}`. Also `proposals/` and [tutorial-icfp25](https://github.com/oxcaml/tutorial-icfp25), which has 7 hands-on activities: data races and TSan, atomics, capsules, quicksort, local lists, merge sort, radix sort.

- **Modes vs types:** "Types describe what the data *is*, while modes describe how it is *used*". A mode is written `x @ mode`. In arrows, `a @ local -> b`. Beware precedence: in `a -> b -> c @ m`, `m` applies to `c`. The legacy defaults are `global aliased many nonportable uncontended forkable unyielding stateful read_write`.
- **Axes:**
  - Locality: `local` < `global`.
  - Contention: `uncontended`, `shared`, `corrupted` < `contended`.
  - Portability: `portable` < `shareable` / `corruptible` < `nonportable`.
  - Uniqueness: `unique` / `aliased`. Linearity: `once` / `many`.
  - Also yield, fork, statefulness and visibility.
  - Immutable / immediate types *mode-cross*.
- **Stack allocation:** use `stack_ {...}` to force it. That gives an error if the value escapes ("This value escapes its region"); without the keyword the compiler infers and silently heap-allocates. `let f (x @ local) = ...` is a promise not to let `x` escape, which makes it useful for API contracts (callbacks that must not capture), not just performance. `exclave_` returns into the caller's region, and `global_` fields can escape. Inference does not cross files, so annotate the mli. Pitfalls: tail calls, partial application with local params, typing of `@@` and `|>`. The legacy keyword syntax `local_` still appears throughout master-branch Jane Street code.
- **`[@zero_alloc]`** is checked statically, including callees. `[@zero_alloc opt]` applies to optimized builds only. Indirect calls count as allocating, while stack allocations are allowed.
- **Unboxed types:** layouts include `value`, `float64`, `bits32`, `bits64`, `word`, `vec128`, `void` and products `l1 & l2`. Types: `float#`, `int32_u`, `int64_u`, `nativeint_u`, `int8#`. Literals like `#1.0`. Unboxed tuples `#(a, b)`, unboxed records `#{ f : float# ; s : string }` with `t.#f`, and `t#` for the unboxed version of record `t`. `'a or_null` (`Null | This v`) is a non-allocating option. Kind annotations look like `type ('a : float64) t` and `type t : bits64`. Kinds like `immediate` and `value non_pointer` are documented in `_06-kinds`.
- **Parallelism** ([janestreet/parallel](https://github.com/janestreet/parallel)): `Parallel.fork_join2 par (fun par -> ...) (fun par -> ...)` returns an unboxed `#(a, b)`. Tasks must be `portable` / `shareable`, which gives data-race freedom at compile time. The scheduler is created once with `with_parallel` (work-stealing via `parallel.scheduler.work_stealing`). Use `Capsule` for mutable state shared across tasks. `handled_effect` uses `local` handler arguments to get effect-safe typed effects.
- **Templates:** `ppx_template` / `[%%template]` with `[@kind ...]` / `[@mode local]` for kind and mode polymorphism. It is used heavily on the base `oxcaml` branch.
- **Agent guidance in the compiler repo:** [oxcaml/AGENTS.md](https://github.com/oxcaml/oxcaml/blob/main/AGENTS.md), and `CLAUDE.md` is just `@AGENTS.md`. It says to build with `make -s boot-compiler` and to run `make -s test` before declaring success. Other rules: `make -s fmt`; lines under 80; "Use pattern-matching and functional programming idioms"; "Avoid `assert false` and other unreachable code"; don't disable warnings or tests; import frontend changes into Merlin with `external/merlin/scripts/import-ocaml-source.sh` and never hand-merge.

### 4.7 Smaller skill seeds

- **Async** ([async](https://github.com/janestreet/async), RWO ch.18): `Deferred.t`, `let%bind` / `let%map`, `Deferred.Or_error`, `Command.async_or_error`, and `Rpc` with versioned types (`Versioned_rpc`, `ppx_stable`). `expect_test_helpers_async` provides the test helpers.
- **Sexp everywhere** (sexplib, ppx_sexp_conv, ppx_sexp_message, sexp CLI): `[@@deriving sexp]` on every type, `[%message]` for errors and logs, and `sexp_grammar` for schemas.
- **patdiff / shexp / ecaml / vcaml:** narrower tooling. ecaml is a pattern for writing Emacs plugins in typed OCaml.
- **learn-ocaml-workshop** (723 stars, frozen 2022): an onboarding curriculum (snake, frogger, lumines, irc-bot). Useful for a teaching-oriented skill.

## 5. Contribution model and maintainers

- **Mirrored monorepo, batch export.** The archived [contribute page](http://web.archive.org/web/2025/https://opensource.janestreet.com/contribute/) says: "Internally we have a weekly release cycle... For each release, we export the changes to the public repositories and increase the version numbers". Changes are made on GitHub as PRs. Then "Someone at Jane Street will take responsibility for migrating the patch through our internal process", and the patch comes back in a later export.
- **Observed reality in 2026:** exports are much less frequent than weekly. On `janestreet/core` master, `public-release` commits are titled with versions like `v0.18~preview.133.03+642` and dated 2025-10-30, 2026-01-14, 2026-03-30, 2026-05-15, 2026-07-10 and 2026-11-03. On 2026-11-03, 337 of the 446 repos received the same export. Only 20 merged PRs show up in the search index for `janestreet/core` in total.
- **The `oxcaml` branch** of each library is exported alongside `master` (base@oxcaml: 2026-11-03, 2026-07-10, ...).
- **Requirements:** a DCO `Signed-off-by` (CONTRIBUTING.md in each repo, real name required) and the MIT license. Contributions must follow the style guide, and significant features need docs and tests.
- **Exceptions to the batch model:**
  - **magic-trace** is developed on GitHub directly. Top committers in the last 100 commits: `Xyene` (Tudor Brindus), `lamoreauxaj`, `Svetlitski`, `lnbrks`, `hlian`, `bnigito`, `cgaebel`. The original author is `trishume`.
  - **oxcaml/oxcaml** is developed in the open on GitHub: 413 PRs created since 2026-10-01. Top committers in the last 100 commits: `jvanburen`, `rricard`, `NickBarnes`, `xclerc`, `riaqn`, `liam923`, `TheNumbat`, `alecsinger`, `zackbach`.
  - **Notably, 28 of the last 100 oxcaml commits (2026-10-27 to 2026-11-07) carry an Anthropic Claude co-author trailer.** 4 have author names tagged "(AI)", and the repo uses claude-code-action. Jane Street is actively using coding agents on its compiler, so an OxCaml skill has a live target audience.
- **Visible maintainers on the batch-exported repos** (merge and sync commits, from GitHub logins): `public-release` (the export bot), `xclerc` (Xavier Clerc), `aalekseyev` (Arseniy Alekseyev), `staronj`, `dkalinichenko-js` / `d-kalinichenko`, `dra27-js` (David Allsopp, merges external PRs on core). On base, `tov` / `jtov-js` (Jesse Tov) also appear.
- **Docs hosting:** API docs are at ocaml.janestreet.com/ocaml-core/latest/doc/. **opensource.janestreet.com now 301-redirects to github.com/janestreet**, so the style guide, contribute page and patdiff pages are reachable only via the Wayback Machine.

## 6. Skill-candidate ranking

| Rank | Skill | Primary evidence | Readiness |
|---|---|---|---|
| 1 | Hardcaml hardware design | hardcaml_agents_docs (JS-authored agent prompts) + hardcaml/docs (~70 pages) + template project | Highest: first-party agent guidance already exists |
| 2 | Write OCaml the Jane Street way | Archived style guide + ppx_js_style rules + base README + base/core source patterns | High: explicit rules, linter-backed |
| 3 | Expect-test driven development | ppx_expect README.mdx + expect_test_helpers_base intf + style guide "expect tests preferred" | High |
| 4 | Bonsai / Incremental UI | bonsai_web/docs/bonsai_best_practices.md (Bad/Good pairs) + testing.md + incremental doc parts 1–8 | High |
| 5 | OxCaml modes / locals / unboxed / parallel | oxcaml jane/doc/extensions (~50 pages) + AGENTS.md + tutorial-icfp25 + parallel README + `oxcaml` branches | High, but the docs move fast; pin a commit |
| 6 | magic-trace / memtrace perf debugging | magic-trace README + wiki; memtrace README + JS blog post | Medium: tool-usage skill, needs Intel PT hardware |
| 7 | Async + RPC + versioned Stable types | async READMEs, RWO ch.18, ppx_stable | Medium: docs are thinner |

## 7. Local copies used

Shallow clones are in `/tmp/claude-1000/-home-ops-Project-jane-skills/67d724a0-997a-4f0b-9855-39f262d45661/scratchpad/src/`. The archived style guide HTML is at `.../scratchpad/web/standards_wb.html`. Both are scratch and will not persist; re-clone from the URLs above.
