# Jane Street public technical voices: source material for persona skills

Compiled 2026-11-07. Scope: professional public record only (podcasts, blog posts, talks, papers, OSS). No contact details or private information collected.

## How this was built, and how far to trust it

- **Signals and Threads transcripts.** The full transcript of every episode (33 entries, 2020-08 to 2026-10) is embedded in the JSON search index on the homepage at `https://signalsandthreads.com/`. It was pulled whole, and speaker turns were parsed by timestamp. Quotes marked **[S&T slug @ timestamp]** are verbatim from that text. The timestamp is the start of the speaker's turn, not of the sentence. One check worth knowing about: a quote at `multicast-and-the-markets @36:11` first looked like Ron's, but on inspection it is Brian Nigito's. A malformed timestamp (`36:1`) had broken the parser. That was fixed and the attribution corrected.
- **Jane Street blog.** Author pages (`blog.janestreet.com/author/<id>`) were listed. About 45 principle-dense posts were downloaded and their text extracted. Quotes marked **[blog: slug]** are verbatim.
- **Tech talks.** The index at `janestreet.com/tech-talks/` (pages 1–7) was listed. Talk titles and speakers come from it. Talk transcripts were **not** mined, which is a gap. They are the next place to look.
- **Paraphrase marking.** Anything not copied from a primary text is marked *(paraphrase)* or *(secondary source)*.
- **Not verified.** Current employment status of several people. "JS-era" means the work dates from their time at Jane Street. Status is recorded only where a primary source states it.

---

## 1. Ranked candidates

The ranking reflects how much first-person, principle-bearing public material exists, and whether that material is enough to build a faithful skill without inventing anything.

| # | Person | Status (per sources) | Area | Persona-worthiness (1–5) | Densest sources |
|---|---|---|---|---|---|
| 1 | **Yaron (Ron) Minsky** | JS since 2002 (blog bio); S&T host | OCaml at JS, API design, types, code review, tooling, formal methods + agents | **5** | ~120 blog posts; host of every S&T episode; Effective ML; Real World OCaml; tech talks |
| 2 | **Richard Eisenberg** | JS Tools & Compilers / OCaml Language team | Dependent types, type-system design, OxCaml modes/layouts, specs and AI | **4** | S&T `future-of-programming`; ICFP'24 + POPL'25 papers; large pre-JS Haskell/GHC record |
| 3 | **Stephen Dolan** | JS Tools & Compilers | Memory management, GC, unboxed types, type inference; creator of `jq` | **4** | S&T `memory-management`; talk "Unboxed Types for OCaml"; *Algebraic Subtyping* thesis; Memtrace; blog |
| 4 | **Leo White** | JS compilers (frontend/type system) | Language design as math + aesthetics; modularity; OxCaml lead voice | **4** | S&T `language-design`; "Introducing OxCaml"; talk "Effective Programming: Adding an Effect System to OCaml"; modes papers |
| 5 | **Andrew Hunter** | JS (ex-Google tcmalloc TL) | Performance engineering, profiling, mechanical sympathy | **3.5** | S&T `performance-engineering-on-hard-mode` |
| 6 | **Andrey Mokhov** | JS (build systems) | Build-system theory, Dune/Jenga, constrained DSLs | **3.5** | S&T `build-systems`; blog on Dune; *Build Systems à la Carte*; Selective functors; algebraic-graphs |
| 7 | **Brian Nigito** | JS | Exchange/market infrastructure, multicast, simplicity, mechanical sympathy | **3.5** | S&T `multicast-and-the-markets`; tech talk "How to Build an Exchange" |
| 8 | **James Somers** | JS writer-in-residence | Technical writing, documentation, expect tests, knowledge sharing | **3.5** | S&T `writing-technically`; ~11 blog posts; outside journalism |
| 9 | **Andy Ray** (+ **Benjamin Devlin**) | JS | Hardcaml, FPGA design, hardware testing | **3** | S&T `programmable-hardware`; talk "OCaml All The Way Down"; Hardcaml blog posts; ZPrize; FPGA/ASIC puzzles |
| 10 | **Doug Patti** | JS Client-Facing Tech | State-machine replication (Concord/Aria), testing to "battle-tested" | **3** | S&T `state-machine-replication...`; blog `getting-from-tested-to-battle-tested` |
| 11 | **Tristan Hume** | **Alumnus.** Left JS in 2022 for Anthropic (thume.ca) | magic-trace, Intel PT, perf tooling | **2.5** (JS-era only) | blog `magic-trace`; magic-trace OSS; thume.ca |
| 12 | **Ty Overby** | JS-era Bonsai author | Functional UI, incremental computation | **2.5** | S&T `building-a-ui-framework`; Bonsai OSS |
| 13 | **Max Slater** | JS-era | OxCaml locality, ownership, data-race freedom | **2.5** | "Oxidizing OCaml" 3-part series |
| 14 | **Chris Casinghino** | JS | Safe performance engineering in OCaml, unboxed types | **2** | talk "Making OCaml Safe for Performance Engineering"; POPL'25 co-author |
| 15 | **Greta Yorsh** | JS compilers (London) | Backend optimization, FDO, verification vs testing | **2** | S&T `compiler-optimization` |
| 16 | **Laurent Mazare** | **Alumnus.** Now Kyutai CTO/co-founder (ai-pulse.eu) | ML in typed languages, ocaml-torch, Python↔OCaml | **2.5** | S&T `python-ocaml-and-machine-learning`; 4 blog posts; ocaml-torch |
| 17 | **Sylvain Gugger** | JS ML-infra (ex-fast.ai/HF) | GPU training performance | **2.5** | S&T `the-uncertain-art...`; talk "Making GPUs Actually Fast" |
| 18 | **Stephen Weeks** | Early JS; MLton creator | Advanced OCaml type tricks | **2** | ~10 blog posts (type-level idioms) |
| 19 | **John Crepezzi** | JS AI tooling (ex-GitHub) | AI dev tools, model-reviewed code, sandboxes | **2** | S&T `the-changing-craft-of-programming` (2026) |
| 20 | **Chris Perl** | JS sysadmin/Linux | Clock sync, Linux internals | **2** | S&T `clock-synchronization`; 4 blog posts |
| 21 | **David Wu** | JS (KataGo author) | Self-play RL, game AI | **2** | KataGo paper (arXiv 1902.10565, JS affiliation); blog |
| — | Jeremie Dimino, Carl Eastlund, Ian Henry, Eric Mannes, Jacob Baskin, Ella Ehrlich, Aaron Bauer | JS | ppx/dune; QuickCheck; trader tools; alt-data; data warehouse; legacy systems; dev education | 1–2 | see §4 |

**Dropped or weak.** Mark Shinwell (flambda) and Antal Spector-Zabusky: this pass found no first-person, principle-bearing public text from either, only co-authorship and compiler work. That is not enough for a faithful persona. Pierre Chambart is OCamlPro, not JS. Guests who are not JS staff (Chris Lattner, Will Wilson, Anil Madhavapeddy, Nate Foster as a visiting researcher) are listed in the episode table but not profiled as JS personas.

---

## 2. Profiles

### 2.1 Yaron (Ron) Minsky: rating 5

**Role.** Joined JS in 2002. Per his blog bio he "claims the dubious honor of having convinced the firm to start using OCaml". Hosts Signals and Threads. Co-author of *Real World OCaml* (with Anil Madhavapeddy and Jason Hickey; 2nd ed., Cambridge UP; https://dev.realworldocaml.org). Long-time public face of JS technology.

**Key public works**
- "Effective ML" lecture (Harvard/Northeastern 2010; revisited 2011): https://blog.janestreet.com/effective-ml/ and https://blog.janestreet.com/effective-ml-revisited/
- "OCaml for the Masses", *ACM Queue* 2011: https://queue.acm.org/detail.cfm?id=2038036 (403 to the fetcher; not quoted here)
- "Formal methods and the future of programming" (2026-06-07): https://blog.janestreet.com/formal-methods-at-jane-street-index/
- Code review and Iron: https://blog.janestreet.com/code-review-that-isnt-boring/, https://blog.janestreet.com/scrutinizing-your-code-in-style/, https://blog.janestreet.com/ironing-out-your-development-style/, https://blog.janestreet.com/designing-a-code-review-tool-part-1/
- Testing: https://blog.janestreet.com/testing-with-expectations/, https://blog.janestreet.com/repeatable-exploratory-programming/
- Naming: https://blog.janestreet.com/notes-on-naming/
- Types and APIs: https://blog.janestreet.com/what-do-haskellers-have-against-exhaustiveness/, https://blog.janestreet.com/the-ml-sweet-spot/, https://blog.janestreet.com/core-principles-uniformity-of-interface/, https://blog.janestreet.com/the-perils-of-polymorphic-compare/, https://blog.janestreet.com/making-something-out-of-nothing-or-why-none-is-better-than-nan-and-null/, https://blog.janestreet.com/howto-static-access-control-using-phantom-types/, https://blog.janestreet.com/ocaml-the-ultimate-refactoring-tool/
- Incrementality: https://blog.janestreet.com/introducing-incremental/, https://blog.janestreet.com/seven-implementations-of-incremental/ (also a tech talk), https://blog.janestreet.com/breaking-down-frp/
- Build/release: https://blog.janestreet.com/making-never-break-the-build-scale/
- CUFP keynote index: https://blog.janestreet.com/observations-of-a-functional-programmer/
- Tech talks: "Jane and the Compiler", "The Saga of Multicore OCaml", "Seven Implementations of Incremental" (https://www.janestreet.com/tech-talks/)
- Signals and Threads: host of all episodes (§3)

**Canonical principle list (verbatim headings from "Effective ML", 2010):**
> Favor readers over writers / Create uniform interfaces / Make illegal states unrepresentable / Code for exhaustiveness / Open few modules / Make common errors obvious / Avoid boilerplate / Avoid complex type-hackery / Don't be puritanical about purity
> [blog: effective-ml]

The 2011 follow-up gives worked code for most of these, including the `connection_state` before/after example for "Make illegal states unrepresentable" and `find` vs `find_exn` for "Make common errors obvious" [blog: effective-ml-revisited].

**Recurring ideas, with quotes**
- *Exhaustiveness as a correctness and refactoring tool.* "exhaustiveness checking serves as a kind of refactoring tool. Whenever you expand the possibilities in a type, the compiler will point you to the places where you forgot to handle the new cases you just created." [blog: what-do-haskellers-have-against-exhaustiveness]. Also: "We go even farther at Jane Street, where we use compiler flags to turn that warning into an error, so that the code can't build when the match is incomplete." (same post)
- "pattern matching and the exhaustivity check on pattern matching is the single best feature, and it continues to mystify me that more programming languages have not picked it up." [S&T building-a-functional-email-server @44:47]
- *Warnings are errors.* "we make fairly aggressive choices about turning on warnings in the OCaml compiler … turn them to errors so you cannot even compile your code when you have an unused variable, that can be annoying in some contexts, but it's so incredibly useful, and it catches so many bugs." [S&T building-a-functional-email-server @43:45]
- *Types as lightweight formal methods with universal guarantees.* "type systems, are a kind of lightweight formal method … the properties you capture in your type system are universally quantified." [S&T compiler-optimization @00:09:49]
- *Offloading carefulness.* "you get into the habit of offloading certain habits of carefulness onto the type system, and then you get to think about other things" [S&T language-design @00:09:39.8]
- *Readability as safety.* "We think that high quality code, and in particular, readable code, helps us maintain the safety of our systems and keeps things simple and clean enough for us to stay nimble." [blog: code-review-that-isnt-boring]. Iron's design principle: "don't be boring." (same post)
- *Code review is a negotiation toward simplicity.* "one of the actually most important parts of the process of code review I find, is not so much that, like, one person writes the code and someone else reads it to validate that it's done the right thing. It's more like, somebody writes the code and the other person says, 'Oh, man. This is, like, too messy for me to even read.' … And I think it's an interesting open question of, like, as we start using more of these AI assistants, how good they will be at generating things that are actually simple." [S&T future-of-programming @56:14]
- *Documentation during review.* "the most productive thing I do usually when code reviewing is sit down and write some documentation" [S&T writing-technically @00:16:54]. Against "self-documenting" absolutism: "The idea that every time you write a library, you do such a good job of creating a clean and simple abstraction that you don't really have to tell a story about it, I just haven't seen very much software that looks like that." [S&T writing-technically @00:25:41]
- *Testing tools drive testing volume.* "Testing tools matter because the smoother the process is, the more tests people will write." [blog: testing-with-expectations]. On the limits of example tests: "it's almost sounds like a comically bad idea of I'm going to have a big complicated program and then I'm going to test it by writing six examples." [S&T why-testing-is-hard-and-how-to-fix-it @01:24:39]
- *Pay-as-you-go power; simple, explicit performance.* "the unboxed type work … is really about taking design decisions that have to do with performance and making them explicit at the level of types." [S&T future-of-programming @17:56]. OCaml has "a very fancy type system and a brutally simple memory representation." [@16:46]. Against gradual typing as a default: "the base choice you make in a language like Haskell or OCaml of like, 'actually, even though it has some ups and downs, we're just going to have types everywhere and that's just how it's gonna be,' I think is at least a reasonable place in the trade off space of designs." [@27:14]
- *Simple on both sides.* "a lot of the art of designing great software is figuring out a thing which is simultaneously simple for the end user and also simple to implement." [S&T from-the-lab-to-the-trading-floor @00:50:54]
- *Mathematically simple foundations generalize.* "the ones that have a kind of tighter and simpler mathematical foundation, at least my sense is, tend to be better at generalizing, like the features that you add to solve one problem, turn out to solve lots of different problems and compose nicely with other ideas." [S&T the-network-as-a-program @00:18:23]
- *Naming.* "Names should be informative" / "Less common systems should have more descriptive names" / "We avoid picking cutesy names for identifiers in programs because it makes the code harder to understand and remember, and you should have similar concerns when picking names for your systems." [blog: notes-on-naming]
- *The ML sweet spot.* "ML is hardly perfect. But it's such a nice compromise that it's going to take a real leap forward on the research side to definitively surpass it." [blog: the-ml-sweet-spot]
- *Formal methods and agents (2026 position change).* "I've been telling people for the last 25 years that Jane Street as an organization was just not interested in formal methods. I'm not saying that anymore." … "Agentic code is getting better, but is still tends towards slop: overly complicated, full of weird bugs and corner cases, often not following essential invariants of the codebase that it's a part of." … "agents thrive on feedback." … "But tests aren't enough! … agents benefit a ton from universal guarantees, the ∀ you get out of type systems." [blog: formal-methods-at-jane-street-index]
- *Readability as the business case for OCaml* *(secondary source, paraphrase).* In "OCaml for the Masses", the group's experience convinced them that OCaml produced smaller, simpler, easier-to-understand systems than Java or C#, which was "a huge win" for an organization that valued readability. Verify the wording against the article before quoting it.

**Technical signatures (draft always/never/prefer)**
- ALWAYS encode state machines as variants carrying per-state data. Never use a record of `option` fields.
- ALWAYS make matches exhaustive and treat the exhaustiveness warning as an error. NEVER use `_ ->` wildcards on types that are expected to grow.
- PREFER `find` returning `option`, with `find_exn` as a visibly named alternative ("make common errors obvious").
- PREFER uniform interfaces (`Comparable`, `Stringable`, `Hashable`) included across types.
- PREFER expect tests for concrete scenarios, so output is captured and failures read as diffs, and add property tests where properties exist.
- ALWAYS optimize for the reader and the reviewer. Treat "too messy to read" as a blocking review comment.
- PREFER explicit, type-level control of performance that you pay for only when you use it.
- NEVER give a system a cute, uninformative name.
- DON'T be puritanical about purity: imperative OCaml is fine. Avoid type hackery whose cost exceeds its guarantee.
- 2026 stance: when agents write the code, push guarantees up into types and specs so the verification bottleneck shrinks.

---

### 2.2 Richard Eisenberg: rating 4

**Role.** The S&T blurb calls him "one of the core maintainers of Haskell" before he joined JS's Tools & Compilers team. A JS visiting-researcher posting places him on the OCaml Language team (unboxed types, modes, representation polymorphism).

**Key works**
- S&T "The Future of Programming" (2023-05-18): https://signalsandthreads.com/future-of-programming/
- "Oxidizing OCaml with Modal Memory Management", ICFP 2024 (Lorenzen, White, Dolan, Eisenberg, Lindley): https://icfp24.sigplan.org/details/icfp-2024-papers/19/Oxidizing-OCaml-with-Modal-Memory-Management
- "Data Race Freedom à la Mode", POPL 2025 Distinguished Paper (Georges, Peters, Elbeheiry, White, Dolan, Eisenberg, Casinghino, Pottier, Dreyer): https://iris-project.org/pdfs/2025-popl-drfcaml.pdf
- Pre-JS (useful for voice): PhD thesis *Dependent Types in Haskell: Theory and Practice* (UPenn), GHC type-system work, GHC Steering Committee.

**Quotes [S&T future-of-programming]**
- "not everyone wants to prove everything all the time." [@12:08] This is the pay-as-you-go stance on dependent types.
- "programming languages developing more and more features that sort of figure out the right line and the right balance between this desire for high-level languages, closer to human thought, and low-level details, easier to execute." [@19:57]
- "when you're used to describing the specification of a thing right next to that thing, that, to me, is going to encourage you to write documentation." [@42:19]
- "as a medium of precise communication, it's still very important to have a programming language that allows that communication to happen." [@49:55]
- "if we're working in a system where the human is not expert enough to be able to read the specification and know that it's the right specification, now we've lost." [@55:40]
- "Although, if we have precise specifications, the simplicity of the implementation becomes less important." [@56:55]
- On language evolution at JS, the "tree smash": "some Jane Street engineers work together to come up with a big diff that happens to all of Jane Street's code, all at once, and we can change the spelling of a keyword if we want to." [@35:35]

**Signatures.** Specifications sit next to code and are human-auditable. Proof is opt-in, for the parts that are "easy to get wrong". Iterate on a language feature internally until experience settles the design, then upstream it. Precision of communication is the purpose of a language, more so in the AI era.

---

### 2.3 Stephen Dolan: rating 4

**Role.** JS Tools & Compilers. Creator of `jq` (jqlang/jq `AUTHORS`: "Created By: Stephen Dolan"). Cambridge PhD *Algebraic Subtyping* (2016; CPHC/BCS Distinguished Dissertation 2017; MLsub). Multicore OCaml contributor.

**Key works**
- S&T "Memory Management" (2022-01-05): https://signalsandthreads.com/memory-management/
- Tech talk "Unboxed Types for OCaml": https://www.janestreet.com/tech-talks/
- Blog "Memory allocator showdown": https://blog.janestreet.com/memory-allocator-showdown/
- ICFP'24 and POPL'25 modes papers (above). "First-Class Subtypes" (with Jeremy Yallop): https://arxiv.org/abs/1905.06546. Thesis: https://www.cs.tufts.edu/~nr/cs257/archive/stephen-dolan/thesis.pdf

**Quotes [S&T memory-management]**
- "OCaml … is very far off the garbage-collect-everything scales, which is the right trade-off only some of the time." [@03:51]
- "And it's not just those bugs that have a cost, it's the things people do to avoid the possibility of those bugs has a cost." [@19:35]
- On fragile performance: "if you get some of this and it's nearly right, and your program changes in a way that makes it just very slightly slower or very slightly bigger, then suddenly that can have a five or 10 times difference in the performance." [@39:38]
- "I think there's always this trade-off between trying to find an efficient solution for the problem and trying to rearrange things so that the problem never ever comes up." [@1:20:49]
- On `nullable`: "it's just trying to arrange the whole type system so that we never, ever have to nest them and we can prove that they will never nest." [@1:20:49]
- "the really difficult thing is when you want both in the same language, because it's very easy to get into a bad state where the bit of the language that assumes everything will be right all the time butts up against the bit of the language where the programmer has explicit control" [@1:21:26]
- On packing: "you either get the tight packing of data, or sometimes you get a compiler error saying, 'I'm afraid I can't do that, Dave.'" [@1:11:58]

**Signatures.** Restructure the problem so the bad case cannot arise, rather than optimizing around it. Count the cost of defensive coding, not only the cost of bugs. Prefer a compile error to a silent fallback in representation choices. Distrust performance that depends on a near-miss of cache or prefetch timing.

---

### 2.4 Leo White: rating 4

**Role.** JS compiler frontend and type system. Author of "Introducing OxCaml" (2025-06-14). Co-author of the modes papers. Known for OCaml effects and modular implicits work.

**Key works**
- S&T "Language Design" (2020-10-21): https://signalsandthreads.com/language-design/
- https://blog.janestreet.com/introducing-oxcaml/ ; https://blog.janestreet.com/applied-PL-research/ ; OCaml 4.08 posts
- Tech talk "Effective Programming: Adding an Effect System to OCaml"

**Quotes [S&T language-design]**
- "language design is that it sits at an interesting intersection between some very interesting pure mathematics, especially on the type system design side of things, and a more aesthetic, kind of, design style." [@00:03:55.0]
- "my favorite example is really architecture, which I think is a very similar area to programming language design, in that it's kind of constrained by mathematics. You know, you have to make sure the building stays up and also, is interesting from a design perspective." [@00:05:43.4]
- "it has good predictable performance, which I think is very important. … an experienced OCaml programmer … [has] a pretty good shot at being able to tell you roughly what the assembly that gets produced looks like" [@00:08:40.1]
- "it really forces you to take the idea of an interface seriously … you have to think seriously about how would you express that feature in the interface, as well as in the implementation." [@00:11:03.4]
- On Rust lacking ML modules: "I think that's a shortcoming in Rust that makes me sad, and makes me less likely to use the language." [@00:14:52.4]
- "the lack of sum types … is just kind of insane. … I'm always amazed when a new language comes out without them." [@00:28:35.5]
- "places where people took a shortcut from the language design perspective, and said, 'oh, let me just make it do this, it'll be fine,' often turn out to be the places that are a bit of a nightmare for you later" [@00:24:47.2]
- "as soon as you give them anything that's a bit like GADTs, they straightaway start doing these kind of encoding stuff, and really that's telling you that this wasn't the feature you've should have given them in the first place." [@00:42:06.4]
- "I think language design is quite a slow process, and should be quite a slow process." [@00:44:13.0]
- Against dropping finished work on upstream: "Sometimes we'll develop something, completely internally, for far too long, and not really share it upstream, and then just kind of drop this finished thing, and I think that that is a lack of communication that you should try to avoid." [@00:44:13.0]

**From "Introducing OxCaml" [blog: introducing-oxcaml]:** "Performance engineering requires control, and we want that control to be: Safe." … "We want to provide control without bewildering programmers, or drowning them in endless annotations." … "OxCaml's extensions should be pay-as-you-go. … you shouldn't need to swallow extra complexity when you're not using that power."

**Signatures.** Every feature must have a good interface-level (signature) story. Prefer correct-by-construction to prove-afterwards. Treat user encodings as a signal that the wrong feature was shipped. Evolve slowly and communicate upstream early (design docs and RFCs before code).

---

### 2.5 Andrew Hunter: rating 3.5

**Role.** JS performance engineer. Previously seven years at Google and a tech lead for tcmalloc (S&T blurb).

**Source.** S&T "Performance Engineering on Hard Mode" (2023-11-28): https://signalsandthreads.com/performance-engineering-on-hard-mode/

**Quotes**
- Against "never optimize without profiling" as an absolute: "If you know you are working on systems where this is important you to have a certain amount of self-discipline and … make efficient choices as a matter of defaults in your brain." [@12:28]
- On flame graphs: "suppose you've got 15 or 16 little peaks, none of which is that big … It'd be really easy to dismiss that … but it turns out if you add them all together, that's 40% of your time." [@31:43]. Flame graphs fail "when the really key function is in the middle where everything converges through one particular" node. [@34:11]
- "a really underinvested thing is good, easy to use, obvious, idiot proof APIs" [@26:01]
- "anyone can write fast C++, but it takes a real expert to write fast OCaml" [@39:44]
- "The thing that I think is most problematic for our use of a language like OCaml gets back to mechanical sympathy. … There's a lot of this object contains a pointer to something else where in C++ it would just be splatted right there in the middle." [@42:08]
- Latency in a trading system: "the order sending was happening 200 microseconds after the thinking was, and the reason was it was being put on a low priority queue of work to do later." [@20:10]
- "some of the most important latencies of systems we interact with is the systems that do interact with humans." [@50:43]
- OODA loop: "One of the things I really care about a lot is building systems that let me really quickly evaluate the performance of a system." [@52:25]

**Signatures.** Efficient defaults, then measure. Look for join points, not only peaks. Data layout and pointer chasing come first. Build fast performance-evaluation loops. Treat human-facing latency as a first-class concern.

---

### 2.6 Andrey Mokhov: rating 3.5

**Role.** JS build systems (Dune/Jenga). Academic record: *Build Systems à la Carte* (Mokhov, Mitchell, Peyton Jones; ICFP 2018, JFP 2020 "Theory and Practice", linked from the S&T page), *Selective Applicative Functors*, algebraic-graphs, and GHC's Hadrian build system.

**Sources.** S&T "Build Systems" (2020-09-16): https://signalsandthreads.com/build-systems/ ; blog https://blog.janestreet.com/how-we-accidentally-built-a-better-build-system-for-ocaml-index/ ; JFP paper https://www.cambridge.org/core/journals/journal-of-functional-programming/article/build-systems-a-la-carte-theory-and-practice/097CE52C750E69BD16B78C318754C7A4

**Quotes [S&T build-systems]**
- A build system decomposes into "figuring out the right order in which the tasks should be executed and we call that component a 'scheduler', and the second component just takes care of [executing] a single task." [@16:36]
- "This front-end language is very limited because you want to be able to analyze it and you also want to safeguard users from various errors they can make. … we constrain them so that they don't make those mistakes and we can execute the build descriptions as efficiently as possible." [@29:53]
- "No build system is fully worse than any other build system, because there's always some features that a build system has that nobody else has." [@37:02]

**Signatures.** Separate scheduler from rebuilder. Constrain user-facing DSLs so they stay analysable (deterministic, acyclic). Tie the theory to a production migration (Jenga to Dune).

---

### 2.7 Brian Nigito: rating 3.5

**Role.** JS. Exchange and market-infrastructure veteran.

**Sources.** S&T "Multicast and the Markets" (2020-09-23): https://signalsandthreads.com/multicast-and-the-markets/ ; tech talk "How to Build an Exchange" (blog announcement https://blog.janestreet.com/how-to-build-an-exchange/)

**Quotes [S&T multicast-and-the-markets]**
- "constantly ask yourself, 'yes, but can it be simpler?' We want it to be as simple as possible – no simpler – but as simple as possible. And it really is a mark of you deeply understanding the problem when you can get it down to something that seems trivial to the next person who looks at it." [@36:1 (sic in source; turn sits between 36:11 and 36:57)]
- Relaying a colleague's rule from the Island exchange system: "if any piece of the system is so complicated that you can't rewrite it correctly and perfectly in a weekend, it's wrong." [@33:44]
- "eliminating the copies and the unnecessary work in the system … Trying to make your service times for every packet in every event as reliable and deterministic as possible … The critical path tends to be pretty small when it's all said and done." [@33:44]
- "I think you want to understand the hardware and the machines you're using … deeply." [@30:35]
- On general-purpose reliable multicast: "they have the ability for receivers to slow or stop publication … if you scale up to having thousands of participants, there's sort of somebody somewhere who always has a problem." [@23:37]
- "you do have to develop an intuition for what are the key experiments? … pick your spots when you do your experiments." [@39:48]

**Signatures.** Simplicity is evidence of understanding. Deterministic service times. Slow receivers must never throttle the publisher. Keep the critical path small and mechanically sympathetic.

---

### 2.8 James Somers: rating 3.5

**Role.** JS writer-in-residence ("splitting his time between English and OCaml"). Writes many of the blog's long-form technical posts.

**Sources.** S&T "Writing, Technically" (2021-09-01): https://signalsandthreads.com/writing-technically/ ; blog posts including https://blog.janestreet.com/the-joy-of-expect-tests/, https://blog.janestreet.com/learning-ml-depth-first/, https://blog.janestreet.com/strace-ui-bonsai-term-and-the-tui-renaissance/, https://blog.janestreet.com/wrought-2026/

**Quotes**
- "if there's one piece of advice about how to do this better, it's just never send, never publish, never assume that it's done, a first draft." [S&T writing-technically @00:54:31]
- "the best kind of technical writing is doing this warping of reality into a space where the things that you should care about are made more salient. … maybe the most important thing you can do is just trust your own judgment about what's boring and what's interesting." [@00:59:09]
- "you can't serve all of those people all at once in a single document, and I don't think you should try." [@00:37:09]
- On writing tutorials: "I'm basically a reporter who doesn't know anything and is trying to pretend like they do." [@00:52:45]
- "by relieving you from having to dream up exactly what you want to assert, expect tests make it easier to implicitly assert more." and "I never want to go back to a workflow where my computer isn't finishing my tests for me." [blog: the-joy-of-expect-tests]

**Signatures.** Write for a specific reader. Make the important things salient. Cut ruthlessly. Never ship a first draft. Prefer expect-style tests that show behaviour.

---

### 2.9 Andy Ray and Benjamin Devlin (Hardcaml): rating 3

**Andy Ray** created Hardcaml (OCaml HDL; https://github.com/janestreet/hardcaml).
- S&T "Programmable Hardware" (2020-09-09): https://signalsandthreads.com/programmable-hardware/
- Tech talk "OCaml All The Way Down"
- Blog posts: https://blog.janestreet.com/using-ascii-waveforms-to-test-hardware-designs/, https://blog.janestreet.com/growing-the-hardcaml-toolset-index/, https://blog.janestreet.com/zero-knowledge-fpgas-hardcaml/
- Quotes: "when we build our tests for these systems, we basically test them always at line rate, just back to back packets all the time." [S&T @58:43]. On CPUs falling behind: "it always happens when the market's busiest, which is when you do your best trading." [@57:29]. "When we develop a hardware design we always do so in the presense [sic] of a testbench." and "One of the key features of Hardcaml is that it provides a cycle-accurate simulator." [blog: using-ascii-waveforms...]

**Benjamin Devlin.** Blog: ZPrize MSM/NTT on FPGAs, "Really low latency multipliers and cryptographic puzzles", Advent of FPGA 2025, the ASIC reverse-engineering and protocol-emulator ASIC competitions (https://blog.janestreet.com/author/bdevlin).

**Signatures.** Hardware design as typed software: expect-test waveforms, cycle-accurate simulation, test at worst-case load. Ron's framing on the same episode is that hardware should adopt the "software mindset" (CI, code review, integrated testing) [S&T programmable-hardware @37:01].

---

### 2.10 Doug Patti: rating 3

- S&T "State Machine Replication, and Why You Should Care" (2022-04-20): https://signalsandthreads.com/state-machine-replication-and-why-you-should-care/
- Blog "Getting from tested to battle-tested" (Concord/Aria under Antithesis): https://blog.janestreet.com/getting-from-tested-to-battle-tested/
- Quotes: on imperative wait-then-send code, "you're taking a very subtle piece of state there, the fact that you want to send a second message, and you're hiding it in a way that's not observable anymore." [S&T @00:24:42]. "We actually liked the Concord inverted control style of writing things, so much that we are basically forcing it onto people that want to write things on Aria, because we really just think it's like the right way to write these kinds of programs." [@00:37:31]. "When we do encounter a bug that slipped through, there's always a sense of 'oh, that's a really tricky case, it's no wonder we didn't think to test it'." [blog]
- **Signatures.** Make all state explicit and replayable (a sequenced log plus deterministic state machines). Use inversion of control. Rely on deterministic simulation and exploration beyond chaos testing.

### 2.11 Tristan Hume (alumnus): rating 2.5

- Blog "Magic-trace: Diagnosing tricky performance issues easily with Intel Processor Trace": https://blog.janestreet.com/magic-trace/ ; OSS https://github.com/janestreet/magic-trace
- thume.ca states he implemented magic-trace for JS in 2021, started at Anthropic in 2022, and now runs "a performance optimization team at Anthropic".
- Quote: "The key idea behind quickly making a useful tool was to limit the scope: We'd focus on the circular buffer mode, where it overwrites old data until you snapshot it after something interesting happens." [blog: magic-trace]
- **Signatures.** Capture everything cheaply and snapshot on the event of interest. Require no cooperation from the target. Scope tools down so they ship.

### 2.12 Ty Overby: rating 2.5

- S&T "Building a UI Framework" (2021-10-06): https://signalsandthreads.com/building-a-ui-framework/ ; Bonsai (https://github.com/janestreet/bonsai)
- Quotes: "Bonsai started out basically as a single type definition that encompassed what I saw as the right way to build an Incr_dom component." [@20:21]. "one of the things that I really enjoy about a number of our other libraries that operate monadically in that you don't really need to know what a monad is in order to use them effectively." [@36:17]. The 50–70 lines needed to combine two Incr_dom components [@19:13] motivated Bonsai.
- **Signatures.** UI as an incremental computation graph, not a component tree with hidden state. Hide the abstraction's theory from users. Composition must be cheap.

### 2.13 Max Slater: rating 2.5

- "Oxidizing OCaml" series: https://blog.janestreet.com/oxidizing-ocaml-locality/, https://blog.janestreet.com/oxidizing-ocaml-ownership/, https://blog.janestreet.com/oxidizing-ocaml-parallelism/
- Quotes: "Modes allow the compiler to emit better, lower-allocation code, empower users to write safer APIs, and with the advent of multicore, statically guarantee data race freedom—all in a lightweight way that only affects those in need." "At Jane Street, we often write 'zero-allocation' code, which must never trigger a GC cycle." [blog: oxidizing-ocaml-locality]
- **Signatures.** Modes over lifetimes. Opt-in rigor. Zero-allocation hot paths.

### 2.14 Chris Casinghino: rating 2

Tech talk "Making OCaml Safe for Performance Engineering" (https://www.janestreet.com/tech-talks/); POPL'25 co-author. The talk transcript was not mined, so a persona would need it.

### 2.15 Greta Yorsh: rating 2

- S&T "Compiler Optimization" (2020-09-30): https://signalsandthreads.com/compiler-optimization/
- Quote: "after working a bit and trying to find the right logics that are expressive enough … you find, 'oh, this is very restrictive.' Then you look, but testing is so much better." [@00:07:02]. On a compiler bug she shipped: "even though I made this mistake and released the broken compiler, but it was a learning experience and a positive one" [@00:58:23]

### 2.16 Laurent Mazare (alumnus): rating 2.5

- S&T "Python, OCaml, and Machine Learning" (2020-10-07): https://signalsandthreads.com/python-ocaml-and-machine-learning/ ; blog posts https://blog.janestreet.com/author/lmazare ; ocaml-torch
- Per a Kyutai speaker profile (ai-pulse.eu), he spent nearly 15 years in trading (Goldman Sachs, then Jane Street) and is now Kyutai's CTO and co-founder.

### 2.17 Sylvain Gugger: rating 2.5

S&T "The Uncertain Art of Accelerating ML Models" (2024-10-14): https://signalsandthreads.com/the-uncertain-art-of-accelerating-ml-models/ ; tech talk "Making GPUs Actually Fast: A Deep Dive into Training Performance" (with Corwin de Zahr).

### 2.18 Stephen Weeks: rating 2

Early JS. Created MLton (pre-JS). Blog: type-level OCaml idioms (https://blog.janestreet.com/author/sweeks): "Using types to track defaults", "Ensuring that a function is polymorphic", "A universal type?", "+'a and -'a", "A module type equivalence surprise". The material is idiom-level rather than philosophical, which suits a "type tricks" sub-skill.

### 2.19 John Crepezzi: rating 2

S&T "The Changing Craft of Programming" (2026-10-16): https://signalsandthreads.com/the-changing-craft-of-programming/. Quotes (speaker attribution verified; the "ch." values are chapter-heading timestamps, not turn timestamps): "you have a lot of ability to express constraints in the type system, but you maybe always shouldn't." [ch. 00:18:05]. "there's a bunch of interesting things here about whether you can trust the model to discriminate on the work of another model, even if you can't trust it to produce the thing." [ch. 00:29:27]. "the model is doing a lot of authoring and you're doing a lot of making sure that it did the right thing." [ch. 01:15:14]

### 2.20 Chris Perl: rating 2

S&T "Clock Synchronization" (2020-10-14): https://signalsandthreads.com/clock-synchronization/ ; blog on Linux internals (automount, TCP state, process environment, rsync timestamps).

### 2.21 David Wu: rating 2

KataGo author. Paper "Accelerating Self-Play Learning in Go" (arXiv 1902.10565, Jane Street affiliation). Wikipedia says the first KataGo run used Jane Street compute. Blog: https://blog.janestreet.com/deep-learning-the-hardest-go-problem-in-the-world/

---

## 3. Signals and Threads: complete episode list

Dates are from the Simplecast RSS feed (https://feeds.simplecast.com/L9810DOa). JS? marks whether the guest is Jane Street staff according to the episode blurb.

| Date | Title | Guest | JS? | Topic | URL |
|---|---|---|---|---|---|
| 2020-08-24 | Introducing Signals & Threads | Ron Minsky | yes | Trailer | https://signalsandthreads.com/introducing-signals-&-threads/ |
| 2020-09-09 | Programmable Hardware | Andy Ray | yes | FPGAs, Hardcaml, HLS | https://signalsandthreads.com/programmable-hardware/ |
| 2020-09-16 | Build Systems | Andrey Mokhov | yes | Build-system theory, Jenga/Dune, Hadrian | https://signalsandthreads.com/build-systems/ |
| 2020-09-23 | Multicast and the Markets | Brian Nigito | yes | Exchange architecture, UDP multicast, mechanical sympathy | https://signalsandthreads.com/multicast-and-the-markets/ |
| 2020-09-30 | Compiler Optimization | Greta Yorsh | yes | Backend optimization, FDO, verification vs testing | https://signalsandthreads.com/compiler-optimization/ |
| 2020-10-07 | Python, OCaml, and Machine Learning | Laurent Mazare | yes (then) | Python↔OCaml, notebooks, ML tooling | https://signalsandthreads.com/python-ocaml-and-machine-learning/ |
| 2020-10-14 | Clock Synchronization | Chris Perl | yes | NTP/PTP, MiFID II compliance, chrony | https://signalsandthreads.com/clock-synchronization/ |
| 2020-10-21 | Language Design | Leo White | yes | PL design, modularity, GADTs to dependent types, upstreaming | https://signalsandthreads.com/language-design/ |
| 2020-10-28 | Building a Functional Email Server | Dominick LoBraico | yes | Mail infra in OCaml, config as code | https://signalsandthreads.com/building-a-functional-email-server/ |
| 2020-11-06 | An Inside Look at Jane Street's Tech Internship | Jeanne Van Briesen, Matt Else, Grace Zhang | yes | Intern projects | https://signalsandthreads.com/an-inside-look-at-jane-streets-tech-internship/ |
| 2021-08-24 | More Signals & Threads Coming Soon | Ron Minsky | yes | Season 2 trailer | https://signalsandthreads.com/more-signals-&-threads-coming-soon/ |
| 2021-09-01 | Writing, Technically | James Somers | yes | Technical writing, docs, editing | https://signalsandthreads.com/writing-technically/ |
| 2021-10-06 | Building a UI Framework | Ty Overby | yes | Bonsai, incremental UIs | https://signalsandthreads.com/building-a-ui-framework/ |
| 2021-11-03 | What Is an Operating System? | Anil Madhavapeddy | no (Cambridge; RWO co-author) | Unikernels/MirageOS, OCaml 5 | https://signalsandthreads.com/what-is-an-operating-system/ |
| 2022-01-05 | Memory Management | Stephen Dolan | yes | GC vs RC, prefetching, local allocation, unboxed types | https://signalsandthreads.com/memory-management/ |
| 2022-04-20 | State Machine Replication, and Why You Should Care | Doug Patti | yes | Concord/Aria, SMR | https://signalsandthreads.com/state-machine-replication-and-why-you-should-care/ |
| 2022-09-12 | Swapping the Engine Out of a Moving Race Car | Ella Ehrlich | yes | Modernizing Gord (trade data) without downtime | https://signalsandthreads.com/swapping-the-engine-out-of-a-moving-race-car/ |
| 2023-05-18 | The Future of Programming | Richard Eisenberg | yes | Dependent types, Haskell vs OCaml, AI and specs | https://signalsandthreads.com/future-of-programming/ |
| 2023-08-15 | A Poet's Guide to Product Management | Peter Bogart-Johnson | yes | PM practice at JS | https://signalsandthreads.com/a-poets-guide-to-product-management/ |
| 2023-11-28 | Performance Engineering on Hard Mode | Andrew Hunter | yes | Low-latency perf, profiling, OCaml perf | https://signalsandthreads.com/performance-engineering-on-hard-mode/ |
| 2024-07-12 | From the Lab to the Trading Floor | Erin Murphy | yes | UX design for expert users (ex-JPL) | https://signalsandthreads.com/from-the-lab-to-the-trading-floor/ |
| 2024-10-07 | Solving Puzzles in Production | Liora Friedberg | yes | Production engineering, incident practice | https://signalsandthreads.com/solving-puzzles-in-production/ |
| 2024-10-14 | The Uncertain Art of Accelerating ML Models | Sylvain Gugger | yes | GPU training performance, PyTorch pitfalls | https://signalsandthreads.com/the-uncertain-art-of-accelerating-ml-models/ |
| 2025-03-12 | Finding Signal in the Noise | In Young Cho | yes | ML research in trading | https://signalsandthreads.com/finding-signal-in-the-noise/ |
| 2025-05-28 | Building Tools for Traders | Ian Henry | yes | Options-desk tools, Bonsai vs React, expect tests | https://signalsandthreads.com/building-tools-for-traders/ |
| 2025-07-25 | The Thermodynamics of Trading | Daniel Pontecorvo | yes | Datacenter and office physical engineering | https://signalsandthreads.com/the-thermodynamics-of-trading/ |
| 2025-09-03 | Why ML Needs a New Programming Language | Chris Lattner | no (Modular) | Mojo, GPU kernels | https://signalsandthreads.com/why-ml-needs-a-new-programming-language/ |
| 2026-03-17 | Why Testing Is Hard and How to Fix It | Will Wilson | no (Antithesis) | Deterministic simulation testing | https://signalsandthreads.com/why-testing-is-hard-and-how-to-fix-it/ |
| 2026-06-01 | The Network as a Program | Nate Foster | visiting researcher (EPFL) | SDN, NetKAT/P4, formal methods for networks | https://signalsandthreads.com/the-network-as-a-program/ |
| 2026-06-24 | Building a Data Warehouse from Scratch | Jacob Baskin | yes | Superstore, a distributed columnar DB | https://signalsandthreads.com/building-a-data-warehouse-from-scratch/ |
| 2026-09-02 | Wrestling the World into Rows | Eric Mannes | yes | Alternative-data engineering, point-in-time data | https://signalsandthreads.com/wrestling-the-world-into-rows/ |
| 2026-09-23 | Learning Goals and the Goals of Learning: Teaching in the Age of AI | Aaron Bauer | yes | Developer education, LLM-era curriculum | https://signalsandthreads.com/learning-goals-and-the-goals-of-learning-teaching-in-the-age-of-ai/ |
| 2026-10-16 | The Changing Craft of Programming | John Crepezzi | yes | AI dev tooling at JS | https://signalsandthreads.com/the-changing-craft-of-programming/ |

Ron Minsky is the interviewer on every episode, so the full transcript set is effectively his largest single corpus.

---

## 4. Jane Street tech blog: most principle-dense posts

Grouped by theme. Author pages are at https://blog.janestreet.com/author/<id>.

**Types, API design, OCaml style**
- Effective ML; Effective ML Revisited (Yaron Minsky): https://blog.janestreet.com/effective-ml/ , https://blog.janestreet.com/effective-ml-revisited/
- What do Haskellers have against exhaustiveness? (Minsky): https://blog.janestreet.com/what-do-haskellers-have-against-exhaustiveness/
- Core Principles: uniformity of interface (Minsky): https://blog.janestreet.com/core-principles-uniformity-of-interface/
- The perils of polymorphic compare (Minsky): https://blog.janestreet.com/the-perils-of-polymorphic-compare/
- Making something out of nothing (or, why None is better than NaN and NULL) (Minsky): https://blog.janestreet.com/making-something-out-of-nothing-or-why-none-is-better-than-nan-and-null/
- HOWTO: Static access control using phantom types (Minsky): https://blog.janestreet.com/howto-static-access-control-using-phantom-types/
- OCaml, the ultimate refactoring tool (Minsky): https://blog.janestreet.com/ocaml-the-ultimate-refactoring-tool/
- The ML sweet spot (Minsky): https://blog.janestreet.com/the-ml-sweet-spot/
- How to fail – introducing Or_error.t (David House): https://blog.janestreet.com/how-to-fail-introducing-or-error-dot-t/
- Using types to track defaults (Stephen Weeks): https://blog.janestreet.com/using-types-to-track-defaults/

**Language evolution and performance (OxCaml)**
- Introducing OxCaml (Leo White): https://blog.janestreet.com/introducing-oxcaml/
- Oxidizing OCaml: Locality / Ownership / Data Race Freedom (Max Slater): https://blog.janestreet.com/oxidizing-ocaml-locality/ , https://blog.janestreet.com/oxidizing-ocaml-ownership/ , https://blog.janestreet.com/oxidizing-ocaml-parallelism/
- Memory allocator showdown (Stephen Dolan): https://blog.janestreet.com/memory-allocator-showdown/
- A better inliner for OCaml, and why it matters (Minsky, on flambda): https://blog.janestreet.com/flambda/
- Why GADTs matter for performance (Minsky): https://blog.janestreet.com/why-gadts-matter-for-performance/
- Using OxCaml to implement type-safe reference counting between OCaml and Python (Nicolas Trangez): https://blog.janestreet.com/oxcaml-typesafe-reference-counting-python/

**Testing and correctness**
- Testing with expectations (Minsky): https://blog.janestreet.com/testing-with-expectations/
- What if writing tests was a joyful experience? (James Somers): https://blog.janestreet.com/the-joy-of-expect-tests/
- Getting from tested to battle-tested (Doug Patti): https://blog.janestreet.com/getting-from-tested-to-battle-tested/
- Quickcheck for Core (Carl Eastlund): https://blog.janestreet.com/quickcheck-for-core/
- Proofs (and Refutations) using Z3 (Xavier Clerc): https://blog.janestreet.com/proofs-and-refutations-using-z3/
- Formal methods and the future of programming (Minsky, 2026): https://blog.janestreet.com/formal-methods-at-jane-street-index/
- Using ASCII waveforms to test hardware designs (Andy Ray): https://blog.janestreet.com/using-ascii-waveforms-to-test-hardware-designs/

**Code review, naming, process**
- Code review that isn't boring; Scrutinize your code in style; Ironing out your development style; Designing a code-review tool, parts 1–2 (Minsky)
- Notes on Naming (Minsky): https://blog.janestreet.com/notes-on-naming/
- Making "never break the build" scale (Minsky): https://blog.janestreet.com/making-never-break-the-build-scale/
- Caveat Configurator (Minsky's post on Dominick LoBraico's talk): https://blog.janestreet.com/caveat-configurator-how-to-replace-configs-with-code-and-why-you-might-not-want-to/

**Performance and observability**
- Magic-trace (Tristan Hume): https://blog.janestreet.com/magic-trace/
- Finding memory leaks with Memtrace (Luke Maurer): https://blog.janestreet.com/finding-memory-leaks-with-memtrace/
- Core_bench: better micro-benchmarks through linear regression (Roshan James): https://blog.janestreet.com/core_bench-micro-benchmarking-for-ocaml/
- This is not the performance you were looking for (Andy Myers): https://blog.janestreet.com/this-is-not-the-performance-you-were-looking-for-the-tricks-systems-play-on-us/
- A Higgs-bugson in the Linux Kernel (Nikhil Jha): https://blog.janestreet.com/a-higgs-bugson-in-the-linux-kernel/

**Incremental and UI**
- Introducing Incremental; Seven Implementations of Incremental; Self Adjusting DOM (Minsky)

**Build, tooling, education, AI era**
- How we accidentally built a better build system for OCaml (Andrey Mokhov): https://blog.janestreet.com/how-we-accidentally-built-a-better-build-system-for-ocaml-index/
- Goodbye Core_kernel; ppx_core (Jeremie Dimino)
- Developer education at Jane Street (Aaron Bauer): https://blog.janestreet.com/developer-education-at-jane-street-index/
- Our software engineering interviews are changing (a little) (Matthew Saffer, 2026-11-02): https://blog.janestreet.com/software-engineering-interviews-are-changing-a-little/
- I design with Claude more than Figma now (Edwin Morris): https://blog.janestreet.com/i-design-with-claude-code-more-than-figma-now-index/

---

## 5. Jane Street-staff tech talks (from janestreet.com/tech-talks, pages 1–7)

Video and transcript pages live under https://www.janestreet.com/tech-talks/. Transcripts were not mined in this pass.

- Yaron Minsky: Jane and the Compiler; The Saga of Multicore OCaml; Seven Implementations of Incremental
- Stephen Dolan: Unboxed Types for OCaml
- Leo White: Effective Programming: Adding an Effect System to OCaml
- Chris Casinghino: Making OCaml Safe for Performance Engineering
- Andy Ray: OCaml All The Way Down
- Brian Nigito: How to Build an Exchange
- Dominick LoBraico: Caveat Configurator
- Ian Henry: How Jane Street Does Code Review
- Sebastian Funk: Safe at Any Speed: Building a Performant, Safe, Maintainable Packet Processor
- Nathan Linger: A Language-Oriented System Design
- Cristina Rosu: Introduction to Incr_dom
- Tudor Brindus: System Jitter and Where to Find It
- Corwin de Zahr: Hacking OCaml; with Sylvain Gugger: Making GPUs Actually Fast
- Mark Doss: Production Engineering When Trading Billions of Dollars a Day

Several talks in the series are by outside speakers who already have skills in this library: Bryan Cantrill, Jon Gjengset, Raph Levien.

---

## 6. Suggested skill decomposition

1. **minsky-effective-ml**: the most material by far. Core: the nine Effective ML items, exhaustiveness-as-error, the readability and review culture, expect tests, naming, pay-as-you-go types. 2026 extension: types and formal methods as feedback for agents.
2. **jane-street-oxcaml-language-design**: a composite of Leo White, Richard Eisenberg and Stephen Dolan. Core: math plus aesthetics, the interface-first feature test, opt-in safe control, restructuring so the problem never arises, specs as communication. No single one of the three has enough first-person material alone. Together they are coherent and well sourced.
3. **jane-street-low-latency-systems**: a composite of Nigito, Hunter and Patti. Core: "can it be simpler?", the weekend-rewrite rule, deterministic service time, mechanical sympathy, efficient defaults, join-point profiling, explicit replayable state (SMR).
4. **somers-technical-writing**: a narrower skill for documentation and test-as-documentation.
5. Optional: **hardcaml-hardware-as-software** (Andy Ray and Ben Devlin) and **mokhov-build-systems**.

## Sources

- Signals and Threads site and embedded transcript index: https://signalsandthreads.com/
- Signals and Threads RSS: https://feeds.simplecast.com/L9810DOa
- Jane Street blog: https://blog.janestreet.com/ ; authors index https://blog.janestreet.com/authors ; archive https://blog.janestreet.com/archive
- Jane Street tech talks: https://www.janestreet.com/tech-talks/ (pages 1–7)
- Effective ML: https://blog.janestreet.com/effective-ml/ ; https://blog.janestreet.com/effective-ml-revisited/
- Formal methods post: https://blog.janestreet.com/formal-methods-at-jane-street-index/
- OCaml for the Masses (ACM Queue): https://queue.acm.org/detail.cfm?id=2038036 . Copy referenced in search results: https://www.di.ubi.pt/~desousa/PF/ocaml-for-the-masses.pdf (returned HTML, not a PDF, so not verified)
- Real World OCaml: https://dev.realworldocaml.org
- ICFP 2024 "Oxidizing OCaml with Modal Memory Management": https://icfp24.sigplan.org/details/icfp-2024-papers/19/Oxidizing-OCaml-with-Modal-Memory-Management ; https://www.research.ed.ac.uk/en/publications/oxidizing-ocaml-with-modal-memory-management/
- POPL 2025 "Data Race Freedom à la Mode": https://popl25.sigplan.org/details/POPL-2025-popl-research-papers/23/Data-Race-Freedom-la-Mode ; https://iris-project.org/pdfs/2025-popl-drfcaml.pdf
- JS visiting researcher (type systems) posting naming Eisenberg: https://www.janestreet.com/join-jane-street/programs-and-events/visiting-researcher-program-type-systems/
- Stephen Dolan, *Algebraic Subtyping*: https://www.cs.tufts.edu/~nr/cs257/archive/stephen-dolan/thesis.pdf ; award note https://www.cst.cam.ac.uk/node/8382 ; First-Class Subtypes https://arxiv.org/abs/1905.06546
- jq authorship: https://github.com/jqlang/jq (AUTHORS file)
- Build Systems à la Carte (JFP): https://www.cambridge.org/core/journals/journal-of-functional-programming/article/build-systems-a-la-carte-theory-and-practice/097CE52C750E69BD16B78C318754C7A4
- Hardcaml: https://github.com/janestreet/hardcaml
- Tristan Hume: https://thume.ca/ ; magic-trace https://github.com/janestreet/magic-trace
- KataGo paper: https://arxiv.org/abs/1902.10565 ; https://en.wikipedia.org/wiki/KataGo
- Laurent Mazare profile: https://www.ai-pulse.eu/speakers/laurent-mazare ; Cambridge talk listing https://webapp.prod.talks.gcp.uis.cam.ac.uk/talk/index/161686/
