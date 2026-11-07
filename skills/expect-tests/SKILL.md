---
name: expect-test-driven-development
description: Write tests the Jane Street way, as expect tests. Start from a blank [%expect] block, let the runtime fill it in, judge the diff, then promote it, and design the printed output so it tells a concise story. Use when writing or reviewing OCaml tests with ppx_expect, adding regression tests for a bug fix, exploring an API or dataset with repeatable output, making nondeterministic output testable, pairing snapshot tests with Base_quickcheck properties, or bringing the snapshot style to another language (Jest, Rust expect-test, cram). Includes a compiled example project and a gate with canary mutations.
---

# Expect-Test-Driven Development

## Overview

An expect test is a block of code that prints things, followed by an `[%expect]` block that holds what it printed. You write the code and leave the block empty. The test runner records the real output and shows it as a diff. You read the diff, and if it is right, you promote it into the source file. From then on, any change in behaviour shows up as a diff.

Yaron Minsky introduced the idea to OCaml in 2015, borrowing it from Mercurial's unified tests and from cram. James Somers's 2023 post describes how it feels day to day: "makes test-writing feel like a REPL session, or like exploratory programming in a Jupyter notebook". According to Somers, expect tests "form the better part of our test suite, complemented in places by property-based testing."

**Toolchain.** Everything below was compiled and run against ppx_expect v0.17.3, expect_test_helpers_core v0.17.0, base_quickcheck v0.17.1 and OCaml 5.4.0. The code blocks are copied from `examples/`, and `scripts/gate.sh` fails if they drift apart.

Two features in the current ppx_expect README are missing from v0.17.x:
- `[%expectation]`, which is an "Uninterpreted extension" on v0.17;
- the runner's `-verbose` flag, which the README dates to December 2024.

Check your version before using either.

## Core Philosophy

"Testing tools matter because the smoother the process is, the more tests people will write." Expect tests remove the slowest part of writing a test, which is typing out the expected value. The thinking does not go away. It moves from writing an assertion to judging a diff, and it moves into designing what to print.

Minsky gave three reasons unified tests are good, and none of them depends on the shell:
- they combine "the scenario and the output of that scenario (and comments) into one readable file";
- the file is constructed automatically;
- they display "test failures as easy-to-interpret diffs".

Somers puts the core of it in one line: "In expect tests, regressions are just diffs."

Dumping state also checks more than hand-picked assertions do. In Somers's order book example, a bug that mangles order sizes slips past targeted assertions that never mention size, but the expect test catches it. Expect tests "make it easier to implicitly assert more. Ironically, they capture things you never expected them to."

## The Loop

### 1. Set up dune once

```lisp
(library
 (name book_test)
 (libraries book core expect_test_helpers_core)
 (inline_tests)
 (preprocess
  (pps ppx_jane)))
```

Put tests in their own directory and test the public interface: "Tests live in their own directory and are written against the public interface, or, when testing private implementations, against a For_testing module exported just for that purpose." The example's `Book.For_testing.total_size` is exactly that.

### 2. Print, then leave the block blank

"The %expect block starts out blank precisely because you don't know what to expect. You let the computer figure it out for you." Write the scenario, print the state you care about, and put `[%expect {||}]` after it.

Use one block per step of a scenario. "Each [%expect] block matches all the output generated since the previous [%expect] block (or the beginning of the test)." Each block therefore shows what a single step did.

### 3. Run it and read the diff

`dune runtest` fails and prints a diff of the source file. It also writes `<file>.ml.corrected` beside it. Below is the real diff for the crossing-order test in `examples/`:

```diff
   let (_ : Book.t) = step book (order 4 Buy ~price:102 ~size:5) in
-  [%expect {||}]
+  [%expect {|
+    fill #4 vs #1: 2 @ 101
+    fill #4 vs #2: 2 @ 101
+    fill #4 vs #3: 1 @ 102
+      Sell 102 x 4  #3
+      ----
+    |}]
```

### 4. Judge the diff before you accept it

Promoting a diff asserts that the output is correct. Somers did not trust his first run: "Naturally my first implementation had all kinds of bugs—some entries in the table looked wrong." The runtime tells you what the code does. Only you can say whether that is what it should do.

*(derived)* Before promoting, check each new line against the specification, out loud or in the commit message. For the diff above:
- The buy fills #1 and #2 at 101 before touching #3 at 102. That is price priority.
- It fills #1 before #2 at the same price. That is time priority.
- It trades at the resting price, not at 102.
- The leftover 4 of #3 stays on the book.

If you cannot say why a line is right, you have not reviewed it, you have only accepted it.

### 5. Promote

Run `dune promote`, or press the editor key that applies the `.corrected` file. Ian Henry describes the loop: "You save the file and you immediately see a diff of all of your tests, and then there's one button that lets you copy in the output to promote it to this is the good version."

`dune runtest --auto-promote` is right for exploration, and Minsky uses it that way in *Repeatable exploratory programming*. It is wrong as a habit for tests you commit, because it promotes bugs just as readily as fixes.

### 6. Shape the output until it tells a story

"Thus the art of expect tests is in producing output that tells a concise story, capturing the state you care about." The best tests "take pains to elide unnecessary detail. Usually they use helper functions and custom pretty-printers to craft the output."

The example shows the difference. Its first test dumps the full book with `print_s [%sexp ...]`, which takes 15 lines of record fields for two orders. The crossing test uses a ten-line printer instead and fits the whole scenario in nine output lines:

```ocaml
let print_ladder book =
  let line (o : Book.Order.t) = printf "  %-4s %d x %d  #%d\n" (Sexp.to_string [%sexp (o.side : Book.Side.t)]) o.price o.size o.id in
  List.iter (List.rev (Book.orders book Sell)) ~f:line;
  print_endline "  ----";
  List.iter (Book.orders book Buy) ~f:line
;;

let step book o =
  let book, fills = Book.add book o in
  List.iter fills ~f:(fun f ->
    printf "fill #%d vs #%d: %d @ %d\n" f.incoming_id f.resting_id f.size f.price);
  print_ladder book;
  book
;;
```

```ocaml
let%expect_test "a crossing order fills at the resting price, oldest first" =
  let book =
    List.fold
      [ order 1 Sell ~price:101 ~size:2; order 2 Sell ~price:101 ~size:2; order 3 Sell ~price:102 ~size:5 ]
      ~init:Book.empty
      ~f:(fun book o -> fst (Book.add book o))
  in
  print_ladder book;
  [%expect {|
    Sell 102 x 5  #3
    Sell 101 x 2  #2
    Sell 101 x 2  #1
    ----
    |}];
  let (_ : Book.t) = step book (order 4 Buy ~price:102 ~size:5) in
  [%expect {|
    fill #4 vs #1: 2 @ 101
    fill #4 vs #2: 2 @ 101
    fill #4 vs #3: 1 @ 102
      Sell 102 x 4  #3
      ----
    |}]
;;
```

The opposite mistake is just as real. Ron Minsky on the podcast: "A really good expect test is where one has really thought carefully about what data do I actually want to visualize?" Ian Henry names the failure mode: "it's a real failure case to just say like, oh, okay, tell me if anything possibly changes". The effort pays off twice, because "the work that you do to visualize your state better also makes it easier to change your program over time."

Andrew Ray says the same about Hardcaml's ASCII waveforms: limited screen space means "you have to think carefully about what information to expose (some might argue this is an advantage)." The `hardcaml` skill has the waveform version.

### 7. Keep it as a regression test

The output you explored with becomes documentation and a regression guard at once. Minsky: "it might make sense to leave in these little experiments as regression tests". A table of inputs and outputs is often clearer than prose:

```ocaml
  [%expect {|
    id  side  price  bid offer
    1   Buy   99      99     -
    2   Buy   100    100     -
    3   Sell  102    100   102
    4   Sell  100     99   102
    5   Sell  101     99   101
    |}]
```

## Patterns

### Errors: print them, do not let them escape

If an exception escapes a test, the runner attaches it to the test as `[@@expect.uncaught_exn]`. That record includes a backtrace, and v0.17 flags it with a CR saying backtraces "are fragile". Use `require_does_raise` instead, so the error is printed as normal output:

```ocaml
let%expect_test "a non-positive size is rejected" =
  require_does_raise [%here] (fun () -> Book.add Book.empty (order 1 Buy ~price:100 ~size:0));
  [%expect {|
    ("order size must be positive" (
      order (
        (id    1)
        (side  Buy)
        (price 100)
        (size  0))))
    |}]
;;
```

On v0.17, `require_does_raise` takes `[%here]` first; the current README omits it. Prefer errors that carry data (`raise_s [%message ... (order : Order.t)]`), because the printed error then shows which input caused it.

### Nondeterminism: censor it before it reaches the block

Time, PIDs, hash-table order and temporary paths make a test flaky. Capture the output with `[%expect.output]`, transform it, then print it again:

```ocaml
let%expect_test "censor what is not deterministic before it reaches the block" =
  stamp "book opened";
  let censor = String.map ~f:(fun c -> if Char.is_digit c then 'X' else c) in
  print_string (censor [%expect.output]);
  [%expect {| XXXX-XX-XX XX:XX:XX.XXXXXXXXXZ book opened |}]
;;
```

To apply the same censoring to a whole file, override `Expect_test_config.sanitize`. Sort lines whose order is not deterministic. For time-dependent logic, a fake clock beats censoring, because censored output can no longer tell you whether the timing was right.

### Properties next to scenarios

Minsky's original pitch already drew the line: "sometimes, you don't want to write down properties – what you want is to write your tests in terms of simple, concrete scenarios." Use both kinds of test:
- **Scenarios** show what happens.
- **Properties** state what must always hold.

When a property test passes it prints nothing, so its `[%expect]` block stays empty, and a failure shows up as a diff like any other:

```ocaml
let%expect_test "matching conserves size and never leaves the book crossed" =
  Base_quickcheck.Test.run_exn
    (module struct
      type t = Book.Order.t list [@@deriving sexp_of]

      let quickcheck_generator = Base_quickcheck.Generator.list order_generator
      let quickcheck_shrinker = Base_quickcheck.Shrinker.list Base_quickcheck.Shrinker.atomic
    end)
    ~f:(fun orders ->
      let book, filled =
        List.fold orders ~init:(Book.empty, 0) ~f:(fun (book, filled) o ->
          let book, fills = Book.add book o in
          book, filled + List.sum (module Int) fills ~f:(fun f -> f.size))
      in
      let added = List.sum (module Int) orders ~f:(fun o -> o.size) in
      [%test_result: int] (Book.For_testing.total_size book + (2 * filled)) ~expect:added;
      match Book.best_bid book, Book.best_offer book with
      | Some bid, Some offer -> assert (bid < offer)
      | _ -> ());
  [%expect {||}]
;;
```

Two details matter here:
- **Keep generated values small.** The generator keeps prices within 95–105 and sizes within 1–10, so orders actually cross. Unbounded integers would almost never trade, and their sums could overflow.
- **Failures reproduce.** Base_quickcheck's `default_config` uses a fixed `Deterministic` seed (see `base_quickcheck/test.ml`), so a failing case comes back on every run.

### Writing the expectation first (classic TDD)

You can still write the expected output by hand before the code exists, and a wrong implementation then fails just as it would with an assertion. Somers: "The difference is that I don't have to do that." Use hand-written expectations when the specification is sharper than your trust in the code: protocol encodings, formats, and anything a counterparty depends on. Use blank blocks to explore.

### Fixing a bug *(derived)*

1. Write a test whose output shows the bug, and promote it. The wrong output is now on record, and reviewers can see it.
2. Fix the code. The test's diff now shows the behaviour changing from wrong to right, which is the most reviewable form of a bug fix.
3. Leave the test in place.

### Beyond OCaml

Somers points to the same idea elsewhere: "Other languages call these “snapshot” tests—see for example Rust's expect-test, which seems to have been inspired by our library, or Javascript's Jest." Cram does the same for shell sessions. The loop above carries over unchanged: blank expectation, read the diff, judge, promote, shape the output. What usually needs work is step 5, a one-key promote, which Ian Henry rebuilt for himself in Janet.

### Where expect tests stop

Expect tests cover the tests you think to write. Doug Patti, on adding whole-system exploration: "for all the careful tests that you think to write, there are some things you can only learn by experiencing that chaos." For distributed or concurrent behaviour, use deterministic simulation as well. See the `deterministic-simulation` and `property-based` skills.

## Mechanics (v0.17)

| Construct | Behaviour |
|---|---|
| `[%expect {\|\|}]` | Matches output since the previous block. Indentation and blank lines around the content are normalised |
| `[%expect_exact "..."]` | Byte-exact match, no normalisation |
| `[%expect.output]` | Returns the output captured so far as a string, for post-processing |
| `[%expect.unreachable]` | Asserts control never gets here. A block that is never reached is rewritten to this |
| `[@@expect.uncaught_exn {\|...\|}]` | Records an escaped exception. The test must then raise on every run |
| Output after the last block | Appended as a new `[%expect]` (or `[@@expect.trailing]` in Async) |
| A block reached several times (in a function or functor) | Passes only if every visit sees the same output; otherwise the correction lists each output |
| `Expect_test_config` in scope | Hooks: `sanitize`, `run`/`IO` (Async), trailing-output syntax |

## Rules

**Always**
- Start new tests with a blank `[%expect {||}]` and let the runtime fill it in.
- Read every promoted line and be able to say why it is correct.
- Write printers that show the state that matters and leave out the rest.
- Use one `[%expect]` per step of a scenario.
- Test through the public interface or a `For_testing` module.
- Print errors with `require_does_raise`, or with `Or_error`/`sexp` values. Never let them escape with a backtrace.
- Make output deterministic: censor, sort, use fake clocks and fixed seeds.

**Never**
- Auto-promote output you have not read, especially output an agent or a refactor produced.
- Dump whole data structures when a few lines of a custom printer tell the story.
- Commit output that contains timestamps, absolute paths, PIDs, addresses or backtraces.
- Edit a promoted block by hand to make a failing test pass. Fix the code, or re-promote after judging the new output.

**Prefer**
- Expect tests to hand-written assertion chains. Somers: "Classical assertion-style unit tests still have their place—just a much smaller one."
- Tables and diffs of state to prose.
- A property test next to scenario tests when an invariant can be stated.
- Bounded generators that produce interesting cases over unbounded defaults.

## Review checklist

1. Does each `[%expect]` block show the effect of exactly one step?
2. Can a reader tell from the output alone what the scenario checks?
3. Is anything in the output irrelevant, nondeterministic or environment-specific?
4. Was every changed line in this diff judged, not just accepted?
5. Does a bug fix come with a test that showed the bug?
6. Is there an invariant that deserves a property test next to these scenarios?
7. Would the output still read clearly after someone adds a field to the type? If not, print a projection of the type rather than all of it.

## Verification

`scripts/gate.sh [switch]` checks three things:
1. `examples/` passes `dune runtest`.
2. Every `ocaml` block in this file appears verbatim in `examples/`.
3. Three canary mutations each fail an expect test, as a diff rather than a build error:
   - the size of a resting order is multiplied by 100, Somers's own example;
   - time priority breaks for sells;
   - a buy at exactly the offer price no longer trades.

It runs `dune` at `nice 19` with 4 jobs in the opam switch you name (default `jane-skills`).

## Sources

- **Yaron Minsky, "Testing with expectations"** (2015). https://blog.janestreet.com/testing-with-expectations/
- **Yaron Minsky, "Repeatable exploratory programming"** (2018). https://blog.janestreet.com/repeatable-exploratory-programming/
- **James Somers, "What if writing tests was a joyful experience?"** (2023). https://blog.janestreet.com/the-joy-of-expect-tests/
- **Carl Eastlund, "Quickcheck for Core"** (2015). https://blog.janestreet.com/quickcheck-for-core/. Background on why generator distributions matter; the API it shows has since been replaced by Base_quickcheck.
- **Doug Patti, "Getting from tested to battle-tested"** (2025). https://blog.janestreet.com/getting-from-tested-to-battle-tested/
- **Andrew Ray, "Using ASCII waveforms to test hardware designs"** (2020). https://blog.janestreet.com/using-ascii-waveforms-to-test-hardware-designs/
- **ppx_expect README** (master, MIT). https://github.com/janestreet/ppx_expect. Matching rules, reachability, exceptions, output capture, configuration.
- **Signals and Threads, "Building Tools for Traders"** (Ian Henry with Ron Minsky, Ep. 23, 2025), 01:09:52–01:18:43. https://signalsandthreads.com/building-tools-for-traders/

Quote gate: `tools/fetch_corpus.sh <dir> $(cat skills/expect-tests/sources.txt)` then `python3 -I tools/verify_quotes.py <dir> skills/expect-tests/SKILL.md`.
