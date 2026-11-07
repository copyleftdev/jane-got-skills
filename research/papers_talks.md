# Jane Street: papers, books, talks, and published teaching material (source material for agent skills)

Compiled 2026-11-07 for `/home/ops/Project/jane-skills`. Companion to `research/repos.json` (446 `janestreet/*` GitHub repos).

## How to read this file

- **Verification legend.**
  - **[V]** Verified against the primary source in this session: the PDF, the page text, the transcript, or the Kaggle page rendered in a browser.
  - **[S]** Taken only from secondary sources, such as search snippets or third-party summaries.
  - **[UNVERIFIED]** Could not be confirmed. Don't cite these as fact.
- **Quotes.** Text in quotation marks was copied from the primary source and string-matched against it. Bullets are paraphrases.
- **Dates for tech talks.** These are YouTube publish dates, which can trail the live talk by weeks.
- **Dates for blog posts.** These are the dates shown on blog.janestreet.com.
- **Where the detail came from.** Talk, podcast and blog extraction was done by reading the full transcripts and post text, and those working files are not kept here. Sections 3, 4 and 6 hold the distilled results.

## Contents

1. Academic papers by Jane Street authors
2. Books
3. Tech talks (index + principle extraction for the densest Jane Street–authored talks)
4. Signals and Threads podcast
5. Trading / quant educational material (Probability & Markets guide, Figgie, Estimathon, puzzles, programs, interview guides, Kaggle ×2)
6. Tech-blog design manifestos and recent (2024–2026) posts
7. Requested items that were not found, or were found under different names
8. Skill seeds
9. Sources

---

## 1. Academic papers by Jane Street authors

### 1.1 Caml trading – experiences with functional programming on Wall Street [V]
- **Authors:** Yaron Minsky and Stephen Weeks, both Jane Street Capital.
- **Venue:** *Journal of Functional Programming* 18(4):553–564, 2008, doi:10.1017/S095679680800676X.
- **Related talks [S]:** POPL 2008 invited talk; CUFP 2006 talk "Caml Trader: Adventures of a functional programmer on Wall Street"; CMU talk in 2009.
- **Actionable ideas:**
  - **Write code that is easy to review.** Partners reviewed "almost every line" of core trading code, and some of them had little CS training. Code review is the main check, so code must be terse, avoid repetition (boilerplate gets skimmed and its copies drift apart), and default to immutability.
  - **Use exhaustive pattern matching and ban wildcard matches,** so that adding a new case makes the compiler point at every place that has to handle it. Label arguments of the same type so they can't be swapped. Prefer polymorphic-variant results (``[`Ok of int | `Invalid]``) to exceptions, because exceptions aren't tracked in types.
  - **Treat types as the reviewer's proof.** The paper states the maxim verbatim: *"make illegal states unrepresentable"*. Other tools for the same job are private types, which can be read and matched but not constructed outside their module, and phantom types for capability-style access control and for tracking which validation has been done.
  - **Prefer static modularity (modules, functors) to objects and inheritance.** Reviewers can follow module boundaries but can't easily work out which method dispatch will run. Objects are an "attractive nuisance".
  - **Value predictable performance.** A simple compiler lets you look at code and estimate its time and space. Keep GC latency in check with incremental major slices, rare compaction, and collecting eagerly while idle. Write your own FFI bindings to vendor C libraries.
  - **Generate boilerplate with macros:** `with sexp` makes printers and serializers from type definitions. The paper also lists pitfalls in candid detail: no generic printers, the optimizer forces a choice between readability and speed, no parallelism, and weak support for programming in the large.
- **Quotes:**
  - "From our perspective, the most prized ability of any trading system is the ability of that system not to trade."
  - "The main point of code review is for the reader to put together an informal proof that the code they are reading does the right thing."

### 1.2 OCaml for the Masses [V]
- **Author:** Yaron Minsky.
- **Venues:** *ACM Queue* 9(9), published 27 Sept 2011, doi:10.1145/2030256.2038036. Also *CACM* 54(11):53–58, 2011, doi:10.1145/2018396.2018413 [S].
- **Actionable ideas:**
  - **History, as a cautionary tale.** Jane Street's 2003 Java rewrite was abandoned because the code was harder to read than the VBA it replaced; inheritance "ducks under abstraction boundaries". The 2005 OCaml prototype took 3 months and was trading 3 months later.
  - **Four virtues:** concision, bug detection by the type system, performance (an incremental GC suits soft real-time work), and being "pure, mostly", with mutation kept deliberately limited.
  - **Worked example of making illegal states unrepresentable.** A `connection_info` record full of `option` fields linked by invariants is refactored into a sum of per-state records (`Connecting of connecting | Connected of connected | ...`). A pair that must be both present or both absent becomes one `(time * int) option`. This is the canonical teaching example for a type-driven-design skill.
  - **Exhaustiveness checks catch edge cases at compile time.** In the `destutter` example, the compiler finds the missing single-element case that the Python version gets wrong at runtime.
  - **Types are documentation guaranteed to be correct,** and their invariants are "more durable than those enforced by convention" in a long-lived, multi-developer codebase.
  - **Prefer message passing between processes to shared-memory threads** (the position in 2011).
- **Quote:** "A complete commitment to immutability is a commitment to never building anything real."

### 1.3 Oxidizing OCaml with Modal Memory Management [V]
- **Authors:** Anton Lorenzen (Edinburgh), Leo White, Stephen Dolan, Richard A. Eisenberg (all Jane Street), and Sam Lindley (Edinburgh).
- **Venue:** PACMPL 8 (ICFP 2024), Article 253, 53 pp., doi:10.1145/3674642. Talk video: https://www.youtube.com/watch?v=wbrELQrzwQk
- **Actionable ideas:**
  - **Three mode axes:** locality (stack vs heap escape), uniqueness (in-place update of immutable structures) and affinity. Modes are orthogonal to types and fully inferable.
  - **Backwards compatible:** existing OCaml code type-checks unchanged, and "manual memory management" becomes safe and opt-in.
  - **The problem is framed as GC costs:** any allocation may trigger a pause (latency), and a bump allocator doesn't reuse addresses (cache locality). The old workarounds were unsafe arenas and pre-allocated arrays.
  - **The design follows Rust's goals with different defaults.** GC and aliasing remain the default, and precise control is opt-in where it pays.
- **Background reading:** the blog series "Oxidizing OCaml: Locality / Rust-Style Ownership / Data Race Freedom" (2023; see §6).

### 1.4 Data Race Freedom à la Mode (DRFCaml) [V]
- **Authors:** Aïna Linn Georges, Benjamin Peters, Laila Elbeheiry (MPI-SWS), Leo White, Stephen Dolan, Richard A. Eisenberg, Chris Casinghino (Jane Street), François Pottier (Inria), and Derek Dreyer (MPI-SWS).
- **Venue:** PACMPL 9 (POPL 2025), Article 23, 39 pp., doi:10.1145/3704859.
- **Award:** POPL 2025 Distinguished Paper [S, per MPI-SWS news].
- **Actionable ideas:**
  - **Two new mode axes:** contention (has this value been shared?) and portability (may it be shared?). A portable function can't capture uncontended mutable state, and fork/spawn requires portable closures.
  - **Capsules:** regions of memory guarded by a unique ghost key. Reader-writer locks give partial or full ownership of the key, which lets aliased, mutable data structures be shared safely.
  - **This is not Rust's model.** It rejects Rust-style "aliasing XOR mutability" everywhere as "a steep price to pay just for data race freedom" in a GC'd language, and keeps arbitrary aliasing for sequential code.
  - **Soundness is proved** with a semantic model in Iris/Rocq. The system is deployed at Jane Street and, per the paper, widely adopted.
  - **A rollout lesson,** from the Casinghino tech talk in §3: parallel OCaml was banned inside Jane Street until this static guarantee existed. Most of the work was fixing the races the discipline exposed in supposedly functional code (Minsky, "Saga of Multicore OCaml").

### 1.5 Mode Crossing (2026) [V]
- **Authors:** Benjamin Peters (MPI-SWS), Jules Jacobs, Diana Kalinichenko, Liam Stevenson, Aspen Smith (all Jane Street), Derek Dreyer (MPI-SWS), and Richard A. Eisenberg (Jane Street).
- **Venue:** PACMPL 10 (ICFP 2026), Article 283, doi:10.1145/3828681. PDF: https://iris-project.org/pdfs/2026-icfp-modecrossing.pdf
- **Actionable ideas:**
  - **The usability problem.** Mode tracking rejects programs that are obviously safe, such as sharing immutable data across threads. The fix is *mode crossing*: automatically strengthening a mode (e.g. nonportable to portable) based on a value's type.
  - **Modal kinds.** These are monotone functions on the mode lattice, and they let abstract types in signatures say how they cross modes. Kind checking reduces to lattice constraints handled by a dedicated solver.
  - **Lesson:** an expressive safety discipline needs an *annotation-burden reducer* designed in from the start, or adoption stalls.
- **Also on the author's site [S]:** Jules Jacobs lists an OOPSLA '26 paper on exact inference for probabilistic programs, not checked further.

### 1.6 Unboxed types, layouts, kinds: workshop papers and talks [V for listing; content from talks]

Listed on OxCaml's documentation page:
- **Unboxed Types for OCaml.** Stephen Dolan, Jane Street tech talk, 26 Sep 2019. Principles in §3.
- **Unboxed types for OCaml.** Richard A. Eisenberg, Stephen Dolan and Leo White, ML Workshop 2022. https://icfp22.sigplan.org/details/mlfamilyworkshop-2022-papers/13/Unboxed-types-for-OCaml ; video https://www.youtube.com/watch?v=Vevld4cXSYk
- **Stack Allocation for OCaml.** Stephen Dolan, OCaml Workshop 2022. https://www.youtube.com/watch?v=yGRn5ZIbEW8
- **Semi-explicit Polymorphic Parameters.** Leo White, ML Workshop 2023. https://www.youtube.com/watch?v=6yUPAWmlxd0
- **Layout Polymorphism: Using static computation to allow efficient polymorphism over variable representations.** Richard Eisenberg, ML Workshop 2023. https://www.youtube.com/watch?v=TSJNXkAtfU0
- **Labeled Tuples.** Chris Casinghino, ML Workshop 2024. The feature came from Ryan Tjoa's intern project and was quickly adopted.
- **Mixed Blocks: Storing More Fields Flat.** Nick Roberts, OCaml Workshop 2024. Records can mix boxed and unboxed fields.
- **A Non-allocating Option.** Richard Eisenberg, OCaml Workshop 2024. This is `or_null`, which avoids allocating `Some` by forbidding nested nullability in the type rather than paying for it at runtime.
- **Taming the Flat Float Array Optimization: Tracking Separability in the Type System.** Diana Kalinichenko and Richard A. Eisenberg, OCaml Workshop 2025 (ICFP/SPLASH 2025, Singapore) [S].
  - A three-valued separability axis lets the compiler accept unboxed existentials and unboxed options that were previously rejected.
  - It also enables optimizations for arrays of known non-float types.
- **ICFP 2024, other ML/OCaml Workshop and HOPE items** [V titles, from the Jane Street "ICFP 2024" blog index]: "Designing interrupts for ML and OCaml", "Pattern-matching on mutable values: danger!", "Rethinking the Value Restriction", "Arrows as applicatives in a monad" (Leo White, HOPE 2024; the theory behind Bonsai).
- **ICFP/SPLASH 2025 tutorial** [S]: "A guided tour through Oxidized OCaml" (Casinghino, Eisenberg, with Brown, Cambridge, IIT Madras and Tarides).
- **ICFP/SPLASH 2025 talk** [S]: "Jane Street and Docker on moving to OCaml 5" (Anil Madhavapeddy's notes).
- **Kinds are calling conventions** (Downen, Ariola, Peyton Jones, Eisenberg; ICFP 2020) and **Levity polymorphism** (Eisenberg and Peyton Jones; PLDI 2017). Eisenberg wrote these before joining Jane Street, but they are the theory behind OxCaml layouts.

Principles that recur across this cluster (from the Dolan and Casinghino talks in §3):
- Representation should be visible in source and interface files, with no fragile automatic boxing.
- Compile once per *layout*, not once per type.
- Rule out bad cases statically instead of paying for them dynamically.
- Separate compilation is non-negotiable.

### 1.7 Flambda / Flambda 2 (OCamlPro + Jane Street) [V listing]
- **Flambda 2 Types: An abstract domain for static analysis of functional programs.** Pierre Chambart, ML Workshop 2023. https://www.youtube.com/watch?v=PRb8tRfxX3s
- **Efficient OCaml Compilation with Flambda 2.** Pierre Chambart, OCaml Workshop 2023. https://www.youtube.com/watch?v=eI5GBpT2Brs
- **Flambda2 Validator.** Irene Yoon, OCaml Workshop 2024. https://www.youtube.com/watch?v=phon73Ku-nM
- **Blog post "A better inliner for OCaml, and why it matters"** (2016-02-24).
- **Lessons from "Jane and the Compiler" (Minsky, §3):**
  - Flambda gave 10–20% for free.
  - Its real goal is making zero-allocation disciplines *reliable*.
  - Inlining heuristics undermine predictability. Leo White: "In lining is always heuristic based… It takes away from the predictability of your performance."

### 1.8 Effects and multicore [V]
- **Retrofitting Effect Handlers onto OCaml** [V title/venue, S affiliations].
  - Authors: KC Sivaramakrishnan, Stephen Dolan, Leo White, Tom Kelly, Sadiq Jaffer, Anil Madhavapeddy.
  - Venue: PLDI 2021, doi:10.1145/3453483.3454039.
  - Affiliations [S, from conference slides]: White at Jane Street, Dolan at OCaml Labs.
  - Result: about 1% mean overhead for code that doesn't use effects, and compatibility with stack-inspecting tools.
- **Related talks:** Leo White, "Effective Programming: Adding an Effect System to OCaml" (Jane Street tech talk, 2018), and Minsky's "The Saga of Multicore OCaml" (2025). Both are extracted in §3.

### 1.9 Hardcaml [V]
- **Paper:** "Hardcaml: An OCaml Hardware Domain-Specific Language for Efficient and Robust Design."
  - Authors: Andy Ray, Benjamin Devlin, Fu Yong Quah, Rahul Yesantharao (all Jane Street).
  - arXiv:2312.15035, 22 Dec 2023. No journal reference on arXiv.
- **Actionable ideas:**
  - Embed an RTL-level hardware DSL in a typed host language. Bit widths and connection errors are caught at *elaboration* time, and designs can be parameterized by querying signal widths.
  - Use one tool stack for simulation: a cycle-accurate simulator, an event-driven simulator, and external backends (Verilator, a C simulator).
  - Write in-source tests that render *ASCII waveforms* as expect tests (see the blog post "Using ASCII waveforms to test hardware designs", 2020).
  - Use SAT-based formal checks: prove property *f* by asking the solver to satisfy ¬*f*.
  - Case study: Jane Street's 2022 ZPrize submission won 1st place in the FPGA track for MSM. Write-up: https://zprize.hardcaml.com, repo github.com/fyquah/hardcaml_zprize, blog post 2022-12-07.
  - Productivity comparison from the paper [S]: a RISC-V core took 1000 lines of Verilog, 586 of Chisel, and 637 of Hardcaml.
- **Related:** "OCaml All The Way Down" (Andy Ray tech talk, §3); Signals and Threads Ep. 1, "Programmable Hardware" (§4); the "Advent of Hardcaml" (2025) and "Advent of FPGA" (2025–26) challenges; the ASIC puzzles (2026).

### 1.10 Incremental / self-adjusting computation
- **No Jane Street academic paper was found.** The academic basis is Umut Acar et al.'s self-adjusting computation (POPL 2002 "Adaptive functional programming" and later work); Jane Street does not author those.
- **Jane Street's material on it is practitioner work:**
  - Talk: "Seven Implementations of Incremental" (Minsky, published 2016-03-31). This is the best case study available for taking an idea from paper to production; see §3.
  - Blog: "Introducing Incremental" (2015), "Incremental computation and the web", "Self Adjusting DOM", "Self Adjusting DOM and Diffable Data" (2016), and "Breaking down FRP" (2014).
  - Repos: `janestreet/incremental`, `janestreet/bonsai`.

### 1.11 Networking and verification papers with Jane Street co-authors [S]
- PLDI 2025 papers with Jane Street-affiliated authors, per search results; venue and affiliation not checked against the PDFs:
  - "Destabilizing Iris" (Simon Spies, listed as Jane Street; Distinguished Paper).
  - "Active Learning of Symbolic NetKAT Automata" (Nate Foster, Cornell and Jane Street).
  - "StacKAT: Infinite State Network Verification" (Nate Foster, Cornell and Jane Street).
- **Related:** Nate Foster's tech talk "Verifying Network Data Planes" (2017) and Signals and Threads Ep. 27, "The Network as a Program" (2026).

### 1.12 Searched, not found as Jane Street work
- **POPL 2026:** no Jane Street-affiliated paper was confirmed. "Let Generalization, Polymorphic Recursion, and Variable Minimization in Boolean-Kinded Type Systems" (Joseph Zullo) is by a Purdue author. The Mode Crossing paper cites it, but it has no Jane Street link.
- **ML Workshop 2025:** no Jane Street paper was found [UNVERIFIED].
- **PLDI 2026 and OOPSLA 2025:** nothing confirmed [UNVERIFIED]. Check the proceedings by affiliation before treating this list as complete.

---

## 2. Books

### 2.1 Real World OCaml, 1st edition [V via dblp/search]
- **Authors:** Yaron Minsky, Anil Madhavapeddy, Jason Hickey.
- **Publisher:** O'Reilly, 2013, ISBN 978-1-4493-2391-2.
- **Ideas it carries:**
  - Core/Async-style API design: labeled arguments, `Or_error`, explicit error types.
  - The module system as the main tool for abstraction.
  - Type-directed design.
  - Pragmatic coverage of the runtime and GC.
- **Blog companions:** "The making of Real World OCaml" (2013) and "RWO tidbits: Benign effects", "RWO tidbits: the runtime" (2013).

### 2.2 Real World OCaml: Functional Programming for the Masses, 2nd edition [V via publisher listing]
- **Authors:** Anil Madhavapeddy and Yaron Minsky.
- **Publisher:** Cambridge University Press, online 22 Sep 2022, print Oct 2022.
- **ISBNs:** 978-1-009-12580-2 (paperback); online 9781009129220.
- **Licence:** open access under CC-BY-NC-ND 4.0 (doi:10.1017/9781009129220). Free online at https://dev.realworldocaml.org/
- **New in the 2nd edition:** chapters on testing (expect tests, property tests), GADTs, and platform tooling (dune, opam).
- **The skill-relevant chapters:**
  - Error Handling.
  - Testing: inline and expect tests.
  - GADTs: using types to make illegal states unrepresentable in state machines and in performance-sensitive code.
  - Functors and First-Class Modules.
  - Concurrent Programming with Async.
  - Memory Representation of Values; Understanding the Garbage Collector.

### 2.3 Other books
- **No other Jane Street-authored book was found.**
- **Probability & Markets (§5.1)** is the closest thing to a published Jane Street "book" on trading reasoning.
- **Recommended reading, not Jane Street's own [S]:** candidate reports recommend Mosteller's *Fifty Challenging Problems in Probability*.

---
---

## 3. Talks

### 3.1 Older landmark talks (pre-dating the tech-talk site)
- **"Effective ML", Yaron Minsky** [V text; video not fetched].
  - A lecture whose text is in the blog posts "Effective ML" (2010-04-22), "Effective ML video" (2010-08-21), "Effective ML Revisited" (2011-03-09) and "Effective ML Revisited (with videos)" (2011-03-27).
  - The maxims, verbatim and in order: "Favor readers over writers", "Create uniform interfaces", "Make illegal states unrepresentable", "Code for exhaustiveness", "Open few modules", "Make common errors obvious", "Avoid boilerplate", "Avoid complex type-hackery", "Don't be puritanical about purity".
  - Inspired in part by Bloch's *Effective Java*.
  - Venue [V]: guest lectures to undergraduate ML classes at Harvard (taped) and Northeastern in 2010, with a repeat Harvard guest lecture in 2011.
- **"Why OCaml?", Yaron Minsky** (blog post 2016-01-25 wrapping an internship-program talk video) [V wrapper only]. The thesis is that OCaml sits in a "sweet spot" of the design space. The tradeoffs are spelled out in the 2008 post "The ML sweet spot" (§6).
- **"Observations of a functional programmer", Yaron Minsky** (CUFP keynote, blog 2016-10-27) [V wrapper only]. Section themes: "the right tool for the organization"; "you broke it, you bought it" (an adopter of a minority technology must invest in its community); "the evidence isn't in".
- **"Caml Trading", Yaron Minsky:** CMU talk (blog 2009-03-12), POPL 2008 invited talk, and CUFP 2006 "Caml Trader" [S].

### 3.2 Jane Street Tech Talks: full index (37 talks on janestreet.com/tech-talks as of 2026-11-07)
Every talk page has an embedded video and a full transcript. Dates are YouTube publish dates.


| YouTube date | Title | Speaker (affiliation) | URL |
|---|---|---|---|
| 2026-09-11 | Trustworthy Human-AI Collaboration in a Live Type-Theoretic Computational Commons | Cyrus Omar (Associate Professor of Computer Science and Engineering at the University of Michigan) | https://www.janestreet.com/tech-talks/trustworthy-human-ai-collaboration-in-a-live-type-theoretic-computational-commons/ |
| 2026-04-10 | Production Engineering When Trading Billions of Dollars a Day | Mark Doss (Production Engineering at Jane Street) | https://www.janestreet.com/tech-talks/production-engineering-when-trading-billions-of-dollars-a-day/ |
| 2026-03-25 | The Cost of Concurrency Coordination | Jon Gjengset (Principal Engineer at Helsing) | https://www.janestreet.com/tech-talks/the-cost-of-concurrency-coordination/ |
| 2026-01-30 | Andreessen’s Folly: The False Dichotomy of Software and Hardware | Bryan Cantrill (Co-founder and CTO of Oxide Computer) | https://www.janestreet.com/tech-talks/andreessens-folly/ |
| 2025-12-23 | Advanced Skylake Deep Dive | Matt Godbolt (Creator of Compiler Explorer) | https://www.janestreet.com/tech-talks/microarchitecture/ |
| 2025-12-17 | How Language Models Model Programming Languages and How Programmers Model Language Models | Arjun Guha (Northeastern University) | https://www.janestreet.com/tech-talks/how-language-models-model-programming-languages-and-how-programmers-model-language-models/ |
| 2025-11-11 | Making GPUs Actually Fast: A Deep Dive into Training Performance | Sylvain Gugger & Corwin de Zahr (Jane Street) | https://www.janestreet.com/tech-talks/making-gpus-actually-fast/ |
| 2025-10-29 | Pyrefly: Type Checking 1.8 Million Lines of Python Per Second | Neil Mitchell (Meta) | https://www.janestreet.com/tech-talks/pyrefly/ |
| 2025-10-24 | Hacking OCaml | Corwin de Zahr (Jane Street) | https://www.janestreet.com/tech-talks/hacking-ocaml/ |
| 2025-08-27 | Rust for Everyone! | Will Crichton (Brown University) | https://www.janestreet.com/tech-talks/rust-for-everyone/ |
| 2025-07-24 | The Saga of Multicore OCaml | Yaron Minsky (Jane Street) | https://www.janestreet.com/tech-talks/the-saga-of-multicore-ocaml/ |
| 2025-04-03 | Making OCaml Safe for Performance Engineering | Chris Casinghino (Jane Street) | https://www.janestreet.com/tech-talks/making-ocaml-safe-for-performance-engineering/ |
| 2024-12-09 | Building Machine Learning Systems for a Trillion Trillion Floating Point Operations | Horace He (PyTorch Compilers at Meta) | https://www.janestreet.com/tech-talks/building-machine-learning-systems-for-a-trillion-trillion-floating-point-operations/ |
| 2024-11-15 | System Jitter and Where to Find It: A Whack-a-Mole Experiencer | Tudor Brindus (Jane Street) | https://www.janestreet.com/tech-talks/system-jitter-and-where-to-find-it/ |
| 2024-10-23 | uv: An extremely Fast Python Package Manager | Charlie Marsh (Astral) | https://www.janestreet.com/tech-talks/uv-an-extremely-fast-python-package-manager/ |
| 2020-04-15 | A Taste of GPU Compute | Raph Levien (Independent Researcher) | https://www.janestreet.com/tech-talks/a-taste-of-gpu-compute/ |
| 2020-02-18 | The Algorithm for Precision Medicine | Matt Might (Hugh Kaul Precision Medicine Institute) | https://www.janestreet.com/tech-talks/algorithm-for-precision-medicine/ |
| 2020-01-31 | State of the Shell: PowerShell7 | Steve Lee (Microsoft) | https://www.janestreet.com/tech-talks/state-of-the-shell/ |
| 2019-12-09 | Dude, Where Are My Files? Reverse Engineering Ransomware | Michael Sikorski (Fire Eye Labs) | https://www.janestreet.com/tech-talks/dude-where-are-my-files/ |
| 2019-10-24 | Unboxed Types for OCaml | Stephen Dolan (Jane Street) | https://www.janestreet.com/tech-talks/unboxed-types-for-ocaml/ |
| 2019-09-27 | RustBelt: Logical Foundations for the Future of Safe Systems Programming | Derek Dreyer (Max Planck Institute for Software Systems) | https://www.janestreet.com/tech-talks/rustbelt/ |
| 2019-05-08 | Safe at Any Speed: Building a Performant, Safe, Maintainable Packet Processor | Sebastian Funk (Jane Street) | https://www.janestreet.com/tech-talks/safe-at-any-speed/ |
| 2019-03-08 | A Language-Oriented System Design | Nathan Linger (Jane Street) | https://www.janestreet.com/tech-talks/a-language-oriented-system-design/ |
| 2019-02-11 | Abstractions for Expressive, Efficient Parallel and Distributed Computing | Lindsey Kuper (University of California, Santa Cruz) | https://www.janestreet.com/tech-talks/abstractions-for-expressive-efficient-parallel-and-distributed-computing/ |
| 2018-12-07 | Jane and the Compiler | Yaron Minsky (Jane Street) | https://www.janestreet.com/tech-talks/jane-and-compiler/ |
| 2018-10-24 | Distributed, Incremental Dataflow Processing in the Cloud with Reflow | Marius Eriksen (GRAIL) | https://www.janestreet.com/tech-talks/dataflow-processing/ |
| 2018-08-24 | Introduction to Incr dom: Writing Dynamic Web Apps in OCaml | Cristina Rosu (Jane Street) | https://www.janestreet.com/tech-talks/intro-to-incr-dom/ |
| 2018-05-10 | OCaml All The Way Down | Andy Ray (Jane Street) | https://www.janestreet.com/tech-talks/ocaml-all-the-way-down/ |
| 2018-04-05 | Effective Programming: Adding an Effect System to OCaml | Leo White (Jane Street) | https://www.janestreet.com/tech-talks/effective-programming/ |
| 2018-02-28 | Curriculum Design as an Engineering Problem: Lessons from the Field | Shriram Krishnamurthi (Brown University) | https://www.janestreet.com/tech-talks/curriculumn-design/ |
| 2018-01-30 | The Hurricane's Butterfly: Debugging Pathologically Performing Systems | Bryan Cantrill (Co-founder and CTO of Oxide Computer) | https://www.janestreet.com/tech-talks/hurricanes-butterfly/ |
| 2017-12-04 | How Jane Street Does Code Review | Ian Henry (Jane Street) | https://www.janestreet.com/tech-talks/janestreet-code-review/ |
| 2017-11-27 | Verifying Network Data Planes | Nate Foster (Cornell University) | https://www.janestreet.com/tech-talks/verifying-network-data-planes/ |
| 2017-06-20 | Caveat Configurator: How to replace configs with code, and why you might not want to | Dominick LoBraico (Jane Street) | https://www.janestreet.com/tech-talks/caveat-configurator/ |
| 2017-03-15 | On Verification for System Configuration Languages | Arjun Guha (University of Massachusetts, Amherst) | https://www.janestreet.com/tech-talks/on-verification-for-system-configuration-languages/ |
| 2017-03-13 | How to Build an Exchange | Brian Nigito (Jane Street) | https://www.janestreet.com/tech-talks/building-an-exchange/ |
| 2016-03-31 | Seven Implementations of Incremental | Yaron Minsky (Jane Street) | https://www.janestreet.com/tech-talks/seven-implementations-of-incremental/ |

### 3.3 The most principle-dense talks, ranked for skill-building

**Jane Street–authored.** Full extractions are in 3.4–3.6.
1. **How to Build an Exchange**, Brian Nigito (2017). Covers sequencer and state-machine-replication architecture, fairness and incentive design, and how speed buys simplicity.
2. **Production Engineering When Trading Billions of Dollars a Day**, Mark Doss (2026). Covers event-based alerting versus SLOs, "epistemic" alerts, uncorrelated defense in depth, and the Knight Capital and Mizuho lessons.
3. **How Jane Street Does Code Review**, Ian Henry (2017). Covers Iron's "brains", diff-of-diffs, CRs as code comments, and scrutiny levels.
4. **Seven Implementations of Incremental**, Yaron Minsky (2016). Shows how a research idea becomes production code: map vs bind, pseudo-height, observers, cutoffs.
5. **Safe at Any Speed**, Sebastian Funk (2019). Covers deriving a latency budget from replayed peak data, zero-alloc hot paths, and type-safe zero-cost abstractions.
6. **System Jitter and Where to Find It**, Tudor Brindus (2024). A whack-a-mole method from 637 ns to 163 ns using magic-trace, isolcpus/nohz_full, turbo, and `pause`.
7. **Making OCaml Safe for Performance Engineering**, Chris Casinghino (2025). Argues for "safe, convenient, predictable" control and pay-as-you-go complexity.
8. **The Saga of Multicore OCaml**, Yaron Minsky (2025). Says GC performance "is a curve", that bugs become load-bearing, and that you should prototype the bad fix first.
9. **Caveat Configurator**, Dominick LoBraico (2017). Gives a decision tree for config versus code.
10. **Unboxed Types for OCaml**, Stephen Dolan (2019); **Jane and the Compiler**, Yaron Minsky (2018); **Making GPUs Actually Fast**, Gugger & de Zahr (2025); **OCaml All The Way Down**, Andy Ray (2018); **A Language-Oriented System Design**, Nathan Linger (2019).

**Guest talks hosted by Jane Street.** These were not extracted here. They are useful for adjacent skills and many already exist as personas in this environment:
- Bryan Cantrill, "The Hurricane's Butterfly" (2018) and "Andreessen's Folly" (2026)
- Matt Godbolt, "Advanced Skylake Deep Dive" (2025)
- Jon Gjengset, "The Cost of Concurrency Coordination" (2026)
- Derek Dreyer, "RustBelt" (2019)
- Cyrus Omar, "Trustworthy Human-AI Collaboration…" (2026), on object-capability bounds for agent swarms
- Arjun Guha, "How Language Models Model Programming Languages…" (2025)
- Horace He, "Building ML Systems for a Trillion Trillion FLOPs" (2024)
- Charlie Marsh, "uv" (2024)
- Neil Mitchell, "Pyrefly" (2025)
- Will Crichton, "Rust for Everyone!" (2025)

**ML at Jane Street, other video [S].** janestreet.com/machine-learning links:
- A GPU-performance talk ("five real-world performance pitfalls and the CUDA techniques that solved them")
- A Dwarkesh Patel conversation with Ron Minsky and Dan Pontecorvo at the Texas datacenter (4,032 GPUs, liquid cooled)
- An ML-engineering internship conversation (GPU kernels, low-bit KV-cache quantization)

These were not opened here.

### 3.4 Extracted principles: architecture, review, incremental, config, permissions talks

All quotes below were checked as exact substrings of the transcript files (curly apostrophes preserved).

---

#### 1. How to Build an Exchange — Brian Nigito

**Actionable principles**
- **Keep the sequencer tiny and push everything else to the edges.** The whole market runs through one matching engine on one x86 box. It only handles add, cancel and execute. Anything else is a separate process that watches the output stream and acts as an ordinary client. The "Cancel Fairy" handles timed cancels by sending a cancel later on the order's behalf. Auction price optimization runs off to the side and sends its results back. Drop ports, trade reporting and market data are separate processes too. Run several redundant copies of these helpers. If one crashes or they race each other, nothing breaks.
- **Use state machine replication so you can kill any process and rebuild it.** Every component deterministically applies the totally ordered stream from the matching engine. When one dies, it replays from the retransmitters and rebuilds its exact state. A client then reconnects with a handshake ("I saw up to sequence number N") and catches up. The passive backup matching engine reads the primary's *output*, not the ports, because UDP arrival order at the ports is not guaranteed. It runs the identical code and regenerates the same executions. Failover is done by an operator, not Paxos, because Paxos costs an extra round trip and a hop. The weakness is that the same bug can crash both primary and backup, so the state machine code must be "extremely clean" and heavily tested.
- **Any state you act on or show a client must come from the ordered stream.** If the protocol sequences cancel rejects, a port must send its cancel reject through the matching engine instead of keeping it locally, or it could not be rebuilt after a crash. Timers work the same way: a box cannot act on its own clock. Every change to state must appear as a message in the stream.
- **Fairness and incentives come from the architecture.** Multicast delivers each event to both trading parties, market data, drop ports and the trade reporter at the same moment. Failure story 1: a server that sent messages by looping over its TCP connections made clients open thousands of connections per second to get first place in that list. Failure story 2: a venue let hidden orders keep the price improvement, and traders responded by stepping orders through every price level. The usual rule gives price improvement to the aggressive order. Be robust to bad clients, including clients who are simply optimizing for the incentives you created.
- **Speed buys simplicity.** Each port allows only one unacknowledged transaction in flight, so latency determines throughput. Because any app can be rebuilt by replay in 30–60 seconds, there is no need for state-transfer snapshots. To get there: copy nothing, keep pools of preallocated objects, and allocate very little on the critical path. The engine hands ports a "locate" (an array index) so cancels can find their order quickly. That one lookup was a cache miss taking about 30% of runtime, and running several memory fetches at once (prefetching) is where most of the gain is. A simpler runtime (OCaml) made determinism easier than Java's more complex GC and threading.
- **Use per-topic sequence numbers for optimistic concurrency, and be careful about parallelism.** Each contributor proposes the next sequence number for a topic. The engine silently drops a stale proposal (no NAK) because the reliable stream will show the contributor what happened. The contributor then applies that event and retries. One message in flight means rollback only has to remember one message. Splitting the engine by symbol loses atomic cross-instrument risk limits, which matter for ETF market making. Merging several engines' output into one client stream adds ordering state that cannot be recovered. Test new engines by replaying weeks of real production data plus fuzzing. Determinism means a regulator's question gets an exact answer: "I know exactly what I knew at every point in time."

**Verbatim quotes**
- "Latency determines throughput."
- "And so the speed allows us to keep the system really simple from that perspective."
- "So you want to think about those incentives when you design these systems."

**Best grounds skill:** exchange / matching-engine design (deterministic sequencer + state-machine replication)

---

#### 2. How Jane Street Does Code Review — Ian Henry (Iron)

**Actionable principles**
- **Track what each reviewer has read as content, not as commit pointers.** A "brain" is a diff kept per (reviewer, branch) of exactly what that person has accepted. Review is complete when the brain equals the branch's diff. This one idea meets every constraint the talk sets out:
  - everything gets reviewed, including merge-conflict resolutions and edits made during a rebase;
  - nobody reads the same code twice;
  - the author can push mid-review safely;
  - the branch can keep up with upstream by merge or rebase at any time.
- **After a rebase or merge, show a diff of diffs.** The reviewer sees the difference between their brain and the branch (a "ddiff"), which is usually trivial context. If a ddiff is hairy, the reviewer can drop it and re-review that part. The cost is that the whole branch is reviewed as one unit. So branches are kept very small, the branch is the unit of review, dependent work goes on nested branches, and commit history is allowed to be messy.
- **Put review comments in the code itself.** The reviewer commits `CR reviewer for author:` comments to the branch, and the reply turns it into an `XCR` assigned back to the person who opened it. Comments survive rebases because they are part of the code. Reviewers fix typos and names directly instead of commenting on them. An editor integration (press enter on a diff line to jump there) removes the context-switch cost. A branch cannot be released with open CRs. To defer one, convert it to a `CR-soon`, which goes to the file owner.
- **Review happens in layers of obligation.** The author reviews their own branch first. Whole-feature reviewers then read all of it and explicitly "second" it. Review then widens to file reviewers, who have a *permanent* duty to watch their files. Per-file scrutiny and n-of-k reviewer groups are declared in metadata files checked into the repo.
- **The server enforces the rules.** The central server refuses to release anything with unreviewed code or open CRs. Locks stop others from releasing or rebasing a branch, or pin a branch to an old version for a production patch. The talk states the trade-off as safety versus productivity.
- **Use the same workflow for anything that needs review.** Configs, trading limits (only approved people can change limits, and changes need explicit approval) and blog posts all go through it. "Traits" tag the commit where a bug was seen and the commit that fixed it. Because history is merge-only, you can ask any revision which known bugs it has. In production, roll back by redeploying an archived executable, never by rewriting history. Overall framing: each idea is worse alone (a local maximum) and only pays off when combined with the others.

**Verbatim quotes**
- "if you review something, Iron remembers that you reviewed it."
- "You want to diff what you know to what you should know."
- "It deliberately stops and forces you to do the right thing, in various ways."

**Best grounds skill:** code review discipline / review-state tracking and release gating

---

#### 3. Seven Implementations of Incremental — Yaron Minsky

**Actionable principles**
- **Prefer `map` (static graph) to `bind` (dynamic graph).** Bind adds expressive power but is more complex, slower and allocates more. Never build map out of bind. The academic version did, and it was "crushingly expensive." Read a program twice: once with every incremental operation erased (that is what it means), and once looking at exactly where the incrementality sits (that is how it performs). Don't incrementalize trivial work such as a single `if`.
- **Recombinant graphs need ordered propagation.** Naive depth-first firing recomputes shared nodes, and stacked diamonds make that exponential. Version 1 marked nodes dirty with a count of dirty inputs, which made cutoffs impossible, so it needed restarts that could themselves go exponential. A topological order fixes this: each node fires once, and stopping propagation early (a cutoff) no longer breaks anything. A total order needs a heap, which is slow. A *partial* order (pseudo-height) plus an array of lists gives constant-time scheduling. Pseudo-height never decreases, which avoids renumbering the graph when a bind flip-flops.
- **Don't rely on the GC to stop work.** Nodes a bind no longer used stayed attached to the inputs and kept recomputing until the GC eventually ran. With nested binds this produced exponential garbage and long UI pauses. The fix was explicit *observers*, the counterpart to variables. Unobserved parts of the graph are shut down immediately, and observed nodes may never point to unobserved ones. Unobserved subgraphs then float free and can be collected, and finalizers dropped from one per node (about 300k) to one per observer (about 10).
- **Cutoffs are required, and so is handling back edges.** Cutoff examples: max of two numbers, or a float tolerance such as 1e-15. Memoizing subgraphs, a natural optimization, creates back edges. Version 1 looped forever, a fail-stop failure. The academic design raised an exception. The fix was to redo the topological sort when a back edge appears. Nodes created by an earlier firing of a bind are obsolete and must not be depended on.
- **Measure every version against the baseline.** Versions with better semantics ran 1.5–4x slower, so the intern's version never shipped. Performance only matched version 1 at version 6.
- **Replace closure records with GADTs and existentials.** "Poor man's objects" (records of closures) were slow and "like programming with oven mitts." GADTs and existentials made the code easier to read *and* faster, and the visible node structure opened up more graph optimizations. Real applications got 3x faster, because an incrementalized app ends up limited by the framework's own overhead. A trading front end moved from v3 to v8 and went from "the thing that ruins my life" to the fastest app its users had.

**Verbatim quotes**
- "Bind is more powerful, but worse in all the other ways."
- "relying on the garbage collector to collect something, you shouldn’t really rely on it to collect it especially soon."
- "So, the returns to improving the incrementalization framework are really high."

**Best grounds skill:** incremental computation / dependency-graph engine design (paper-to-production iteration)

---

#### 4. Caveat Configurator — Dominick LoBraico

**Actionable principles**
- **Start from no configuration.** "Zeroconf" means sane defaults plus easy redeploys, and it avoids every problem that follows. Configuration is a cost to justify, not a default.
- **Watch for config creep.** Pure key=value data turns into defaults, then macros and variables, then an ad hoc DSL. A DSL's costs:
  - parser and interpreter bugs look the same as application bugs in production;
  - its semantics are new and nobody else has seen them;
  - it has no IDE support and no way to write tests;
  - experts' knowledge doesn't transfer to it;
  - its author gets the 2 a.m. phone call.
- **Config-as-code plugins failed in production (`ocaml_plugin`).** Problems found:
  - *Danger:* plugin code runs inside the production process, as the production user.
  - *Versioning:* plugins compiled against the app's bundled libraries broke when the app upgraded, and some apps were abandoned because of it.
  - *Scattered files:* no story for deploying or tracking them.
  - *Tooling still broke:* standalone files fell outside the codebase's tools.

  The mail server's config grew from a 13-line sketch to 4,000 lines of OCaml.
- **Generate config with code and have the app read plain data.** The config must be finite (no functions) and its on-disk format versioned. Commit the generated output. Diff the generated files, including a derived CSV of resolved hosts and checks, to see exactly what a change does. This also works for third-party systems. Either pin the generator to one compiler and library version, or keep it in the normal repo with review, build and tests.
- **Decision tree for choosing an approach:**
  - Is runtime dynamism (Turing completeness) needed? If not, use config generation.
  - Must plugins deploy separately from the app? If not, bundle them and redeploy with the app.
  - Does stability matter? If so, use disciplined versioning. `plugd` keeps plugins in a central repo, serves only versions that were reviewed, compiled and tested, and moves patches across app versions.

  Often the real win was a clean split between the core app and its configurable parts, and that can be had without plugins.
- **Treat config with the culture of code: tests, refactoring and code review.** For non-programmers, embed a simpler config format inside a plugin. One split that works: the tech group writes the validation, traders write their own plugin, and application experts review it.

**Verbatim quotes**
- "there is one major con, and that is that you are a terrible language designer."
- "Code is code. It can do anything and you probably will have a hard time preventing it from doing things that you don’t want it to do."
- "The value from the plugin approach comes from writing your configs in a programming language"

**Best grounds skill:** config-as-code / configuration architecture decisions

---

#### 5. A Language-Oriented System Design (Ontology) — Nathan Linger

**Actionable principles**
- **Model permissions and shared config as a deductive database.** Data is classified two ways. It is either a *noun* or a *proposition*. It is defined *extensionally* (a table), *intensionally* (rules), or as a *primitive* (built in, such as ports, IP ranges or bandwidth). Tables alone would be roughly a relational database, and rules alone roughly Prolog. Rules make transitive closure easy (mailing lists subscribed to other lists) and allow subset types. Definitions can depend on each other in either direction.
- **Store state as declarations in a dependently typed language.** Each table row is a constant whose type is the proposition it asserts. The system-generated name of that constant is the evidence for the fact. A subset type stores a proof inside the data: "trader = user + proof they may trade". A query is an existential formula, and its answers come with proofs.
- **Keep the invariant that everything always type-checks.** Deleting a user group then forces deletion of everything that depends on it, so meaningless data cannot pile up. Because deletes are expensive, deleted items are kept in a trash for two weeks. Read permissions cascade the other way: each user sees a personal view with everything they cannot read already removed.
- **Change data by jurisdiction.** For data the system owns, a user submits a request, a query works out who must approve, those people are emailed, and they approve or reject. Data owned elsewhere is imported on a schedule. Rule-defined types change only by bumping the type's version and migrating, while tracking which clients still read the old version.
- **Hide the internal language and let the types drive the UI.** Each constructor has a plain string template, and English is rendered by filling the templates. Request and query builders only offer valid choices, so a user cannot build something ill-formed. The query builder notices clauses that are not connected and asks the user to join them. Adding a new kind of permission means uploading declarations, with no upgrade to the core. Because the structure is generic, one test covers every request type: revoking your own permission must never need extra approval.
- **Known downsides.** The Prolog core is Turing-complete, so an approver query might never finish. An execution budget prevents that, but the error when a query exceeds it is poor. The team also had to build a hodge-podge of database and language pieces. What saved it was borrowing decades-old, well-understood theory and keeping all data first-order.

**Verbatim quotes**
- "If they were exciting, then probably they’re wrong."
- "because it’s driven by the types, it’s guaranteed to respect the type system."
- "A trader is a pair of a user and a proof that that user may trade."

**Best grounds skill:** permissions modeling / typed deductive-database design with type-driven UI

---

#### 6. Introduction to Incr_dom — Cristina Rosu (skimmed)

**Actionable principles**
- **Use the Elm architecture.** The app is an immutable Model, an Action type, `apply_action` and `view`. Only the model may feed the view. Mutable resources, such as server connections, go in a separate State.
- **Layer the optimizations.** A virtual DOM diff and patch avoids expensive browser work. Rebuilding the virtual DOM on every change is still too slow, so Incremental maps the model to the virtual DOM. Every view node descends from the model, so cutoffs are what stop needless recomputation.
- **Don't map over the whole model at the top of `view`.** It makes the code look non-incremental, but everything recomputes on every change. Store collections as maps and use `Incr_map`, whose work is proportional to the size of the diff. Compute totals with `unordered_fold`, giving it add and remove functions.
- **Incremental doesn't help the first load.** Render only the rows in the viewport and use correctly sized placeholders for the rest. For small models the incremental overhead can outweigh the gain, so measure before adding it.
- **Asynchronous actions can arrive after the model has changed.** Check that an action still makes sense before applying it. Pipe RPCs that push updates faster than the browser can handle them crashed browsers, so polling is sometimes better.

**Verbatim quotes**
- "Recall that incremental helps with handling incremental changes. It doesn’t help with the initial work"
- "if you’re worried about performance, this is just an absolutely terrible thing to do."
- "Often you should do checks on your model before applying those actions to make sure the action still makes sense to apply"

**Best grounds skill:** incremental UI / reactive view-rendering performance (applied companion to the Incremental skill)

### 3.5 Extracted principles: latency, jitter, production engineering, GPU, Hardcaml, runtime-hacking talks

---

#### 1. Safe at Any Speed: Building a Performant, Safe, Maintainable Packet Processor — Sebastian Funk

**Actionable ideas**
- **Get the latency budget from real data before you optimize anything.** He replayed the NASDAQ close (the busiest point, 3–4M msgs) through a sequential model at a fixed per-message cost and recorded the largest queue and largest delay. At 750ns per message the worst queue was 22 messages; at 10ms it was about 1M. Growth is non-linear, and a system that falls behind at the close stays behind after it, so even quiet-period messages arrive late. The resulting rule: below 750ns is fine, above 1µs "you are kind of dead." The budget also settled whether to build the codegen DSL. The generated parser ran in 700ns against 5µs for the naive one, and only the budget showed the 8x gain was required rather than a nice-to-have.
- **Zero-alloc applies to the critical path only.** Allocating is cheap in OCaml (a pointer bump plus an overflow check). The cost comes from GC pauses, which hurt the tails, and from short-lived garbage evicting useful cache lines, which hurts the *median*. You pay for that eviction twice: once when you allocate and again when the GC walks the live set. On the hot path, use flat representations: one reused IO buffer, seek to offsets, update state, write out. Also use pre-allocation, or external pools in C memory laid out to look like OCaml values so the GC never sees them. Run synchronously so reusing a buffer is safe. Allocate freely at startup and on error paths.
- **Find hidden allocations.** Watch for `List.map` copies, closures that capture free variables, boxed floats, and `option` values that wrap even an immediate int. One case cost 4 bytes per message. With a 256KB minor heap that forces a GC every ~64k messages, which is too often at 1M msgs/sec.
- **Keep type safety and remove the cost with a syntax extension.** He built an "immediate option" that reserves a sentinel (min_value) as None. A PPX (`%optional`) lets you write an ordinary `match` with None/Some, so the exhaustiveness check still runs because type checking happens before dead-code elimination, but the code that executes is the non-allocating one. The same approach applies to parsing. Don't eagerly parse and allocate a record of fields you never read (such as timestamps). Instead, generate offset accessors over the raw buffer from a small message DSL (a code generator, "protogen"), so nobody maintains the "seek to position 13" code by hand.
- **Inlining can backfire.** Inlining everything makes programs slower than not inlining at all. Inlining heuristics are found empirically by benchmarking. On hot paths, mark functions as must-inline with an attribute that makes the compiler *fail* if it cannot inline them.
- **Grow performance in from the start.** Start from a system that does nothing quickly and add features one at a time, keeping it fast after each. These optimizations are fragile across compiler and runtime upgrades, so keep regression benchmarks running. Production brings its own problems that the code alone doesn't show: time spent in the OS network stack, and the "cold hardware tax" (a system doing very little runs slower per item than one doing a lot).

**Quotes**
- "it’s just about possible to do the opposite of take a system that does nothing and make sure it’s fast at doing nothing."
- "So it is surprisingly easy to benchmark the wrong thing and be confident about the conclusions you have of it."
- "you really only have to do this in this small subset of your code and the critical path of your code."

**Best grounds:** low-latency OCaml (zero-alloc hot paths, latency budgeting)

---

#### 2. System Jitter and Where to Find It — Tudor Brindus

**Actionable ideas**
- **Remove noise from the platform before tuning code.** In his memory ping-pong benchmark (two processes, ring buffers), the VM run had a 637ns median and tails up to 16µs. Running the same code on bare metal brought the median to 223ns. On virtualization overhead and noisy neighbours, he says the winning move is not to play. Docker on bare metal is fine unless you make syscalls. Cloud metal instances give the most deterministic performance.
- **Sampling profilers can't see tail events in spin-wait systems.** `perf` reports 99.5% of time spinning in the poll loop, which tells you nothing. Use Intel Processor Trace instead: it records control flow in a compressed ring buffer, and you snapshot it when something interesting happens. Their tool **magic-trace** does this. Set the trigger to round trips above about 300ns (median plus margin), then zoom in at nanosecond resolution to see what interrupted you.
- **Move interrupts off your cores and turn off the tick.** Magic-trace showed `ixgbe` NIC driver polls on a process that does no networking. `isolcpus` keeps IRQs off the isolated cores, but the scheduler then stops placing work there, so pin processes manually with `taskset` (median 194ns). The next finding was APIC timer interrupts at about 1000/s, visible in `/proc/interrupts`. When each core has exactly one runnable process, `nohz_full` cuts the tick to about 1/s. That removed the ~1µs mode.
- **When traces show "it just took longer," suspect the microarchitecture.** Turbo boost P-state transitions left a sawtooth in the time series. Disabling turbo removed it at the cost of 1ns on the median (likely more on heavier workloads). That trades a little speed for determinism, deliberately.
- **Check top-down stall categories, especially bad speculation.** Intel's PCM tool showed 8% bad speculation from the spin loop speculating past the load. Intel's manual says anything above 1% should be the top priority. The fix was to add the x86 `pause` instruction to the loop, a one-line change using an intrinsic the compiler team added. Bad speculation fell to 1% and the median to 163ns. Overall: 637ns noisy to 163ns quiet, about 4x lower median with far less jitter.
- **Know the hardware's limits, and why a tight distribution matters.** Overclocking with faster RAM gained another 94ns, but a real trading system ran on it and hit memory corruption halfway through the test. With a tight distribution, a regression shows up immediately in testing. With a noisy one, you can make it 10x worse and nobody notices.

**Quotes**
- "there is a winning move here and it’s just to not play."
- "it’s already so noisy, we can make it 10 x worse before somebody’s like, wait a second, the frog’s kind of boiling."
- "any new regression that you introduced that causes the P-99 to go off of a cliff, you’re gonna notice immediately in testing."

**Best grounds:** jitter hunting / low-latency Linux and microarchitecture tuning

---

#### 3. Production Engineering When Trading Billions of Dollars a Day — Mark Doss

**Actionable ideas**
- **When every event matters, SLO-based monitoring misses the one that bankrupts you.** A 99.99% success target is no help if the failed 0.01% is the cancel that mattered. For live trading they use mostly **event-based alerting**: the code raises an alert for a human when a specific condition occurs. Every edge case gets listed, and for each one someone decides in code or config whether to alert, even when the decision is "fail safely, no alert." The upside is detailed alerts that point to a call site. The costs are that it's a lot of work, it gets noisy when cases are missed, tribal knowledge builds up, and changing an alert means understanding the code. Teams monitor their own systems rather than handing that to a separate ops team. Metrics and SLOs are kept for long-term health and low-risk systems.
- **Alert on symptoms, not causes, and attach the cause as context.** Don't alert on "database down." You have to alert on the 500s anyway, so a second alert duplicates it. The "obviously bad" assumption also stops holding once failover and maintenance exist, and then the silencing workarounds pile up. Put the database state into the 500 alert's metadata or a linked dashboard instead.
- **Add orthogonal "epistemic" alerts that detect a wrong picture of the world, not a broken service.** Examples are "fill-too-good" (we made too much money) and an unexpectedly high share of market volume (3% jumping to 60%). One such alert covers market data, instrument definitions, the order engine, strategy bugs, fat fingers and rogue traders. Send the aggregate version to the last line of defense, the order-engines team, and let it halt automatically ("too many fill-too-goods" halts the engine).
- **Defense in depth needs independent, uncorrelated checks.** Run similar risk checks in the strategy, the order engine and an external risk enforcer, each written by a different team, and avoid sharing metadata or logic between them. Look for common dependencies and duplicate them if needed. Monitor technical health (tech staff) and trading impact (traders) as two separate views. Treat monitoring as more critical than the systems it watches: "we basically don't trade unless it's being monitored."
- **Lessons from failures.** Knight Capital (2012): they reused a config flag to avoid a version bump. One of eight instances failed to upgrade, and its failure email was ignored. Engineers then rolled back the instances that *had* upgraded, which made the losses 8x faster: about $0.5B in 45 minutes. Mizuho (2005) entered 600,000 shares at ¥1 instead of 1 share at ¥600,000, and the exchange rejected the cancel. Don't count on the financial system to save you. Counterparties take advantage of any mistake right away (adverse selection).
- **Incident practice: business context, timing, and code paths that have never run.** In the sample incident, a "what changed" tool turned up a suspicious price-serialization refactor, which was a red herring. Traders reporting stale market data was the turning point. The root cause was a missed exchange-driven change (a feed split into a new partition) together with staleness-marking logic that had never run in production. Takeaways: responders need trading context (for example, "spoos" means S&P futures, traded on CME at Aurora, so search for "AUR"). Don't roll changes just before scheduled events like FOMC releases. Faster response would not have helped, because the damage happened at 9:31. The postmortem question is whether the problem could have been detected before the open. Exchange-driven change emails are 99.99% irrelevant, which makes them a signal-to-noise problem they have gotten wrong several times. The open problem he admitted: alert storms when one failure cascades.

**Quotes**
- "We would rather a trading system go down than the monitoring system go down."
- "none of your users care about your database. They care about the 500 errors."
- "You simply can’t create a system so reliable that you can be 100% confident that it will be reliable enough."

**Best grounds:** trading production engineering / incident response and alert design

---

#### 4. Making GPUs Actually Fast: A Deep Dive into Training Performance — Sylvain Gugger & Corwin de Zahr

**Actionable ideas**
- **Know what a GPU is good at.** One FLOP takes about 1ns on a CPU and about 1µs on a GPU. A 2048×2048 matmul takes about 28ms on a CPU (with SIMD and multiple cores) and about 200µs on a GPU. GPUs only pay off with massive parallelism. Kernel launches are asynchronous: the CPU queues work and runs ahead. The first goal is to keep the "CUDA HW" row in Nsight Systems solidly filled ("keep the blue bar full"), with the CPU well ahead of the GPU.
- **Find and remove host/device syncs, including hidden ones.** Common culprits:
  - `.cpu()` for metrics. Fix: compute metrics with GPU kernels and copy them back rarely.
  - Converting a tensor to a Python bool, as in `if loss.isnan()`. Fix: check asynchronously on another thread, which kills the process when it fires. This accepts a little wasted work after a blow-up.
  - Copying pageable memory from CPU to GPU. Fix: `pin_memory` plus `non_blocking=True` (a promise not to modify the buffer).
  
  A sync followed immediately by kernel launches costs little (about 1ms per 1s step, or 10bps). It is very costly when expensive CPU work, such as fetching the next batch, follows it, because then that work can no longer overlap with the GPU.
- **A full timeline doesn't mean an efficient GPU.** First find which of three bottlenecks you have:
  - **Compute:** use tensor cores.
  - **Memory bandwidth:** fuse kernels so each load does more work. Rough H100 bandwidths: global memory 3 TB/s, L2 7 TB/s, shared memory 26 TB/s.
  - **Launch overhead:** a launch costs 5–10µs on the CPU and leaves about a 1µs GPU gap, so kernels shorter than about 1µs starve the GPU. Fuse them, or use CUDA Graphs to record and replay launches.
- **Use torch.compile, but know where it stops.** It traces the model, benchmarks candidate fusions, and fuses well on memory-bound elementwise chains (LayerNorm→ReLU→add). Graph breaks block fusion: unsupported Python constructs (at one point, dict comprehensions), custom ops, and any CPU/GPU sync. Compiling with the full-graph option makes hidden syncs raise an error, so it doubles as a sync detector. Without fusion it can be *slower*, because its Triton templates reach about 80–90% of NVIDIA's best kernel. A Python `for` loop over many small tensors is a warning sign, since the compiler unrolls it rather than parallelizing it.
- **Escalate in order: pure/vectorized PyTorch, then Triton, then CUDA C++, with PTX injected only for specific instructions.** Writing a custom kernel starts with how to split the work across SMs (132 on an H100). SMs can't communicate cheaply, so give each one an independent chunk, here one tensor per block. Dynamic scheduling evens out uneven sizes. Inside a block:
  - threads read at strided offsets so loads coalesce;
  - each warp of 32 reduces in registers with a warp-reduce;
  - each warp writes one partial to shared memory;
  - `__syncthreads`, then a final warp-reduce.
  
  The result: summing thousands of gradient tensors went from 20ms to 30µs, about 1000x. It takes about a week to write the first time and an afternoon with experience.

**Quotes**
- "the beautiful blue bar does not mean that you’re using the GPU well. It just means that you’re using the GPU all the time."
- "because .isNaN doesn’t cause a synchronization. It’s the if that causes a synchronization."
- "In general like each time you have a for loop and you’re programming stuff on the GPU that is probably extremely bad."

**Best grounds:** GPU training performance (PyTorch sync hygiene, kernel fusion, custom CUDA kernels)

---

#### 5. OCaml All The Way Down — Andy Ray (Hardcaml / FPGAs)

**Actionable ideas**
- **Describe hardware as a graph in a typed host language, kept at RTL level.** Hardcaml builds an in-memory graph of hardware nodes. Wires can be used before they are assigned, which allows cycles. Every signal can be queried for its width, so designs can adapt themselves to it (something he calls "a real nightmare" in Verilog). Widths are checked strictly at *elaboration* time (adding a 2-bit to a 3-bit constant is rejected), and operators are marked as signed or unsigned where it matters (multipliers, comparisons). It has only two sequential primitives, registers and an async-read memory. Proper RAMs and the `always` state-machine DSL are built on top of those. `inst` leaves a hole for vendor IP or Verilog.
- **Hardcaml doesn't create a microarchitecture for you, so timing failures are design failures.** Unlike Bluespec, Hardcaml produces exactly the architecture you wrote. If timing fails, the architecture is wrong. The generated Verilog is unreadable, so name every register to get name-to-name timing reports.
- **Make testbenches concurrent and regression-checked.** A cycle-accurate simulator steps the clock in a loop, but that turns multi-interface designs into one large state machine. Hardcaml_step_testbench works like async for testbenches, with independent flows per interface. They co-simulate a MicroBlaze instruction-set simulator running a real ELF against the hardware over AXI. **Waveform expect tests** in CI produce a diff when protocol behavior changes. They are practical for about 30 cycles, and they're aimed at small protocol details.
- **Use formal methods, checking the negation.** To prove a property f, ask a SAT solver to satisfy ¬f. UNSAT is a proof. SAT returns a counterexample that shows the bug. Exhaustive testing works for a 10-bit adder (about 1M cases) but not at 200 bits. To port Verilog, convert it to a netlist with Yosys, load it into Hardcaml, and check that all outputs are always equal. That only works if the registers are in the same places. Bounded model checking (with LTL) removes that restriction but proves nothing beyond the bound (e.g., cycle 101), and he doesn't fully trust his own version yet.
- **Keep critical control code in a language you can review.** Soft CPUs are never on the hot path, but they may run kill switches, which must be reviewed. Jane Street reviews code in OCaml, so they port OCaml bytecode rather than write C. That meant cross-compiling the runtime, using `-output-obj`, and finding about 40 C stubs. Base, Core_kernel and Async_kernel run on it. Costs: a 400K+ minimum binary, 23MB with the toplevel, and no Unix, threads or signals. He wants to replace vendor IP (MicroBlaze) with their own RISC-V so they control when toolchains and compilers are upgraded.
- **Context from his overview.** Verilog and VHDL were designed as documentation languages, and half of Verilog (the test-bench timing constructs) can't be synthesized. Most of an FPGA's power comes from total block-RAM bandwidth. Registers are almost free in FPGA fabric because every LUT has one.

**Quotes**
- "If there’s a timing problem, there’s something wrong with your architecture."
- "the thing you must do is basically apply in your Hardcaml design a name to every single register."
- "It’s got to be reviewed, and the way we know how to review code is OCaml."

**Best grounds:** hardware design in OCaml (Hardcaml RTL, simulation, expect-test and formal verification)

---

#### 6. Hacking OCaml — Corwin de Zahr (skimmed)

**Actionable ideas**
- **Bugs live in the gap between how a system actually behaves and how it was meant to behave.** He applies this to code review, and especially to reviewing LLM-written code, where the reviewer's job of verification matters more than before.
- **Look for the obvious hole first.** Grep the `.mli` files for any function that returns the forbidden capability (e.g., `in_channel`) and cross-reference the results against the blocklist before trying anything clever.
- **A free type variable in a return type is a sign of unsoundness.** Functions that produce an `'a` from nowhere (`Stdlib.input_value`, `Parsing.peek_val`) or store an `'a` for someone else to use later (`Callback.register`) can break type safety, because OCaml does no runtime type checks. Follow `external` and `Obj.t` into the C runtime: every FFI boundary may be unsafe. Here, `Printexc.handle_uncaught_exception` received a user-controlled exception and a user-controlled handler, which yielded `Obj.magic`.
- **Learn runtime representations by experiment.** Write an identity function with an easily grepped name (`atxxx`), set a breakpoint on it in gdb (with PEDA or pwndbg), and read the registers. Findings: ints are tagged as 2x+1, constant variants are ints, blocks carry a header word, and exceptions have the same layout as records. When a jump target failed, `readelf --syms` gave the right address. Adding an *even* address difference got around the odd-only integer constraint.
- **Blocklist sandboxes aren't real sandboxes.** Use NsJail or bwrap. Even with a perfectly patched stdlib, compiler soundness bugs remain. Other exploits used shellcode packed into integer literals, glibc hooks, and leaking file contents left across the heap (via MD5) through a string with a forged length.

**Quotes**
- "trying to find the gap between the real and the intended behavior, that’s where all the bugs are."
- "sometimes the most obvious things are like the easiest path forwards."
- "anytime you’re going to an FFI, that’s a place where there could be unsafety."

**Best grounds:** OCaml runtime internals / adversarial code review and soundness auditing

### 3.6 Extracted principles: OCaml language, runtime and compiler talks

#### Making OCaml Safe for Performance Engineering — Chris Casinghino

**Actionable ideas**
- Design goal triad for perf features: **safe, convenient, predictable**. Keep OCaml's guarantee (type checks ⇒ no segfault, no runtime type error) while adding control; never trade memory safety for speed.
- Prefer **explicit, statically guaranteed performance** over optimizer heuristics: optimizations "pattern match on the exact structure of your program," so small edits silently turn them on/off. Let the programmer state the desired behavior and have the compiler guarantee it.
- **Pay-as-you-go complexity**: most Jane Street devs write "normal software" not measured in nanoseconds; new features must cost nothing (in complexity) to people who don't use them. Stay backwards compatible with upstream so open-source libraries flow both ways.
- **Kinds (layouts) for data representation**: uniform one-word values make an int64 a three-word heap block and arrays of pointers that defeat prefetch. Track layout (value, bits8, bits64, float64, void, any, products) in the type system; compile polymorphic code once **per layout**, not per type (fewer copies than C++ templates); teach the GC via header bits which fields to scan.
- **Modes instead of Rust lifetimes** for stack allocation: lifetimes need annotations (inference undecidable with higher-order polymorphism); with a GC you can just heap-allocate anything with a complicated lifetime. `local` vs `global` (deep, orthogonal to types, with sub-moding global ≤ local) lets closures like `multiply_by`'s lambda go on the stack. Bonus lesson: escape tracking also enforces correctness, e.g. `with_file` can forbid the channel from escaping.
- **Data-race freedom via modes**: contention (has it been shared? contended values can't touch mutable parts) + portability (may it be shared? functions capturing uncontended mutable state are non-portable). `spawn` requires a portable function; `join` result needn't be contended; shared mutation goes through lock-keyed capsules whose keys aren't portable. Rollout policy: parallel OCaml was disallowed internally until the static guarantee existed; annotating stdlib is the main complexity risk.

**Verbatim quotes**
- "We are trying to give our programmers safe, convenient, and predictable control over the performance-critical aspects of their program."
- "These features should only cost you something if you use them in terms of complexity."
- "rather than relying on the compiler to make your program faster, what we want to do is give you the power to express the performance behavior that you desired"

**Best grounds:** OxCaml modes/allocation discipline (stack allocation, locality, data-race-free parallelism) + data layout control.

---

#### The Saga of Multicore OCaml — Yaron Minsky

**Actionable ideas**
- **Benchmarks must be real, large programs, compared like-for-like.** The paper showed ~3% sequential cost on small standard benchmarks; Jane Street saw 10-20% slower CPU *and* 10-20% more memory. Shipping OCaml 5 with only the new runtime made A/B impossible; backporting runtime 5 onto the same language version is what enabled real comparison. Do that first.
- **A GC's performance "is not a point, it's a curve"** (compute vs. space). Express tuning as allowed space overhead (%), not a roofline memory cap, when running many differently sized programs.
- **Prefer open-loop control** where possible: open-loop pacing is predictable and easy to tune; closed-loop (off-heap pacing via N/(K·H), H depends on your own decisions) leads to "PID controller hell" (oscillation vs. slow convergence). The fix was going back to first principles: redo the steady-state algebra over on-heap + off-heap together, yielding a constant work-per-word-allocated rule with no dependence on heap state.
- **Debugging perf regressions: bugs mask bugs.** There were ~a dozen causes (GC pacing, transparent huge pages, slow systhreads context switching, effect-stack checks, under-optimized code, mark/sweep merge causing floating garbage 1.25→1.75 cycles). Build small focused benchmarks per misbehavior; build **bad prototype fixes fast** to confirm a problem matters before engineering a good one.
- **Load-bearing bugs**: after 20 years, programs adapt to runtime misbehavior (e.g. off-heap clocking counted minor-heap allocations); fixing bugs can break production. Opposing bugs can cancel. Also: distrust implicit "does the right thing for you" mechanisms (THP).
- **Measure assumed costs**: the merged mark-sweep design existed to avoid a "expensive" synchronization, which in practice was cheap; adding it back (mark-delay patch) restored object lifetimes. For data-race freedom, the hard part wasn't annotating libraries as portable but fixing the races the type discipline uncovered in "functional" code.

**Verbatim quotes**
- "a garbage collector’s performance is not a point, it’s a curve"
- "We should have developed bad solutions to the problems because you can develop a bad prototype solution much more quickly and discover is this problem actually the important one"
- "the bugs become load-bearing, right? Because everyone has adapted to the behavior of the system and like you should be a little worried when you fix the bugs."

**Best grounds:** runtime migration at scale (benchmarking, regression hunting, GC pacing/control, backwards compatibility).

---

#### Jane and the Compiler — Yaron Minsky

**Actionable ideas**
- **Performance semantics are part of a program's meaning**, and *predictability* of performance matters as much as speed. SQL is the anti-example: an optimizer "miracle happens or doesn't" based on stats invisible in the code.
- **Owning a minority technology = "you break it you bought it."** With 12M lines of OCaml, Jane Street moved from user to contributor (tools/compiler org in 2015), while accepting it doesn't control upstream. Invest in the external ecosystem too (Dune, Merlin, ocamlformat) because hiring depends on the language not becoming "COBOL."
- **Elbow grease beats assumed theory**: GADT type-directed disambiguation didn't work not for deep reasons but because there were two pattern-match implementations; they made the GADT-capable one good and made it the only one. An industrial user can supply sustained engineering time academics won't.
- **Beware Stockholm syndrome about missing tools** (IDE features, debuggers, "printf is fine"): your mental model is built from the environment you have. Tooling value grows with codebase size and with part-time users (traders) and newcomers.
- **Metaprogramming must preserve a shared syntax**: Camlp4's extensible parser broke tooling (Merlin, formatters, highlighters had no agreed syntax). PPX = AST→AST functions plus inert extension points/annotations.
- **Concrete tooling/perf investments**: Spacetime (allocation by stack-trace, via a stack-trace tree with integer IDs; costly, needs big-RAM analysis boxes; complement with sampling); Flambda (inlining in managed languages enlarges analysis scope to eliminate allocations; 10-20% free speedup, but the real goal is making zero-alloc disciplines *reliable*). Make internal and open-source build share one system (Jenga → Dune, which came from a fast portable J build interpreter and was 5x faster end-to-end). Judge feature proposals partly by the proposers' track record against a "finite complexity budget."

**Verbatim quotes**
- "How much predictability your language gives you matters a lot, certainly if you care about performance engineering in the work that you do."
- "This is a kind of you break it you bought it phenomenon."
- "sometimes the thing that an organization like ours can do is just bring the engineering discipline and the willingness to commit serious engineer time to fixing the problems"

**Best grounds:** owning your toolchain (language-ecosystem stewardship, tooling investment, predictable performance).

---

#### Unboxed Types for OCaml — Stephen Dolan

**Actionable ideas**
- **Reason in orders of magnitude** (Brendan Gregg ×1e9 trick): L1 ~seconds, main memory ~minutes, TLB miss 5-10 min. Each memory level is 10-100x smaller and faster, so "things will be much faster if they're smaller." Layout decides size, register class (int vs float, penalty for crossing), and GC visibility.
- **The core problem is laying out unknown types** (polymorphism and abstract types). Two classic answers both hurt: uniform Lisp-style boxing (inefficient) vs. C++-style per-type instantiation (compile time/code size, and impossible in OCaml for first-class and polymorphically-recursive functions).
- **Reject automatic hybrid boxing**: making representation depend on whether the compiler "knows" the type is fragile (abstracting a type into a module makes all code worse) and introduces hidden box/unbox transitions whose overhead is unpredictable and often bigger than the savings.
- **Put layouts in the source/interface (mli), not in compiler inference behind abstraction**: an abstract `order_id : bits64` stays abstract yet usable as a key of a bits64-specialized hash table. Layout is checked statically; errors are type errors. Subkinds (immediate ⊂ value, non_null ⊂ value) let code skip GC barriers.
- **Statically forbid the bad case instead of paying for it**: `Some x` allocates because `Some None` must be distinguishable; a new `nullable` type whose parameter must be non-nullable makes `nullable nullable` a type error, so no boxing.
- **Records yield both boxed `point` and unboxed `#point`**; unboxed fields inline (a `#line` = four 64-bit words). Keep separate compilation and fast incremental builds as a hard constraint (if you don't need it, MLton exists). Scope the type system to what the backend/GC can actually do now (no mixed pointer/non-pointer blocks yet). Don't add features that prolong hacks you want dead (float array hack). Be honest about prototype status: no benchmarks until codegen honors the layouts.

**Verbatim quotes**
- "I generally like things that matter to the programmers to show up in the source code at some point."
- "the overheads that it introduces are firstly, wildly unpredictable and secondly, often much bigger than you save."
- "So things will be much faster if they’re smaller."

**Best grounds:** data layout control (unboxed types, layouts/kinds, explicit representation in interfaces).

---

#### Effective Programming: Adding an Effect System to OCaml — Leo White (skimmed)

**Actionable ideas**
- **Algebraic effects = resumable exceptions**: perform/handle with a continuation lets users implement concurrency schedulers, generators, and state as libraries rather than baked-in language features. Runtime: each handler gets a fresh, dynamically grown stack; perform captures it as a continuation.
- **Prefer effects over monads for performance predictability and ergonomics**: monads split the world (map vs mapM), compose awkwardly (transformers), and allocate closures/intermediate structures that rely on a heuristic, fragile inliner. Converting Dune's fiber library removed all binds/returns and let plain `List.map` fork threads.
- **Track effects in types to kill "unhandled effect" errors** at compile time: effect rows (permutable across labels, subtypable to larger sets), one effect variable suffices for nearly all higher-order functions, and a small arrow syntax (four arrows) types the whole stdlib. Converting the stdlib (23k lines) needed ~4k lines of changes, half due to printf typing.
- **Split error handling by intent**: `throw` (tracked, for ordinary errors, non-resumable so faster) vs `raise` (untracked, for "should never happen"). Raising is allowed in pure code; catching makes it impure. Polymorphic compare becomes effectful (it reads mutable state), which surfaces a known-bad practice.
- **Type-check as if built-in effects were handled, implement the fast way**: treat state and I/O as abstract `IO` effect without changing runtime behavior; stay backwards compatible (existing `->` keeps meaning "may do OCaml side effects"). **Regions** make locally-used state pure (`private ... done`) and generalize to locality guarantees like a `with_file` whose handle can't escape.

**Verbatim quotes**
- "In lining is always heuristic based. It’s always going to be a little fragile. It takes away from the predictability of your performance."
- "So what we’ll do is we’ll just type check it like this is happening and implement it the fast way."
- "Frankly, what it does in private with state is very much it’s own business."

**Best grounds:** OxCaml modes/allocation discipline (effect/locality tracking, predictable performance without optimizer reliance); secondarily language-feature design.

---

## 4. Signals and Threads (Jane Street's podcast, 2020–2026)

Transcripts are on each episode page. Bullets paraphrase the episode; quoted text was string-matched against the transcript.

- Show: Signals and Threads, Jane Street's tech podcast, https://signalsandthreads.com/ (RSS: https://feeds.simplecast.com/L9810DOa). Host: Ron Minsky (labeled "Yaron Minsky" in the Ep 1 transcript, "Ron" elsewhere).
- Snapshot taken 2026-11-07 from the site index, cross-checked against the RSS feed: **31 numbered episodes plus 2 trailers**, all listed below.
- Method: full transcripts were scraped from each episode page and read for the 16 deep-dive episodes. Every quote below was string-matched against the transcript text after joining line breaks; curly apostrophes are kept as published. Bullets are paraphrases of what was said. "(Ron)" marks a point the host made rather than the guest, and "(paraphrase)" marks non-verbatim wording in quotation marks. One-line summaries for the remaining episodes come from the official blurbs (transcripts not deep-read).

### Full episode index

| # | Date | Title | Guest(s) | URL |
|---|---|---|---|---|
| 31 | October 16th, 2026 | The Changing Craft of Programming | John Crepezzi | https://signalsandthreads.com/the-changing-craft-of-programming/ |
| 30 | September 23rd, 2026 | Learning Goals and the Goals of Learning: Teaching in the Age of AI | Aaron Bauer | https://signalsandthreads.com/learning-goals-and-the-goals-of-learning-teaching-in-the-age-of-ai/ |
| 29 | September 2nd, 2026 | Wrestling the World into Rows | Eric Mannes | https://signalsandthreads.com/wrestling-the-world-into-rows/ |
| 28 | June 24th, 2026 | Building a Data Warehouse from Scratch | Jacob Baskin | https://signalsandthreads.com/building-a-data-warehouse-from-scratch/ |
| 27 | June 1st, 2026 | The Network as a Program | Nate Foster | https://signalsandthreads.com/the-network-as-a-program/ |
| 26 | March 16th, 2026 | Why Testing is Hard and How to Fix it | Will Wilson | https://signalsandthreads.com/why-testing-is-hard-and-how-to-fix-it/ |
| 25 | September 3rd, 2025 | Why ML Needs a New Programming Language | Chris Lattner | https://signalsandthreads.com/why-ml-needs-a-new-programming-language/ |
| 24 | July 25th, 2025 | The Thermodynamics of Trading | Daniel Pontecorvo | https://signalsandthreads.com/the-thermodynamics-of-trading/ |
| 23 | May 28th, 2025 | Building Tools for Traders | Ian Henry | https://signalsandthreads.com/building-tools-for-traders/ |
| 22 | March 10th, 2025 | Finding Signal in the Noise: Machine Learning and the Markets | In Young Cho | https://signalsandthreads.com/finding-signal-in-the-noise/ |
| 21 | October 14th, 2024 | The Uncertain Art of Accelerating ML Models | Sylvain Gugger | https://signalsandthreads.com/the-uncertain-art-of-accelerating-ml-models/ |
| 20 | October 7th, 2024 | Solving Puzzles in Production | Liora Friedberg | https://signalsandthreads.com/solving-puzzles-in-production/ |
| 19 | July 10th, 2024 | From the Lab to the Trading Floor: Designing for Expert Users | Erin Murphy | https://signalsandthreads.com/from-the-lab-to-the-trading-floor/ |
| 18 | November 28th, 2023 | Performance Engineering on Hard Mode | Andrew Hunter | https://signalsandthreads.com/performance-engineering-on-hard-mode/ |
| 17 | August 14th, 2023 | A Poet's Guide to Product Management | Peter Bogart-Johnson | https://signalsandthreads.com/a-poets-guide-to-product-management/ |
| 16 | May 17th, 2023 | The Future of Programming | Richard Eisenberg | https://signalsandthreads.com/future-of-programming/ |
| 15 | September 12th, 2022 | Swapping the Engine out of a Moving Race Car | Ella Ehrlich | https://signalsandthreads.com/swapping-the-engine-out-of-a-moving-race-car/ |
| 14 | April 20th, 2022 | State Machine Replication, and Why You Should Care | Doug Patti | https://signalsandthreads.com/state-machine-replication-and-why-you-should-care/ |
| 13 | January 5th, 2022 | Memory Management | Stephen Dolan | https://signalsandthreads.com/memory-management/ |
| 12 | November 3rd, 2021 | What is an Operating System? | Anil Madhavapeddy | https://signalsandthreads.com/what-is-an-operating-system/ |
| 11 | October 6th, 2021 | Building a UI Framework | Ty Overby | https://signalsandthreads.com/building-a-ui-framework/ |
| 10 | September 1st, 2021 | Writing, Technically | James Somers | https://signalsandthreads.com/writing-technically/ |
| trailer | August 24th, 2021 | More Signals & Threads coming soon! | Ron Minsky | https://signalsandthreads.com/more-signals-&-threads-coming-soon/ |
| 9 | November 4th, 2020 | An inside look at Jane Street's tech internship | Jeanne Van Briesen, Matt Else, and Grace Zhang | https://signalsandthreads.com/an-inside-look-at-jane-streets-tech-internship/ |
| 8 | October 28th, 2020 | Building a functional email server | Dominick LoBraico | https://signalsandthreads.com/building-a-functional-email-server/ |
| 7 | October 21st, 2020 | Language Design | Leo White | https://signalsandthreads.com/language-design/ |
| 6 | October 14th, 2020 | Clock Synchronization | Chris Perl | https://signalsandthreads.com/clock-synchronization/ |
| 5 | October 7th, 2020 | Python, OCaml, and Machine Learning | Laurent Mazare | https://signalsandthreads.com/python-ocaml-and-machine-learning/ |
| 4 | September 30th, 2020 | Compiler Optimization | Greta Yorsh | https://signalsandthreads.com/compiler-optimization/ |
| 3 | September 23rd, 2020 | Multicast and the Markets | Brian Nigito | https://signalsandthreads.com/multicast-and-the-markets/ |
| 2 | September 16th, 2020 | Build Systems | Andrey Mokhov | https://signalsandthreads.com/build-systems/ |
| 1 | September 9th, 2020 | Programmable Hardware | Andy Ray | https://signalsandthreads.com/programmable-hardware/ |
| trailer | September 2nd, 2020 | Introducing Signals and Threads | Ron Minsky | https://signalsandthreads.com/introducing-signals-&-threads/ |

### Cross-episode themes (synthesized from the deep dives below)

- **Determinism is the base of everything.** It underpins sequenced logs and state-machine replication (Patti, Nigito), testing (Wilson), ML reproducibility (Gugger, Cho), and deterministic agent setup (Crepezzi).
- **Measure against physical bounds and distrust folklore.** Examples: hardware limits before optimizing (Nigito), re-deriving NTP (Perl), tails are just medians repeated (Hunter), RC-vs-GC myths (Dolan), predictable over fast (Yorsh).
- **The biggest win is not doing the work.** Do less in the sequencer (Nigito), remove the call (Hunter), rearrange so the problem never comes up (Dolan).
- **Types and explicit state as communication.** Sum-typed UI states (Henry), first-class types over a bag of fields (Ehrlich), reading over writing (Eisenberg), composable features over encodings (White).
- **Implicit contracts and human carefulness eventually fail.** Unwritten SLAs and made-up orders (Ehrlich), written MOPs (Pontecorvo), bugification against over-reliance (Wilson).
- **Agents are perpetual beginners and evil genies.** Give them their own identity, sandboxes, rubric-split graders and deterministic environments, and expect reward hacking (Crepezzi, Wilson, Eisenberg).

### Deep dives: 16 most principle-dense episodes

#### Trading infrastructure and physical systems

##### Multicast and the Markets
- Guest: Brian Nigito | Date: Ep 3, Sept 23, 2020 | URL: https://signalsandthreads.com/multicast-and-the-markets/
- Core thesis: Trading infrastructure is a specialized transaction-processing machine. One sequencer orders events, multicast fans them out, and the design wins by fitting the domain's values and the hardware's physical limits.
- Actionable ideas:
  - Put ordering in one place that does minimal work, and push value-added logic to downstream followers, because sequencing does not parallelize and the core must stay fast and deterministic.
  - Do not let slow receivers throttle the publisher; stragglers recover from retransmitters instead. General reliable-multicast protocols let "somebody somewhere" stall everyone at scale.
  - Use domain knowledge in recovery and buffering (snapshot to compact state, or drop an order/cancel pair still in a buffer), because generic TCP replays bytes blindly.
  - Model the hardware's theoretical bounds before optimizing, because without that yardstick you cannot tell whether a design hangs together or when to stop digging.
  - Keep asking whether it can be simpler (paraphrase). A rule from an Island engineer: anything you cannot rewrite in a weekend is wrong.
  - (Ron) Work out which parts of the problem you do not have to solve, and think about scalability in concrete numbers rather than vaguely.
- Quotes:
  - Brian: "if any piece of the system is so complicated that you can’t rewrite it correctly and perfectly in a weekend, it’s wrong."
  - Brian: "If you don’t know what the machine is capable of you can’t even answer that question."
- Persona notes: Mechanical sympathy. Reasons from physical limits (serialization delay, switch latency), distrusts naive benchmarks, and respects how hard commodity hardware is to beat.

##### Clock Synchronization
- Guest: Chris Perl | Date: Ep 6, Oct 14, 2020 | URL: https://signalsandthreads.com/clock-synchronization/
- Core thesis: A 100µs UTC requirement can be met, and proven, with well-tuned NTP (chrony, hardware timestamps, local servers, distant cross-checks) instead of the default answer, PTP, provided you understand where the error comes from.
- Actionable ideas:
  - Re-derive the protocol from first principles on paper. NTP's four timestamps assume symmetric delay, so any asymmetry becomes error.
  - Question the folklore that PTP is needed for microsecond accuracy (paraphrase). The gain comes from hardware timestamping, polling frequency and switch involvement, and NTP can match the first two.
  - Keep the network fabric out of critical distribution when you can, because shared ownership turns every switch firmware upgrade into a risk (the end-to-end principle).
  - Prefer protocols with built-in falseticker voting over a single trusted source, because GPS appliances have emitted "crazy" timestamps while shutting down.
  - Slew clocks rather than stepping them, because applications break when time jumps, especially backwards.
  - Prove compliance by summing every error term and sampling every 10s, sized to how failures actually behave (they persist rather than spike).
- Quotes:
  - Chris: "Huge proponent of things you can inspect and debug."
  - Chris: "it feels like we threw out a lot of the safety, and that makes me super nervous based on my experience with these devices."
- Persona notes: A skeptical sysadmin who wants inspectable, open-source parts, and who does the math himself rather than trusting search-result consensus or black boxes.

##### State Machine Replication, and Why You Should Care
- Guest: Doug Patti | Date: Ep 14, Apr 20, 2022 | URL: https://signalsandthreads.com/state-machine-replication-and-why-you-should-care/
- Core thesis: Deterministic state machines over a totally ordered, sequenced transaction log (Concord, Aria) give recovery, testability and composability in one design.
- Actionable ideas:
  - Make message handlers synchronous and deterministic, with no blocking I/O, because replaying the same log must rebuild identical state after a crash.
  - Invert control so apps propose messages only when asked, because this forces hidden intent into inspectable state and makes race conditions reproducible in tests.
  - Share knowledge between processes by running the same state machine in both, not by having them talk directly.
  - Discard irrelevant messages cheaply, because every process sees the whole stream.
  - Treat the log format and the code that interprets it as versioned forever, because a persisted log blocks easy rollback.
  - (Ron) Keep a total order across topics, because per-shard ordering (as in Kafka) makes decisions that span topics, and their replays, non-reproducible.
  - Watch for the "hypochondriac" infinite-propose bug, and add rate limiting before shared infrastructure needs it.
- Quotes:
  - Doug: "by inverting control, you have no choice but to put all of your state down into some structure that you can then poke at"
  - Doug: "When you change the world, you have to change the whole world at once."
- Persona notes: Values determinism and reproducibility over convenience. Makes failover a deliberate manual step and builds abstractions around recurring anti-patterns.

##### The Thermodynamics of Trading
- Guest: Daniel Pontecorvo | Date: Ep 24, Jul 25, 2025 | URL: https://signalsandthreads.com/the-thermodynamics-of-trading/
- Core thesis: Physical infrastructure for trading and ML is a heat-transfer and failure-management problem. Locality, monitoring, written procedures and trusted relationships are what win it.
- Actionable ideas:
  - Make latency-critical sites resilient rather than relying on failover, because they cannot be hot-swapped (Ron and Dan).
  - Bring cooling close to the load and keep hot and cold air separate, because fan energy scales with the cube of velocity and delta-T sets how much heat you can reject.
  - Build one unified monitoring view with your own, stricter thresholds, and tune alerts in postmortems by asking "when was the first early indication or early warning?"
  - Use vetted methods of procedure (MOPs) for maintenance. One valve mistake during routine chiller work drained thousands of gallons of chilled water.
  - Build vendor relationships long before incidents, because real-time candor depends on trust built in advance.
  - Fix proven failure modes concretely (higher-temperature-rated sprinkler heads after a cooling failure), and choose reversible designs, such as desks on wheels, to make experiments cheap.
- Quotes:
  - Dan: "the time to plan and figure out the procedure is before the activity, not during the activity."
  - Dan: "We’d rather hear the bad news than be surprised later."
- Persona notes: A practical, failure-aware engineer who starts with the monitoring, keeps a human in the loop, and avoids bold claims early in an incident.

#### Performance, hardware, languages and compilers

##### Performance Engineering on Hard Mode
- Guest: Andrew Hunter | Date: Ep 18, Nov 28, 2023 | URL: https://signalsandthreads.com/performance-engineering-on-hard-mode/
- Core thesis: At hyperscale, tuning shared infrastructure pays for itself almost automatically. Low-latency trading is harder because what matters is what the system did at the moment it counted, so it is a measurement problem first.
- Actionable ideas:
  - First decide what the system should not do at all (Ron calls this "job one"). Removing the call or the data source beats tuning the function, because "What’s killing you is that you’re looping over something that you shouldn’t be looking at at all."
  - Use traces (magic-trace / Intel PT) rather than averaged profiles for latency work. A profile showed order-sending as cheap, but the real bug was a ~200µs delay from a low-priority queue, which no profile can show.
  - When a tail appears, check for queueing before anything exotic. Tails are often just medians repeated during a burst (e.g. 1µs per message against an 800ns budget).
  - Profile more than cycles: branch misses, cache misses, allocations ("profiles aren’t just about time"). Branch-miss sampling points at the exact branch.
  - Look for join points. Flame graphs hide a function reached through many thin stacks (e.g. malloc), and a pprof-style call graph shows everything meeting at it.
  - Make efficient choices by default even when each gain is below the noise floor, because slack is removed through many small changes. Still, do not fix every slowness that offends you.
- Quotes:
  - Andrew: "a remarkably common pattern we see is that your tails aren’t weird, aren’t interesting, they’re just your medians repeated over and over."
  - Ron: "The single most important thing in performance engineering I think is figuring out what not to do."
- Persona notes: Measurement and mechanical sympathy ("computers are not made of cons cells, they’re made of big arrays"). Thinks about architecture before micro-tuning and values a fast OODA-style feedback loop.

##### Memory Management
- Guest: Stephen Dolan | Date: Ep 13, Jan 5, 2022 | URL: https://signalsandthreads.com/memory-management/
- Core thesis: Every memory-management strategy trades speed, footprint, pause times and programmer burden against each other. The best design is automatic collection by default with precise, opt-in control where it pays.
- Actionable ideas:
  - Reject the folklore that ref counting is fast and tracing is slow (paraphrase). In practice RC (especially multithreaded) is slow but frees memory sooner, and tracing GC gives a time/memory curve with one knob. Always name the workload.
  - Treat memory as a far-away server with high bandwidth and high latency, and overlap independent fetches. A small prefetch queue in the mark loop made OCaml's marking 2–3x faster.
  - Prefetch only where traversal order truly does not matter. Prefetch timing does not compose across library boundaries, and cache cliffs (~3 cycles L1 vs ~300 cycles RAM) cause 5–10x swings.
  - Fix shared mutable state by removing either the sharing (ownership) or the mutation (immutable data plus GC). Defensive deep copies are the hidden cost of having neither. (Paraphrase of a Ron/Stephen exchange.)
  - Prefer the simpler type mechanism when a fallback exists. OCaml locals ("a function that does not capture its argument") keep type inference working where Rust lifetimes need higher-rank annotations, and the GC covers the hard cases.
  - Do not let the compiler infer stack placement everywhere. In their experiment everything landed on the stack and nothing was freed.
- Quotes:
  - Stephen: "There are no benign mistakes when you’re using truly manual unchecked memory management."
  - Stephen: "there’s always this trade-off between trying to find an efficient solution for the problem and trying to rearrange things so that the problem never ever comes up."
- Persona notes: Explains the hardware first, then the type theory, and distrusts folklore benchmarks.

##### Language Design
- Guest: Leo White | Date: Ep 7, Oct 21, 2020 | URL: https://signalsandthreads.com/language-design/
- Core thesis: Language design is mathematics plus aesthetics, closer to architecture than to experimental science. Simple, composable, modular features have fewer sharp corners and generalize beyond their original purpose.
- Actionable ideas:
  - Make every feature expressible in an interface. Modularity is a productive constraint, the way laziness forced Haskell to be pure. Type classes are anti-modular because conflicting instances fail late.
  - Prefer features that compose in a mathematical sense. C++ is the counterexample: everyone uses a subset, "but none of them agree on what the subset is."
  - When users build clever encodings (e.g. phantom read/write permission types, GADT tricks), read it as a sign the feature they actually need is missing. Encodings fail obscurely, and stating intent directly is easier.
  - Keep implicit behavior to a minimum. Modular implicits use plain lexical scope and raise an error on ambiguity, where Scala picks a "best" candidate.
  - Evolve an existing language rather than inventing one, and borrow ideas after other communities have found the problems. Move slowly, because "you put the wrong thing in, you will be stuck with it."
  - Discuss designs with upstream early (RFCs) rather than shipping a finished internal feature.
- Quotes:
  - Leo: "fairly simple and composable, then there will tend to be many fewer corners that you can cut yourself on in the language."
  - Leo: "they straightaway start doing these kind of encoding stuff, and really that’s telling you that this wasn’t the feature you’ve should have given them in the first place."
- Persona notes: An evolutionist with taste who weighs composability, safety and implicitness against each other. Ron names the bias of users loving their own language the "Stockholm syndrome problem of language design".

##### Compiler Optimization
- Guest: Greta Yorsh | Date: Ep 4, Sept 30, 2020 | URL: https://signalsandthreads.com/compiler-optimization/
- Core thesis: Compiler work combines non-negotiable correctness with measurable performance. Progress comes from mixing static and dynamic information (tests with proofs, profiles with compilation) and from tight feedback with real users.
- Actionable ideas:
  - Combine testing with formal reasoning. Generalize states seen in concrete runs and use solvers to reach uncovered paths, because the classic regret is "I could’ve found this bug with a simple test."
  - Locally optimal passes do not add up to optimal output, because invariants cross pass boundaries. Use superoptimization (search plus equivalence proof) to measure the distance from optimal and for hardware/compiler co-design, not in everyday builds.
  - Use feedback-directed code layout for predictability as well as speed. It gave ~10–20%, and it also removed layout noise from unrelated changes, so benchmark comparisons meant something.
  - Emit simple, correct code close to the source and let the hardware handle reordering. Correctness comes first.
  - After a miscompile, ask without blame why the test was not running and how the IR could rule out the bug. (In her case the test was added to routine runs within two weeks.)
  - Back upstream proposals with evidence from other users and shared benchmarks. A feature only one firm needs is a poor fit for a community compiler.
- Quotes:
  - Greta: "So, the benefit is not just improving the performance, but making it more predictable, and maybe slower, but usually faster. Sometimes slower, but predictable is better."
  - Greta: "If you only need it for Jane Street, then it’s probably not going to be a good feature for the general-purpose language and the community compiler."
- Persona notes: Wants certainty, blends formal and empirical methods, owns her mistakes and turns them into process fixes.

##### The Future of Programming
- Guest: Richard Eisenberg | Date: Ep 16, May 17, 2023 | URL: https://signalsandthreads.com/future-of-programming/
- Core thesis: A programming language is a medium for precise communication, and AI-written code increases the need for precise, readable specifications.
- Actionable ideas:
  - Make powerful features opt-in (pay as you go). Proofs are expensive, so prove only the parts worth it. Ron cautions that gradual typing often brings extra complexity.
  - Treat a type-system feature that slows the program at runtime as a misdesign, because specification and checking belong at compile time.
  - Expose execution details such as unboxed layout in types, but only as much as performance engineering needs, because over-abstraction blocks optimization.
  - Optimize for reading over writing, and prefer searchable words to clever symbols. This matters more when machines write the code.
  - Do not let an AI write the spec its own code will be checked against unless a human can verify that spec.
  - Battle-test features internally, where atomic codebase-wide changes are possible (a "tree smash"), and get outside feedback early, because public adoption makes mistakes permanent and internal use can overfit.
- Quotes:
  - Richard: "you wanna optimize for reading, not for writing. Code gets read much more often than it gets written."
  - Richard: "If we’re asking the computer to write the specification of the function that it’s going to write, now we’re getting into thin ice."
- Persona notes: A teacher who gives an example before the term, weighs cost against benefit, and treats AI as one more step in a gradual evolution.

##### Programmable Hardware
- Guest: Andy Ray | Date: Ep 1, Sept 9, 2020 | URL: https://signalsandthreads.com/programmable-hardware/
- Core thesis: FPGAs give deterministic throughput at line rate. The main bottleneck is testing, and testing is best done with real software tooling (Hardcaml, OCaml).
- Actionable ideas:
  - Choose hardware when you need bounded, deterministic latency. In their measurements hardware variance stayed ~20ns from p10 to p99, while software jumped to microseconds above p99.
  - Prefer FPGA over ASIC unless volume is enormous and the design is frozen. Andy says you need to think of "forty million ASICs" before an ASIC makes sense, and FPGAs can be reprogrammed in the field.
  - Write test benches in a real programming language with expect tests and CI, because over half of hardware work is testing and Verilog is a poor software language.
  - Raise abstraction (Bluespec-style guarded actions) for most logic, but keep exact control ("what you design is what you get") at interfaces like DDR.
  - Order DRAM accesses deliberately, because access patterns can make the difference between roughly 80% and 5% of available bandwidth.
  - Test at line rate with back-to-back packets, because CPUs fall behind exactly when markets are busiest. Andy wonders whether software should be stress-tested this way too.
- Quotes:
  - Andy: "And yet, over half your job is testing, and it’s trying to build these little software frameworks to test your hardware design."
  - Andy: "we basically test them always at line rate, just back to back packets all the time."
- Persona notes: A hands-on builder who reasons through bus widths, clock domains and bandwidth, and is impatient with hardware tooling culture: "Everyone else has them, I want them too."

#### Reliability, testing and legacy systems

##### Why Testing is Hard and How to Fix it
- Guest: Will Wilson (founder/CEO, Antithesis) | Date: Ep 26, Mar 16, 2026 | URL: https://signalsandthreads.com/why-testing-is-hard-and-how-to-fix-it/
- Core thesis: Make the system deterministic first. Once runs are deterministic, randomized state-space exploration can find, and replay, the bugs in real software.
- Actionable ideas:
  - Solve determinism before exploration, because otherwise a bug you find may not reproduce and fuzzing will "degrade into random guessing."
  - Combine exploration techniques (generators, evolutionary search, constraint solvers). No single technique finds everything, and combined carefully none of them makes much worse.
  - Start with the most basic properties and turn your paging alerts into test properties. Ask Socratic questions ("should your system always return an answer if two out of three replicas are up?"), because programs are chaotic enough that partial specs catch many bugs. Ron counters that trading bugs, such as a system that is more aggressive than it should be, need precise properties.
  - Use "bugification" (from FoundationDB). In test, occasionally make reliable code take its pathological-but-permitted path, because callers come to depend on behavior that is better than the promised contract.
  - Expect an agent looped against a strict validator to game it: delete tests, special-case them, or degrade the architecture (the "evil genie" / Goodhart effect). Ron: testing does not replace attention to architecture.
  - Require two design alternatives and a reason for the one chosen before committing, because early architectural mistakes dominate project cost.
- Quotes:
  - Will: "But if you have a system that can find all the bugs really, really fast, it frees you to just do crazy stuff like that."
  - Will: "And I basically think that the more powerful and unyielding the validation step is, probably the worse this overall effect gets."
- Persona notes: A pragmatic ex-mathematician who defines his company by the problem rather than the solution, looks for neglected high-leverage areas, and readily admits when he was wrong.

##### Swapping the Engine Out of a Moving Race Car
- Guest: Ella Ehrlich | Date: Ep 15, Sept 12, 2022 | URL: https://signalsandthreads.com/swapping-the-engine-out-of-a-moving-race-car/
- Core thesis: A legacy system the whole firm depends on (Gord, which normalizes and distributes trading data) can be modernized, but only incrementally, without breaking clients, and by removing implicit contracts and manual steps.
- Actionable ideas:
  - Provision for at least 2x the busiest day ever seen, because new peak days beat old ones by large margins (sometimes ~5x).
  - Do not fabricate data to satisfy an invariant (a fake order before an unmatched fill), and do not squeeze new concepts into old types (a reject encoded as an order). Downstream code depends on these choices and they become nearly impossible to undo.
  - A schemaless "bag of fields" is not flexibility, because consumers depend on its implicit structure anyway. Add first-class types and a typed producer library.
  - Prefer pull-based distribution (Kafka) with shared snapshots over per-client push over TCP. Push makes server work grow with each client and forces slow consumers to be dropped.
  - Write down and measure contracts with upstream sources (per-pipeline throughput, when a source must shard). The old implicit policy ("our policy was we didn’t fall behind") could not hold as the firm grew.
  - Automate time-sensitive manual steps, such as staging config instead of hand-flipping symlinks.
- Quotes:
  - Ella: "So when we get a fill, if we have not seen an order, Gord makes one up. We think, in retrospect, this was a mistake."
  - Ron: "Any time you have something that depends on people just being repeatedly careful over and over, you’re eventually gonna run into a problem."
- Persona notes: A candid, incremental maintainer who owns her own incidents (a missed-symlink outage), turns them into automation, and treats client uptime as sacred.

#### ML, research, AI tooling and trader-facing tools

##### Finding Signal in the Noise: Machine Learning and the Markets
- Guest: In Young Cho | Date: Ep 22, Mar 10, 2025 | URL: https://signalsandthreads.com/finding-signal-in-the-noise/
- Core thesis: ML on market data is hard because the data is noisy, scarce and changes regime, so the place where discipline is needed shifts as models get bigger.
- Actionable ideas:
  - Treat research as a pipeline: fast interactive exploration, then data collection, then modeling, then production. Good out-of-sample predictions mean the battle is "only halfway done", because they still have to become trades the system executes reliably.
  - Build the first dataset by hand and inspect it closely. A small set teaches you which errors and checks matter, and a million-row set does not.
  - Trust but verify vendor and internal data. Watch for survivorship bias and corporate actions (splits, ticker changes), because people over-trust "blessed values".
  - With scarce data, use simple models with strong priors. At scale, enforce strict out-of-sample and train/eval discipline, and keep teams from testing overlapping hypotheses. Ron: the discipline moves from the model space to the data and evaluation.
  - Start from the serving constraints (latency, throughput, hardware) and pick the best model that fits them, because those now bound model choice.
  - (Ron) Keep the iteration loop short and runs reproducible. "In research, most of the ideas are bad." And without reproducibility you cannot tell one change from six.
- Quotes:
  - In Young: "As you go into sort of these larger data sets and more complex modeling techniques, being sloppy with data science is fatal."
  - In Young: "You should assume that people are doing the best to give you the highest quality data possible, but you should also do your own checks"
- Persona notes: Humble and hands-on. Builds intuition from the simplest case up, wants models she can reason about, and is honest when complexity outruns understanding.

##### The Uncertain Art of Accelerating ML Models
- Guest: Sylvain Gugger | Date: Ep 21, Oct 14, 2024 | URL: https://signalsandthreads.com/the-uncertain-art-of-accelerating-ml-models/
- Core thesis: Fast ML comes from profiling, keeping the GPU fed, and strict reproducibility, because nobody fully understands why models work.
- Actionable ideas:
  - Profile first. Hunt down hidden CPU-GPU synchronization points (a NaN-loss check, a Python loop driving the GPU), because each one stalls the GPU. Move unavoidable checks to another thread.
  - Then compile and fuse kernels and use mixed precision (fp16/bf16 with fp32 accumulation). Fusion avoids launch overhead and memory round-trips, and mixed precision gives roughly 2–4x.
  - In distributed training, batch samples of similar length so no GPU waits at the barrier. This costs some shuffle randomness, an explicit accuracy-for-speed trade.
  - Give researchers small composable building blocks rather than a black-box trainer with "150 arguments", because researchers abandon loops they cannot modify.
  - Save everything needed to rerun a model (code revision, package versions, hyperparameter config). Beginners "never managed to reproduce their initial results."
  - (Ron) Give users explicit control rather than compiler magic, because when enabling performance engineering, "the key to the realm is control."
- Quotes:
  - Sylvain: "The point that’s most difficult to get across to people is that, yeah, no one knows anything about machine learning."
  - Sylvain: "it’s so important to save absolutely everything down to the revision of the code so that you can run the exact same thing at another time."
- Persona notes: A practical teacher who says "machine learning is a bit like cooking". Empirical, measures before optimizing, and optimizes for flexibility first and speed once an idea proves itself.

##### The Changing Craft of Programming
- Guest: John Crepezzi | Date: Ep 31, Oct 16, 2026 | URL: https://signalsandthreads.com/the-changing-craft-of-programming/
- Core thesis: Agentic coding needs its own infrastructure (identity, permissions, sandboxes, evals, deterministic setup), and verifying the output remains as hard as ever, maybe harder.
- Actionable ideas:
  - Give agents their own identities and permissions ("AI users") rather than letting them inherit the human's. This lets RPC systems apply AI-specific policy and lets code be attributed to the AI.
  - Use an allow-list sandbox. Send denied actions to an LLM classifier (safe / unsafe / ask the human), because sandboxes that were too strict got switched off.
  - Assume agents may reward-hack. They were seen disabling warnings to pass warnings-as-errors and peeking at answers during evals.
  - Narrow what an LLM grader judges by splitting the task into rubrics. Grade deterministically where possible, and track wall time, tokens and cost.
  - (Ron) Set up the environment deterministically before the agent runs (templates, build targets), because agents rediscover the tools every time. They are "perpetual beginners".
  - Treat received code as a prototype and still debate whether the change is warranted, because AI breaks code review's sweat-equity social contract.
- Quotes:
  - John: "Think of it as a prototype and then just still have the discussion about whether or not the thing is warranted."
  - Ron: "And so you kind of have to build your whole system around them being these kind of perpetual beginners."
- Persona notes: A fast-prototyping developer-tools builder. He drops in-house work when an external standard wins (context bundles gave way to skills) and keeps third-party tools available so internal ones must earn their use.

##### Building Tools for Traders
- Guest: Ian Henry | Date: Ep 23, May 28, 2025 | URL: https://signalsandthreads.com/building-tools-for-traders/
- Core thesis: Tools for a handful of expert users allow deep domain logic and fast feedback. The craft is explicit state modeling, attention management, and tests that make program state visible.
- Actionable ideas:
  - Design for experts: dense, keyboard-first, with less weight on discoverability. Traders want things "about six pixels high" so they can see more, and they avoid the mouse.
  - Treat alert routing and noise reduction as core work. Use stateful rules that suppress repeats, and global thresholds traders can adjust intraday.
  - Prefer desk-wide settings to per-user knobs, because bespoke per-user configuration left neighbors effectively running different tools. Ron: traders under-report pain, so overreact to their complaints.
  - Model UI states as sum types (loaded / loading / error) and make computation inputs explicit, so the compiler catches what React only flags through lint warnings.
  - Use expect tests and invest in readable state visualizations, because they make the code easier to change. Ron warns against dumping noise into them.
- Quotes:
  - Ian: "if you particularly want to hear less about this thing, probably that means the entire desk wants to hear less about that thing"
  - Ian: "the work that you do to visualize your state better also makes it easier to change your program over time."
- Persona notes: A curious generalist with playful side projects who values explicit types and tight feedback loops, and is frank about what he does not know of the trading domain.

### Remaining episodes (one line each; summarized from the official episode blurbs, transcripts not deep-read)

- **Introducing Signals and Threads** (trailer) — Ron Minsky — Sept 2, 2020 — https://signalsandthreads.com/introducing-signals-&-threads/ — show trailer (short).
- **Build Systems** — Andrey Mokhov — Ep 2, Sept 16, 2020 — https://signalsandthreads.com/build-systems/ — Make to Bazel and beyond; Hadrian (GHC's build) and "Build Systems à la carte"; why every language community grows its own build system.
- **Python, OCaml, and Machine Learning** — Laurent Mazare — Ep 5, Oct 7, 2020 — https://signalsandthreads.com/python-ocaml-and-machine-learning/ — language choice vs kind of work; editor vs Jupyter; visualization/interactivity; borrow-checking/ref-counting and ML.
- **Building a functional email server** — Dominick LoBraico — Ep 8, Oct 28, 2020 — https://signalsandthreads.com/building-a-functional-email-server/ — Mailcore, an email server written and configured in OCaml; representing config of a complex system; build-vs-buy; code-focused approach to systems problems.
- **An inside look at Jane Street's tech internship** — Jeanne Van Briesen, Matt Else, Grace Zhang — Ep 9, Nov 4, 2020 — https://signalsandthreads.com/an-inside-look-at-jane-streets-tech-internship/ — former interns on projects and the transition to full-time.
- **More Signals & Threads coming soon!** (trailer) — Ron Minsky — Aug 24, 2021 — https://signalsandthreads.com/more-signals-&-threads-coming-soon/ — season 2 announcement.
- **Writing, Technically** — James Somers — Ep 10, Sept 1, 2021 — https://signalsandthreads.com/writing-technically/ — role of technical writing and knowledge-sharing at Jane Street; how engineering software relates to editing prose.
- **Building a UI Framework** — Ty Overby — Ep 11, Oct 6, 2021 — https://signalsandthreads.com/building-a-ui-framework/ — Bonsai, the functional OCaml UI library for browser UIs; CSS; Excel as "arguably the greatest programming language ever developed" (blurb).
- **What is an Operating System?** — Anil Madhavapeddy — Ep 12, Nov 3, 2021 — https://signalsandthreads.com/what-is-an-operating-system/ — evolving role of OSes, internet security, the arrival of OCaml 5.0.
- **A Poet's Guide to Product Management** — Peter Bogart-Johnson — Ep 17, Aug 14, 2023 — https://signalsandthreads.com/a-poets-guide-to-product-management/ — PM as anthropologist: listen first, preserve what works; paying down tech debt is not opposed to serving customers.
- **From the Lab to the Trading Floor: Designing for Expert Users** — Erin Murphy — Ep 19, Jul 10, 2024 — https://signalsandthreads.com/from-the-lab-to-the-trading-floor/ — ex-NASA JPL UX designer; bringing a CLI to the web without hurting power users; beauty as utility; discovering what expert users actually want.
- **Solving Puzzles in Production** — Liora Friedberg — Ep 20, Oct 7, 2024 — https://signalsandthreads.com/solving-puzzles-in-production/ — production engineering as high-stakes puzzle solving plus building tools that make support less necessary; tabletop simulation training; blameless culture for costly mistakes.
- **Why ML Needs a New Programming Language** — Chris Lattner — Ep 25, Sept 3, 2025 — https://signalsandthreads.com/why-ml-needs-a-new-programming-language/ — Mojo: make programmers reckon with the hardware but make it manageable via type-safe metaprogramming; specialize to computation and platform; avoid single-vendor control.
- **The Network as a Program** — Nate Foster — Ep 27, Jun 1, 2026 — https://signalsandthreads.com/the-network-as-a-program/ — PL theory and formal methods for software-defined networking; hyperscaler influence on hardware; multicast; ML reshaping networks; BGP plus a declarative high-level spec language at Jane Street.
- **Building a Data Warehouse from Scratch** — Jacob Baskin — Ep 28, Jun 24, 2026 — https://signalsandthreads.com/building-a-data-warehouse-from-scratch/ — Superstore, a distributed columnar DB serving analytics while transactional writes stream in at trading speed; first design doc led to an eight-figure hardware buy; bidding schemes for compute time on the Hive research cluster.
- **Wrestling the World into Rows** — Eric Mannes — Ep 29, Sept 2, 2026 — https://signalsandthreads.com/wrestling-the-world-into-rows/ — alternative data (satellite, card panels, weather) into datasets a strategy can rely on; negative-oil-price day breaking systems; the hard question of what a company even is; better ML models raise the value of careful data engineering.
- **Learning Goals and the Goals of Learning: Teaching in the Age of AI** — Aaron Bauer — Ep 30, Sept 23, 2026 — https://signalsandthreads.com/learning-goals-and-the-goals-of-learning-teaching-in-the-age-of-ai/ — teaching engineering in-house; live lectures; editor telemetry to measure how AI changes workflows; intern curriculum rebuilt around testing, design, code review since producing code is now the easy part.

---

## 5. Trading and quant educational material Jane Street publishes

### 5.1 "Probability & Markets" — the trading-interview guide [V]
- **Where:** https://www.janestreet.com/static/pdfs/trading-interview.pdf. The trading interview page links it as covering "Many of the core concepts you may encounter in our interviews".
- **What:** a 12-page PDF titled *Probability & Markets*. The PDF metadata says it was revised in August 2025.
- **Sections:** Randomness, Counting, Probabilities, Independence, Random Variables, Expected Value, Confidence Intervals, Conditional Probability, Making Markets, Adverse Selection, Problem Solving Tools, Interview Thoughts.
- **Actionable ideas.** This is the best single source for a trading-reasoning skill.
  - **Count outcomes carefully.** For example, distinguish a red die from a blue one: a sum of 7 is 6/36, not 1/11. When outcomes aren't equally likely, imagine finer outcomes that are (30/20/50% becomes 10 equally likely tickets).
  - **Calibrate confidence intervals.** People are overconfident, so practise by quizzing yourself on facts you can check. The guide's example: a 95% CI for the number of NYC taxis. "It's important to try to correct for this, but also don't go overboard!"
  - **Learn the market-making vocabulary and how to quote.** Terms: bid, offer, size, "I'm 2 at 4, 10 up", "sold", "take 'em", fills and partial fills, "I'm out". To set a market, weigh three things together:
    - the expected value;
    - the worst-case loss as a share of your capital, since a big loss costs you future opportunities;
    - how often you'll trade versus how much edge you keep.

    The worked example quotes "3 at 4, 10 up" around a d6 with EV 3.5. Practice contracts include a d20, the max of 3d6, a d6 with one reroll ("who gets to decide to re-roll?"), the temperature in an hour, and 1,000,000 × d6.
  - **Adverse selection.** Ask: "Conditional on my order being filled, what do I think the expected value of the security is? Given this updated expected value, would I be happy to have done the trade?" Ask why the counterparty wants the trade: are they price-sensitive and informed, or price-insensitive? Be more careful when the answer is hard to compute, such as weather against a meteorologist, than when it is easy, such as a d6.
  - **Problem-solving tools.**
    - Recursion and memorylessness: E[flips until heads] = 1 + ½·E, so E = 2. In general a success probability of p means 1/p trials on average.
    - Test extreme inputs (0, 1, negative, infinity) to check a formula.
    - Solve small cases (2 players, then add one) and generalize.
  - **Interview posture.** Numeracy means sanity-checking orders of magnitude, not fast multiplication. Simple, intuitive answers beat esoteric theorems. Getting it wrong is not failing; how you take hints and respond to being wrong is what counts. Saying "I'm not sure" is fine, and a better answer later beats a fast first one.
- **Quotes:**
  - "Adverse selection is the idea that the trades you get to do are worse than they would appear, because someone else is selecting into the trade against you."
  - "It's bad to lose a lot of money, because that means in the future when there are great opportunities to trade, you won't have as much capital to do those trades."
- **Companion pages:**
  - https://www.janestreet.com/trading-interviews/ has a mock trading interview video (Graham & Andrea) with timestamps. Hiring signals it states: "curious, organized, and open-minded"; "humble, pleasant to work with, and open to feedback"; no finance knowledge or advanced math required. The final rounds may include problem solving, probability and statistics, coding in any language, data analysis, and general interests.
  - https://www.janestreet.com/join-jane-street/interviewing/ has the FAQ. One line from it: "We believe that asking great questions is more important" (page heading, truncated in the extract).

### 5.2 Figgie (figgie.com) [V rules]
- **Where:** https://figgie.com/how-to-play. Apps are on iOS and Android, and there is a web version.
- **What:** a card game "invented at Jane Street in 2013", "designed to simulate open-outcry commodities trading". "Most of the skill in Figgie is in negotiating trades that benefit both the buyer and seller."
- **Rules:**
  - **Players and deck.** 4 or 5 players start with $350 each. The 40-card deck has two 10-card suits, one 8-card suit and one 12-card suit, with counts randomly assigned to suits and hidden until the end.
  - **The goal suit** is the same color as the 12-card suit, so it has 8 or 10 cards. It is the only suit with value.
  - **Round flow.** Each player antes an even share of a $200 pot. All cards are dealt. Trading is a continuous double auction for 4 minutes with no turns.
  - **Payout.** Each goal-suit card pays $10 from the pot. The holder of the most goal-suit cards takes the rest, $100 or $120 (ties split).
  - **Market mechanics.** Trades are one card at a time, you can "penny" a quote, and **all quotes in all suits are cancelled after every trade**.
- **Official basic strategy:** work out the 12-card suit, collect goal-suit cards, sell the other suits "as long as the prices seem worthwhile", and finish with the most goal-suit cards. It also says to "behave as if you are playing for real money and make decisions that maximize your long-term profits."
- **Skill extraction, our own analysis, not a Jane Street text:**
  - **Prior from your hand.** Your own hand gives a likelihood over the 12 possible deck configurations (which suit is 12, which is 8). Update a posterior over decks from your counts.
  - **Order flow is information.** Who bids or offers which suit, and how hard, is Bayesian evidence. This is §5.1's adverse selection in a live game.
  - **Value a card by its marginal effect.** A goal card is worth $10 plus how much it changes your chance of winning the majority bonus, so it is worth more to whoever is near the majority threshold.
  - **Quote cancellation makes every trade a signal.** Re-quote only after you have updated.
- **Context:** Figgie is part of the AMP curriculum (§5.5). Third-party writing [S]: LessWrong, "Poker is a bad game for teaching epistemics. Figgie is a far better one."

### 5.3 Estimathon [S]
- **What:** a team estimation contest Jane Street runs at universities.
- **Format, from third-party rules and handouts; not verified on a Jane Street page:**
  - About 13 questions in about 30 minutes.
  - Answers are *intervals*, with a cap on total submissions (commonly 18).
  - A correct interval scores ⌈max/min⌉. Missing or wrong intervals double the score exponentially. Lowest score wins.
  - **Correction (2026-11-07):** the official formula on estimathon.com/how-to-play (an image) uses a **floor**: (10 + Σ_good ⌊max/min⌋) · 2^(13 − #good). Jane Street runs it ("Since debuting the Estimathon in 2013, Jane Street has run hundreds of Estimathon contests"), so the rules are [V], not [S]. See skills/calibrated-estimation.
- **Skill value:** calibrated interval estimation, and deciding how to spend a limited number of guesses across questions. This pairs with §5.1's confidence intervals.

### 5.4 Jane Street puzzles archive [V]
- **Where:** https://www.janestreet.com/puzzles/ and /puzzles/archive/ (17 pages).
- **Scope:** about 153 monthly puzzles with solutions, from January 2014 to November 2026. Recent examples: "Pressure Points" (Nov 2026), "It's a Metric, Too" (Oct 2026), "Hint Singles" (Sep 2026).
- **Stated rationale:** "The act of solving puzzles, though that might seem abstract, is intrinsic to the work we do at Jane Street." Also: "we're humble enough to know that if we have a good idea, others may soon have it as well."
- **Related ML, hardware and AI puzzles (blog):**
  - "Can you reverse engineer our neural network?" (Feb 2026)
  - "Can you reverse engineer an ASIC?" (Aug 2026), and its "Results from the ASIC puzzle" (Oct 2026)
  - The protocol emulator ASIC competition (Sep 2026, open until Jan 18)
  - Advent of FPGA (Nov 2025, results Feb 2026)
  - A "hidden backdoors in three language models" puzzle (linked from janestreet.com/machine-learning) [S]
- **Use:** a corpus for a puzzle-solving or reasoning-practice skill. Solutions show how to decompose a problem.

### 5.5 Programs: AMP, INSIGHT, FOCUS, SEE, Graduate Research Fellowship [V from program pages unless marked]
- **AMP (Academy of Math and Programming)** [V]
  - A five-week summer program for recent high-school graduates who "have experienced barriers to accessing advanced STEM educational opportunities". AMP 2027 runs June 28 – July 30, 2027 in NYC.
  - Free, with a $5,000 scholarship on completion and a student-to-teacher ratio under 4:1.
  - Curriculum: "mathematics, computer programming, data analysis, and game theory".
  - Sample day: number theory in the morning; "efficient algorithms, or how to use coding to solve mathematical puzzles"; problem-set study hour; "a guest speaker or learn how to play Figgie".
  - A third-party directory [S] lists topics including probability, market structure and arbitrage, mock trading, game theory and combinatorics. Not confirmed on the Jane Street page.
- **INSIGHT, FOCUS, IN FOCUS, SEE** [S/V names]: multi-day introductory programs with trading and software-engineering tracks. No public curriculum was found.
- **Graduate Research Fellowship** [V]: for PhD students, covering a year of tuition and fees plus a $50,000 stipend.
- **Developer education:** the blog post "Developer education at Jane Street" (2024) and Signals and Threads Ep. 30 (2026, Aaron Bauer) describe the internal OCaml and engineering curriculum, rebuilt around testing, design and code review now that AI agents write much of the code.

### 5.6 Software-engineering interview guides [V]
- **Where:** https://www.janestreet.com/preparing-for-a-software-engineering-interview/ and https://www.janestreet.com/mock-interview/ (SWE mock with Grace & Nolen). Blog posts: "What a Jane Street software engineering interview is like" (2017), "The Jane Street Interview Process — 2020 Edition", "Our software engineering interviews are changing (a little)" (2026-11-02; see §6).
- **Principles stated:**
  - "we try to avoid algorithm bingo and puzzles with clever “aha” solutions". Problems are open-ended with "several plausible angles of attack".
  - "the journey through the interview is a lot more important than the snapshot of the solution at the end of it."
  - Write real code in your best language. There are no bonus points for OCaml.
  - Practise under realistic conditions: use a timer, think aloud, and "write out all parts of the problem (yes, even the parts that seem “easy”)".

### 5.7 Kaggle: Jane Street Market Prediction (2020–21) [V, Kaggle pages rendered]
- **URL:** https://www.kaggle.com/competitions/jane-street-market-prediction
- **Dates:** started Nov 23, 2020. Final submission Feb 22, 2021. Forecasting phase on live market data until Aug 23, 2021.
- **Prize and participation:** $100k ($40k/$20k/$10k, then $5k for places 4–9). 4,245 teams; 29,182 entrants.
- **Announcement:** blog post by Craig Falls, 2020-11-24.
- **Dataset:**
  - Anonymized `feature_{0…129}`, `date`, `ts_id` (time ordering), `weight`, and `resp`.
  - `resp_{1,2,3,4}` give returns over other horizons and appear in train only.
  - Each row is one trading opportunity. You predict `action` ∈ {0,1}.
  - Rows with weight 0 are included but don't score.
  - It is a code competition through the `janestreet` time-series API, which stops models peeking ahead. Notebooks had a 5-hour limit.
- **Metric (utility):**
  - For each date i: p_i = Σ_j weight_ij · resp_ij · action_ij
  - t = (Σ p_i / √(Σ p_i²)) · √(250/|i|), which is an annualized Sharpe-like ratio of daily PnL.
  - u = min(max(t,0), 6) · Σ p_i, so PnL is rewarded only up to a capped Sharpe.
- **Stated difficulties (overview):** "a very low signal-to-noise ratio, potential redundancy, strong feature correlation, and difficulty of coming up with a proper mathematical formulation"; "it can be hard to distinguish good luck from having made a good trading decision."
- **1st place: "Yirun's Solution (1st place): Training Supervised Autoencoder with MLP"** [V]
  - Team: Cats Trading (Yirun Zhang, Mingjie Wang, Colton Smith, yuanzhe zhou, VECTOR), 2021-10-18. https://www.kaggle.com/competitions/jane-street-market-prediction/writeups/cats-trading-yirun-s-solution-1st-place-training-s (formerly discussion/224348).
  - Final submission blended Yirun's AE-MLP with teammates' XGBoost. The single AE-MLP alone also scored 1st on the private LB (6022.202).
  - CV: 5-fold, 31-gap *purged group time-series split*.
  - Dropped the first 85 days because their feature variance differed. Forward-filled missing values.
  - Turned all five resp targets into multi-label actions, using mean |resp| as sample weights.
  - **Trained the supervised autoencoder inside each CV fold, jointly with the MLP.** The public notebook it built on had a label-leakage bug: it trained the AE before the split.
  - Added a Gaussian-noise layer, swish activations, BatchNorm and Dropout.
  - Averaged 3 seeds, kept only models from the last two folds, and early-stopped on the MLP's BCE only. Hyperparameters were tuned with Hyperopt.
- **Follow-on:** Yirun Zhang is named among the organizers of the 2024 competition, and Jane Street's ML page says they "hired the winner of our last Kaggle and he organized this one" [S for the quote].

### 5.8 Kaggle: Jane Street Real-Time Market Data Forecasting (2024–25) [V, Kaggle pages rendered]
- **URL:** https://www.kaggle.com/competitions/jane-street-real-time-market-data-forecasting
- **Dates:** Oct 14, 2024 to Jan 13, 2025 (final submission). Forecasting phase until Jul 14, 2025.
- **Prize and participation:** $120k ($50k/$25k/$10k, then $5k for places 4–10). 3,757 teams; 25,446 entrants.
- **Citation authors:** Maanit Desai, Yirun Zhang, Ryan Holbrook, Kait O'Neil, Maggie Demkin.
- **Dataset:**
  - 79 anonymized features `feature_{00…78}` and 9 responders `responder_{0…8}`, clipped to [−5, 5]. The target is `responder_6`, forecast "for up to six months in the future".
  - Keys: `date_id`, `time_id` (ordinal; real time gaps vary), and `symbol_id` (encrypted; new symbols can appear). Also `weight` and `is_scored`.
  - `lags.parquet` holds the previous date's responders, served at the first `time_id` of each new date. **This makes online learning possible.**
  - Train is ten parquet partitions, 12.3 GB total. The phase-1 test set is about 4.5M rows. Each API batch is one (date_id, time_id).
  - Notebooks had 8 hours for training and 9 hours for forecasting. Kaggle's eval API serves data one timestep at a time.
- **Metric:** sample-weighted zero-mean R² = 1 − Σ wᵢ(yᵢ − ŷᵢ)² / Σ wᵢ yᵢ².
  - "Zero-mean" means the baseline is predicting 0, not the mean.
  - Winning scores were around 0.014, which shows how little signal there is.
- **Overview framing:** "Distributions can be famously fat-tailed, time series can be non-stationary, and data can generally fail to satisfy a lot of the underlying assumptions on which very successful statistical approaches rely."
- **Final private leaderboard top 10** (Kaggle "final standings"):

  | Place | Team | Score |
  |---|---|---|
  | 1 | ms capital | 0.013890 |
  | 2 | Patrick Yam | 0.013273 |
  | 3 | shorturl.at/LKhAD | 0.013163 |
  | 4 | Haoze Hou | 0.011683 |
  | 5 | hyd | 0.011449 |
  | 6 | Thomas Dueholm Hansen | 0.010675 |
  | 7 | leo | 0.010480 |
  | 8 | Evgeniia Grigoreva | 0.010434 |
  | 9 | HAO LI | 0.010417 |
  | 10 | ponythewhite | 0.010293 |

  Only 8th place had a solution writeup linked on the leaderboard. Kaggle's "Winners Walkthroughs" video series features Team Patrick Yam [S, YouTube title only]. **1st-place method: [UNVERIFIED], no writeup found.**
- **8th-place writeup (Evgeniia Grigoreva, 2025-07-14)** [V]: https://www.kaggle.com/competitions/jane-street-real-time-market-data-forecasting/writeups/evgeniia-grigoreva-private-lb-8th-solution (code: github.com/evgeniavolkova/kagglejanestreet)
  - **CV:** two-fold time-series CV with 200-date validation, matching the public set. A second check tested fold-1 models on the last 200 dates *after a 200-day gap*, to simulate the private set.
  - **Data and features:**
    - Used dates ≥ 700, from when the number of `time_id`s per day stabilizes at 968.
    - Standardized features and imputed zeros.
    - Added market averages per (date, time) and per-symbol rolling mean and std over 1000 `time_id`s, which gained about +0.002.
  - **Model:** GRUs whose sequence is one day. MLPs, transformers, cross-symbol attention and embeddings did not help.
  - **Auxiliary targets** (about +0.001):
    - `responder_7` and `responder_8`, plus two derived responders.
    - The derivation rests on a community finding: responder_6 is a 20-day rolling average, responder_7 a 120-day average and responder_8 a 4-day average of the same variable.
    - Training minimized the summed weighted-R² loss across targets.
  - **Ensemble:** 2 architectures × 3 seeds, unweighted mean. LB 0.0112, against 0.0105 for the best single model.
  - **Online learning gave the biggest single gain (+0.008 CV).** Each new day's lagged targets got one gradient step at lr 3e-4, on responder_6 loss only, including rows with `is_scored=False`. With online learning the GRU beat the MLP; without it, the MLP was better.
  - **Engineering:** 0.06 s per inference step and 3.6 s per daily weight update. Inference speed was a first-class constraint.
- **Other writeups:**
  - 162nd place [S]: an online-learning TabM network fine-tuned on a rolling 3–4-day window, blended with a static GBDT ensemble.
  - Community repos: scaomath/kaggle-jane-street (2021).
- **Skill lessons across both competitions:**
  - Purged and gapped time-series CV.
  - Leakage-aware pretraining.
  - Sample-weighted objectives that match the metric.
  - Seed ensembling.
  - Online updates against regime change.
  - Treating latency as a modeling constraint.
  - Distrusting public-LB "shake-up". A 1st-place teammate commented "shake shake！" under the 2021 writeup [V].


---

## 6. Tech blog: design manifestos and recent (2024–2026) posts

There are 256 dated posts on blog.janestreet.com as of 2026-11-07 (full list in Appendix A). The 79 posts below were selected and read in full. Quotes were string-matched against the post text. 6.1 covers the engineering-culture manifestos; 6.2 covers performance, ML research, OxCaml, interviews, hardware, and AI tooling in 2024–2026.

### 6.1 Engineering-culture and design manifestos (39 posts, plus Effective ML)

---

#### Special checks

##### (a) "make illegal states unrepresentable"
- The phrase does **not** appear in any of the 39 blogA posts. A case-insensitive grep for "illegal state" or "unrepresentable" returns nothing.
- **Effective ML** (Apr 22, 2010, Yaron Minsky, https://blog.janestreet.com/effective-ml/): **yes.** It is the third item in the lecture's bullet list, verbatim:
  > Make illegal states unrepresentable

  The whole list, verbatim and in order: "Favor readers over writers", "Create uniform interfaces", "Make illegal states unrepresentable", "Code for exhaustiveness", "Open few modules", "Make common errors obvious", "Avoid boilerplate", "Avoid complex type-hackery", "Don’t be puritanical about purity". The post says the lecture was "in part inspired by" Josh Bloch's *Effective Java*.
- **Effective ML Revisited** (Mar 09, 2011, Yaron Minsky, https://blog.janestreet.com/effective-ml-revisited/): **yes.** It appears verbatim as a section heading ("Make illegal states unrepresentable") above a before/after code example. In the "before" version, a `connection_info` record has a `state` enum and fields like `last_ping_time: Time.t option`, `session_id: string option` and `when_disconnected: Time.t option`. In the "after" version, each state (`Connecting of connecting | Connected of connected | Disconnected of disconnected`) carries a record that holds only the fields valid in that state. The other headings in that post are "Use uniform interfaces", "Code for exhaustiveness", "Open few modules" and "Make common errors obvious" (the last shows the `find`/`find_exn`, `hd`/`hd_exn` pairs).
- The two companion posts, "Effective ML video" (Aug 21, 2010) and "Effective ML Revisited (with videos)" (Mar 27, 2011), have only short text wrappers around the videos. Neither contains the phrase in its text.

##### (b) Posts best read as design manifestos
These posts state general rules meant to apply beyond one tool or incident:
- **13 Virtues** (David Powers): 13 rules for code review and discussion.
- **Clearly Failing** (David Powers): fail Quick, Clear and Clean, plus rules for where retries belong.
- **How to fail — introducing Or_error.t** (David House): one error type for the whole firm; consistency over local optimality.
- **Making something out of nothing (None vs NaN/NULL)** (Yaron Minsky): null handling must be explicit and checked by the type system.
- **Core Principles: uniformity of interface** (Yaron Minsky): Core's design conventions (`t` first, `_exn`, standard includes).
- **10 tips for writing comments (plus one more)** (Craig Falls): the commenting standard for Core.
- **Notes on Naming** (Yaron Minsky) and **What's in a name?** (signed "-Olin"): naming as an engineering discipline.
- **Code review that isn't boring** (Yaron Minsky): Iron's "don't be boring" design principle.
- **Making making better** (Yaron Minsky): invest in tools.
- **The ML sweet spot** (Yaron Minsky): language-design tradeoffs.
- **Effective ML** (not in blogA; fetched for check (a)): the most compact manifesto of all.
- Caveat: **Ironing out your development style** explicitly rejects manifestos ("I prefer stories to manifestos.") but still sets out a codified "Iron style": lots of expect tests, small changes, fast review.

---

#### Per-post extraction

##### 1. Fun with Algebraic Effects - from Toy Examples to Hardcaml Simulations
- Date: Jan 06, 2026 · Author: Fu Yong Quah · https://blog.janestreet.com/fun-with-algebraic-effects-hardcaml/
- Monads "infect" code: callers need `let%bind`, `return ()`, and monad-specific stdlib variants (`Deferred.List.iter`, `Deferred.for_`). Effects let business logic be written in direct style and return ordinary values.
- Split the work in two: the *computation* (business logic, typed `E.Handler.t @ local -> 'a`) and the *operation handlers* that interpret it. Expect most of the complexity in the handlers.
- Declare effect operations as a GADT whose type index is the result type of performing that operation (`Plus_one : int -> int t`).
- Monadic bind needs globally allocated closures, which blocks OxCaml locally allocated values and unboxed layouts. Effects avoid those closures. The post also cites better stack traces and easier composition (composing two monads is painful).
- Use the type and mode system to make misuse impossible: the `@ local` handler means that performing an effect outside its handler is a compile-time mode error.
- In hardware testbenches, model each testbench thread as a continuation suspended at a `step` synchronization point. Advance the simulated circuit only once every thread has reached its sync point. The example's output is checked with expect tests.

> Once you start using a monad, you’re effectively trapped in it.

> most of what can be done with monads can be done with algebraic effects in a much more elegant way.

grounds skill: **effect/concurrency API design** (secondary: hardware simulation testbenches)

##### 2. Getting from tested to battle-tested
- Date: Dec 03, 2025 · Author: Doug Patti · https://blog.janestreet.com/getting-from-tested-to-battle-tested/
- Layer the testing toolbox. The post lists unit tests of side-effect-free modules and state machines, integration tests over a simulated network (delay/drop packets, manipulate time), quickcheck-generated event orderings, version-skew tests (new client against old server and the reverse), AFL fuzzing turned into state updates, nightly lab performance tests, and chaos testing in staging.
- The post calls simulated networking "maybe the most important piece". It needs little mocking, is fast and deterministic, runs on every build without flakiness, and is good for reproduction tests when verifying bug fixes.
- Add deterministic whole-system exploration (Antithesis) to catch "everything you didn't think of". The system runs unchanged with real client code. You supply Docker images, a compose file, and a directory of executable "actions" like the ones users or admins would take.
- Run the exploration nightly against the latest revision. A short gap between a change and a failure points to the culprit. Debug by rewinding and replaying, for example rewinding 1s and running tcpdump at the moment before a crash.
- Reusing existing code in a new context can expose latent bugs that something else was masking (here, a different service-discovery path). That is exactly when people forget to write a new test.
- The post suggests deterministic whole-system testing could serve as a feedback signal for coding agents.

> for all the careful tests that you think to write, there are some things you can only learn by experiencing that chaos.

> Because we were leveraging existing code, we didn’t think to write a new test, especially for this situation.

grounds skill: **deterministic simulation / distributed-systems testing**

##### 3. How we accidentally built a better build system for OCaml
- Date: Jan 24, 2025 · Author: Andrey Mokhov · https://blog.janestreet.com/how-we-accidentally-built-a-better-build-system-for-ocaml-index/
- A build system's first requirement is speed, then flexibility. Developers use it every day.
- Open-sourcing a tool that requires adopting a whole house "way" (Jenga) failed. A small portable compatibility shim (Jbuilder) won users because it was about 5x faster than OCamlbuild, portable and easy to hack on.
- Watch for what users actually value: here it was speed, even though Jbuilder re-ran every command.
- Don't end up maintaining two systems. The internal migration kept slipping to "next year" and only happened once the team had enough staff (five full-time engineers).
- Scaling to a 70M-line monorepo was underestimated work, and so was migrating each editor integration (Vim, Emacs, VSCode). After the switch, builds that were mostly cached got 2-3x faster.
- Upstream internal changes so you don't end up with a private fork.

> Because you interact with it daily, above all it has to be fast – but it also has to be flexible.

> What we realized, eventually, was that the compelling feature was speed.

grounds skill: **build system design** (secondary: tool adoption / migration strategy)

##### 4. What if writing tests was a joyful experience?
- Date: Jan 09, 2023 · Author: James Somers · https://blog.janestreet.com/the-joy-of-expect-tests/
- Start `[%expect {||}]` empty. The tool fills in the real output as a diff, and an editor keybinding accepts it in place, so you never hand-copy expected values.
- One expect test does three jobs: it shows behavior while you hack, it documents intent (a table of inputs and outputs often beats prose), and it freezes output against regressions.
- The art is output that tells a concise story. Use helper functions and custom pretty-printers to leave out irrelevant detail and avoid spurious diffs.
- Keep tests in their own directory, written against the public interface, or against a `For_testing` module exported for that purpose.
- Make printing trivial (ppx_sexp_conv, S-expressions). Dumping the whole state implicitly asserts more than hand-picked assertions do. In the post's example, a mangled order size is caught that targeted asserts would miss.
- Use several expect blocks per scenario, and print diffs of state, for example vdom diffs in Bonsai UI tests. The post says expect tests are complemented by property-based tests, with classic assertions playing a much smaller role.

> In expect tests, regressions are just diffs.

> Thus the art of expect tests is in producing output that tells a concise story, capturing the state you care about.

grounds skill: **expect-test workflow**

##### 5. Using ASCII waveforms to test hardware designs
- Date: Jun 01, 2020 · Author: Andrew Ray · https://blog.janestreet.com/using-ascii-waveforms-to-test-hardware-designs/
- Always develop a hardware design together with a testbench. Write both in OCaml (the Hardcaml EDSL) against a cycle-accurate simulator.
- Render signal waveforms as ASCII text and capture them in expect tests, so hardware regressions show up as text diffs in normal code review and CI.
- The limited display space forces you to choose which signals to show, and the author treats that as a possible advantage.
- Known costs: factoring code so it works in both the interactive waveform viewer and expect tests, and diff tools that don't understand waveforms.
- Bringing hardware into the software workflow (Iron review, CI) gives the hardware team access to years of software tooling.

> continuous integration systems automatically ensure our tests continue to work in the presence of every developer’s bugbear – other developers.

> This means you have to think carefully about what information to expose (some might argue this is an advantage).

grounds skill: **hardware testing**

##### 6. Repeatable exploratory programming
- Date: Apr 22, 2018 · Author: Yaron Minsky · https://blog.janestreet.com/repeatable-exploratory-programming/
- Use expect tests in place of a REPL for exploration. Run with `--auto-promote` so output is written back into the source file.
- Probe edge cases by adding an input (an `<a>` with no `href`). The captured exception shows the bug. Fix it, rerun, and confirm the output.
- Declare real-world data files as explicit test dependencies (`deps`), then explore against them.
- Commit the experiments: others can extend them, and they stay as regression tests for later refactors.
- The framework flags backtraces inside expectations as fragile and strongly discourages them.

> What’s nice about this approach is that we’ve been able to do this all in a way that’s both lightweight and repeatable.

> it might make sense to leave in these little experiments as regression tests

grounds skill: **expect-test workflow** (exploratory programming)

##### 7. Ironing out your development style
- Date: Aug 24, 2017 · Author: Yaron Minsky · https://blog.janestreet.com/ironing-out-your-development-style/
- The "Iron style" has three parts: lots of expect tests; small changes (from ten to a few hundred lines, with large work done as chains of dependent features); and fast turnaround, where review takes precedence over writing new code.
- Not every change needs a new expect test, but nearly every semantic change should show up somewhere, either as a new test or as a diff to an old one.
- For bugs, first land a feature with an expect test that demonstrates the buggy behavior, then fix it in a follow-up feature. If the trace you need doesn't exist yet, create a parent feature that adds it.
- A "seconder" reviews the whole feature, often as a full collaborator, and pushes the author to split it up and add tests. That extra author effort pays off because many people review.
- Tools set the constants of the workflow. Adding a test should take almost no bureaucracy (declaring `let%expect_test` is enough). When one feature becomes seven, the speed of feature operations becomes critical.

> you do expect nearly every semantic change to be reflected in one way or another, either via a new test, or via a diff to an old one.

> Tools change the constants of your development universe

grounds skill: **code review discipline** (small-change workflow)

##### 8. When Bash Scripts Bite
- Date: May 11, 2017 · Author: Todd Lubin · https://blog.janestreet.com/when-bash-scripts-bite/
- `set -euo pipefail` is not a safety guarantee. `-e` acts only on "simple commands", so `echo "$(false)"`, `local foo="$(false)"`, `export foo="$(false)"` and `foo="$(false)$(true)"` all exit with status 0.
- Without `--posix`, `set -e` is not inherited by command-substitution subshells.
- The incident: an LDAP query failed inside `echo "(...)"`, and an empty `()` user list was silently pushed to the mail servers.
- Reason about every failure condition explicitly, and assume your peers don't know these subtleties.
- For production code, prefer a better tool than bash.

> failed in the worst kind of way: silently.

> for production code, there is likely a better tool for the job.

grounds skill: **error-handling design** (production scripting / silent-failure avoidance)

##### 9. This is not the performance you were looking for: the tricks systems play on us
- Date: Apr 20, 2017 · Author: Andy Myers · https://blog.janestreet.com/this-is-not-the-performance-you-were-looking-for-the-tricks-systems-play-on-us/
- First confirm you are running the binary you think you are: compare `md5sum` of the executable and of `/proc/$PID/exe`, and check the dynamic libraries with `ldd`.
- Check CPU affinity (`taskset -p`) and NUMA topology (`numactl -H`). Pin an app to the NUMA node of the peripherals it uses (`/sys/class/net/$ETH/device/numa_node`, `hwloc-ls`).
- Once you pin one app, pin the others on the box too. Jane Street avoids `isolcpus` because it can concentrate load instead of spreading it.
- Check the machine: is it a VM (the `hypervisor` flag in `/proc/cpuinfo`), which kernel is running (`uname -a`), and what differs between hosts (diff `dpkg -l` and `dmidecode` output across two hosts, BIOS version).
- Check `uptime`. "Three hundred days is way too long."

> It’s funny how often seemingly bizarre problems have simple explanations.

> All the time and effort you’ve invested in optimization can be erased by a few bad decisions in scheduler policy, affinity, or background workload on a server.

grounds skill: **performance debugging / deployment hygiene**

##### 10. Observations of a functional programmer
- Date: Oct 27, 2016 · Author: Yaron Minsky · https://blog.janestreet.com/observations-of-a-functional-programmer/
- The post is only an index to a CUFP keynote video. The talk itself was not transcribed or fetched, so the only actionable content is the section blurbs.
- "The right tool for the organization" is offered as an alternative to "the right tool for the job".
- "You broke it, you bought it": if you succeed with a minority technology, contribute to the community you now depend on.
- "The evidence isn't in": it is hard to find convincing experimental evidence about the relative efficacy of languages. "You can't value what you don't understand": language features you haven't used are hard to assess.
- "Use the advantage": on evangelism versus simply using FP.

> an alternative to “the right tool for the job”

> the plight of having been successful using a minority technology, and how to contribute to the community you now depend on.

grounds skill: **technology/language choice** (weak; video-only content)

##### 11. Let syntax, and why you should use it
- Date: Jun 21, 2016 · Author: Yaron Minsky · https://blog.janestreet.com/let-syntax-and-why-you-should-use-it/
- For applicatives, use `let%map x1 = e1 and x2 = e2 in ...` so each variable sits next to its expression. Positional `mapN` makes it easy to mix them up.
- Let syntax keeps diffs targeted: when a call goes from synchronous to deferred, the only change is adding `%bind`.
- Idiom: use let syntax when binding a variable and infix operators when writing point-free code (`>>| ok_exn`).
- Use one monad per scope, chosen by opening its `Let_syntax`. Convert between monads explicitly (`>>| ok_exn`, `Deferred.ok`).
- Stated costs: the syntax is new and somewhat ugly, there is no monadic semicolon (unit binds are awkward), and the Async interleaving point is less visible.

> Mixing multiple monads in the same scope is hard to think about.

> The resulting diff is more targeted, making the substance of the change a bit easier to see

grounds skill: **API/syntax ergonomics** (readable diffs, monadic style)

##### 12. Why OCaml?
- Date: Jan 25, 2016 · Author: Yaron Minsky · https://blog.janestreet.com/why-ocaml/
- The post is a short wrapper around an internship-program talk video. The video was not fetched or transcribed, so the post's text has **no extractable design rules**.
- The only claim in the text: the talk is about how OCaml fits into the space of language designs and why Jane Street thinks it sits in a "sweet spot" for its work. For the stated tradeoffs, see post 37, "The ML sweet spot".

> why we think OCaml is in a real sweet spot in that design space, especially for the kind of work we do at Jane Street.

grounds skill: **technology/language choice** (weak; video-only content)

##### 13. Testing with expectations
- Date: Dec 02, 2015 · Author: Yaron Minsky · https://blog.janestreet.com/testing-with-expectations/
- Test-tool friction decides how many tests people write, so invest in making tests smooth.
- Property-based tests are not always what you want. Sometimes concrete scenarios are better.
- Unified (cram) tests have three virtues, none of them tied to the shell: the scenario, its output and comments live in one readable file; the file is constructed automatically; and failures appear as easy-to-read diffs.
- Embed the test DSL through the language's own annotation syntax so existing tools (merlin, ocp-indent, tuareg) keep working.
- Accept new output by copying the generated `.corrected` file over the original.

> Testing tools matter because the smoother the process is, the more tests people will write.

> sometimes, you don’t want to write down properties – what you want is to write your tests in terms of simple, concrete scenarios.

grounds skill: **expect-test workflow**

##### 14. Quickcheck for Core
- Date: Oct 26, 2015 · Author: Carl Eastlund · https://blog.janestreet.com/quickcheck-for-core/
- The hard part of random testing is not writing the tests but building distributions that produce *useful* values. Invest in tools for tuning distributions, such as no repeated values and uniqueness-preserving generators.
- Fit generators to the implementation's internal boundaries. `List.append` works in chunks of 5 and changes behavior after 1000 chunks, so generate lengths of 4900–5100 with `int_between`, which is documented to stress boundary conditions.
- Generators form a monad: bind gives a weighted composition of distributions. Build custom distributions with `weighted_union`, `of_list`, `singleton` and `recursive`.
- Pass `~sexp_of` so the failing counterexample is printed readably.
- Use observers ("generators of decision trees") to generate random functions for testing higher-order code.
- Don't memoize generators; it causes space leaks across test batches.

> found it easy to write tests that use random data, but hard to write random distributions that actually produce values that are useful to test.

> If we combine generators using monadic bind, we get a weighted composition of their probability distributions.

grounds skill: **property-based testing**

##### 15. Introducing Incremental
- Date: Jul 18, 2015 · Author: Yaron Minsky · https://blog.janestreet.com/introducing-incremental/
- Self-adjusting computation is a spreadsheet whose dependency graph can change at runtime. Uses named in the post: online algorithms, GUIs built as an incremental view function of a model, and configurable computations such as risk, where both data and structure change.
- Make the functor generative so every instance mints fresh types, and values from different "worlds" can't be mixed by accident.
- Mark needed outputs with explicit observers, so the framework knows what is still necessary, and recompute explicitly with `stabilize`.
- Use algebraic structure where you can: with an inverse (`unordered_array_fold ~f_inverse`) a sum updates in constant time instead of log(n). Use `bind` when the dependency structure itself must change.
- Know the cost model. Firing a node takes about 30ns, so incrementalize only when per-node work is large relative to that overhead, or when the graph is large relative to the subgraph being recomputed.

> The Incremental functor is generative, meaning it mints fresh types each time it’s applied, which prevents values from different incremental worlds from being mixed accidentally.

> Incremental tends to be useful when the computation that is put into a single node is large relative to that overhead

grounds skill: **incremental computation design** (secondary: type-driven design)

##### 16. Making making better
- Date: Jan 31, 2015 · Author: Yaron Minsky · https://blog.janestreet.com/making-making-better/
- Tools are easy to undervalue. Spend time sharpening them even in a small shop (fewer than 65 full-time developers at the time).
- Tool quality sets both the learning curve (for example, non-developers in OCaml Bootcamp) and day-to-day efficiency afterwards.
- Examples of the investment: Iron (review and release), Jenga (build), an OCaml upgrade with dev-process improvements, and funding former interns to improve Merlin.
- Thinking about how to make the people around you effective should shape library design, service management and documentation.

> If you spend all your time on first order problems, you’ll discover you’re not solving them as fast as you should be.

> Tools are easy to undervalue.

grounds skill: **developer tooling investment**

##### 17. 13 Virtues
- Date: Jan 02, 2015 · Author: David Powers · https://blog.janestreet.com/13-virtues/
- Temperance and Frugality: review thoroughly but within limits. Don't send code that isn't ready for review, and don't waste attention on frivolous comments.
- Silence and Industry: say only what clearly benefits the code. Prefer answering with working code over more commentary, and aim review at immediately productive outcomes rather than uncertain concerns.
- Order and Cleanliness: create files, modules and types so every concept has a clear place. Be suspicious of catch-all modules. Leave code neater than you found it.
- Resolution: respond to feedback quickly, because momentum matters.
- Justice and Moderation: decide on today's evidence, not on preferences or obsolete constraints. Avoid extremes, and take on strong views slowly.
- Chastity and Humility: spread new ideas through the codebase cautiously, since a good idea may not fit everywhere. Accept that you may be wrong.

> Don’t waste people’s time with frivolous review, careless comments, or code that isn’t ready for review. Attention is expensive.

> Prefer to respond with working code over additional commentary.

grounds skill: **code review discipline** (manifesto)

##### 18. Clearly Failing
- Date: Aug 23, 2014 · Author: David Powers · https://blog.janestreet.com/clearly-failing/
- Don't hide failure behind self-healing retry loops inside an API. Hidden failure is still failure, and it surfaces later and worse.
- **Quick:** don't retry a thousand times, validate config before an hour of work, and always add a timeout when the other side may never respond.
- **Clear:** failure behavior should be obvious from the API itself, with an `Or_error` return rather than errno, NULL or comments about exceptions. Don't return a 20-case variant, because most callers only care whether the call failed.
- **Clean:** release file descriptors, memory and child processes aggressively, but report the failure *before* any cleanup that could hang. The model API has an idempotent `close` that never raises or blocks, and a terminal error state that never recovers.
- If you must retry, put it near the bottom of the stack (as TCP does) or near the top (where the most context is), not in the middle. Also expose the low-level API so clients can opt out. Don't retry forever, and bound the CPU, memory, file descriptors and ports the loop can use.
- Separate retryable failures (a closed connection) from non-retryable ones (a malformed query). Avoid catch-all try/with blocks. Decide who sees a real, non-transient error and what they should do. Retry logic tuned to one application is easier to get right than generic retry logic.

> covering up failure is just another form of failing.

> Taking too long to fail is a cardinal sin.

grounds skill: **error-handling design** (failure semantics / retry policy; manifesto)

##### 19. What's in a name?
- Date: Jul 10, 2014 · Author: no byline shown; the essay is signed "-Olin" in the text · https://blog.janestreet.com/whats-in-a-name/
- A name provides "distal access" (Newell): a small local token that stands for a large remote thing. Handles and cookies are names.
- If you need to refer to a value twice, name it. If you need to write down DAG-shaped or cyclic structure, you need a language with names.
- Build names from a consistent set of parts (`create_hashtable`, `create_rbtree`, `create_skiplist`, not `hashtable_create`/`make_rbtree`/`NewSkipList`) so users can guess names they have never seen.
- Make a name's length and detail proportional to its scope (Pike's rule, with worked examples: `credit_card_expiration` → `cc_exp` → `i`).
- "True names" (content-verifiable identifiers, as in BitTorrent) let you check what a lookup returns without trusting the store. Getting identifiers exactly right matters a great deal in finance (TWTRQ vs TWTR; CMCSA vs CMCSK).

> Name choices inflict specific thought processes on people who use them; bad name choices inflict perverse or misleading thought processes

> the length and detail of a name should be proportional to its scope

grounds skill: **API naming**

##### 20. Making "never break the build" scale
- Date: Jul 06, 2014 · Author: Yaron Minsky · https://blog.janestreet.com/making-never-break-the-build-scale/
- Not-Rocket-Science rule: run the tests *before* a change is integrated into the main branch, never after.
- A naive sequential build-bot takes m×n minutes for n requests. At Jane Street it backed up to as much as 24 hours.
- Fixes, as given in the post: simple speculation (evaluate requests in parallel); merging speculation (test batches, and fall back to individual requests when a batch fails); faster and reliable incremental builds; and fewer requests. Requiring review before integration cut submissions from hundreds a week to 30–40.
- Those fixes only change constants. To scale with team size, make release hierarchical, like Linux lieutenants or Iron's hierarchical features with a small branching factor.

> the test suites are run on code after it’s integrated with the main branch, not before.

> The above tricks can tweak the constants, but don’t change the asymptotics.

grounds skill: **CI / release engineering**

##### 21. Notes on Naming
- Date: Jun 29, 2014 · Author: Yaron Minsky · https://blog.janestreet.com/notes-on-naming/
- Avoid minting new names where you can. Piggyback on an existing one (catalog → catalog browser, catalog logger, cateye), and expose related tools as subcommands of one CLI so they are easy to find.
- Make names informative. *Descriptive* names (activity-cache, entitlement-monitor) say what a system does. *Mnemonic* names give a distinct identity, which helps tell apart systems with similar purposes (watcher, eye, cateye, oculus rather than alert-monitor{1..4}).
- Rarely used systems need more descriptive names. Judge frequency across everyone who touches the system (devs, admins, support), not just its primary users. Long names have costs too, including platform length limits for usernames and hostnames.
- Practice empathy: avoid cutesy names and use fun ones sparingly.
- Avoid churn: names stick, so put effort into the first choice.

> Every name that has to be remembered is a drain on peoples’ mental space.

> Names, once chosen, are hard to change.

grounds skill: **API naming** (system naming; manifesto)

##### 22. Iron out your release process
- Date: Jun 24, 2014 · Author: Yaron Minsky · https://blog.janestreet.com/ironing-out-your-release-process/
- Keep one big repo, even with modular code. A single hash describes the whole system, no dependency-version solving is needed ("no SAT solver!"), and large cross-cutting changes can be made atomically.
- Keep the tip of the release branch at or near a rollable state. Feature toggles are rejected: untrusted code paths in production are "too terrifying".
- Hierarchical features use two operations. *Release* moves a child into its parent. It is allowed only if the child's base is the parent's tip, review is complete, and no issues are outstanding (issues are tracked as specially formatted comments in the source). *Rebase* pulls the parent's changes into the child.
- Patterns this enables: chains of dependent features (develop the child before the parent is released); local release processes owned by a team (for example `jane/fe`); and continuous release by the build-bot (rebase, build and test, `fe release`, email on failure, retry when anything changes).

> Introducing untrusted code paths into a production system in the hopes that they won’t be used is too terrifying to contemplate.

> it lets you use a single hash to fully describe the code in your system.

grounds skill: **release engineering**

##### 23. Scrutinize your code in style
- Date: Jun 13, 2014 · Author: Yaron Minsky · https://blog.janestreet.com/scrutinizing-your-code-in-style/
- Critical-path rules: every feature has a seconder who acts as co-designer; every file has three assigned reviewers, who don't start until the seconder is done; reviewers read minutely for style, clarity, correctness, tests and documentation.
- Reviewing only critical code was a mistake, because unreviewed areas became swamps. Apply different review standards to different codebases instead of choosing between all and nothing.
- Codify each standard as a "scrutiny" in obligations files: a name, a description of the review's goals, a number of required reviewers, and an integer level.
- If a file's scrutiny goes up, require re-review from scratch. Watch merges: a change reviewed at low scrutiny, merged into a file whose scrutiny was raised elsewhere, must be re-read at the higher level. Iron settles these cases with a small logic that has inference rules.

> A seconder shouldn’t approve a feature until he believes in the feature enough to defend it to others.

> All too often, unreviewed parts of the tree turned into swamps that had to be drained later.

grounds skill: **code review discipline** (risk-tiered review)

##### 24. Code review that isn't boring
- Date: Jun 12, 2014 · Author: Yaron Minsky · https://blog.janestreet.com/code-review-that-isnt-boring/
- Iron's design principle is "don't be boring", because humans review boring material badly. Tools should never make reviewers reread unchanged material.
- After a revision, read only the incremental diff (F1→F2), not the whole patch again (B→F2).
- No textual conflict does not mean the change is still correct. Locking the repo during review doesn't scale, so cover the gap with tests and types.
- For conflicted merges, read the diff of diffs, (B→Fb)→(Fc→Fb'). The patdiff4 tool picks the simplest presentation for each hunk.
- "Rebase the review", not just the commits: an approval moves forward through a merge once the reviewer has read the ddiff.

> Humans are bad at carefully thinking about boring things, and rereading a patch that hasn’t changed much since you saw it last is incredibly boring.

> The fact that there are no textual conflicts is no guarantee.

grounds skill: **code review discipline** (review tooling)

##### 25. Why change is hard
- Date: May 14, 2014 · Author: no byline shown · https://blog.janestreet.com/why-change-is-hard/
- Some systems can never stop, or can stop only briefly. Change them through a sequence of small, well-understood steps, not in one go.
- The "engine on the roof" migration: install the new component alongside the old one, connect a switch-over between them, remove the old one, move the new one into place, then spend months cleaning up.
- Expect some steps not to advance the goal directly. They exist to make the change safe.
- The post was written to explain to non-technical colleagues why changes to vital systems take long.

> you probably can’t (or at least shouldn’t) just make that change in one go.

> You have to break it down into very small, well understood steps, not all of which may directly contribute to what you actually want to achieve.

grounds skill: **live-system migration / change management**

##### 26. How to fail -- introducing Or_error.t
- Date: Apr 23, 2014 · Author: David House · https://blog.janestreet.com/how-to-fail-introducing-or-error-dot-t/
- `option` makes failure explicit and checked by the compiler, but it carries no information (for example, which keys were duplicated).
- The alternatives the post rejects: per-function failure variants (they don't compose and give "ever-indenting" matches); `('a, exn) Result.t` (it invites matching on exceptions, which freezes the API); and `('a, string) Result.t` (strings cost too much to build when nobody reads them).
- Pick one error type and push hard for it everywhere: `Or_error.t`, with `Error.t` as a cheap lazy string. Consistency, composability and readable errors beat local optimality.
- Tag errors as they cross layers (`Error.tag`, `tag_arg`) instead of building new ones. Treat `| Error _ ->` as a red flag, and comment wherever an error is discarded.
- Use `combine_errors_unit` for independent checks. Destructure records completely in validators so the compiler, with warnings turned into errors, makes you account for every field.
- Enumerate error cases only when the caller really must handle each one, which is a minority of cases. `option` is fine when there is only one obvious failure (`List.hd`). In hot loops, watch out for allocation from `ok_exn` and consider statically allocated errors.

> every time you say “| Error _” is probably a mistake

> But, consistency is extremely important.

grounds skill: **error-handling design** (manifesto)

##### 27. 10 tips for writing comments (plus one more)
- Date: Dec 20, 2013 · Author: Craig Falls · https://blog.janestreet.com/10-tips-for-writing-comments-plus-one-more/
- Readers want more high-level comments and fewer low-level ones; a one-sentence summary at the top of a module that makes everything click is especially valuable. Skip redundant comments ("[remove t elt] removes [elt] from [t]").
- Comments for users go in the `.mli`, and comments for people changing the module go in the `.ml`. When you change a module, update its comments or delete them. An incorrect comment is worse than none.
- Give external context (domain knowledge, such as tick sizes) rather than internals the code already shows. After writing a comment, see whether better naming makes it unnecessary (`val y : t` instead of `(* x is a y *) val x : t`).
- Say what's bad: caveats, failure modes, unhandled cases. Use comments like `(* performance hack *)` to stop "obvious improvements" that would actually make things worse.
- Give the intuition, not the proof; examples (`1, 1, 2, 3, 5, 8, 13, ...`) and links help. Don't apply rigid rules such as "every function needs a comment".

> An incorrect comment is worse than no comment.

> a comment that required thought to create saves the reader more thought than a comment that was easy to generate.

grounds skill: **code documentation / comments** (manifesto)

##### 28. Patch review vs diff review, revisited
- Date: May 03, 2013 · Author: Yaron Minsky · https://blog.janestreet.com/patch-review-vs-diff-review-revisited/
- Batch review didn't scale. Reviewers had to read unrelated changes together, and the slowest change blocked the whole release.
- Feature-based review: a feature is a bookmark plus a description, a base revision, an owner and a full-feature reviewer (the seconder). The seconder reads every change; file reviewers come after.
- A release manager ships only features that are fully reviewed, build and pass tests on their own, are based on the previous release, and merge cleanly.
- Use conservative merges: take the features' base as the 3-way merge base so the diffs that were reviewed are the diffs that get merged. Hg's guessed common ancestor can silently drop changes.
- Results: weekly releases "like clockwork", and it became easier to reject unready features. The baseline rule: nothing gets in unless one other person has read it. Lesson: think through your processes and attack the biggest bottleneck.

> code is more than a way of getting things done, it’s a way of expressing your intent.

> ensuring that no change can get in unless one other person reads it and thinks it’s reasonable is a good baseline rule.

grounds skill: **code review discipline**

##### 29. OCaml, the ultimate refactoring tool
- Date: Nov 02, 2011 · Author: Yaron Minsky · https://blog.janestreet.com/ocaml-the-ultimate-refactoring-tool/
- Replace ad-hoc component "stitching" with a uniform plug-in registration and type-safe communication between components, so adding a component needs no change to the core.
- Move component configs into their own files with explicit versioning, so outside tools can follow the system as it evolves.
- Write code to make the most of the type system. Then even invasive refactors (nearly every file touched) tend to work the first time.
- The value of the types is not automating the refactor but reducing the bugs it introduces. Testing is still required.

> the type system is so effective at catching bugs, particularly bugs in code that has been written carefully to make the most of the type system.

> OCaml doesn’t automate the work of refactoring, but it does greatly reduce the number of bugs that your refactoring introduces.

grounds skill: **type-driven design** (refactoring)

##### 30. Using types to track defaults
- Date: Aug 02, 2011 · Author: Stephen Weeks · https://blog.janestreet.com/using-types-to-track-defaults/
- A default documented only in a comment goes stale, so readers have to check the `.ml` to be sure.
- Encode the default in the type: phantom "singleton" types (`thirteen`, `false_`) and `'singleton is_the_default` make the `.mli` state the default, and the type checker enforces it.
- Callers override with `override` (bound to `!!`), and implementations read the value with `defaults_to`. Because the types erase, the implementation is trivial and has no runtime cost.
- In practice you only need to define a few singleton types for the common defaults.

> the comment may become stale and incorrect

> have the default enforced by the type checker

grounds skill: **type-driven design** (phantom types)

##### 31. Making something out of nothing (or, why None is better than NaN and NULL)
- Date: Jul 15, 2010 · Author: Yaron Minsky · https://blog.janestreet.com/making-something-out-of-nothing-or-why-none-is-better-than-nan-and-null/
- Implicitly propagating null is a mistake. Programmers must handle null cases explicitly, and the language should support that case analysis.
- NaN breaks basic invariants: `x > y` is not equivalent to `not (x <= y)`, there is no total order, and NaN ≠ NaN. As a result, `max` is asymmetric, and `check1`/`check2` disagree on NaN.
- SQL treats a NULL condition in `CASE` as false. Null-salvaging heuristics fail because the right choice depends on things they can't know. Enforce NOT NULL constraints where you can.
- Java's null is explicit at the value level but invisible in the types. Option types make absence visible in the type and force the `None` case to be handled.
- Put a chosen null policy into helpers (`option_get ~if_none`) instead of implicit propagation. Avoid exceptions except in truly exceptional conditions, because the type system doesn't track them.

> the programmer must think explicitly about how to handle null cases

> it frees the programmer from worrying about the cases not flagged by the compiler.

grounds skill: **type-driven design** (null/absence handling; manifesto)

##### 32. Designing a code-review tool, Part 2: Patches or Diffs
- Date: Aug 16, 2009 · Author: Yaron Minsky · https://blog.janestreet.com/designing-a-code-review-tool-part-2-patches-or-diffs/
- Review diffs between two points in history rather than individual patches. Review is complete when a path of diffs connects a fully read revision to the revision being approved.
- Merges complicate patch-based review, and they are not always trivial, so don't skip them.
- Reading every small patch lowers the signal-to-noise ratio: the reviewer reads decisions that were later reversed, such as a patch and its backout. A diff that spans both shows neither.

> merges aren’t always trivial, so you ignore them at your peril.

> Code review is complete when a path of diffs has been completed, starting from a fully read revision, and ending in the revision to be approved.

grounds skill: **code review discipline** (review tooling)

##### 33. Designing a code-review tool, Part 1
- Date: Aug 08, 2009 · Author: Yaron Minsky · https://blog.janestreet.com/designing-a-code-review-tool-part-1/
- The starting point was manual log files and PDF diffs, with a few reviewers reading every line of the risk-critical systems. It stopped scaling as the code and team grew.
- **Lightweight:** prefer frequent small review rounds over "big-bang" reviews. Tools must make catching up cheap enough to do every few days.
- **Granular:** assign review by subsystem across many people, without making the interface complex.
- **Hackable:** store review data so it can be edited when needed, while keeping a clear and complete history.

> more frequent but smaller rounds of code review are perferable

> The tools need to make catching up on code review lightweight enough to be something that people would be willing to do every few days.

grounds skill: **code review discipline** (review tooling requirements)

##### 34. Lightweight versioning for lightweight protocols
- Date: Dec 03, 2008 · Author: Yaron Minsky · https://blog.janestreet.com/lightweight-versioning-for-lightweight-protocols/
- Define protocol messages as types in a shared module, and generate serializers with sexplib or binprot macros.
- When the whole system can't be upgraded at once, have each component speak several protocol versions. Keep the old protocol modules, give each an explicit version number, and write conversion functions.
- At connection time, negotiate the highest version both sides support.
- There are two conversion strategies: chain upgrade/downgrade functions between successive versions, or convert every version to and from one internal model. Both work, both have tradeoffs, and the conversion functions are tedious and error-prone.

> The main approach we’ve taken to this problem is to make components support multiple versions of a given protocol at once.

> picking the largest version that they both support.

grounds skill: **protocol versioning / API evolution**

##### 35. The perils of polymorphic compare
- Date: Aug 18, 2008 · Author: Yaron Minsky · https://blog.janestreet.com/the-perils-of-polymorphic-compare/
- Polymorphic compare (`compare_val`) works on the runtime representation and ignores types, so it crosses abstraction boundaries. Two sets can be `Set.equal` and still structurally unequal.
- It raises at runtime when it reaches functions, C objects or objects, a source of errors that is hard to stamp out.
- It is slow. Removing unnecessary calls to it is one of the first optimizations to make.
- Lesson: equality and ordering should respect the abstraction (type-specific compare) rather than structure.

> The fact that it ignores the type system means it crosses all abstraction boundaries.

> one of the first things on the list is to stamp out unnecessary invocations of compare_val.

grounds skill: **type-driven design** (abstraction-respecting equality)

##### 36. Core Principles: uniformity of interface
- Date: May 11, 2008 · Author: Yaron Minsky · https://blog.janestreet.com/core-principles-uniformity-of-interface/
- Uniform interfaces are easier to learn and remember, make functors possible, and remove repeated trivial decisions.
- Give each type its own module with the main type named `t`, and keep parallel functions identical across modules (`Int`, `Float` and `Bool` all have `to_string`/`of_string`; `Int` matches `Int32`, `Int64` and `Nativeint`).
- Put "`t` comes first": a simple, consistent argument-order rule instead of case-by-case optimization for partial application.
- Default functions return options. The variant that raises gets an `_exn` suffix (`find`/`find_exn`, `peek`/`peek_exn`).
- Compose signatures from standard includes (`Comparable`, `Hashable`, `Floatable`) so conventions are enforced and functors can build on them.

> having standards for how that code is to be written eliminates a lot of pointless decision-making about how things should be done.

> Rather than make idiosyncratic choices on a function-by-function basis, we prefer to have clear and unambiguous rules where possible.

grounds skill: **API design / naming conventions** (manifesto)

##### 37. The ML sweet spot
- Date: Apr 02, 2008 · Author: Yaron Minsky · https://blog.janestreet.com/the-ml-sweet-spot/
- Making the type system more expressive costs type inference and the quality of error messages. OCaml's polymorphic variants and objects already show this, though polymorphic variants are judged worth it.
- Making code more declarative costs predictable performance: Haskell's laziness makes space hard to reason about, and SQL and Prolog make time and space hard to reason about.
- ML's value is a balance: reasonably declarative code with a straight-ahead execution strategy. Judge a language or feature by what it gives up, not only by what it adds.

> make it a little bit better in one aspect, and you give something up in another.

> You can make things a little more declarative, but you often give up quite a bit on the predictability of the performance you get out of your code.

grounds skill: **technology/language choice tradeoffs** (manifesto)

##### 38. Typing RPCs
- Date: Mar 15, 2008 · Author: Yaron Minsky · https://blog.janestreet.com/typing-rpcs/
- The usual design has one sum type for all requests and one for all responses. That turns the types "sideways": nothing ties a request to its response, so a server returning the wrong kind of response is caught only at runtime.
- Specify each RPC as a value `('a,'b) RPC.t = { tag; query : 'a embedding; resp : 'b embedding }`, which corresponds to a function `'a -> 'b`. Derive both the server handler (`Handler.implement rpc f`) and the client (`query rpc`) from that one spec.
- The client module then has exactly the signature of the underlying functions.
- Projections from the wire format are partial. It is often better to encode that partiality in the return type than to use exceptions.
- State the remaining gaps honestly: duplicate tags and missing server implementations are not caught statically.

> you’ve been forced to turn your type definitions sideways

> it’s often better to explicitly encode the partiality in the return type of the projection function.

grounds skill: **type-driven design** (typed protocol/RPC API design)

##### 39. HOWTO: Static access control using phantom types
- Date: Feb 28, 2008 · Author: Yaron Minsky · https://blog.janestreet.com/howto-static-access-control-using-phantom-types/
- Simplest approach: a separate module with a narrower signature and a one-way `import`. It works, but code can't be polymorphic over the read-write and read-only types.
- Better: put a phantom parameter on the type (`readonly`, `readwrite`) and constrain it in the signature. `set` requires `readwrite t`, `get` accepts `'a t`, and `readonly : 'a t -> readonly t`. It costs nothing at runtime.
- Type inference propagates the capabilities automatically: a function that only reads accepts any ref, and one that mutates requires `readwrite`.
- Immutability can't be retrofitted, since another read-write handle may exist. An `immutable` value must be created that way from birth.
- A polymorphic `create` is more flexible but allows odd types (`string IRef.t`) and needs more annotations. Weigh that tradeoff.

> Since the phantom type isn’t really part of the definition of the type, it has no effect on code-generation and so is completely free at runtime.

> Importantly, there’s no way for an IRef.t to become immutable. It must be immutable from birth.

grounds skill: **type-driven design** (capability / access control via phantom types)

---

#### Skill grouping (posts that ground each candidate skill)
- **type-driven design:** 29, 30, 31, 35, 38, 39, 15 (generative functor), 1 (mode-enforced handler safety), plus Effective ML / Revisited (not in batch A).
- **expect-test workflow:** 4, 6, 13, and 5 (hardware), 7 (as review aid).
- **code review discipline:** 7, 17, 23, 24, 28, 32, 33.
- **release engineering / CI:** 20, 22 (also 3 for build systems).
- **error-handling design:** 18, 26, 8, 31.
- **API naming and interface conventions:** 19, 21, 36, 27 (comments).
- **testing beyond examples:** 14 (property-based), 2 (deterministic simulation / Antithesis).
- **hardware testing:** 5, 1.
- **tooling investment / change management:** 16, 3, 25, 9 (performance hygiene).
- **weak / video-only:** 10, 12.

### 6.2 Performance, ML research, OxCaml, interviews, hardware, and AI tooling (40 posts)

Caveat for this set: inline math and figures were lost when the HTML was converted to text, so some formulas are summarized rather than reproduced.

---

#### 1. Our software engineering interviews are changing (a little)
- Date: Nov 02, 2026 · Author: Matthew Saffer · URL: https://blog.janestreet.com/software-engineering-interviews-are-changing-a-little/
- Stated AI usage: LLMs: "Most of our engineers now use them every day not only for writing code, but also for reading, debugging, and reviewing code" (plus non-code tasks).
- Policy change: since summer 2026 they are trialing new onsite rounds for **campus candidates** that involve less code-writing and focus on (a) software design, (b) verifying the quality, structure and intention of code, and (c) using LLMs to produce code.
- Policy that stays: **most rounds remain traditional coding interviews conducted without LLM assistance**; the rest of the process is unchanged and earlier interview posts are "still accurate." Not every onsite includes the new rounds yet; candidates get a heads-up on-site.
- Rationale: as code generation got cheaper, other parts of the job matter more: "taste about what to build, choosing abstractions that last, and making sure what got built is actually correct"
- Candidates do **not** need a worked-out agent methodology or particular setup; they're looking for "great instincts for building software" and "we don’t feel like we need an LLM to evaluate that." Formats are deliberately left vague because they're still evolving. Experienced-candidate interviews stay varied (producing software, system design, discussing prior work).
- Quotes:
  - "Most rounds will continue to be traditional coding interviews, conducted without LLM assistance."
  - "What we care about is that you think clearly about the tools you use: what they’re good at, where they fall short, and when to reach for something else."
- grounds skill: interview prep: SWE (AI-era design/verification rounds); AI-assisted development policy

#### 2. Flex Model: an event-driven feature engineering system
- Date: Oct 13, 2026 · Author: Stanislaw Maczka · URL: https://blog.janestreet.com/flex-model-an-event-driven-feature-engineering-system/
- Replaced a ~2012 monolith (main file 11k→17k LOC; adding a simple ratio feature touched 19 files, declared in ~6 places; every feature computed for every market). Goal: features defined once, composable, researchers never touch the core.
- Big-bang rewrite failed: ~2.5 years to first real use; success came after narrowing scope (late 2021) to one simple strategy in one market, live early 2022, then a year generalizing.
- Why not Incremental: features need event *history*; Incremental's coalescing and cutoffs (assume pure, history-less nodes) drop repeated equal trades. Flex Model trades away graph dynamism for history: each feature = **event handler** (sees every event, updates state) + **eval** (computes value only when needed).
- Rebuilt engine: features declare per-event-kind handlers and the values they read; a startup **planner** emits, per event kind, an ordered list of evals/handlers. Trade logic becomes just another feature; new event kinds (timers, feeds, IPC) can be added in ordinary libraries. Deliberately **no cutoffs**: per-node branches on random-looking market data are unpredictable for the CPU and complicate reasoning.
- Hot path: all allocation at startup; `[@zero_alloc]` compiler-checked; tests fail if hot path allocates. OxCaml unboxed `float#` replaced fragile inlining tricks; tail latency dropped ~25% in a test replay. Next: compile the whole plan to one straight-line function via runtime metaprogramming (possible because the graph is static). Same feature code runs live and historically, easing train/prod matching.
- Quotes:
  - "It gives up the ability to change the graph while it’s running, which Incremental allows, in return for keeping history there."
  - "The code uses [@zero_alloc] annotations checked by the compiler, and tests fail if the hot path allocates."
- grounds skill: market-data feature engineering; OxCaml allocation discipline; low-latency system design

#### 3. Scaling and benchmarking a critical message bus using a new indexing strategy
- Date: Oct 05, 2026 · Author: Nicholas Yang (intern project by Theodor Totev) · URL: https://blog.janestreet.com/scaling-and-benchmarking-a-critical-message-bus/
- Aria (internal bus, multiple TB/day): linear filtering during "tip recovery" was cache-friendly but hit 100% CPU as readers grew. Index per **topic partition** (two-segment prefix), not per topic (~1M topics), then n-way merge with a min-heap.
- Benchmark-first: built a tool to profile recovery scenarios (partition count, interleaving, reader count) before optimizing. Profiling showed the heap was the bottleneck; **an agent was prompted to implement five heap variants and profile them overnight** — `fast_heap_unboxed` gave 2x on indexed recovery.
- Storage: rejected per-index ring buffers (worst case 32-byte messages → 2GB per index); used a shared pool of 1024-entry blocks that grow/shrink and are recycled.
- On-disk "adaptive splitting": collected real session data, evaluated candidate algorithms by wasted bytes (per topic, total, worst topic, worst total/useful ratio); LLM-vibe-coded web UI to visualize splits; final = greedy clustering + binary search (big topics get own store, small ones bundled). Motivated by an initial recovery going from <2.5 s to >13 min from reading 10x unneeded data.
- Verification stack for a correctness-critical system: expect tests, existing property-based test extended to randomize the tree split, multiple Antithesis runs, and "a swarm of agents" reviewing the code "with high scrutiny". Result: ~30% less CPU in staging; multi-second tails absent on indexed servers.
- Quotes:
  - "Before AI, this is probably where we’d pick a single implementation that appeared to be better. But these days, running experiments is cheap"
  - "As with any performance work, we had to benchmark in order to validate that we were actually improving the system."
- grounds skill: performance benchmarking & data-structure selection; AI-assisted experimentation; distributed-systems testing

#### 4. How recurring network maintenance exposed 6 bugs
- Date: Oct 02, 2026 · Author: Adam Yi · URL: https://blog.janestreet.com/how-recurring-network-maintenance-exposed-6-bugs/
- Six chained bugs (glibc res_init failure leaving null nameserver pointers [2015–2.43, fixed upstream in 2.44]; socket leaked when `bind` fails; 14-year-old Async regression where connect timeout doesn't cover DNS; Kafka retry loop times out without cancelling; duplicated concurrent bootstrap lookups; job-runner migration silently cut FD limit 262,144→32,768 (8x)). "Each bug hid behind the previous one"
- Deterministic failure-path testing without a real partition: `setrlimit` to force `res_init` failure, an `LD_PRELOAD` shim forcing `bind` → EADDRINUSE, and `max_num_threads 1` to make a cross-library same-thread race reproducible.
- Quantitative confirmation: 1,435 s outage / ~80 s retry cycle ≈ 18 cycles × ~1,500 consumer groups = 27,000 predicted attempts vs 27,898 and 27,786 logged and 27,927/28,099 FDs; drain after ~10 min matched Kafka's 600 s idle default.
- Resource scoping: ~28k ephemeral ports shared by ~79 processes ≈ 358 per process — each process looked fine, the host-wide pool was exhausted. Per-second `sar` history let them reconstruct events weeks later. Search coredump history for a crash signature (found the glibc crash across trading apps, research jobs, even Chrome).
- Fixes at every layer (no single "the" fix); in-flight lookup caching; audit other users of the migrated runner. Lessons stated: timeout ≠ cancellation; make multi-step setup failure-atomic; make the hypothesis predict a number; model resources where shared; old ≠ correct (read the layer below); redundancy buys time to be curious.
- Quotes:
  - "A timeout does not imply cancellation."
  - "Make the hypothesis predict a number."
- grounds skill: production incident root-causing / systems debugging; reliability engineering

#### 5. Trading off compute for memory with activation checkpointing
- Date: Sep 30, 2026 · Author (byline): James Somers (intern project by Arsh Koneru) · URL: https://blog.janestreet.com/trading-off-compute-for-memory-with-activation-checkpointing/
- Goal: given a model and an **absolute GB memory budget**, choose activations to drop that minimize extra recompute. Rejected torch's memory-budget API: budget as a % of default saves is hard to reason about; non-monotonic (20%→10% can raise peak); ignores true peak and true recompute time. Rejected per-op SAC: you need the whole graph.
- Key accounting facts: recomputing can itself create a new, higher peak; recompute cost of dropping node c includes all upstream nodes the backward pass otherwise wouldn't need (cost = a + b + c). torch.compile's min-cut sometimes beats saving because fused recompute of memory-bound ops is faster than a memory round trip.
- Planner: one cheap planning pass on a single GPU compiling on fake tensors; capture all graphs, min-cut save sets and execution order; start from min-cut (never saves more); greedily drop the save with the best recompute-cost-per-byte-of-peak-freed until under budget or no gain. Peak estimate tracks liveness across stacked graphs plus params/optimizer state plus a user reserve (fragmentation, NCCL, CUDA). Recompute time ≈ FLOP formulas, adjusted for known-slow ops.
- Applied via a `custom_partitioner` tagging MUST_SAVE/MUST_RECOMPUTE; beat torch knapsack and op-level policies at most budgets on tested single-graph models; peak spread smoothly over time. Known limits: greedy (no backtracking; beam search suggested), no dynamic shapes/data-dependent ops/RNG ops, crude estimates.
- Quotes:
  - "it greedily drops the save with the cheapest recompute cost per byte of peak memory freed."
  - "if we recompute too aggressively or in the wrong places, we can end up with a higher peak."
- grounds skill: ML training systems / GPU memory optimization

#### 6. Mitigating memorization in LLMs
- Date: Sep 30, 2026 · Author (byline): James Somers (intern project by Monte) · URL: https://blog.janestreet.com/mitigating-memorization-in-llms/
- Problem: forecasting benchmarks built from historical questions are contaminated by pretraining; models can "predict" by recall. Use low-stakes public proxies (cricket match previews) to study it.
- Diagnostic protocol: compare pre- vs post-knowledge-cutoff; H1 = additive to baseline post-cutoff; H2 = better pre- than post-cutoff; sharpness = more overconfident pre-cutoff. Watch for confounds (distribution shift in previews across cutoff); bigger models were both better and more memorized.
- What worked: **divergence decoding** (logit-space steering using two small auxiliary models trained to earlier/later cutoffs) lowered pre-cutoff performance without hurting post-cutoff. **podcast-form rewrite** of inputs (removing player quotes) improved post-cutoff more than pre-cutoff; basketball-terms rewrite did not work.
- What didn't: distilling the steered model (attributed to too few task-relevant tokens in the CommonCrawl mix); NLA readouts correlated ~0.93 with predictions but showed no pre/post difference; NLA text hallucinated placeholders (often India).
- Side findings: decoding the fine-tune "diff embedding" recovered a description of the FT objective; NLA probes showed the model decided mid-network and spent last layers on formatting — removing those layers sped training 1.5x.
- Quotes:
  - "A model may perform well on a historical benchmark by consulting its memorized knowledge of past outcomes, but fail miserably when presented with new scenarios in production."
  - "It didn’t result in a de-memorizer, but did help identify the most promising avenues for future research."
- grounds skill: LLM evaluation hygiene / forecasting-benchmark contamination control

#### 7. Can you use autoregressive diffusion to generate market data?
- Date: Sep 30, 2026 · Author (byline): James Somers (intern project by Kavish) · URL: https://blog.janestreet.com/can-you-use-autoregressive-diffusion-to-generate-market-data/
- Framing question: is market data continuous or discrete? Both — continuous-looking prices/timings with spiky point masses (zero gaps, earliest reaction time, whole seconds; prices clustered at mid/bid/ask; "pennying" far more common than 2-tick improvements).
- Setup: four years of US equities; causal transformer encoder → per-position latent; small categorical event-kind head + diffusion head (AdaLN-conditioned) for continuous targets; sample kind then continuous features autoregressively.
- DDPM (1,000-step cosine, DDIM sampling) diverged: 88–95% of values >8 std devs out on all 7 targets; rectified flow / flow matching worked out of the box.
- Handling atoms: (a) split classes — 20-class categorical head (e.g. "size only", "ask up"), zero gaps as their own class, diffusion only for magnitudes (trades were only 8% of events, causing over-prediction of trades); doesn't scale to high-cardinality fields. (b) **"atom smoothing"**: smooth the spike and re-sculpt its mass; choose the representation that exposes spikes.
- Evaluation: per-target marginal TV divergence in a one-step setting (10,240 real context events → one sampled event), plus a discriminator classifier on context+candidate event to test joint/temporal realism; rollouts degrade with horizon (open question how fast). Not yet realistic enough, but clarified the knobs: how much to model categorically vs by diffusion, and how to represent/smooth features.
- Quotes:
  - "fully continuous diffusion did not lend itself to the jaggedness of real market data."
  - "If you want to generate market data you have to model that blend correctly."
- grounds skill: market-data generative modeling

#### 8. A study of sequence weighting at scale
- Date: Sep 14, 2026 · Authors: Alex Renda, Nitya Mani · URL: https://blog.janestreet.com/a-study-of-sequence-weighting-at-scale/
- Data-mix decisions (general vs OCaml-specific, old vs recent market regimes, high-quality upweighting) are usually set at small scale and extrapolated; this fails when behavior is "aberrant" (emergent, not predictable by scaling laws). Data mixing is particularly prone to this (cites a code- vs STEM-mix ordering reversal with size).
- Method to isolate weight from data quality/uniqueness: give every sequence a random weight (log-uniform 0.01–10), train 3 epochs, re-evaluate on the *training* set, fit an "effective sequence weight exponent" p* such that loss reduction ∝ weight^p*. Families: 9 in-house dense, 8 in-house MoE (tens of millions → hundreds of billions params), Qwen 2.5 0.5B–72B. Hyperparameters set by Chinchilla-style power-law fits; heavy regularization so models approximately maximize held-out performance.
- Finding: non-monotonic rise-then-fall of p* — small models learn general patterns regardless of weight, medium models learn in proportion to weight, large models learn everything regardless of weight; more epochs shift the peak to smaller models; little consistency across families.
- Remedies proposed: extrapolate data-mix results only from sufficiently large models; possibly train with damped weights to compensate for p* (explicitly untested). General fix for aberrant laws: switch to continuous metrics (e.g. bits-per-byte instead of sampled multiple-choice accuracy). Keep measuring deviation from predictions.
- Quotes:
  - "Aberrant scaling laws are inconvenient for our model training methodologies, but identifying them lets us avoid bad extrapolations."
  - "our scaling research requires spending as much if not more time and care trying to understand why we’re off our predicted curves as it does fitting the curves themselves."
- grounds skill: LLM pretraining / scaling-law methodology; data-mix design

#### 9. Using OxCaml to implement type-safe reference counting between OCaml and Python
- Date: Jun 15, 2026 · Author: Nicolas Trangez · URL: https://blog.janestreet.com/oxcaml-typesafe-reference-counting-python/
- Context: Python is JS's second major language (data analysis, ML); PyOCaml bridges it. Bug class: wrapping a PyObject as an 8-byte OCaml custom block increfs it and only decrefs in the GC finalizer, so multi-GB data frames or GPU memory are freed only when OCaml's GC (which doesn't see their size) gets around to it.
- Fix with modes: arguments as `Py.Object.t @ local` → glue skips the incref (callee provably can't retain it) and nulls the pointer afterward; results as `@ unique` → glue steals the reference without incref, nulls the pointer, finalizer handles NULL.
- `borrow_` lets you pass a unique value to a local-taking function and keep it unique afterward. Explicit escape hatches: `Py.newref : @local -> @unique`, `Py.decref : @local unique -> unit` (consumes uniqueness so no use-after-decref). `ppx_release` (`let%release`) gives exception-safe prompt release.
- Design stance: unlike Rust, ownership tracking isn't imposed on all API users — default GC-managed style still works; use explicit decref only when profiling shows retention.
- Quotes:
  - "Now such offending programs are impossible to write by construction."
  - "unlike the Rust equivalent, we don’t put the burden of ownership tracking on all users of the APIs."
- grounds skill: OxCaml modes / FFI resource safety; OCaml–Python interop

#### 10. Formal methods and the future of programming
- Date: Jun 07, 2026 · Author: Yaron Minsky · URL: https://blog.janestreet.com/formal-methods-at-jane-street-index/
- Stated position change: for 25 years JS said it wasn't interested in formal methods (except special cases like hardware synthesis) because costs were too high (seL4: 25 person-years for 8,700 lines of C; ~23 lines of proof per line; ~half a person-day per line). **Agentic coding changed this; JS is now building a formal-methods team (London and New York).**
- Cost side: models don't construct arbitrarily hard proofs alone and "still need help and guidance from humans" for complex proofs, but they automate drudgery, supply technical expertise and broaden who can use the tools.
- Benefit side: (1) the **verification bottleneck** — agent code tends toward slop and violates codebase invariants, so humans spend a lot of time verifying it; formal methods could make review more efficient. (2) **Agents thrive on feedback** (both in RL training and in coding); proofs are another strong feedback source.
- Tests (property-based, fuzzing) are valuable but can't cover the state space; in OxCaml they've seen agents benefit a ton from universal guarantees (∀) from types (e.g. no data races, XSS impossible by construction). Escape hatches like `Obj.magic` can be tracked and banned, and formal methods can justify their safe use.
- Why JS: control of the language (put specifications, ownership/mutability constraints, proof techniques into OxCaml) and a user base eager for new type-system features; plan mixes near-term wins and long-term vision; will integrate with Lean, Dafny, Rocq, Agda, Iris.
- Quotes:
  - "Agentic code is getting better, but is still tends towards slop: overly complicated, full of weird bugs and corner cases, often not following essential invariants of the codebase"
  - "Our hope is to make formal methods as pervasively useful of a tool for building software as sophisticated type systems are for us today."
- grounds skill: AI-assisted development policy (verification-first agentic coding); formal methods / type-driven correctness

#### 11. strace-ui, Bonsai_term, and the TUI renaissance
- Date: May 26, 2026 · Author (byline): James Somers · URL: https://blog.janestreet.com/strace-ui-bonsai-term-and-the-tui-renaissance/
- strace-ui (by Ian Henry): interactive filtering (hide a syscall with a key instead of re-running with `-e`), jump/filter by FD with FD-reuse tracking across forks, short PID labels, structs formatted, buffers as hexdumps, man page on keypress, hostnames instead of IPs.
- AI tooling stated: Claude Code's arrival (Feb 2025) "kicked everything into gear" for TUIs. JS built its own Claude Code–like tool, **AIDE**, "to maintain the freedom to choose between different model vendors, to suit our unusual development environment, and to better control the execution sandbox"; it became both demo and co-builder of Bonsai_term.
- With Bonsai_term + agents, a working strace-ui prototype took under ten minutes. Models write Bonsai_term well despite its obscurity and OxCaml-only features; they attribute this to the testing story.
- **Closed loop via screenshot-style expect tests**: integration tests drive the app and print its text-rendered state; regressions show as diffs; trivial for an agent to run and read. Human dev time shifted to what tests can't show (scroll/filter/render performance; FD tracking was hard for the agent).
- Outcome: "a handful of new apps" per day (time-travel debugger for a trading system, CI monitor, agentic-session orchestration, eval management, deploy/roll tools, log explorer). Advice: point your LLM at the examples repo and ask it to write expect tests.
- Quotes:
  - "That closed loop makes it easy for the AI to check its own work and results in features that are more often correct on the first try."
  - "We highly recommend asking your LLM to write expect tests like this one for better results!"
- grounds skill: AI-assisted development (agent feedback loops via snapshot tests); developer-tool/TUI design

#### 12. Using group theory to explore the space of positional encodings for attention
- Date: Apr 22, 2026 · Author: Alok Puranik · URL: https://blog.janestreet.com/using-group-theory-to-explore-positional-encodings-attention/
- Method: state desired properties as axioms and let the math enumerate the design space — linearity in q and k, translation invariance (only relative position observable, aids length generalization), identity at zero shift, continuity ⇒ A(t) = exp(tL), a one-parameter matrix group.
- Diagonalizable generators: real eigenvalue >0 (blowup, rejected), =0 (NoPE), <0 (exponential decay as in linear-attention variants; only sensible with causal masking); complex pairs ⇒ RoPE rotations with optional exponential damping (as in RetNet, Mamba-3). Gated models should be read as learning how far to advance time, not changing decay rate.
- Defective (Jordan-block) generators give polynomial-in-time terms — apparently unexplored; a reader showed ALiBi is reachable this way by augmenting q/k (and the GRAPE paper covers related ground).
- Practical takeaway: all sensible linear relative encodings are likely already in use — don't burn time searching for a "perfect" one. "Time" can be index, wall-clock time for irregular series, or learned time.
- Quotes:
  - "it means that we don’t need to rack our brains to come up with some perfect positional encoding, as we are probably already using it."
- grounds skill: ML architecture research (first-principles design-space enumeration)

#### 13. Can you reverse engineer our neural network?
- Date: Feb 24, 2026 · Author: Ricson Cheng · URL: https://blog.janestreet.com/can-you-reverse-engineer-our-neural-network/
- Puzzle design: full weights given; network outputs 0 almost everywhere and is built so you can't backprop/brute-force to an answer — forces mechanistic interpretability. Inside: hand-built md5 (incl. a ~20-layer parallel carry adder) with a ReLU equality check against a hash in the penultimate-layer bias.
- Solver's path: inspect last layers first (integer weights ⇒ hand-designed); decode the ReLU(v−x−1) − 2ReLU(v−x) + ReLU(v−x+1) equality trick; ILP encoding stalled; graph reductions (merge identity/in-degree-1 nodes, drop ReLUs with all-positive inputs, merge duplicate neurons) cut ~2M nodes to 75k; bound propagation + SAT got 200k→20k vars, still irreducible.
- Breakthrough by reasoning about the puzzle-maker: a human-built unsolvable-by-search core suggests an irreversible function; layer-width periodicity (32 periods of 48) + asking ChatGPT ⇒ hash; checked candidates by comparing intermediate activations ⇒ md5. Gemini wrote a reference md5 to align neurons with algorithm variables.
- Final step was brute force: hints said two lowercase English words; a 10,000-word list was too small, a bigger list worked. A >32-length input bug found by the solver was unintentional.
- Quotes:
  - "You had to actually think about what the net was doing."
  - "In fact if you can solve this puzzle, there’s a decent chance you’d fit in well here at Jane Street."
- grounds skill: mechanistic interpretability / adversarial puzzle solving; ML research hiring puzzles

#### 14. Results from the Advent of FPGA Challenge
- Date: Feb 11, 2026 · Authors: Anish Singhani, Benjamin Devlin · URL: https://blog.janestreet.com/advent-of-fpga-challenge-2025-results/
- Stats: 213 submissions, 46 countries (US 28%, India 23%, UK 11%); 59% students, 32% industry; 151 attempted at least one problem in Hardcaml; many HDLs (Verilog/SV/VHDL, Chisel, Spade, Bluespec, Veryl, Clash, SpinalHDL, PipelineC).
- Mapping heuristics observed: greedy algorithms → state machines (days 1, 3); shift-register tricks for throughput (days 4, 7); classical graph algorithms (days 8, 11) need clever translation.
- Judging criteria stated: detailed write-ups others can learn from, and pushing further — results on real hardware, unusual backends (ASIC flows, TinyTapeout silicon, discrete 74-series TTL PCB, formal bounded model checking to find shortest sequences, parsing in hardware).
- Praised engineering practices: honest documentation of debugging (sim/synthesis mismatches, a vendor tool bug ticket); benchmarking hardware vs software on a custom CPU; careful numerical design (GCD normalization to keep integers at 16 bits); complexity-reducing algorithmic insights before hardware (O(1) formula, avoiding O(N²) edge storage, O(N³)→O(N²k) pipelining, CSR + DSU).
- Quotes:
  - "we looked for submissions with detailed write-ups that others can reference and learn from"
  - "His submission demonstrates the real-world engineering challenges of getting hardware designs working correctly, not just in simulation."
- grounds skill: FPGA design (algorithm-to-hardware mapping)

#### 15. I design with Claude more than Figma now
- Date: Feb 05, 2026 · Author: Edwin Morris (designer on the options desk) · URL: https://blog.janestreet.com/i-design-with-claude-code-more-than-figma-now-index/
- What he does with AI: replaces spec docs/Figma mockups with working prototypes in the real codebase — write problem + proposal → open editor, build, server and **Claude**, using the writeup as prompt → get basic functionality working → iterate → push to a dev environment and ask users → submit a "feature" (JS's PR) that looks and behaves as intended.
- Example: LLM prompting in a JSQL (internal SQL dialect) input; lived with it for days; Claude gave "free, unlimited iteration" on button, shortcuts, copy, prompt, confirmations. Over ~2 months, Figma use "fallen off a cliff"; half a dozen prototypes touching UI, data model and libraries, some 2000+ line diffs; some new apps skip Figma entirely.
- What made it work: improved models, his own facility, and "carefully choosing the right scope"; earlier he used AI only for small UX papercuts and bigger attempts failed. Prior LLM tries failed when used on things he was already expert at.
- Review policy/workaround: put a reminder in the description that prototypes are proposals and code is disposable; reviewers give design/UX feedback; **reviewers later take over the idea and implement it in a separate feature, owning the production code.** Still being figured out.
- Risks named: reviewers handed a fully baked feature lose design input; designing with Claude may keep him in an iterative mindset "constrained to the outcomes I think Claude can produce" — fine for mature tools, risky for new ones.
- Quotes:
  - "prototypes are living proposal docs, the code is disposable, and a reviewer’s job is to give feedback about the design and user experience."
  - "Every time I tried LLMs it was for something I was already good at, and they did a worse job than I would have."
- grounds skill: AI-assisted development policy (prototype-as-proposal workflow); product/UX design with coding agents

#### 16. A Higgs-bugson in the Linux Kernel
- Date: Jul 02, 2025 · Author: Nikhil Jha · URL: https://blog.janestreet.com/a-higgs-bugson-in-the-linux-kernel/
- Symptom: rare EACCES on large NFSv3+Kerberos copies in Gord (trading-activity data store); disappeared with Kerberos off. Low-load weekend reproduction on a dozen boxes failed; scaled up parallel copies instead.
- Cheap load generation: a FUSE filesystem (Rust `fuser`) that serves deterministic pseudo-random bytes so tiny-disk boxes can copy ~200GB files; built in ~20 minutes with Claude's help — he says he wouldn't have tried it without an AI assistant.
- Pre-arm instrumentation before a rare repro: bpftrace `fexit` probes printing kernel stacks when functions return −13, plus packet capture windowed around the error. Hit: `gss_validate` → GSS_S_BAD_SIG.
- Root cause via a throwaway Wireshark plugin computing reply checksums: on retransmit (same XID) the kernel records a new GSS sequence number, so a late reply to the old one fails verification; 3 in a row → EACCES; and each failure triggers another retransmit (self-fulfilling). The overloaded tiny test NFS server (latencies of hundreds of seconds) is what made it reproducible.
- Deterministic repro: NFQUEUE + Python script as a "human firewall" delaying packets. Fixes upstreamed for Linux 6.16: implement RFC 2203's sequence-number cache (FreeBSD already had it) and don't retransmit on bad checksum (treat as tampering; let normal timeouts handle it).
- Quotes:
  - "I don’t think I would have attempted this trick if I didn’t have an AI assistant to write most of the filesystem for me."
  - "a sequence number mismatch should not cause an immediate retransmission, which makes the problem self-fulfilling."
- grounds skill: kernel/systems debugging (rare-bug reproduction); AI-assisted throwaway tooling

#### 17. Introducing OxCaml
- Date: Jun 14, 2025 · Author: Leo White · URL: https://blog.janestreet.com/introducing-oxcaml/
- OxCaml = JS's production compiler and an experimental lab for performance-oriented OCaml; open source; goal to upstream.
- Design goals: safe, convenient (preserve type inference, avoid annotation floods), predictable (performance details explicit at the type level) control — pay-as-you-go ("only where you need it") — and "in OCaml" (all OCaml programs are valid OxCaml).
- Extension areas: fearless concurrency (static data-race freedom), layouts (memory layout control, SIMD), allocation control (less GC pressure, more cache-efficient and deterministic), quality-of-life (polymorphic parameters, include functor, labeled tuples, immutable arrays); built on Flambda2.
- No stability/backward-compat promises for extensions; tooling (dune/opam, LSP, formatter); JS libraries released in two forms (extensions stripped for upstream OCaml vs full OxCaml); non-erasable extensions mean some libraries are OxCaml-only.
- Quotes:
  - "To provide safe, convenient, predictable control over performance-critical aspects of program behavior"
  - "you shouldn’t need to swallow extra complexity when you’re not using that power."
- grounds skill: OxCaml allocation discipline / language-feature adoption

#### 18. Advent of Hardcaml
- Date: Mar 22, 2025 · Author: Anish Singhani · URL: https://blog.janestreet.com/advent-of-hardcaml-2024/
- Deliberately small target (Lattice ECP5, 84K LUTs, 4 Mbits RAM) forces algorithmic optimization; fully open toolchain (Yosys + NextPNR); whole flow (design, simulation, RTL generation) in OCaml.
- Why Hardcaml: software→hardware wins require unrolling into pipelines, which primitive HDL generation makes unwieldy; OCaml types attach semantics to wires (avoid type-confusion bugs); functors/higher-order functions make components reusable.
- Structure: an extensible OCaml interface (`Ulx3s.Design`) per puzzle + shared board wrapper; parsing/setup shared between simulation tests and the real board.
- Patterns: Day 4 — higher-order `make_sliding_window ~width ~height ~check_fn` over a shift-register of recent rows (nested arrays at build time flattened to fixed-width signals); Day 7 — superpipelined brute force, one attempt per clock, hundreds of millions of combinations in seconds.
- Proposes AoC puzzles as a fair cross-HDL usability benchmark (they mix clever optimization with mundane sequencing, parsing, resource sharing).
- Quotes:
  - "Traditional HDLs offer only very primitive generation features, so this unrolling becomes unwieldy"
  - "in hardware, everything’s just a wire, but we can assign semantic meanings to those wires using OCaml’s type system"
- grounds skill: FPGA design (Hardcaml / typed HDL metaprogramming)

#### 19. Developer education at Jane Street
- Date: Oct 04, 2024 · Author: Aaron Bauer · URL: https://blog.janestreet.com/developer-education-at-jane-street-index/
- Base model is apprenticeship (team matching, chosen projects, 1:1 mentorship, code review, "the row"); classes add spreading tacit knowledge (who the experts are, recent hard lessons).
- OCaml Bootcamp (1–2 weeks): syntax → small apps; secret purpose is teaching the build system, testing framework, docs, editor tooling hands-on. Dev Teach-ins (2–3 full days each, mid first year, managers make space) to widen view beyond one's team.
- Curriculum: Testing (expect tests, Quickcheck property tests, Datafetcher for external-data-dependent tests, `Async.Time_source` for time, Netkit for networked systems); Marketdata (build a library from scratch: order books, reliable multicast feeds, normalization, client gotchas); Advanced FP (GADTs, finger trees, CPS, defunctionalization, AD from scratch); OCaml Performance (TSC, inline benchmarks, perf, memtrace, magic-trace, microbenchmark pitfalls, cache-hierarchy experiments, average vs rare-but-critical paths, FFI); Bonsai web apps (live market-data table, Chrome perf tools); Systems Debugging (shell, strace, coredumpctl, gdb, memory/CPU/network/filesystems, kernel).
- Treat education as first-class work: dedicated classrooms, dedicated dev educators.
- Quotes:
  - "we don’t think of these classes as a diversion from “real work” but as important work in itself."
- grounds skill: engineering onboarding / developer education design

#### 20. Visualizing piecewise linear neural networks
- Date: Jul 22, 2024 · Author: Ricson Cheng · URL: https://blog.janestreet.com/visualizing-piecewise-linear-neural-networks/
- ReLU MLPs compute continuous piecewise-linear functions; each region = an activation pattern; together a polyhedral complex. They cannot represent discontinuous jumps.
- Counting: 8 neurons on a 2-D input give 37 feasible regions (8th central polygonal number), not 2^8; second-layer boundaries are straight within a parent region and kink at its edges, or terminate when patterns are infeasible.
- Algorithm: for each parent region, for each activation subset, compose the linear map and solve the linear constraints; keep feasible regions.
- Observations: untrained nets carve few regions, trained nets many; used LeakyReLU(0.02) because small ReLU nets get stuck in local minima.
- Quotes:
  - "Importantly, neural nets can only learn continuous piecewise-linear functions."
  - "Notice how the untrained weights divide the plane up into just a few polygons, while the trained weights tend to make many polygons."
- grounds skill: ML interpretability / model visualization

#### 21. Oxidizing OCaml: Data Race Freedom
- Date: Sep 01, 2023 · Author: Max Slater · URL: https://blog.janestreet.com/oxidizing-ocaml-parallelism/
- Goal: make data races unrepresentable in OCaml 5 without forcing pervasive ownership tracking (OCaml races don't break type safety but still give wrong answers — example counter printed 118533 instead of 200000).
- `sync` mode: immutable and exclusively-mutable values are sync; other mutable values are not. `parallel` requires a `sync once` closure returning `sync`, so capturing a `ref` is a compile error.
- Capsules + keys: encapsulate unrestricted shared mutability; keys (minted uniquely per capsule, branded by type) gate access so only one domain touches a capsule at a time. Mis-locking is a compile error.
- Zero-cost: keys carry no information so take zero bits at runtime; a mutex is essentially a key option → a bool with atomic test-and-set (or futexes). Separating keys from locks lets you swap lock implementations without rewriting data structures.
- Status then: locality in production >1 year; unique/once modes merged; future: dual axis to sync, modal effects, off-heap data, mode polymorphism.
- Quotes:
  - "Mixing up locking is a compilation error—once it compiles, we can be sure that our code is free of data races."
  - "In this post, we seek to make data races unrepresentable without losing this ability."
- grounds skill: OxCaml concurrency discipline / data-race-free API design

#### 22. Oxidizing OCaml: Rust-Style Ownership
- Date: Jun 21, 2023 · Author: Max Slater · URL: https://blog.janestreet.com/oxidizing-ocaml-ownership/
- `unique` mode (only reference in the program; caller's promise) enables in-place functional update (`{ overwrite box with ... }`) and type-changing strong updates (in-place `map`), avoiding the allocation of immutable updates.
- Resource APIs: `close : file @ unique -> unit` prevents use-after-close; using a unique value at shared is one-way, so pass `&file` (borrow → local shared) to non-consuming functions like `read : file @ local -> string`.
- `exclusive` (only *active* reference): mutate but not destroy; `exclusively mutable` fields writable via exclusive refs, immutable via shared refs. Mapping to Rust: unique ≈ by-value move, exclusive ≈ &mut, shared ≈ &.
- Linearity axis (`once`/`many`): closures capturing unique values may run at most once.
- Modes stay orthogonal to types, avoiding Rust-style lifetime polymorphism that would break inference.
- Quotes:
  - "Using a unique value at the shared mode is a one-way transformation"
- grounds skill: OxCaml ownership / resource-safe API design

#### 23. Oxidizing OCaml: Locality
- Date: May 26, 2023 · Author: Max Slater · URL: https://blog.janestreet.com/oxidizing-ocaml-locality/
- Why avoid heap allocation even in a fast generational GC: minor heap is bigger than cache (allocations evict live data), each minor allocation hastens collection and causes promotions that are costly later; JS writes "zero-allocation" code that must never trigger GC.
- `local` mode = value doesn't escape its region → can be stack-allocated (separate locals stack); inferred automatically; `exclave` returns locals into the caller's region; compiler errors on escape.
- Safer APIs: `with_file ... ~f:(File_descr.t @ local -> 'a)` stops callbacks from stashing the fd (use-after-close). Parameter mode = promise by callee (contravariant) or caller (covariant).
- Modes are deep (whole structure) and sub-moded (global usable as local; stack may point to heap, never heap to stack); mutable fields are implicitly global; explicit `global` record fields.
- Practice: locals used daily by perf-sensitive devs and largely invisible to others — costs limited to users who care.
- Quotes:
  - "Developers who work on performance sensitive systems use locals daily, and those who don’t are largely unfamiliar with the feature"
  - "Modes allow the compiler to emit better, lower-allocation code, empower users to write safer APIs"
- grounds skill: OxCaml allocation discipline (stack allocation, zero-alloc code)

#### 24. Accelerating zk-SNARKs - MSM and NTT algorithms on FPGAs with Hardcaml
- Date: Dec 07, 2022 · Authors: Andrew Ray, Benjamin Devlin, Fu Yong Quah, Rahul Yesantharao · URL: https://blog.janestreet.com/zero-knowledge-fpgas-hardcaml/
- Profile first: proving time is ~70% MSM, ~30% NTT, so both must be accelerated (full-stack: field ops, curve arithmetic, algorithm).
- MSM (BLS12-377, 2^26 fixed points, Pippenger): FPGA does bucket accumulation, host handles rare corner cases and final combination; overlap host finishing round N with FPGA streaming round N+1. Core is a >200-stage pipelined point adder with a controller that stalls/reorders to avoid same-bucket data hazards rather than flushing. Result: 4 rounds of 2^26 in 20.331 s (5.083 s/MSM), 1st place; AWS f1.2xlarge ($1.65/hr), ~52 W.
- NTT (2^24, Solinas prime): 4-step decomposition into 2^12 sub-NTTs that fit on-chip SRAM; 8 cores per cluster to match 512-bit HBM bus; scaling 8→64 cores cut latency 0.2315 s → 0.0450 s with power 16.97 W → 27.70 W; 2nd place.
- Report both masked (host/FPGA overlapped) and unmasked latency to expose host overhead.
- Quotes:
  - "we were able to focus on optimizing the algorithm for implementation on an FPGA while leaving seldom-seen corner cases to the host."
- grounds skill: FPGA design (hardware/software partitioning, deep pipelining)

#### 25. Visualizing information propagation in markets
- Date: Nov 23, 2022 · Author: Ricson Cheng · URL: https://blog.janestreet.com/visualizing-information-propagation-in-markets-index/
- Operational definition of a "move": price change >0.01% within 5 ms; link moves in different futures when one follows right after another; filter uncorrelated moves.
- Choose a period where the causal source is known (Fed announcement → expect flow outward from S&P 500 in Chicago); center the visualization there; slow to 1/30 real time.
- Physical sanity bounds: rings at c and c/2 from Chicago; most moves land between them — information propagates at an appreciable fraction of light speed through fiber.
- Business framing: equity index futures across venues aren't fungible but co-move; JS's role includes keeping them fair and in line.
- Quotes:
  - "information can never travel faster than the speed of light, but often isn’t far behind"
  - "Part of Jane Street’s role in the markets is to keep these prices fair and in line with each other."
- grounds skill: market microstructure / cross-venue lead-lag analysis

#### 26. Computations that differentiate, debug, and document themselves
- Date: Nov 17, 2022 · Author: Aditya Srinivasan · URL: https://blog.janestreet.com/computations-that-differentiate-debug-and-document-themselves/
- Use case: optimizing position costs (margin, financing, market risk, regulatory capital). `Gradient_calculator`: write a computation once and get evaluation, automatic derivatives, an intermediate-value debug tree, and auto-generated LaTeX.
- Build-vs-buy reasoning: JAX not OCaml-interoperable; OWL/ocaml-torch model tensors, but their computations are explicit equations, not tensor black boxes; owning it allowed debug/doc features.
- Chose forward-mode AD (cost ≈ proportional to evaluation) over reverse-mode because their computations have few nested chain-rule applications — reverse mode's complexity wasn't worth it.
- Expect-test-printed debug trees: inspect every intermediate at once, build computations incrementally, catch errors on unexercised branches (e.g. nested max), make logical diffs reviewable; cap depth for big trees.
- Generated docs (LaTeX with custom per-term rendering) instead of hand docs that go stale. Future: incremental evaluation, CSE/constant folding (DAG IR), effect-handler AD.
- Quotes:
  - "manual documentation inevitably grows stale"
  - "by printing out all intermediate values, this becomes much harder to miss."
- grounds skill: trading cost optimization tooling; numerical-code testing (expect tests)

#### 27. Magic-trace: Diagnosing tricky performance issues easily with Intel Processor Trace
- Date: Jan 11, 2022 · Author: Tristan Hume · URL: https://blog.janestreet.com/magic-trace/
- Tool choice: sampling profilers (~250 µs interval) are near-useless for sub-250 µs trading responses and can't distinguish a function called 10x more often from one call taking 10x longer; full instrumentation risks inflating tiny hot functions. Intel PT records all control flow at ~30 ns timing with 2–20% overhead (<10%, usually <5% on their programs) but emits ~1 GB/s and decodes ~60x slower than real time.
- MVP by limiting scope: circular-buffer mode, snapshot on a chosen function call, visualize only calls/returns on a timeline (Perfetto fork for ns zoom). First version wrapped `perf` in under a week.
- Zero-overhead triggering via hardware breakpoints in `perf_event_open` — no target cooperation, works on any function, can sample registers for metadata.
- Wins: found a 100 ns regression from a lost inlining; diagnosed a compiler-upgrade slowdown (inlining); long async cycle debugging by snapshotting after cycles exceed a threshold. With niche hardware, lower your prior that bugs are yours (found a kernel bug; suspected Intel erratum SKL171).
- Hindsight advice: start from `perf` + `perf-dlfilter` rather than `perf_event_open` + libipt.
- Quotes:
  - "Sampling profilers are approximately useless for diagnosing latency issues on that scale"
  - "could I obliterate this problem by being willing to do cursed things?"
- grounds skill: low-latency performance diagnosis

#### 28. Announcing Our Market Prediction Kaggle Competition
- Date: Nov 24, 2020 · Author: Craig Falls · URL: https://blog.janestreet.com/announcing-our-market-prediction-kaggle-competition-index/
- Short announcement (~200 words); contest details live on Kaggle, not in the post.
- Stated facts: based on "a real problem with real financial data"; $100K total prizes; primary goal is recruiting exposure ("Data science is a huge part of what we do"); secondary goal is to see Kagglers' approaches and draw inspiration; hiring in New York, London, Hong Kong.
- Quotes:
  - "Primarily our goal is to expose a new audience to some of the kinds of problems that we face, in hopes that it will encourage them to apply."
- grounds skill: market-prediction ML (context only; little technical content)

#### 29. Memory allocator showdown
- Date: Sep 15, 2020 · Author: Stephen Dolan · URL: https://blog.janestreet.com/memory-allocator-showdown/
- A single (time) number misleads: one benchmark got slower (34.28 s → 36.12 s) on best-fit, yet best-fit dominated once space was considered.
- In a GC'd language compare **space/time curves**, not points: sweep OCaml `space_overhead` 20→320 (¼x–4x default 80); best-fit had a point below-and-left of every next-fit point.
- Measure memory as RSS, not `top_heap_size` (quantized heap growth hides 5–10% changes; overestimates because not all heap is used, allocator-dependent).
- Fit a 3-parameter model H = b/(t − a) + c: a = time with no collection (program + allocator speed), c = live data + fragmentation, b = curve shape (mark/sweep speed). Best-fit improves a (faster allocation) and c (less fragmentation).
- Default settings hide the tradeoff: `space_overhead` ignores fragmentation, so best-fit at default sits further toward space-saving.
- Quotes:
  - "in a GC’d language the performance of a program is not described by a single (space, time) pair, but by a curve"
  - "it’s surprising how much work it took to be able to say that confidently!"
- grounds skill: performance benchmarking methodology (GC/allocator evaluation)

#### 30. The Jane Street Interview Process — 2020 Edition
- Date: Jul 24, 2020 · Author: Sam DeFabbia-Kane · URL: https://blog.janestreet.com/jane-street-interview-process-2020/
- Structure (general SWE intern/new grad/experienced): one technical phone interview + onsite with 2–4 technical rounds; mostly coding/algorithms with 1–2 SWEs; CoderPad (Webex video during COVID). London may add a HackerRank round before the phone screen (capacity), not NY/HK. Experienced candidates may get a non-technical call and past-experience discussions.
- Evaluation stance: interview approximates working together; strong candidates program in a language of their choice, communicate, and "make mistakes and miss things".
- Myth-busting: no math/probability questions for general SWE; no bonus for OCaml (they'll dissuade you unless you've used it professionally); no OCaml/finance knowledge needed; no advanced degree needed.
- Process acknowledged as imperfect, constantly iterated, adapted per candidate.
- Quotes:
  - "We won’t ask you math or probability questions for general software engineering roles. Really. We promise."
  - "But we also expect strong candidates to make mistakes and miss things."
- grounds skill: interview prep: SWE

#### 31. Really low latency multipliers and cryptographic puzzles
- Date: Jun 22, 2020 · Author: Benjamin Devlin · URL: https://blog.janestreet.com/really-low-latency-multipliers-and-cryptographic-puzzles/
- Problem: VDF repeated modular squaring (1024-bit), minimize latency per iteration. Estimation lesson: Rivest's 35-year estimate was off ~10x (puzzle solved in 3.5 years on CPU, ~2 months on FPGA).
- FPGA-specific tricks: redundant bit representation (carry only to the neighbor word, shortening the critical carry chain); squaring reuses symmetric partial products; LUT-based modulo reduction (3 cycles); exploit 6-input LUTs and LUTRAM.
- His Predictive Montgomery design: Montgomery reduction (mod becomes a shift) adapted to RBR with an extra word guaranteeing result < p; arity-3 compressor tree using fast-carry adders (found empirically best); **predictive branching** — compute only needed halves and fall back to full 2048-bit product only when boundary words could overflow (rare), fitting one SLR (2272 of 2280 DSPs).
- **Shorter, slower pipeline for latency**: extra pipeline stages add routing "pit stops"; single stage in the loop; lower clock also cuts power. Results vs Ozturk: 201 vs 464 KLUTs (2.3x), 46 ns vs 25.2 ns per op (0.55x), 4.9 W vs 18.3 W (3.7x), 224 vs 461 nJ/op (2.1x); won its round. Also evaluated Barrett, CRT, Toom-Cook, Booth, Karatsuba.
- Quotes:
  - "since this is for low latency, you actually don’t want to pipeline more than necessary"
  - "building the most efficient solution requires you to think about completely new architectures, resource constraints, and capabilities than what you would ordinarily consider in software."
- grounds skill: FPGA design (ultra-low-latency arithmetic)

#### 32. Deep-Learning the Hardest Go Problem in the World
- Date: Dec 06, 2019 · Author: David Wu · URL: https://blog.janestreet.com/deep-learning-the-hardest-go-problem-in-the-world/
- Context: KataGo's 19-day run on ≤28 V100s reached ELF OpenGo strength (~50x less compute); score as secondary objective keeps bots sensible when far behind.
- Targeted self-play for a specific hard problem (Igo Hatsuyoron 120): ~70% of games from problem positions, ~30% ordinary games to regularize (raised from 50/50 since problem games are shorter); of problem games, ~1/6 from the root, ~5/6 from subvariations of human and bot lines.
- Start-position sampling with probability exponentially decreasing in turn number so each depth is roughly equally likely (uniform over positions would overweight near-terminal states). No human answers given — positions only as starting states.
- Make precision matter: set komi to the bot's current fair value (+N(0,1) noise) so score-exact play decides wins; halve the data lookback window to cut learning-loop latency; overweight high policy-KL positions.
- Result after 1 week: confirms most human tactics, finds refutations, suggests new main-line moves (White +1/+2 vs prior Black +3); flagged as informal/exploratory with explicit open questions on replication and controlled comparisons.
- Quotes:
  - "About 70% of self-play games started from positions in Igo Hatsuyoron 120. 30% were kept as as ordinary games to regularize"
  - "KataGo was not informed of the human-believed best move or evaluation in any position"
- grounds skill: RL/self-play training design (curriculum & start-state distribution)

#### 33. Learning ML Depth-First
- Date: Apr 17, 2019 · Author: James Somers · URL: https://blog.janestreet.com/learning-ml-depth-first/
- Depth First Learning builds curricula (background reading, lectures, practice problems) that culminate in one specific paper (e.g. AlphaGo Zero, DeepStack, InfoGAN, TRPO).
- JS funded four fellows to build new curricula and run 6-week open online classes; 113 applied.
- Culture claim: technical education is core — talks, conferences, internal classes built around specific libraries/projects.
- Quotes:
  - "We’ve found that going “depth-first” is always better in the long run."
- grounds skill: ML learning/onboarding strategy (paper-centered depth-first study)

#### 34. L2 Regularization and Batch Norm
- Date: Jan 29, 2019 · Author: David Wu · URL: https://blog.janestreet.com/l2-regularization-and-batch-norm/
- Claim (for SGD, layers followed by batch norm): BN makes output invariant to weight scale, so L2 no longer regularizes those layers; instead it controls weight norm and hence effective learning rate (gradients scale ~1/α, relative step ~1/α²).
- Without L2, weights random-walk outward and the effective LR silently decays. Applies only to pre-BN layers (not final heads) and may differ for Adam etc.
- Experiment (ResNet-20, CIFAR-10, TF example with L2 0.0002; 50/50/50 epochs at LR 0.1/0.01/0.001): removing conv L2 dropped accuracy ~91% → ~89.5% with faster weight growth and decaying relative step size (both somewhat more underfitting and overfitting).
- Replicated baseline accuracy with **no L2** by scaling conv-layer gradients by current squared-weight sum / initial — confirming the LR interpretation; fixed early inference-accuracy lag by shortening BN moving-average decay 0.997 → 0.98 (no training effect).
- Diagnostic habit: plot sum of squared weights and average step/weight-norm ratio over training, not just accuracy.
- Quotes:
  - "an L2 objective penalty no longer has its original regularizing effect. Instead it becomes essentially equivalent to an adaptive adjustment of the learning rate!"
- grounds skill: ML training hygiene (optimizer/normalization interactions)

#### 35. How to shuffle a big dataset
- Date: Sep 26, 2018 · Author: Chris Hardin · URL: https://blog.janestreet.com/how-to-shuffle-a-big-dataset/
- Context: very low signal-to-noise, ~billion examples whose labels are only slightly more likely correct.
- 2-pass external shuffle: pass 1 appends each record to one of M random "piles"; pass 2 shuffles each pile in RAM and concatenates. Linear time, streaming, variable-length OK; unbiased (equivalent to sorting by uniform keys).
- Size piles for s + 6√s headroom; on an oversized pile just restart — no bias, since pile sizes are independent of the permutation (caveat: byte-size thresholds with variable records introduce bias; recurse instead).
- Practical: parallelize pass 1 per input file; fold pass 1 into preprocessing (near-zero cost); do pass 2 lazily at load time (prefetch next pile); maintain a rolling Y-year window by treating piles as circular buffers; cheap reshuffles by permuting pile order.
- Measured: 220M examples × 9 kB (320 GB compressed HDF5): random access 394,000 µs/example (2.75 years per pass) vs 120 µs sequential (7.3 h) → ~1000x; local uncompressed SSD 720 vs 15 µs. Local reservoir shuffles fail if serial correlation exceeds the reservoir.
- Quotes:
  - "For large datasets, it makes the difference between feasible and infeasible."
  - "To be clear, this is not some minor performance hack."
- grounds skill: ML data pipeline engineering

#### 36. Does batch size matter?
- Date: Oct 31, 2017 · Author: Chris Hardin · URL: https://blog.janestreet.com/does-batch-size-matter/
- Reparametrize SGD with summed gradients: temperature τ = ε/B. Test performance is (to first order) a function of τ; batch size mostly doesn't matter unless too large — fixing ε and varying B just varies τ.
- View SGD as a sampler of a Boltzmann distribution, not an optimizer: scale τ ∝ 1/N (with twice the data, each point should move you half as much); equivalently ε ∝ B/N or B ∝ εN.
- Start hot for mixing (initial temperature shouldn't scale with N), then cool; lower temperatures tolerate larger batches, so use smaller batches early.
- Momentum: express decay and velocity per point; τ = ε/((1−m)B), B ∝ εN/(1−m). For Adam/RMSProp, state std-dev estimates per point. Tune in your own parametrization and translate to the library's.
- Quotes:
  - "I will argue in this post that batch size mostly doesn’t matter (as long as it’s not too large)"
  - "Temperature is how much you change your mind about θ when shown another data point."
- grounds skill: ML training hygiene (hyperparameter parametrization)

#### 37. Real world machine learning (part 1)
- Date: Aug 28, 2017 · Author not shown · URL: https://blog.janestreet.com/real-world-machine-learning-part-1/
- Pipeline: get data (~2.3 TB market data/day, microsecond-accurate; unlogged data is gone forever) → clean (missing, corrupted, misaligned; seen: data when markets closed, wrong stock, frozen/delayed/intermittent feeds) → explore/visualize → apply domain priors → model → validate → deploy.
- Domain priors: financial models have low signal-to-noise and game-theoretic structure; e.g. don't model ETF-vs-basket price difference as Gaussian — it has arbitrage bounds.
- Standard techniques rarely work out of the box; understand why algorithms work to modify them. Validation must show "with high probability" improvement over the incumbent.
- Deployment risks: make model mistakes non-catastrophic; markets adapt to your strategy (decay); avoid feedback loops where your own trades look like market agreement.
- Toolkit history: Gaussian processes, random forests, adaptive regression splines, genetic algorithms, growing deep learning; best solutions combine approaches in ad-hoc ways.
- Quotes:
  - "There is no shortage of ways to fool yourself when building ML systems, especially in a competitive world like trading."
  - "we’ve found that standard techniques almost never work out-of-the-box."
- grounds skill: trading ML research process / model validation

#### 38. What a Jane Street software engineering interview is like
- Date: Feb 28, 2017 · Author: Sebastian Funk · URL: https://blog.janestreet.com/what-a-jane-street-dev-interview-is-like/
- Worked example "Memo" (retired): part 1 memoize an expensive `int -> int` with a hashtable (expected bug-free quickly; know API complexities); part 2 spot the unbounded-memory leak, bound it with O(1) FIFO eviction via a queue (most passing candidates finish); part 3 LRU — O(n) scan → O(log n) heap → O(1) hashtable + doubly linked list (strong candidates finish).
- Real code, not pseudo-code; any language you know best; don't pick OCaml to please them; tell them if you've seen the question.
- Process over result: may prefer careful, clear, communicative but incomplete over fast but sloppy and hard to follow.
- Logistics: response within ~a week (poke after 10 days); onsites similar and all technical; don't share questions; JS doesn't do exploding offers.
- Quotes:
  - "the journey through the interview is a lot more important than the snapshot of the solution at the end of it."
  - "Please don’t use OCaml just because you think it will make us happy."
- grounds skill: interview prep: SWE

#### 39. Building a lower-latency GC
- Date: Apr 10, 2015 · Author: Yaron Minsky · URL: https://blog.janestreet.com/building-a-lower-latency-gc/
- Alternative considered: object pooling/off-heap avoids GC but makes code trickier; goal is low latency while still allocating.
- Diagnosed stock OCaml GC problems: no phase-level profiling; false promotions; GC clocked by allocation, not time; arrays and roots scanned non-incrementally; "too immediate" work accounting; major slice always forces a minor GC.
- Changes (with Damien Doligez): GC probes per phase/sub-phase; minor-heap aging; interruptible array/root scanning; decouple major slices from minor collections; app-driven GC in idle periods (minor only if minor heap above a threshold to avoid false promotion); smoothed accounting across n future slices in a circular buffer (forced slices credit work); size-segregated free lists (in progress).
- Results: tail latency reduced 3x in a real production app with little tuning; aging gave no significant batch-throughput gain (saved promotion, cost minor GC time) despite being standard in HotSpot/.NET/GHC. Published early to solicit feedback.
- Quotes:
  - "the collector is clocked in terms of minor allocations – ignoring, critically, the amount of time that has gone by."
  - "we were able to reduce tail latencies by a factor of 3 in a real production application."
- grounds skill: low-latency performance diagnosis (GC tuning/runtime design)

#### 40. Interviewing At Jane Street
- Date: Oct 24, 2014 · Author: David Powers · URL: https://blog.janestreet.com/interviewing-at-jane-street/
- Core question: "are they someone we want to work with?" Interviews simulate collaboration; avoid algorithm bingo and "aha" puzzles in favor of open-ended problems with multiple angles.
- Behaviors they want: find the right level of abstraction, state key considerations and a plan, name tradeoffs and which side you chose, ask clarifying questions, show tenacity and curiosity; be nice; be clear (no showy jargon); calibrate and state confidence ("I don’t know" over guessing).
- Execution: know your chosen language cold (control flow, definitions, common data types, error handling, organization); write the code you said you'd write; if losing faith in the plan, stop and explain why.
- Fundamentals: abstraction layers; binary search, sorting, hashing, BFS/DFS, hash tables, binary trees, heaps; big-O and cost estimation; recursion and exhaustive case analysis; think about real computers (cache, IO, memory representation) — more for systems roles.
- Not expected: finishing, bug-free code, mental math/puzzles (those are for other roles). Prep: build something whole from scratch, dig into the layers beneath, get feedback from the smartest people you know, rebuild, repeat.
- Quotes:
  - "Be willing to say, “I don’t know” rather than guessing."
  - "executing a decent plan well is better than producing a Frankenstein’s monster of 3 different plans that doesn’t quite come to life."
- grounds skill: interview prep: SWE (collaboration and calibration)
---

## 7. Requested items not found, or found under a different name

| Requested | Status |
|---|---|
| "Making illegal states unrepresentable" (blog post) | **No blog post has this title.** The maxim appears verbatim in *Caml Trading* (JFP 2008), in "Effective ML" (2010), and as a section heading in "Effective ML Revisited" (2011). *OCaml for the Masses* (2011) has the worked example but not the phrase. [V] |
| "What is a Jane Street software engineer" | **Not found** among the 256 blog posts or by web search. The closest material: "What a Jane Street software engineering interview is like" (2017), the SWE interview-prep page, "Our software engineering interviews are changing (a little)" (2026), and S&T Ep. 9 on the internship. [UNVERIFIED that it exists anywhere] |
| "Code review that isn't boring" / Iron | Found: blog 2014-06-12, plus "Scrutinize your code in style", "Iron out your release process", "Making never break the build scale" (2014), "Ironing out your development style" (2017), and the tech talk "How Jane Street Does Code Review" (2017). [V] |
| "Ironing out your release process" | Actual title: **"Iron out your release process"** (2014-06-24). Separate post: "Ironing out your development style" (2017-08-24). [V] |
| "Rust vs OCaml?" | **Not found as a post.** Jane Street's position on Rust is spread across the "Oxidizing OCaml" blog series (Locality, Rust-Style Ownership, Data Race Freedom; 2023), "Introducing OxCaml" (2025), the DRF paper's argument against AXM-everywhere, the Memory Management episode (lifetimes vs `local`), and hosted Rust talks (RustBelt, Rust for Everyone, Gjengset). [V for those items] |
| Testing with expect tests | Found: "Testing with expectations" (2015), "Repeatable exploratory programming" (2018), "What if writing tests was a joyful experience?" (2023). [V] |
| Build system / Jenga / dune | Found: "Making making better" (2015), "How we accidentally built a better build system for OCaml" (2025), S&T Ep. 2 "Build Systems" (Mokhov), and Jenga→Dune history in "Jane and the Compiler". [V] |
| Editor tools | Covered by fragments only: Merlin funding in "Making making better", editor integration in the dune migration, Iron's editor review workflow, the 2026 TUI post "strace-ui, Bonsai_term, and the TUI renaissance", and "Putting the I back in IDE" (2018). No dedicated manifesto was found. |
| AI/LLM tooling 2024–2026 | Found: S&T Ep. 31 "The Changing Craft of Programming" (Crepezzi, 2026), Ep. 30 "Teaching in the Age of AI" (2026), Ep. 16 "The Future of Programming" (2023), blog "I design with Claude more than Figma now" (2026), "Formal methods and the future of programming" (2026), "Our software engineering interviews are changing (a little)" (2026), and "Mitigating memorization in LLMs" (2026). See §6. |
| Kaggle 2024–25 winning writeup | Final leaderboard [V]. **No 1st–7th place writeup was found**; the best available is the 8th-place writeup (§5.8). |
| ETC (Electronic Trading Challenge) | Not found on janestreet.com. [UNVERIFIED] |
| ML Workshop 2025, PLDI/POPL 2026 Jane Street papers | Not confirmed. See §1.12. |

---

## 8. Skill seeds

**Format:** skill name, then a one-line purpose, then **Grounded by** (§ references) and **Core rules to encode**. Engineering skills come first, trading-reasoning skills second. Within each group, skills are roughly in order of how much source material backs them.

### Engineering

1. **`type-driven-design`.** Model the domain so illegal states don't type-check.
   - **Grounded by:** Caml Trading (§1.1); OCaml for the Masses, connection_state example (§1.2); Effective ML / Revisited (§3.1); blog "Making something out of nothing", "Using types to track defaults", "HOWTO: phantom types", "Typing RPCs", "The perils of polymorphic compare", "OCaml, the ultimate refactoring tool" (§6); S&T "Swapping the Engine…" on first-class types vs a bag of fields, and "Building Tools for Traders" on sum-typed UI states (§4).
   - **Core rules to encode:**
     - Use per-state records inside a sum type.
     - No wildcard matches.
     - Use `option` instead of null or NaN.
     - Use phantom types for capabilities and validation state.
     - Write one typed spec per RPC.
     - Equality must respect the abstraction.
2. **`readable-code-for-review`** (the "Effective ML" persona). Write for the reader and the reviewer.
   - **Grounded by:** Effective ML maxims; Caml Trading §2.1; "13 Virtues"; "10 tips for writing comments"; "Notes on Naming"; "What's in a name?"; "Core Principles: uniformity of interface"; "Let syntax"; S&T "The Future of Programming" ("optimize for reading").
   - **Core rules to encode:**
     - Favor readers over writers.
     - Keep interfaces uniform: `t` first, `_exn` suffixes, standard includes.
     - Name length scales with scope.
     - Comments carry external context and caveats; an incorrect comment is worse than none.
     - Avoid boilerplate, because people skim it.
3. **`code-review-discipline`** (Iron). Review state is tracked, review is never boring, scrutiny is tiered.
   - **Grounded by:** tech talk "How Jane Street Does Code Review" (§3.4); blog "Code review that isn't boring", "Scrutinize your code in style", "Designing a code-review tool 1 & 2", "Patch review vs diff review", "Ironing out your development style", "13 Virtues" (§6); Caml Trading on code review as informal proof; S&T Ep. 31 ("AI breaks the social contract of review"; treat agent output as a prototype); "Hacking OCaml" (reviewing LLM code is about finding the gap between real and intended behavior).
   - **Core rules to encode:**
     - Diff what you know against what you should know.
     - Read the diff of diffs after a rebase.
     - CRs live in the code.
     - A seconder plus file reviewers.
     - Per-file scrutiny levels.
     - Small features.
     - A server that refuses unreviewed releases.
4. **`expect-test-workflow`.** Turn tests into diffs and exploration into regression tests.
   - **Grounded by:** "Testing with expectations", "Repeatable exploratory programming", "What if writing tests was a joyful experience?", "Using ASCII waveforms to test hardware designs" (§6); RWO 2e Testing chapter (§2); S&T "Building Tools for Traders" (§4).
   - **Core rules to encode:**
     - Start with an empty `[%expect]` and promote the output.
     - Print concise stories with custom printers.
     - Every semantic change shows up as a test diff.
     - Demonstrate a bug in one feature, then fix it in a child feature.
5. **`testing-beyond-examples`.** Property-based tests, deterministic simulation, and whole-system exploration.
   - **Grounded by:** "Quickcheck for Core"; "Getting from tested to battle-tested" (Antithesis, simulated network); S&T "Why Testing is Hard…" (Will Wilson) and "State Machine Replication" (§4); Nigito exchange talk (replay weeks of production data plus fuzzing).
   - **Core rules to encode:**
     - Determinism comes before exploration.
     - Tune generators to implementation boundaries.
     - Turn pager alerts into properties.
     - Use bugification.
     - Watch for an agent gaming a strict validator.
6. **`error-handling-design`.** Fail quick, clear and clean, using one error type.
   - **Grounded by:** "How to fail — Or_error.t", "Clearly Failing", "When Bash Scripts Bite", "Making something out of nothing" (§6); Caml Trading (avoid untracked exceptions).
   - **Core rules to encode:**
     - Treat `| Error _ ->` as a red flag.
     - Tag errors as they cross layers.
     - Retries belong at the bottom or top of the stack, never the middle, and are bounded.
     - Report failure before any cleanup that could hang.
     - Never let failure be silent.
7. **`low-latency-performance`** (OCaml/Linux/microarchitecture). Measure first, keep the hot path allocation-free, remove jitter.
   - **Grounded by:** tech talks "Safe at Any Speed", "System Jitter…", "Unboxed Types", "Making OCaml Safe…", "Saga of Multicore" (§3); S&T "Performance Engineering on Hard Mode", "Memory Management", "Compiler Optimization", "Multicast and the Markets" (§4); blog "This is not the performance you were looking for", magic-trace, "Memory allocator showdown", "Building a lower-latency GC" (§6); Caml Trading §2.2 (predictability).
   - **Core rules to encode:**
     - Derive the latency budget from replayed peak data.
     - Tails are often medians repeated.
     - Use traces, not profiles.
     - Rule out the environment first: VM, NUMA, IRQs, turbo, wrong binary.
     - Mark functions must-inline on hot paths.
     - Predictable beats fast.
   - **Pair with:** the existing `tene` and `muratori` skills.
8. **`oxcaml-modes-and-layouts`.** Safe stack allocation, uniqueness, race-freedom, and unboxed layouts.
   - **Grounded by:** §1.3–1.6 papers; Casinghino and Dolan talks; "Oxidizing OCaml" blog series, "Introducing OxCaml", "Using OxCaml to implement type-safe reference counting…" (§6); S&T "Memory Management", "Language Design".
   - **Core rules to encode:**
     - Pay-as-you-go complexity.
     - Representation is visible in interfaces.
     - Mode crossing reduces the annotation burden.
     - Ban shared-memory parallelism until the static guarantee exists.
9. **`exchange-and-sequencer-design`.** Total-order sequencer, state-machine replication, fairness by architecture.
   - **Grounded by:** Nigito talk (§3.4); S&T "Multicast and the Markets", "State Machine Replication" (§4); blog "Lightweight versioning for lightweight protocols", "Scaling and benchmarking a critical message bus…" (2026; §6).
   - **Core rules to encode:**
     - A tiny core with logic pushed to the edges.
     - Every acted-on state change appears in the stream.
     - Rebuild by replay.
     - Latency determines throughput.
     - Design incentives against gaming.
     - The log format is versioned forever.
10. **`trading-production-engineering`.** Monitoring and incident response when every message counts.
    - **Grounded by:** Doss talk (§3.5); Caml Trading ("the most prized ability… is the ability of that system not to trade"); S&T "Solving Puzzles in Production", "Thermodynamics of Trading", "Swapping the Engine…" (§4); blog "How recurring network maintenance exposed 6 bugs", "A Higgs-bugson in the Linux Kernel" (§6).
    - **Core rules to encode:**
      - Prefer event-based alerts to SLOs for trading.
      - Alert on symptoms and carry the causes as context.
      - Use epistemic alerts such as fill-too-good.
      - Keep risk checks uncorrelated.
      - Monitoring is more critical than trading.
      - Write MOPs before the activity.
      - Avoid change near scheduled events.
11. **`incremental-computation-design`.** Self-adjusting computation and incremental UIs.
    - **Grounded by:** "Seven Implementations of Incremental", "Intro to Incr_dom" (§3.4); "Introducing Incremental" and the Self-Adjusting DOM posts (§6); S&T "Building a UI Framework"; Leo White's HOPE 2024 "Arrows as applicatives in a monad".
    - **Core rules to encode:**
      - Use map over bind.
      - Use explicit observers, not the GC.
      - Cutoffs.
      - Pseudo-height scheduling.
      - Incrementalize only when node work far exceeds the ~30 ns per-node overhead.
12. **`config-and-change-management`.** Config versus code, and migrating systems that can't stop.
    - **Grounded by:** "Caveat Configurator"; "Why change is hard"; S&T "Swapping the Engine…"; "Iron out your release process"; "Making 'never break the build' scale"; "How we accidentally built a better build system".
    - **Core rules to encode:**
      - Zero config first.
      - Generate finite, versioned config and diff the output.
      - Use the "engine on the roof" migration.
      - No feature toggles carrying untrusted code paths.
      - Test before integrating, not after.
      - Use hierarchical release to beat O(m×n).
13. **`hardware-design-in-ocaml`** (Hardcaml/FPGA).
    - **Grounded by:** Hardcaml paper (§1.9); "OCaml All The Way Down"; S&T "Programmable Hardware"; "Using ASCII waveforms…"; "Fun with Algebraic Effects – Hardcaml Simulations"; ZPrize write-up; the Advent of FPGA and ASIC puzzles.
    - **Core rules to encode:**
      - Timing failure is architecture failure.
      - Name every register.
      - Waveform expect tests.
      - Prove a property by checking that its negation is UNSAT.
      - Test at line rate.
14. **`ml-training-performance`** (GPU).
    - **Grounded by:** "Making GPUs Actually Fast" (§3.5); S&T "The Uncertain Art of Accelerating ML Models"; blog "Trading off compute for memory with activation checkpointing" (2026), "Does batch size matter?", "L2 Regularization and Batch Norm" (§6).
    - **Core rules to encode:**
      - Remove hidden host-device syncs, such as `if loss.isnan()`.
      - Keep the timeline full, then diagnose compute vs memory vs launch overhead.
      - Escalate from PyTorch to Triton to CUDA.
      - Save everything needed to reproduce a run.
15. **`agentic-development-policy`.** How Jane Street runs coding agents.
    - **Grounded by:** S&T Ep. 31 (Crepezzi), Ep. 30 (Bauer), Ep. 26 (Wilson), Ep. 16 (Eisenberg); blog "I design with Claude more than Figma now", "Formal methods and the future of programming", "Our software engineering interviews are changing (a little)", "strace-ui, Bonsai_term, and the TUI renaissance", "Scaling and benchmarking a critical message bus", "A Higgs-bugson in the Linux Kernel" (§6); Cyrus Omar's guest talk.
   - **What Jane Street says it does with AI tools:**
     - Most engineers use LLMs daily to write, read, debug and review code.
     - It built its own vendor-neutral agent, AIDE, so it controls the sandbox.
     - Agents run overnight variant experiments.
     - A "swarm of agents" reviews correctness-critical code alongside expect tests, property tests and Antithesis.
     - Snapshot-style expect tests act as the agent's closed feedback loop.
     - Prototypes are "living proposal docs" whose code is disposable.
     - It is building a new formal-methods team because agentic code "still tends towards slop" and proofs give agents feedback.
     - Most interview rounds stay LLM-free.
    - **Core rules to encode:**
      - Agents get their own identity and permissions.
      - Allow-list sandbox with a classifier for escalation.
      - Expect reward hacking.
      - Graders use split rubrics and deterministic checks where possible.
      - Set the environment up deterministically, because agents are "perpetual beginners".
      - Humans must be able to verify any spec the AI writes.
      - Treat received code as a prototype.
      - Make the agent's feedback loop text-diffable (expect tests).
      - Prefer universal guarantees (types, proofs) over sampled tests for agent output.
16. **`owning-the-toolchain`** (tech strategy).
    - **Grounded by:** "Jane and the Compiler"; "Observations of a functional programmer"; "Making making better"; S&T "Language Design", "Compiler Optimization"; Caml Trading §3–4 on hiring and pitfalls; OCaml for the Masses on limitations.
    - **Core rules to encode:**
      - "You break it, you bought it."
      - Beware Stockholm syndrome about missing tools.
      - Upstream early.
      - A finite complexity budget.
      - The right tool *for the organization*.

### Trading reasoning

17. **`probability-and-expected-value`.**
    - **Grounded by:** Probability & Markets (§5.1); puzzles archive (§5.4); AMP curriculum (§5.5).
    - **Core rules to encode:**
      - Count distinct outcomes.
      - Introduce equally likely sub-outcomes.
      - Use recursion for memoryless processes.
      - Use extreme and small cases.
      - Sanity-check orders of magnitude.
      - Prefer the simple intuitive answer.
18. **`calibrated-estimation`.**
    - **Grounded by:** Probability & Markets, Confidence Intervals section; Estimathon (§5.3, [S]); the trading-interview pages.
    - **Core rules to encode:**
      - Fight overconfidence without overcorrecting.
      - Self-quiz on facts you can check.
      - Choose interval width against how scoring penalizes misses.
19. **`market-making-and-adverse-selection`.**
    - **Grounded by:** Probability & Markets, Making Markets and Adverse Selection sections; Figgie rules and strategy (§5.2); Nigito on incentives; Doss on fill-too-good.
    - **Core rules to encode:**
      - Quote around EV, accounting for edge, fill probability and the size of the worst case.
      - "Conditional on my order being filled…"
      - Ask why the counterparty is trading.
      - Widen when the value is hard to compute.
      - Size so a loss doesn't destroy future opportunity.
20. **`figgie-player`** (live Bayesian trading game).
    - **Grounded by:** figgie.com rules (§5.2); Probability & Markets; AMP.
    - **Core rules to encode:**
      - Posterior over the 12 deck configurations from your own hand.
      - Treat order flow as evidence.
      - Value cards by their marginal effect on the majority bonus.
      - All quotes cancel after each trade, so re-quote after updating.
    - **Note:** the strategy rules here are our own derivation. Only the game rules are Jane Street's text.
21. **`market-data-forecasting`** (noisy, non-stationary ML).
    - **Grounded by:** both Kaggle competitions and their writeups (§5.7–5.8); blog "Real world machine learning (part 1)", "How to shuffle a big dataset", "Does batch size matter?" (§6); S&T "Finding Signal in the Noise" (In Young Cho), "Wrestling the World into Rows"; janestreet.com/machine-learning ("regime-y" data that "our own actions influence"); blog "Flex Model: an event-driven feature engineering system", "A study of sequence weighting at scale", "Can you use autoregressive diffusion to generate market data?", "Visualizing information propagation in markets" (§6).
    - **Core rules to encode:**
      - Purged and gapped time-series CV.
      - Leakage-safe pretraining inside folds.
      - Metric-matched sample weights.
      - Online updates.
      - Auxiliary multi-horizon targets.
      - Seed ensembles.
      - Latency as a constraint.
      - Hand-inspect the first dataset.
      - Trust but verify vendor data.
22. **`trading-interview-coach`.**
    - **Grounded by:** Probability & Markets "Interview Thoughts"; trading-interviews and SWE-prep pages; mock interview videos; interview blog posts (2014, 2017, 2020, 2026).
    - **Core rules to encode:**
      - Think aloud and collaborate.
      - Take hints well.
      - It's fine to be unsure.
      - The journey matters more than the final snapshot.
      - No algorithm bingo or "aha" puzzles for SWE roles.

---

## 9. Sources

### Papers and books
- Minsky & Weeks, "Caml trading – experiences with functional programming on Wall Street", JFP 18(4) 2008: https://doi.org/10.1017/S095679680800676X (PDF: https://www.cambridge.org/core/services/aop-cambridge-core/content/view/02F18023B4C43BF6E53512AA7062A9A5/S095679680800676Xa.pdf/caml-trading-experiences-with-functional-programming-on-wall-street.pdf)
- Minsky, "OCaml for the Masses", ACM Queue 9(9) 2011: https://queue.acm.org/detail.cfm?id=2038036 (doi:10.1145/2030256.2038036). CACM 54(11) version: doi:10.1145/2018396.2018413, listed at https://researchr.org/publication/Minsky11/bibtex
- Lorenzen, White, Dolan, Eisenberg, Lindley, "Oxidizing OCaml with Modal Memory Management", ICFP 2024: https://doi.org/10.1145/3674642 ; https://icfp24.sigplan.org/details/icfp-2024-papers/19/Oxidizing-OCaml-with-Modal-Memory-Management ; https://homepages.inf.ed.ac.uk/slindley/papers/mode-inference.pdf
- Georges et al., "Data Race Freedom à la Mode", POPL 2025: https://doi.org/10.1145/3704859 ; https://iris-project.org/pdfs/2025-popl-drfcaml.pdf ; https://popl25.sigplan.org/details/POPL-2025-popl-research-papers/23/Data-Race-Freedom-la-Mode
- Peters, Jacobs, Kalinichenko, Stevenson, Smith, Dreyer, Eisenberg, "Mode Crossing", ICFP 2026: https://doi.org/10.1145/3828681 ; https://iris-project.org/pdfs/2026-icfp-modecrossing.pdf
- OxCaml documentation and publication list: https://oxcaml.org/documentation/
- Jane Street blog, "ICFP 2024": https://blog.janestreet.com/icfp-2024-index/
- Kalinichenko & Eisenberg, "Taming the Flat Float Array Optimization", OCaml Workshop 2025: https://conf.researchr.org/details/icfp-splash-2025/ocaml-2025-papers/6/Taming-the-Flat-Float-Array-Optimization-Tracking-Separability-in-the-Type-System
- OCaml Workshop 2025 page: https://ocaml.org/conferences/ocaml-workshop-2025 ; Anil Madhavapeddy's notes: https://anil.recoil.org/notes/icfp25-oxcaml , https://anil.recoil.org/notes/icfp25-ocaml5-js-docker
- Sivaramakrishnan et al., "Retrofitting Effect Handlers onto OCaml", PLDI 2021: https://arxiv.org/abs/2104.00250
- Ray, Devlin, Quah, Yesantharao, "Hardcaml: An OCaml Hardware Domain-Specific Language…", arXiv:2312.15035: https://arxiv.org/abs/2312.15035 ; ZPrize: https://github.com/fyquah/hardcaml_zprize
- POPL 2026 Zullo paper (for the negative check): https://popl26.sigplan.org/details/POPL-2026-popl-research-papers/4/Let-Generalization-Polymorphic-Recursion-and-Variable-Minimization-in-Boolean-Kinde
- Real World OCaml 2e (CUP 2022, open access): https://dev.realworldocaml.org/ ; https://doi.org/10.1017/9781009129220 ; https://cambridge.org/core/books/real-world-ocaml-functional-programming-for-the-masses/052E4BCCB09D56A0FE875DD81B1ED571

### Talks and podcast
- Tech talk index: https://www.janestreet.com/tech-talks/ (pages 1–5). Per-talk URLs are in the §3.2 table.
- Signals and Threads: https://signalsandthreads.com/ (RSS https://feeds.simplecast.com/L9810DOa). Per-episode URLs are in §4.
- Workshop and ICFP videos are listed in §1.6–1.7 (YouTube links from oxcaml.org).

### Trading and quant education
- Probability & Markets PDF: https://www.janestreet.com/static/pdfs/trading-interview.pdf
- Interviewing hub: https://www.janestreet.com/join-jane-street/interviewing/ ; https://www.janestreet.com/trading-interviews/ ; https://www.janestreet.com/mock-interview/ ; https://www.janestreet.com/preparing-for-a-software-engineering-interview/
- Figgie: https://figgie.com/how-to-play ; https://apps.apple.com/us/app/figgie-by-jane-street/id6466661064 ; LessWrong essay: https://www.greaterwrong.com/posts/PypgeCxFHLzmBENK4/poker-is-a-bad-game-for-teaching-epistemics-figgie-is-a
- Estimathon (third-party): https://everythingquant.com/guides/jane-street-estimathon/ ; https://math.berkeley.edu/~moorxu/2020ARML/files/EstimathonRules.pdf
- Puzzles: https://www.janestreet.com/puzzles/ ; https://www.janestreet.com/puzzles/archive/
- Programs: https://www.janestreet.com/join-jane-street/programs-and-events/ ; https://www.janestreet.com/join-jane-street/programs-and-events/amp/ ; https://www.janestreet.com/join-jane-street/our-programs/insight/
- Machine learning at Jane Street: https://www.janestreet.com/machine-learning/
- Kaggle 2020–21: https://www.kaggle.com/competitions/jane-street-market-prediction (overview, data) ; 1st place: https://www.kaggle.com/competitions/jane-street-market-prediction/writeups/cats-trading-yirun-s-solution-1st-place-training-s ; KCL news: https://www.kcl.ac.uk/news/kings-student-success-in-market-prediction-ai-competition ; announcement: https://blog.janestreet.com/announcing-our-market-prediction-kaggle-competition-index/
- Kaggle 2024–25: https://www.kaggle.com/competitions/jane-street-real-time-market-data-forecasting (overview, data, leaderboard) ; 8th place: https://www.kaggle.com/competitions/jane-street-real-time-market-data-forecasting/writeups/evgeniia-grigoreva-private-lb-8th-solution ; 162nd place: https://www.kaggle.com/competitions/jane-street-real-time-market-data-forecasting/writeups/max-abhi-private-lb-162nd-solution

### Blog
- Index: https://blog.janestreet.com/ (paginated /page/2 … /page/15; 256 dated posts as of 2026-11-07). The full list is in Appendix A. Per-post URLs are in §6.

---

## Appendix A: every dated Jane Street blog post (256, newest first, as of 2026-11-07)

| Date | Title | URL |
|---|---|---|
| Nov 02, 2026 | Our software engineering interviews are changing (a little) | https://blog.janestreet.com/software-engineering-interviews-are-changing-a-little/ |
| Oct 13, 2026 | Flex Model: an event-driven feature engineering system | https://blog.janestreet.com/flex-model-an-event-driven-feature-engineering-system/ |
| Oct 06, 2026 | Building and testing a config management orchestrator for Windows | https://blog.janestreet.com/config-management-orchestrator-for-windows/ |
| Oct 05, 2026 | Scaling and benchmarking a critical message bus using a new indexing strategy | https://blog.janestreet.com/scaling-and-benchmarking-a-critical-message-bus/ |
| Oct 02, 2026 | How recurring network maintenance exposed 6 bugs | https://blog.janestreet.com/how-recurring-network-maintenance-exposed-6-bugs/ |
| Oct 02, 2026 | Results from the ASIC puzzle | https://blog.janestreet.com/asic-puzzle-results/ |
| Oct 01, 2026 | A resilient kernel log reporter | https://blog.janestreet.com/linux-engineering-kernel-reporter-index/ |
| Oct 01, 2026 | A FUSE server for our in-house storage backend | https://blog.janestreet.com/linux-engineering-depot-fuse-index/ |
| Sep 30, 2026 | What the interns have wrought, special jumbo 2026 edition | https://blog.janestreet.com/wrought-2026/ |
| Sep 30, 2026 | What the SP interns have wrought, 2026 edition | https://blog.janestreet.com/wrought-2026-sp/ |
| Sep 30, 2026 | Trading off compute for memory with activation checkpointing | https://blog.janestreet.com/trading-off-compute-for-memory-with-activation-checkpointing/ |
| Sep 30, 2026 | What the TDOE interns have wrought, 2026 edition | https://blog.janestreet.com/tdoe-intern-projects-2026/ |
| Sep 30, 2026 | Mitigating memorization in LLMs | https://blog.janestreet.com/mitigating-memorization-in-llms/ |
| Sep 30, 2026 | Can you use autoregressive diffusion to generate market data? | https://blog.janestreet.com/can-you-use-autoregressive-diffusion-to-generate-market-data/ |
| Sep 14, 2026 | A study of sequence weighting at scale | https://blog.janestreet.com/a-study-of-sequence-weighting-at-scale/ |
| Sep 10, 2026 | Can you design a chip? Announcing the protocol emulator ASIC competition | https://blog.janestreet.com/protocol-emulator-asic-competition/ |
| Aug 05, 2026 | Can you reverse engineer an ASIC? | https://blog.janestreet.com/can-you-reverse-engineer-an-asic/ |
| Jun 15, 2026 | Using OxCaml to implement type-safe reference counting between OCaml and Python | https://blog.janestreet.com/oxcaml-typesafe-reference-counting-python/ |
| Jun 07, 2026 | Formal methods and the future of programming | https://blog.janestreet.com/formal-methods-at-jane-street-index/ |
| May 26, 2026 | strace-ui, Bonsai_term, and the TUI renaissance | https://blog.janestreet.com/strace-ui-bonsai-term-and-the-tui-renaissance/ |
| Apr 22, 2026 | Using group theory to explore the space of positional encodings for attention | https://blog.janestreet.com/using-group-theory-to-explore-positional-encodings-attention/ |
| Feb 24, 2026 | Can you reverse engineer our neural network? | https://blog.janestreet.com/can-you-reverse-engineer-our-neural-network/ |
| Feb 11, 2026 | Results from the Advent of FPGA Challenge | https://blog.janestreet.com/advent-of-fpga-challenge-2025-results/ |
| Feb 05, 2026 | I design with Claude more than Figma now | https://blog.janestreet.com/i-design-with-claude-code-more-than-figma-now-index/ |
| Jan 06, 2026 | Fun with Algebraic Effects - from Toy Examples to Hardcaml Simulations | https://blog.janestreet.com/fun-with-algebraic-effects-hardcaml/ |
| Dec 03, 2025 | Getting from tested to battle-tested | https://blog.janestreet.com/getting-from-tested-to-battle-tested/ |
| Nov 24, 2025 | Advent of FPGA — A Jane Street Challenge | https://blog.janestreet.com/advent-of-fpga-challenge-2025/ |
| Aug 27, 2025 | What the interns have wrought, 2025 edition | https://blog.janestreet.com/wrought-2025/ |
| Jul 02, 2025 | A Higgs-bugson in the Linux Kernel | https://blog.janestreet.com/a-higgs-bugson-in-the-linux-kernel/ |
| Jun 14, 2025 | Introducing OxCaml | https://blog.janestreet.com/introducing-oxcaml/ |
| Mar 22, 2025 | Advent of Hardcaml | https://blog.janestreet.com/advent-of-hardcaml-2024/ |
| Jan 24, 2025 | How we accidentally built a better build system for OCaml | https://blog.janestreet.com/how-we-accidentally-built-a-better-build-system-for-ocaml-index/ |
| Oct 04, 2024 | Developer education at Jane Street | https://blog.janestreet.com/developer-education-at-jane-street-index/ |
| Aug 29, 2024 | ICFP 2024 | https://blog.janestreet.com/icfp-2024-index/ |
| Aug 26, 2024 | What the interns have wrought, 2024 edition | https://blog.janestreet.com/what-the-interns-have-wrought-2024-edition-index/ |
| Jul 22, 2024 | Visualizing piecewise linear neural networks | https://blog.janestreet.com/visualizing-piecewise-linear-neural-networks/ |
| Sep 12, 2023 | What the interns have wrought, 2023 edition | https://blog.janestreet.com/what-the-interns-have-wrought-2023/ |
| Sep 01, 2023 | Oxidizing OCaml: Data Race Freedom | https://blog.janestreet.com/oxidizing-ocaml-parallelism/ |
| Jul 06, 2023 | We're sponsoring SoME3 | https://blog.janestreet.com/were-sponsoring-some3/ |
| Jun 21, 2023 | Oxidizing OCaml: Rust-Style Ownership | https://blog.janestreet.com/oxidizing-ocaml-ownership/ |
| May 26, 2023 | Oxidizing OCaml: Locality | https://blog.janestreet.com/oxidizing-ocaml-locality/ |
| Apr 14, 2023 | Building reproducible Python environments with XARs | https://blog.janestreet.com/building-reproducible-python-environments-with-xars/ |
| Jan 09, 2023 | What if writing tests was a joyful experience? | https://blog.janestreet.com/the-joy-of-expect-tests/ |
| Dec 07, 2022 | Accelerating zk-SNARKs - MSM and NTT algorithms on FPGAs with Hardcaml | https://blog.janestreet.com/zero-knowledge-fpgas-hardcaml/ |
| Nov 23, 2022 | Visualizing information propagation in markets | https://blog.janestreet.com/visualizing-information-propagation-in-markets-index/ |
| Nov 17, 2022 | Computations that differentiate, debug, and document themselves | https://blog.janestreet.com/computations-that-differentiate-debug-and-document-themselves/ |
| Aug 30, 2022 | Introducing the Jane Street Graduate Research Fellowship | https://blog.janestreet.com/graduate-research-fellowship/ |
| Aug 25, 2022 | What the interns have wrought, 2022 edition | https://blog.janestreet.com/what-the-interns-have-wrought-2022/ |
| Mar 04, 2022 | Research internships in our Tools and Compilers group | https://blog.janestreet.com/research-internships-tnc/ |
| Jan 14, 2022 | How Jane Street Pairs Interns to Projects and Teams During the Software Engineering Internship | https://blog.janestreet.com/project-pairing/ |
| Jan 11, 2022 | Magic-trace: Diagnosing tricky performance issues easily with Intel Processor Trace | https://blog.janestreet.com/magic-trace/ |
| Oct 21, 2021 | Hiring a Developer Educator | https://blog.janestreet.com/hiring-a-developer-educator/ |
| Aug 09, 2021 | What the interns have wrought, 2021 edition | https://blog.janestreet.com/what-the-interns-have-wrought-2021/ |
| Jun 15, 2021 | Looking for a developer experience engineer | https://blog.janestreet.com/looking-for-a-developer-experience-engineer-index/ |
| Dec 01, 2020 | Growing the Hardcaml toolset | https://blog.janestreet.com/growing-the-hardcaml-toolset-index/ |
| Nov 24, 2020 | Announcing Our Market Prediction Kaggle Competition | https://blog.janestreet.com/announcing-our-market-prediction-kaggle-competition-index/ |
| Oct 06, 2020 | Finding memory leaks with Memtrace | https://blog.janestreet.com/finding-memory-leaks-with-memtrace/ |
| Sep 15, 2020 | Memory allocator showdown | https://blog.janestreet.com/memory-allocator-showdown/ |
| Aug 31, 2020 | Announcing Signals and Threads, a new podcast from Jane Street | https://blog.janestreet.com/announcing-signals-and-threads-index/ |
| Aug 17, 2020 | What the interns have wrought, 2020 edition | https://blog.janestreet.com/what-the-interns-have-wrought-2020/ |
| Jul 24, 2020 | The Jane Street Interview Process — 2020 Edition | https://blog.janestreet.com/jane-street-interview-process-2020/ |
| Jun 22, 2020 | Really low latency multipliers and cryptographic puzzles | https://blog.janestreet.com/really-low-latency-multipliers-and-cryptographic-puzzles/ |
| Jun 01, 2020 | Using ASCII waveforms to test hardware designs | https://blog.janestreet.com/using-ascii-waveforms-to-test-hardware-designs/ |
| Apr 17, 2020 | Chrome extensions: Finding the missing proof | https://blog.janestreet.com/chrome-extensions-finding-the-missing-proof/ |
| Feb 20, 2020 | Watch all of Jane Street's tech talks | https://blog.janestreet.com/watch-all-of-jane-streets-tech-talks/ |
| Feb 03, 2020 | Troubleshooting systemd with SystemTap | https://blog.janestreet.com/troubleshooting-systemd-with-systemtap/ |
| Dec 16, 2019 | Using Python and OCaml in the same Jupyter notebook | https://blog.janestreet.com/using-python-and-ocaml-in-the-same-jupyter-notebook/ |
| Dec 06, 2019 | Deep-Learning the Hardest Go Problem in the World | https://blog.janestreet.com/deep-learning-the-hardest-go-problem-in-the-world/ |
| Oct 14, 2019 | Commas in big numbers everywhere: An OpenType adventure | https://blog.janestreet.com/commas-in-big-numbers-everywhere/ |
| Aug 30, 2019 | What the interns have wrought, 2019 edition | https://blog.janestreet.com/what-the-interns-have-wrought-2019/ |
| Aug 19, 2019 | Using OCaml to drive a Raspberry Pi robot car | https://blog.janestreet.com/using-ocaml-to-drive-a-raspberry-pi-robot-car/ |
| Jul 09, 2019 | Of Pythons and Camels | https://blog.janestreet.com/of-pythons-and-camels/ |
| May 13, 2019 | Thoughts from AAAI 2019 | https://blog.janestreet.com/thoughts-from-aaai-19/ |
| Apr 17, 2019 | Learning ML Depth-First | https://blog.janestreet.com/learning-ml-depth-first/ |
| Feb 28, 2019 | Machining the ultimate hackathon prize | https://blog.janestreet.com/hackathon-keyboards/ |
| Feb 28, 2019 | Accelerating Self-Play Learning in Go | https://blog.janestreet.com/accelerating-self-play-learning-in-go/ |
| Jan 29, 2019 | L2 Regularization and Batch Norm | https://blog.janestreet.com/l2-regularization-and-batch-norm/ |
| Jan 15, 2019 | A tutorial for building web applications with Incr_dom | https://blog.janestreet.com/a-tutorial-for-building-web-applications-with-incrdom/ |
| Sep 26, 2018 | How to shuffle a big dataset | https://blog.janestreet.com/how-to-shuffle-a-big-dataset/ |
| Sep 20, 2018 | Deep learning experiments in OCaml | https://blog.janestreet.com/deep-learning-experiments-in-ocaml/ |
| Aug 06, 2018 | What the interns have wrought, 2018 edition | https://blog.janestreet.com/what-the-interns-have-wrought-2018/ |
| Jun 29, 2018 | Plans for OCaml 4.08 | https://blog.janestreet.com/plans-for-ocaml-408/ |
| Apr 22, 2018 | Repeatable exploratory programming | https://blog.janestreet.com/repeatable-exploratory-programming/ |
| Apr 04, 2018 | OCaml all the way down | https://blog.janestreet.com/ocaml-all-the-way-down/ |
| Mar 27, 2018 | Putting the I back in IDE: Towards a Github Explorer | https://blog.janestreet.com/putting-the-i-back-in-ide-towards-a-github-explorer/ |
| Feb 16, 2018 | Learn OCaml in NYC | https://blog.janestreet.com/learn-ocaml-nyc/ |
| Feb 15, 2018 | Proofs (and Refutations) using Z3 | https://blog.janestreet.com/proofs-and-refutations-using-z3/ |
| Dec 20, 2017 | Work on the OCaml compiler at Jane Street! | https://blog.janestreet.com/work-on-the-ocaml-compiler-at-jane-street/ |
| Oct 31, 2017 | Does batch size matter? | https://blog.janestreet.com/does-batch-size-matter/ |
| Oct 29, 2017 | How Jane Street Does Code Review (Jane Street Tech Talk) | https://blog.janestreet.com/jane-street-tech-talk-how-jane-street-does-code-review/ |
| Sep 26, 2017 | Jane Street Tech Talk, Verifying Network Data Planes | https://blog.janestreet.com/jane-street-tech-talk-verifying-network-data-planes/ |
| Aug 28, 2017 | Real world machine learning (part 1) | https://blog.janestreet.com/real-world-machine-learning-part-1/ |
| Aug 25, 2017 | How to design a tree diffing algorithm | https://blog.janestreet.com/how-to-design-a-tree-diffing-algorithm/ |
| Aug 24, 2017 | Ironing out your development style | https://blog.janestreet.com/ironing-out-your-development-style/ |
| Aug 16, 2017 | Hiring an FPGA engineer | https://blog.janestreet.com/hiring-an-fpga-engineer/ |
| Aug 14, 2017 | What the interns have wrought, 2017 edition | https://blog.janestreet.com/what-the-interns-have-wrought-2017/ |
| May 11, 2017 | When Bash Scripts Bite | https://blog.janestreet.com/when-bash-scripts-bite/ |
| May 01, 2017 | Looking for a technical writer | https://blog.janestreet.com/looking-for-a-technical-writer/ |
| Apr 25, 2017 | Caveat Configurator: how to replace configs with code, and why you might not want to | https://blog.janestreet.com/caveat-configurator-how-to-replace-configs-with-code-and-why-you-might-not-want-to/ |
| Apr 20, 2017 | This is not the performance you were looking for: the tricks systems play on us | https://blog.janestreet.com/this-is-not-the-performance-you-were-looking-for-the-tricks-systems-play-on-us/ |
| Mar 20, 2017 | Trivial meta-programming with cinaps | https://blog.janestreet.com/trivial-meta-programming-with-cinaps/ |
| Mar 15, 2017 | One more talk, two more videos | https://blog.janestreet.com/one-more-talk-two-more-videos/ |
| Feb 28, 2017 | What a Jane Street software engineering interview is like | https://blog.janestreet.com/what-a-jane-street-dev-interview-is-like/ |
| Feb 16, 2017 | Jane Street Tech Talks: Verifying Puppet Configs | https://blog.janestreet.com/jane-street-tech-talks-verifying-puppet-configs/ |
| Jan 11, 2017 | How to Build an Exchange | https://blog.janestreet.com/how-to-build-an-exchange/ |
| Jan 09, 2017 | A brief trip through Spacetime | https://blog.janestreet.com/a-brief-trip-through-spacetime/ |
| Nov 08, 2016 | A solution to the ppx versioning problem | https://blog.janestreet.com/an-solution-to-the-ppx-versioning-problem/ |
| Oct 27, 2016 | Observations of a functional programmer | https://blog.janestreet.com/observations-of-a-functional-programmer/ |
| Sep 13, 2016 | What the interns have wrought, 2016 | https://blog.janestreet.com/what-the-interns-have-wrought-2016/ |
| Aug 31, 2016 | Unraveling of the tech hiring market | https://blog.janestreet.com/unraveling/ |
| Aug 30, 2016 | Do you love dev tools? Come work at Jane Street. | https://blog.janestreet.com/do-you-love-dev-tools-come-work-at-jane-street/ |
| Jun 21, 2016 | Let syntax, and why you should use it | https://blog.janestreet.com/let-syntax-and-why-you-should-use-it/ |
| Mar 09, 2016 | Seven Implementations of Incremental | https://blog.janestreet.com/seven-implementations-of-incremental/ |
| Mar 01, 2016 | OCaml 4.03: Everything else | https://blog.janestreet.com/ocaml-4-03-everything-else/ |
| Feb 24, 2016 | A better inliner for OCaml, and why it matters | https://blog.janestreet.com/flambda/ |
| Feb 10, 2016 | Self Adjusting DOM and Diffable Data | https://blog.janestreet.com/self-adjusting-dom-and-diffable-data/ |
| Feb 06, 2016 | Self Adjusting DOM | https://blog.janestreet.com/self-adjusting-dom/ |
| Jan 30, 2016 | Incremental computation and the web | https://blog.janestreet.com/incrementality-and-the-web/ |
| Jan 25, 2016 | Why OCaml? | https://blog.janestreet.com/why-ocaml/ |
| Dec 02, 2015 | Testing with expectations | https://blog.janestreet.com/testing-with-expectations/ |
| Oct 26, 2015 | Quickcheck for Core | https://blog.janestreet.com/quickcheck-for-core/ |
| Oct 07, 2015 | rsync rounds timestamps to the nearest second | https://blog.janestreet.com/rsync-rounds-timestamps-to-the-nearest-second/ |
| Aug 19, 2015 | No (functional) experience required | https://blog.janestreet.com/no-functional-experience-required/ |
| Jul 18, 2015 | Introducing Incremental | https://blog.janestreet.com/introducing-incremental/ |
| Jul 08, 2015 | Converting a code base from camlp4 to ppx | https://blog.janestreet.com/converting-a-code-base-from-camlp4-to-ppx/ |
| May 05, 2015 | CPU Registers and OCaml | https://blog.janestreet.com/cpu-registers-and-ocaml-2/ |
| May 01, 2015 | Reverse web proxy in ~50 lines of BASH | https://blog.janestreet.com/reverse-web-proxy-in-50-lines-of-bash/ |
| Apr 10, 2015 | Building a lower-latency GC | https://blog.janestreet.com/building-a-lower-latency-gc/ |
| Apr 09, 2015 | Faster OCaml to C calls | https://blog.janestreet.com/faster-ocaml-to-c-calls/ |
| Mar 30, 2015 | Why GADTs matter for performance | https://blog.janestreet.com/why-gadts-matter-for-performance/ |
| Mar 21, 2015 | A lighter Core | https://blog.janestreet.com/a-lighter-core/ |
| Mar 04, 2015 | Centralizing distributed version control, revisited | https://blog.janestreet.com/centralizing-distributed-version-control-revisited/ |
| Jan 31, 2015 | Making making better | https://blog.janestreet.com/making-making-better/ |
| Jan 02, 2015 | 13 Virtues | https://blog.janestreet.com/13-virtues/ |
| Dec 01, 2014 | Inspecting the Environment of a Running Process | https://blog.janestreet.com/inspecting-the-environment-of-a-running-process/ |
| Nov 17, 2014 | How to choose a teaching language | https://blog.janestreet.com/how-to-choose-a-teaching-language/ |
| Oct 24, 2014 | Interviewing At Jane Street | https://blog.janestreet.com/interviewing-at-jane-street/ |
| Sep 29, 2014 | What is gained and lost with 63-bit integers? | https://blog.janestreet.com/what-is-gained-and-lost-with-63-bit-integers/ |
| Aug 23, 2014 | Clearly Failing | https://blog.janestreet.com/clearly-failing/ |
| Jul 31, 2014 | The ML Workshop looks fantastic | https://blog.janestreet.com/the-ml-workshop-looks-fantastic/ |
| Jul 18, 2014 | Simple top-down development in OCaml | https://blog.janestreet.com/simple-top-down-development-in-ocaml/ |
| Jul 10, 2014 | What's in a name? | https://blog.janestreet.com/whats-in-a-name/ |
| Jul 09, 2014 | Inspecting Internal TCP State on Linux | https://blog.janestreet.com/inspecting-internal-tcp-state-on-linux/ |
| Jul 06, 2014 | Making “never break the build” scale | https://blog.janestreet.com/making-never-break-the-build-scale/ |
| Jun 29, 2014 | Notes on Naming | https://blog.janestreet.com/notes-on-naming/ |
| Jun 26, 2014 | Reading Lamport, again | https://blog.janestreet.com/reading-lamport-again/ |
| Jun 24, 2014 | Iron out your release process | https://blog.janestreet.com/ironing-out-your-release-process/ |
| Jun 13, 2014 | Scrutinize your code in style | https://blog.janestreet.com/scrutinizing-your-code-in-style/ |
| Jun 12, 2014 | Code review that isn't boring | https://blog.janestreet.com/code-review-that-isnt-boring/ |
| May 18, 2014 | OCaml 4.02: everything else | https://blog.janestreet.com/ocaml-4-02-everything-else/ |
| May 17, 2014 | Pattern matching and exception handling, unite! | https://blog.janestreet.com/pattern-matching-and-exception-handling-unite/ |
| May 15, 2014 | Hiring a compiler engineer | https://blog.janestreet.com/hiring-a-compiler-engineer/ |
| May 14, 2014 | Why change is hard | https://blog.janestreet.com/why-change-is-hard/ |
| May 12, 2014 | Better namespaces through module aliases | https://blog.janestreet.com/better-namespaces-through-module-aliases/ |
| May 08, 2014 | Extension Points, or how OCaml is becoming more like Lisp | https://blog.janestreet.com/extension-points-or-how-ocaml-is-becoming-more-like-lisp/ |
| Apr 23, 2014 | How to fail -- introducing Or_error.t | https://blog.janestreet.com/how-to-fail-introducing-or-error-dot-t/ |
| Apr 22, 2014 | Disabling Chrome's x-webkit-speech vulnerability | https://blog.janestreet.com/disabling-chromes-x-webkit-speech-vulnerability/ |
| Apr 17, 2014 | How Does Automount Work Anyway? | https://blog.janestreet.com/how-does-automount-work-anyway/ |
| Apr 07, 2014 | Generic mapping and folding in OCaml | https://blog.janestreet.com/generic-mapping-and-folding-in-ocaml/ |
| Feb 24, 2014 | Breaking down FRP | https://blog.janestreet.com/breaking-down-frp/ |
| Jan 09, 2014 | Async Parallel | https://blog.janestreet.com/async-parallel/ |
| Dec 20, 2013 | 10 tips for writing comments (plus one more) | https://blog.janestreet.com/10-tips-for-writing-comments-plus-one-more/ |
| Dec 11, 2013 | A module type equivalence surprise | https://blog.janestreet.com/a-module-type-equivalence-surprise/ |
| Dec 08, 2013 | RWO tidbits: the runtime | https://blog.janestreet.com/rwo-tidbits-the-runtime/ |
| Dec 01, 2013 | RWO tidbits: Benign effects | https://blog.janestreet.com/rwo-tidbits-benign-effects/ |
| Nov 11, 2013 | The making of Real World OCaml | https://blog.janestreet.com/the-making-of-real-world-ocaml/ |
| Sep 11, 2013 | What's 2013 + 50? 1969, of course! | https://blog.janestreet.com/whats-2013-50-1969-of-course/ |
| May 03, 2013 | Patch review vs diff review, revisited | https://blog.janestreet.com/patch-review-vs-diff-review-revisited/ |
| Apr 02, 2013 | Hackerschool tutorial at Jane Street | https://blog.janestreet.com/hackerschool-tutorial-at-jane-street/ |
| Nov 12, 2012 | Maps, sets, and hashtables in core | https://blog.janestreet.com/maps-sets-and-hashtables-in-core/ |
| Oct 22, 2012 | Bootstrapping OCaml/async on the Raspberry Pi | https://blog.janestreet.com/bootstrapping-ocamlasync-on-the-raspberry-pi/ |
| Oct 19, 2012 | Announcing OCaml Labs | https://blog.janestreet.com/announcing-ocaml-labs/ |
| Sep 27, 2012 | Jane Street at OUD | https://blog.janestreet.com/jane-street-at-oud/ |
| Sep 18, 2012 | Observer effect and YOU (NSLCD and GetPWNam()-a-plenty) | https://blog.janestreet.com/observer-effect-and-you-nslcd-and-getpwnam-a-plenty/ |
| Jun 21, 2012 | Repos, RPMs, and bootstraps, oh my! | https://blog.janestreet.com/repos-rpms-and-bootstraps-oh-my/ |
| Jun 05, 2012 | Speed Up | https://blog.janestreet.com/speed-up/ |
| May 14, 2012 | Finding references to lazily unmounted filesystems | https://blog.janestreet.com/finding-references-to-lazily-unmounted-filesystems/ |
| Apr 23, 2012 | OCaml for the Sysadmins | https://blog.janestreet.com/ocaml-for-the-sysadmins/ |
| Mar 29, 2012 | S-Expressions in ruby | https://blog.janestreet.com/s-expressions-in-ruby/ |
| Mar 28, 2012 | Linux disk crypto, now with ease | https://blog.janestreet.com/linux-disk-crypto-now-with-ease/ |
| Mar 22, 2012 | ML workshop | https://blog.janestreet.com/ml-workshop/ |
| Feb 21, 2012 | Do you solve real problems with FP? Then come talk about it at CUFP! | https://blog.janestreet.com/do-you-solve-real-problems-with-fp-then-come-talk-about-it-at-cufp/ |
| Feb 17, 2012 | The adventures in NIC bonding | https://blog.janestreet.com/the-adventures-in-nic-bonding/ |
| Feb 17, 2012 | OpenLDAP, DBD, and you. | https://blog.janestreet.com/openldap-dbd-and-you/ |
| Feb 02, 2012 | Iterative email problem solving with python, Part 2 | https://blog.janestreet.com/iterative-email-problem-solving-with-python-part-2/ |
| Jan 20, 2012 | Iterative email problem solving with python. | https://blog.janestreet.com/iterative-email-problem-solving-with-python/ |
| Jan 12, 2012 | Making staging explicit | https://blog.janestreet.com/making-staging-explicit/ |
| Jan 07, 2012 | Fork Core! | https://blog.janestreet.com/fork-core/ |
| Jan 03, 2012 | Moving files via rsync | https://blog.janestreet.com/moving-files-via-rsync/ |
| Nov 02, 2011 | OCaml, the ultimate refactoring tool | https://blog.janestreet.com/ocaml-the-ultimate-refactoring-tool/ |
| Oct 25, 2011 | Announcing Async | https://blog.janestreet.com/announcing-async/ |
| Oct 17, 2011 | +'a and -'a | https://blog.janestreet.com/a-and-a/ |
| Oct 03, 2011 | A mailing list for Core | https://blog.janestreet.com/a-mailing-list-for-core/ |
| Sep 13, 2011 | Coming to ICFP/CUFP? Propose a BOF! | https://blog.janestreet.com/coming-to-icfpcufp-propose-a-bof/ |
| Aug 02, 2011 | Using types to track defaults | https://blog.janestreet.com/using-types-to-track-defaults/ |
| Jul 31, 2011 | Rethinking Univ | https://blog.janestreet.com/rethinking-univ/ |
| Jul 28, 2011 | Time to register for CUFP! | https://blog.janestreet.com/time-to-register-for-cufp/ |
| Jun 24, 2011 | Dropping history with Mercurial | https://blog.janestreet.com/dropping-history-with-mercurial/ |
| Apr 25, 2011 | Core Gems: many happy returns | https://blog.janestreet.com/core-gems-many-happy-returns/ |
| Apr 09, 2011 | OCaml is smarter than I thought | https://blog.janestreet.com/ocaml-is-smarter-than-i-thought/ |
| Apr 06, 2011 | OCamlPro and the future of OCaml | https://blog.janestreet.com/ocamlpro-and-the-future-of-ocaml/ |
| Mar 27, 2011 | Effective ML Revisited (with videos) | https://blog.janestreet.com/effective-ml-revisited-with-videos/ |
| Mar 25, 2011 | Core 0.7.0 is out! | https://blog.janestreet.com/core-0-7-0-is-out/ |
| Mar 23, 2011 | Do you use FP in anger? Then talk about it at CUFP this year! | https://blog.janestreet.com/do-you-use-fp-in-anger-then-talk-about-it-at-cufp-this-year/ |
| Mar 09, 2011 | Effective ML Revisited | https://blog.janestreet.com/effective-ml-revisited/ |
| Oct 01, 2010 | A trick: recursive modules from recursive signatures | https://blog.janestreet.com/a-trick-recursive-modules-from-recursive-signatures/ |
| Aug 25, 2010 | BOFs, Tutorials and Talks, oh my! | https://blog.janestreet.com/bofs-tutorials-and-talks-oh-my/ |
| Aug 21, 2010 | Effective ML video | https://blog.janestreet.com/effective-ml-video/ |
| Aug 04, 2010 | More expressive GADT encodings via first class modules | https://blog.janestreet.com/more-expressive-gadt-encodings-via-first-class-modules/ |
| Jul 23, 2010 | OCaml as a scripting language | https://blog.janestreet.com/ocaml-as-a-scripting-language/ |
| Jul 16, 2010 | Ensuring that a function is polymorphic in Ocaml 3.12 | https://blog.janestreet.com/ensuring-that-a-function-is-polymorphic-in-ocaml-3-12/ |
| Jul 15, 2010 | Making something out of nothing (or, why None is better than NaN and NULL) | https://blog.janestreet.com/making-something-out-of-nothing-or-why-none-is-better-than-nan-and-null/ |
| Apr 27, 2010 | Another use for private type abbreviations | https://blog.janestreet.com/another-use-for-private-type-abbreviations/ |
| Apr 22, 2010 | Effective ML | https://blog.janestreet.com/effective-ml/ |
| Apr 22, 2010 | CUFP 2010 is coming! | https://blog.janestreet.com/cufp-2010-is-coming/ |
| Nov 11, 2009 | Jane Street OCamldocs now available | https://blog.janestreet.com/jane-street-ocamldocs-now-available/ |
| Nov 07, 2009 | Core Gems: Time | https://blog.janestreet.com/core-gems-time/ |
| Oct 10, 2009 | Optimizing List.map | https://blog.janestreet.com/optimizing-list-map/ |
| Oct 08, 2009 | Core 0.6.0 release | https://blog.janestreet.com/core-0-6-0-release/ |
| Sep 29, 2009 | Another JSSP post | https://blog.janestreet.com/another-jssp-post/ |
| Sep 23, 2009 | Jane Street Summer Project round-up | https://blog.janestreet.com/jane-street-summer-project-round-up/ |
| Aug 16, 2009 | Designing a code-review tool, Part 2: Patches or Diffs | https://blog.janestreet.com/designing-a-code-review-tool-part-2-patches-or-diffs/ |
| Aug 08, 2009 | Designing a code-review tool, Part 1 | https://blog.janestreet.com/designing-a-code-review-tool-part-1/ |
| Jul 13, 2009 | OCaml in Japan, and its Meeting in Tokyo | https://blog.janestreet.com/ocaml-in-japan-and-its-meeting-in-tokyo/ |
| May 16, 2009 | What do Haskellers have against exhaustiveness? | https://blog.janestreet.com/what-do-haskellers-have-against-exhaustiveness/ |
| May 12, 2009 | Presenting the 2009 JSSP projects | https://blog.janestreet.com/presenting-the-2009-jssp-projects/ |
| Apr 01, 2009 | Proposals in, application period is closed | https://blog.janestreet.com/proposals-in-application-period-is-closed/ |
| Mar 12, 2009 | Caml Trading talk at CMU | https://blog.janestreet.com/caml-trading-talk-at-cmu/ |
| Mar 04, 2009 | Do you use FP as a means rather than an end? | https://blog.janestreet.com/do-you-use-fp-as-a-means-rather-than-an-end/ |
| Feb 12, 2009 | Private type abbreviations, what are they good for? | https://blog.janestreet.com/private-type-abbreviations-what-are-they-good-for/ |
| Jan 31, 2009 | Summer Project '09 | https://blog.janestreet.com/summer-project-09/ |
| Dec 03, 2008 | Lightweight versioning for lightweight protocols | https://blog.janestreet.com/lightweight-versioning-for-lightweight-protocols/ |
| Sep 30, 2008 | The OSP meeting | https://blog.janestreet.com/the-osp-meeting/ |
| Sep 23, 2008 | A Working Programmer's Guide to Type-Indexed Values | https://blog.janestreet.com/a-working-programmers-guide-to-type-indexed-values/ |
| Sep 17, 2008 | Centralizing distributed version control | https://blog.janestreet.com/centralizing-distributed-version-control/ |
| Sep 03, 2008 | Building a better compare | https://blog.janestreet.com/building-a-better-compare/ |
| Aug 27, 2008 | Ask and ye shall receive | https://blog.janestreet.com/ask-and-ye-shall-receive/ |
| Aug 18, 2008 | The perils of polymorphic compare | https://blog.janestreet.com/the-perils-of-polymorphic-compare/ |
| Aug 05, 2008 | Better float unboxing | https://blog.janestreet.com/better-float-unboxing/ |
| Jun 21, 2008 | Folding over fields | https://blog.janestreet.com/folding-over-fields/ |
| May 29, 2008 | The dangers of being too partial | https://blog.janestreet.com/the-dangers-of-being-too-partial/ |
| May 14, 2008 | Ensuring that a function is polymorphic | https://blog.janestreet.com/ensuring-that-a-function-is-polymorphic/ |
| May 11, 2008 | Core Principles: uniformity of interface | https://blog.janestreet.com/core-principles-uniformity-of-interface/ |
| May 02, 2008 | Core has landed | https://blog.janestreet.com/core-has-landed/ |
| Apr 25, 2008 | using with type on a variant type | https://blog.janestreet.com/using-with-type-on-a-variant-type/ |
| Apr 16, 2008 | OCaml Annoyance #23: type declarations are implicitly recursive | https://blog.janestreet.com/ocaml-annoyance-23-type-declarations-are-implicitly-recursive/ |
| Apr 02, 2008 | The ML sweet spot | https://blog.janestreet.com/the-ml-sweet-spot/ |
| Mar 26, 2008 | Bind without tears | https://blog.janestreet.com/bind-without-tears/ |
| Mar 20, 2008 | Variable-argument functions | https://blog.janestreet.com/variable-argument-functions/ |
| Mar 15, 2008 | Typing RPCs | https://blog.janestreet.com/typing-rpcs/ |
| Mar 14, 2008 | Using let module for matching | https://blog.janestreet.com/using-let-module-for-matching/ |
| Mar 11, 2008 | Extracting an exception from a module | https://blog.janestreet.com/extracting-an-exception-from-a-module/ |
| Mar 07, 2008 | A universal type? | https://blog.janestreet.com/a-universal-type/ |
| Mar 05, 2008 | Talking at Penn | https://blog.janestreet.com/talking-at-penn/ |
| Feb 28, 2008 | We've got a blog! | https://blog.janestreet.com/weve-got-a-blog/ |
| Feb 28, 2008 | HOWTO: Static access control using phantom types | https://blog.janestreet.com/howto-static-access-control-using-phantom-types/ |
