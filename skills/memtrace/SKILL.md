---
name: memtrace-and-magic-trace
description: Find OCaml memory leaks and allocation problems with Jane Street's Memtrace, and diagnose short, rare latency events with magic-trace (Intel Processor Trace), following Jane Street's own write-ups. Use when an OCaml process's memory grows, when you need to know which allocation sites survive or what the heap held at a given moment, when a queue may be backing up, when writing a custom analysis over a .ctf trace, or when a latency spike is too short or too rare for a sampling profiler. Includes a compiled command-line analyzer (live-at-end, heap snapshot, lifetimes over time) with expect tests and canaries, plus the toolchain traps that make memtrace hang or misread traces on OCaml 5.
---

# Memtrace and magic-trace

## Overview

Two Jane Street tools answer two questions that ordinary profilers answer badly:

| Question | Tool | Why not a sampling profiler |
|---|---|---|
| What is holding my memory, and who allocated it? | **Memtrace**: statistical allocation tracing built on OCaml's `Gc.Memprof` | Profilers rank by how much was *allocated*. A leak is about what *survives* |
| What happened in the 10 ms before that latency spike? | **magic-trace**: Intel Processor Trace in a ring buffer, snapshotted on a trigger | Samples arrive every ~250 µs, too coarse for microsecond events |

Memtrace "is a streaming client for OCaml's Memprof, which generates compact traces of a program's memory use". At Jane Street "it has been used to find memory leaks in real systems, and it's one of the core tools we teach in our Performance analysis" teach-in. Luke Maurer's blog post puts the method in one line: "we're finding we can often find a space leak using just some basic data visualization and the human ability to say “Hang on, what's that?”"

How this skill was checked:
- **Memtrace** was run, not just read. `examples/` holds two workloads, a never-evicted cache and a queue whose producer outpaces its consumer. It also holds `live.exe`, a command-line analyzer, and expect tests that trace both workloads under real `Gc.Memprof` sampling.
- **magic-trace** could not be run here. This machine is an AMD Threadripper, and magic-trace needs Intel Processor Trace. The section on it is taken from Jane Street's post and the System Jitter talk.

## Step 0: Toolchain (2026-11-07; the OCaml 5.4 rows were run on this machine)

| memtrace | OCaml | Tracing to process exit (`trace_if_requested`) | `stop_tracing` and keep running | Trace format |
|---|---|---|---|---|
| 0.2.3 (opam default) | 4.11–4.14 | works *(per the 2020 blog; not run here)* | works | v002 |
| 0.2.3 | 5.0–5.2 | **fails**: OCaml 5.0–5.2 shipped without `Gc.Memprof` *(not run here)* | fails | v002 |
| 0.2.3 | **5.4** (and 5.3, which introduced the same `Memprof` semantics; not run here) | works | **hangs the process** at the next GC that frees a sampled block | v002 |
| v0.18 preview (`janestreet-bleeding`) | 5.4 | works | works | **v003** |

Why 0.2.3 hangs on 5.3 and later:
- OCaml 5.3's `Gc.Memprof.stop` documents that "Promotion and deallocation callbacks from a profile may run after [stop] is called, until [discard] is applied to the profile".
- memtrace 0.2.3 never calls `discard`. Its `stop` takes the tracer lock to close the writer and never releases it.
- The next deallocation callback therefore spins forever in `lock_tracer`.

The upstream issue (janestreet/memtrace#22, "Support 5.3 statmemprof") is still open. Master's rewritten tracer calls `Gc.Memprof.discard` and does not hang. The `opam install` message for 0.2.3 still says that tracing the current process is unsupported on multicore OCaml, which is stale for 5.3 and later.

Consequences:
- **On OCaml ≥ 5.3 with 0.2.3,** only trace to process exit, and analyse in a *different* process.
- **Writer and reader must agree on the format.** The 0.2.3 tools (`memtrace_hotspots`, `memtrace_dump_trace`) reject v0.18 traces with `malformed trace: trace format v003, but expected v002`.
- **The v0.18 API differs.** `Collect` and `Promote` take `(Obj_id.t * Domain_id.t)`, so the 2020 blog's analysis program needs a one-line change to compile.
- **v0.18 does not install the `memtrace_*` command-line tools.** Use the viewer, or an analysis like `examples/`.

## Step 1: Collect a trace

Link `memtrace`, then start tracing at the top of `main`, after any daemonising fork, as the README says:

```ocaml
let () =
  Memtrace.trace_if_requested ();
  match Sys.argv with
  | [| _; "leak" |] -> Memtrace_live.Workloads.leaky_server ~requests:20_000
  | [| _; "backlog" |] -> Memtrace_live.Workloads.backlogged_pipeline ~ticks:200_000
  | _ ->
    prerr_endline "usage: workload.exe leak|backlog";
    exit 2
;;
```

```sh
MEMTRACE=trace.ctf ./main.exe                       # default sampling rate
MEMTRACE=trace.ctf MEMTRACE_RATE=1e-3 ./main.exe    # denser, for small or short programs
```

Sampling rate:
- The default rate is tuned for production. The library notes that rates "larger than about 1e-4 will have some performance impact".
- For a short test program, raise it. At the default rate, the 20,000-request example produced an 864-byte trace with almost no samples. At `1e-3` it produced about 16,000 samples.

Overhead is the reason memtrace exists. The blog contrasts it with the older Spacetime profiler: it "can run with low enough overhead to be used in production systems".

## Step 2: Rank what survives, not what was allocated

This is the core of leak hunting. Here is the leak in the example:

```ocaml
let cache : (int, Bytes.t) Hashtbl.t = Hashtbl.create 16
let remember i = Hashtbl.replace cache i (Bytes.create 1024)
let scratch () = ignore (Sys.opaque_identity (Array.make 64 0))
```

`scratch` allocates about 5× more than `remember`. An allocation ranking such as `memtrace_hotspots` puts it on top: 82% of allocation volume, against 16% for the leak. Restricting to allocations **never collected by the end of the trace** turns that around. The blog does the same thing with the viewer filter "Only show allocations: Live somewhere between".

```ocaml
let live_at_end filename =
  let survivors, _, _, word_bytes = read filename in
  rank ~word_bytes survivors
;;
```

```ocaml
let%expect_test "allocation volume points at the churn, survivors point at the leak" =
  let file = trace_to_file ~f:(fun () -> Memtrace_live.Workloads.leaky_server ~requests:20_000) in
  print_endline "ranked by allocation volume:";
  top 1 (Memtrace_live.allocated file);
  print_endline "ranked by what is still live at the end:";
  top 1 (Memtrace_live.live_at_end file);
  [%expect {|
    ranked by allocation volume:
    Memtrace_live__Workloads.scratch (src/workloads.ml:4), majority: true
    ranked by what is still live at the end:
    Memtrace_live__Workloads.remember (src/workloads.ml:3), majority: true
    |}]
;;
```

From the command line:

```sh
$ live.exe trace.ctf
   20562.5 KB  91.3%  Memtrace_live__Workloads.remember (src/workloads.ml:3)
    1023.4 KB   4.5%  Memtrace_live__Workloads.scratch (src/workloads.ml:4)
```

The byte estimate is (samples ÷ sampling rate) × word size: about 20.1 MB here, against 20,000 × 1,032 bytes ≈ 20.6 MB actually retained. Allocations made inside `Stdlib` (such as `Hashtbl.replace`) are charged to the first frame outside `Stdlib`, so the report names your code.

Not everything live at the end is a leak. The blog separates three phases:
- startup state;
- "A gradual accumulation that continues throughout processing";
- the output built at the end.

Only the middle one is suspicious. Narrow the analysis to allocations made in the middle of the run that are still live at the end.

## Step 3: When nothing leaks but memory balloons, look at the heap at a moment, and at lifetimes

If most of what is live at the end was allocated recently, the blog's conclusion is that it is not a straightforward leak, so "we can rule that out". The next tools are these:

- **Snapshot at time t.** Look at allocations made before t that were still live after it: `live.exe trace.ctf --at 0.4`. In the backlogged example, the snapshot is mostly items made by `produce`.
- **Lifetimes over time.** For allocations whose backtrace contains a function, plot the median lifetime against allocation time: `live.exe trace.ctf --lifetimes Memtrace_live__Workloads.produce`. A queue whose producer outpaces its consumer shows lifetimes that grow with time. The blog's diagnosis: "if the producer outpaces the consumer and no backpressure is applied, then the queue can balloon to larger and larger sizes."

Two cautions:
- **Truncation.** Allocations never collected are counted as freed at the end of the trace, so lifetimes for late allocations are cut short. "This effect is particularly pronounced at the end". In the example, the median lifetime rises from 0.09 s to 0.50 s and then falls back to 0.05 s at the end. That fall is the cut-off, not a recovery.
- **Baseline.** Compare against a known-good run. The example's test checks that the backlogged pipeline's peak median lifetime is more than 10× the balanced pipeline's. It does not assert any absolute number, because timestamps are wall-clock time.

## Step 4: Write your own analysis when the viewer can't

"Fortunately, the Memtrace library itself offers a simple yet powerful way to slice the data any way you can think of." The reader API is small:
- `Reader.open_` and `Reader.iter` stream events;
- `Alloc` events carry `obj_id`, `nsamples`, `source` and a backtrace of location codes;
- `Reader.lookup_location_code` resolves those codes into `{filename; line; defname}`;
- `Collect` and `Promote` events refer back to an `obj_id`.

`examples/src/memtrace_live.ml` is about 130 lines that do the live-at-end, snapshot and lifetime analyses.

For tests of tracing code, trace in-process and read the file back. This needs v0.18, because on 0.2.3 with OCaml ≥ 5.3 `stop_tracing` hangs:

```ocaml
let trace_to_file ~f =
  let filename = Filename.temp_file "memtrace_live" ".ctf" in
  let tracer = Memtrace.start_tracing ~context:None ~sampling_rate:1e-3 ~filename in
  f ();
  Memtrace.stop_tracing tracer;
  filename
;;
```

Memprof samples at random, so test the **shape** of the result (which site ranks first, whether it holds the majority) and never exact counts or shares. A first version of this suite asserted "≥ 90%". The share hovered around 90%, so the test failed 2 runs in 15 until the assertion was changed to "majority".

## magic-trace: when the event is shorter than a sample

From Tristan Hume's post:
- Sampling profilers "interrupt the program every 250 microseconds or so". For systems that wait on packets and must respond far faster than that, they "are approximately useless for diagnosing latency issues on that scale".
- Intel Processor Trace records all control flow "with timing information accurate to around 30ns".
- magic-trace keeps a ring buffer and snapshots "a trace of around 10ms leading up to a function call you chose to instrument". You then view it in a Perfetto timeline.

Use it like this:
- **Capture.** Call `Magic_trace.take_snapshot` (or choose any existing function with the fuzzy-finder), then run `magic-trace attach`. The trigger uses a hardware breakpoint, so it "requires no cooperation from the target, no overhead when not attached".
- **Trigger on the tail.** Put the snapshot call behind your own condition, such as a round trip that exceeded the median plus a margin. Tudor Brindus's jitter hunt used about 300 ns.
- **Cost and limits.** Overhead is 2–20%, usually under 5% in their measurements. It needs a post-Skylake Intel CPU and is unsupported on many VMs: "AMD doesn't yet". Decoding is slow, so keep snapshots short.
- **What it shows that nothing else does.** Whether a function was "called 10 times more than you expected or one call to it taking 10 times longer than expected". In Brindus's talk it showed NIC driver interrupts and timer ticks landing on an isolated core. See the `low-latency` skill for that workflow.

On AMD, there is no Processor Trace equivalent that magic-trace supports. Fall back to instrumentation (explicit timestamps around the suspect path), and use `perf` only for throughput questions.

## Rules

**Always**
- Check the memtrace and OCaml versions against the table in Step 0 before tracing.
- Rank by survival (live at end, or live across a time t) when hunting leaks, not by allocation volume.
- Raise `MEMTRACE_RATE` for short runs, and leave the default in production.
- Read traces with tools of the same memtrace version that wrote them.
- In tests, assert shapes and comparisons against a baseline, never exact sampled numbers or wall-clock times.

**Never**
- Call `Memtrace.stop_tracing` and keep running on memtrace 0.2.3 with OCaml ≥ 5.3.
- Read the end of a lifetime plot as recovery without accounting for truncation.
- Treat "live at end" as "leaked" without separating startup state and final output from mid-run accumulation.
- Reach for a sampling profiler to explain a microsecond-scale tail event.

**Prefer**
- A 50-line custom analysis over squinting at a viewer that cannot express the question.
- Comparing against a known-good run over reading absolute numbers.

## Verification

`scripts/gate.sh [switch]` (default `hardcaml-bleeding`, which has memtrace v0.18) runs four checks:
1. It refuses any switch without memtrace v0.18.
2. It runs `examples/` under `dune runtest`. Three expect tests trace real workloads in-process. They were checked over 20 clean runs with no failures.
3. It checks that every `ocaml` block in this file is the compiled code.
4. It requires three canaries to fail as expect diffs: the leak is fixed, `live_at_end` ranks every allocation, and the pipeline is balanced.

## Sources

- **Luke Maurer, "Finding memory leaks with Memtrace"** (2020). https://blog.janestreet.com/finding-memory-leaks-with-memtrace/
- **Memtrace README.** https://github.com/janestreet/memtrace. Also issue #22 and `src/memprof_tracer.ml` on master (v0.18 preview) versus 0.2.3 in opam.
- **OCaml 5.4 `Gc.Memprof`** (`gc.mli`): the stop/discard semantics.
- **Tristan Hume, "Magic-trace: Diagnosing tricky performance issues easily with Intel Processor Trace"** (2022). https://blog.janestreet.com/magic-trace/
- **Tudor Brindus, "System Jitter and Where to Find It"** (tech talk). https://www.janestreet.com/tech-talks/system-jitter-and-where-to-find-it/

Quote gate: `tools/fetch_corpus.sh <dir> $(cat skills/memtrace/sources.txt)` then `python3 -I tools/verify_quotes.py <dir> skills/memtrace/SKILL.md`.
