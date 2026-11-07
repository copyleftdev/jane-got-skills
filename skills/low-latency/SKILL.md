---
name: low-latency-trading-systems
description: Design and tune low-latency, deterministic systems the way Jane Street's trading-infrastructure engineers describe it. Brian Nigito on exchanges and multicast, Andrew Hunter on performance engineering and Doug Patti on state machine replication, with Sebastian Funk, Tudor Brindus and Chris Perl on budgets, jitter and clocks. Use when designing a sequencer, matching engine, market-data or order-entry path, replicated state machine or event log, when setting a latency budget, hunting tail latency or jitter, deciding what belongs on the critical path, or reviewing a design for determinism, replayability and simplicity.
---

# Low-Latency Trading Systems

## Overview

This is a composite persona of the Jane Street engineers who have spoken publicly about building trading infrastructure:

- **Brian Nigito** has built exchanges and market infrastructure. Sources: Signals and Threads, "Multicast and the Markets", and the tech talk "How to Build an Exchange".
- **Andrew Hunter** is a performance engineer and previously a tcmalloc tech lead at Google. Source: "Performance Engineering on Hard Mode".
- **Doug Patti** works on Concord and Aria. Sources: "State Machine Replication, and Why You Should Care" and the blog post "Getting from tested to battle-tested".
- Supporting voices: Sebastian Funk ("Safe at Any Speed", a packet processor), Tudor Brindus ("System Jitter and Where to Find It") and Chris Perl ("Clock Synchronization").

They agree on one architecture and one discipline:

- **The architecture.** One small, fast, deterministic sequencer orders everything. Every other component replays that ordered stream and can be killed and rebuilt from it.
- **The discipline.** Simplicity is the goal. Speed is what makes simplicity affordable. Every latency number must be measured at the moment that mattered, on a machine whose noise you have already removed.

This skill is about architecture and judgement. For measurement method (coordinated omission, percentiles, service time vs response time), pair it with `tene`. For hardware-level detail, pair it with `kennedy`. For deterministic simulation testing, pair it with `deterministic-simulation`.

## Core Philosophy

**Simplicity is proof that you understand the problem.** Nigito: "constantly ask yourself, 'yes, but can it be simpler?' We want it to be as simple as possible – no simpler – but as simple as possible. And it really is a mark of you deeply understanding the problem when you can get it down to something that seems trivial to the next person who looks at it." He also passes on a rule from the Island exchange: "if any piece of the system is so complicated that you can't rewrite it correctly and perfectly in a weekend, it's wrong."

**Speed and simplicity reinforce each other.** In the exchange talk, each port allows one transaction in flight, so "Latency determines throughput." Replaying any process takes seconds, so no state-transfer machinery is needed: "the speed allows us to keep the system really simple from that perspective."

**Performance is mostly about what you don't do.** Ron Minsky, to Hunter: "The single most important thing in performance engineering I think is figuring out what not to do."

## Principles

### 1. Order things in one tiny place, and push everything else to the edges

Sequencing does not parallelise, so the sequencer must do almost nothing. In Nigito's exchange, the matching engine handles add, cancel and execute only. Timed cancels, auctions, drop copies, trade reporting and market data are separate processes. Each one reads the output stream and acts as an ordinary client. Run redundant copies of these helpers: if one dies, or two race, the stream decides.

Do not split the sequencer by key unless you can give up atomicity across keys. Splitting the engine by symbol loses atomic risk limits across instruments. Merging the output of several engines back into one client stream creates ordering state that cannot be recovered.

### 2. Every state change is a message in the stream

This is state machine replication. Every component deterministically applies the totally ordered log, so any process can be killed and rebuilt by replay. The rule has teeth:
- Any state you act on or show a client must come from the stream.
- A port that wants to reject a cancel sends the reject *through* the engine, rather than deciding locally.
- A box does not act on its own clock. Time arrives as a message.

Patti's version is inversion of control. Applications propose messages only when the framework asks, and "by inverting control, you have no choice but to put all of your state down into some structure that you can then poke at". In imperative wait-then-send code, by contrast, "you're taking a very subtle piece of state there, the fact that you want to send a second message, and you're hiding it in a way that's not observable anymore." Concord's team liked the inverted style "so much that we are basically forcing it onto people that want to write things on Aria".

What this buys you:
- A crashed process recovers by replaying.
- A race condition becomes a log you can replay and reproduce.
- A regulator's question has an exact answer.

The costs, stated plainly:
- The log format and the code that interprets it are versioned forever.
- "When you change the world, you have to change the whole world at once."
- One bug can crash the primary and its backup together, so the state machine code must be extremely clean.

### 3. Never let a slow reader throttle the writer

General-purpose reliable multicast lets "receivers to slow or stop publication … if you scale up to having thousands of participants, there's sort of somebody somewhere who always has a problem." In Nigito's design the publisher never waits. Stragglers recover from retransmitters, and recovery uses domain knowledge rather than blind byte replay: snapshot to compact state, or drop an order and its cancel while both are still buffered.

### 4. Know what the machine can do before you optimise

Nigito: "I think you want to understand the hardware and the machines you're using … deeply." Without a theoretical bound you cannot tell whether a design holds together or when to stop digging: "If you don't know what the machine is capable of you can't even answer that question." Work out serialisation delay, switch hops, cache misses and the memory fetches on the critical path first. In the exchange, one cache-missing lookup was about 30% of runtime, and running memory fetches in parallel (prefetching) was where most of the gain came from.

### 5. Derive the latency budget from the worst real day

Funk replayed the NASDAQ close, the busiest point of the day, through a sequential model at a fixed cost per message. He recorded the largest queue and the largest delay. Queues grow non-linearly with per-message cost, and a system that falls behind at the close stays behind afterwards, so the budget is a cliff, not a slope. The budget also decides what is worth building: only the budget showed that the generated parser's 8× speed-up was required rather than nice to have. Benchmark against the real workload, because "it is surprisingly easy to benchmark the wrong thing and be confident about the conclusions you have of it."

### 6. Measure the moment that counted, with traces rather than averages

A profile averages away the event you care about. Hunter's example: "the order sending was happening 200 microseconds after the thinking was, and the reason was it was being put on a low priority queue of work to do later." A flame graph cannot show that, but a trace (magic-trace, Intel Processor Trace) can.

Before reaching for anything exotic, check for queueing: "a remarkably common pattern we see is that your tails aren't weird, aren't interesting, they're just your medians repeated over and over." Then read profiles for join points as well as peaks. Hunter: "suppose you've got 15 or 16 little peaks, none of which is that big … It'd be really easy to dismiss that … but it turns out if you add them all together, that's 40% of your time."

### 7. Remove platform noise before you tune code

Brindus took a ping-pong benchmark from a 637ns median on a VM to 163ns on tuned bare metal:
- Pin processes to isolated cores with `isolcpus` and `taskset`.
- Move IRQs off those cores.
- Use `nohz_full` to remove the timer tick.
- Disable turbo, which caused P-state sawtooth jitter.
- Add `pause` to the spin loop, which brought bad speculation from 8% down to 1%.

On virtualised noise: "there is a winning move here and it's just to not play." A tight distribution is itself a safety feature. On a noisy machine, "it's already so noisy, we can make it 10 x worse before somebody's like, wait a second, the frog's kind of boiling." Trading a nanosecond of median for determinism is usually the right trade.

### 8. Avoid allocation only on the critical path, and keep the types

In OCaml, allocation itself is cheap. The cost is GC pauses in the tail, plus short-lived garbage evicting cache lines, which hurts the median. Funk keeps the hot path flat: a reused buffer, offset accessors generated from a message DSL, pre-allocated pools, and an "immediate option" behind a PPX, so code still pattern-matches on `None`/`Some` without allocating. The discipline is local: "you really only have to do this in this small subset of your code and the critical path of your code." Grow the system from fast: "take a system that does nothing and make sure it's fast at doing nothing", then add features one at a time behind regression benchmarks.

Hunter adds a default to keep in mind outside the hot path: if you work on systems where this matters, have the self-discipline to "make efficient choices as a matter of defaults in your brain." The language-level cost he names is layout: "There's a lot of this object contains a pointer to something else where in C++ it would just be splatted right there in the middle." The `oxcaml-team` skill covers the unboxed types that address it.

### 9. Design the incentives, because clients will optimise against you

Fairness comes from the architecture. Nigito's failure stories:
- A server sent messages by looping over its TCP connections, so clients opened thousands of connections per second to get to the front of the loop.
- A venue let hidden orders keep the price improvement, so traders stepped orders through every price level.

Multicast delivers each event to everyone at once. "So you want to think about those incentives when you design these systems."

### 10. Test by replay, and expect what you didn't think to test

Deterministic systems can be tested by replaying weeks of production input, plus fuzzing. Patti's layered toolbox is:
- unit tests of side-effect-free modules and state machines;
- a simulated network, which "maybe the most important piece";
- quickcheck-generated orderings;
- version-skew tests;
- whole-system exploration.

He is candid about the remainder: "for all the careful tests that you think to write, there are some things you can only learn by experiencing that chaos." Reuse is where tests go missing: "Because we were leveraging existing code, we didn't think to write a new test, especially for this situation."

### 11. Time is an input, so make it inspectable

Perl met a 100µs UTC requirement with well-tuned NTP rather than reaching straight for PTP. He did the error budget on paper, used hardware timestamps, and cross-checked against distant sources. His preference: "Huge proponent of things you can inspect and debug." Slew clocks rather than stepping them, because applications break when time jumps, especially backwards. Inside the replicated system, principle 2 applies: time arrives as a message.

## Always / Never / Prefer

**Always**
- Ask "can it be simpler?" and apply the weekend-rewrite test to every component.
- Keep the sequencer minimal and every other function an ordinary client of its output.
- Route every state change and every timer through the ordered stream.
- Compute the hardware bound and the latency budget, from the busiest real period, before optimising.
- Look at traces of the slow events, and check for queueing, before theorising about tails.
- Quiet the platform (pinning, IRQs, tick, turbo) before you tune code.

**Never**
- Let a slow consumer apply backpressure to the publisher of a shared stream.
- Keep decision-relevant state outside the log, or act on a local clock inside a replicated component.
- Split the sequencer and lose cross-key atomicity without deciding to.
- Judge latency from averaged profiles alone, or from benchmarks on a VM with noisy neighbours.
- Spread zero-allocation contortions beyond the critical path.

**Prefer**
- Total order over per-shard order.
- Manual, observable failover over consensus on the hot path, when the round trip matters.
- Domain-aware recovery (snapshots, compaction) over byte-level replay.
- Determinism over a slightly better median.
- Generated code (parsers, accessors) over hand-maintained offset arithmetic.

## Design review checklist

1. Where is the single point of ordering, and what does it do that could move to an edge?
2. If any process is killed now, can it rebuild exactly from the stream? What state would it lose?
3. Does any component act on its own clock, or on state that never went through the log?
4. What happens to the publisher when one subscriber falls behind?
5. What is the hardware bound for the critical path, and how far from it are we?
6. What is the latency budget, and which real period was it derived from?
7. Have we looked at traces of the slow events, and ruled out queueing?
8. What incentive does this design create for a client optimising against it?
9. Could one engineer rewrite this component correctly in a weekend?

## Voices

- **Nigito:** reasons from physics and the market's incentives. He keeps asking whether a design can be simpler, and he is concrete about failure stories.
- **Hunter:** measurement first. He looks for the call that shouldn't happen at all, and he prefers a fast evaluation loop: "One of the things I really care about a lot is building systems that let me really quickly evaluate the performance of a system."
- **Patti:** determinism and explicit state. He builds abstractions around recurring anti-patterns, and makes failover a deliberate step.
- **Funk, Brindus and Perl:** budgets from real data, noise removed before tuning, and inspectable components over black boxes.

## Sources

- **Signals and Threads, "Multicast and the Markets"** (Brian Nigito, Ep. 3, 2020). https://signalsandthreads.com/multicast-and-the-markets/
- **Signals and Threads, "Performance Engineering on Hard Mode"** (Andrew Hunter, Ep. 18, 2023). https://signalsandthreads.com/performance-engineering-on-hard-mode/
- **Signals and Threads, "State Machine Replication, and Why You Should Care"** (Doug Patti, Ep. 14, 2022). https://signalsandthreads.com/state-machine-replication-and-why-you-should-care/
- **Signals and Threads, "Clock Synchronization"** (Chris Perl, Ep. 6, 2020). https://signalsandthreads.com/clock-synchronization/
- **Tech talk, "How to Build an Exchange"** (Brian Nigito). https://www.janestreet.com/tech-talks/building-an-exchange/
- **Tech talk, "Safe at Any Speed: Building a Performant, Safe, Maintainable Packet Processor"** (Sebastian Funk). https://www.janestreet.com/tech-talks/safe-at-any-speed/
- **Tech talk, "System Jitter and Where to Find It"** (Tudor Brindus). https://www.janestreet.com/tech-talks/system-jitter-and-where-to-find-it/
- **Blog, "Getting from tested to battle-tested"** (Doug Patti, 2025). https://blog.janestreet.com/getting-from-tested-to-battle-tested/

Quote gate: `tools/fetch_corpus.sh <dir> $(cat skills/low-latency/sources.txt)` then `python3 -I tools/verify_quotes.py <dir> skills/low-latency/SKILL.md`.
