# jane-skills

Agent skills and personas built from Jane Street's public technical record:
talks, papers, open source, and the Signals and Threads podcast.

- `research/` — sourced dossiers (people, GitHub, papers/talks, public business data)
- `skills/<name>/SKILL.md` — one skill per directory, Claude Code skill format

Personas encode a person's *published* engineering philosophy. Every principle
traces to a public source; nothing private is collected.

## Skills

| Skill | Kind | Grounding | Gate |
|---|---|---|---|
| `skills/minsky` (`minsky-effective-ml`) | persona | ~20 blog posts, ACM Queue 2011, 8 Signals and Threads episodes | quote gate: 60/60 verbatim |
| `skills/oxcaml-team` (`oxcaml-language-design`) | composite persona (White, Dolan, Eisenberg) | 3 Signals and Threads episodes, 6 blog posts, OxCaml docs, ICFP'24/POPL'25 | quote gate: 42/42 verbatim, speaker-checked |
| `skills/low-latency` (`low-latency-trading-systems`) | composite persona (Nigito, Hunter, Patti; Funk, Brindus, Perl) | 4 Signals and Threads episodes, 3 tech-talk transcripts, 1 blog post | quote gate: 39/39 verbatim, speaker-checked |
| `skills/calibrated-estimation` (`calibrated-estimation`) | practice | *Probability & Markets* (Confidence Intervals), official Estimathon rules and formula (estimathon.com) | quote gate: 10/10 verbatim; `scripts/tests` (18): official scorer, closed-form expected score vs 40k simulated contests with a ceiling-rule canary, planner vs brute force, exact-binomial calibration verdicts |
| `skills/memtrace` (`memtrace-and-magic-trace`) | practice | Memtrace blog + README, magic-trace blog, System Jitter talk, OCaml 5.4 `gc.mli` | quote gate: 20/20 verbatim; `scripts/gate.sh`: compiled analyzer + 3 expect tests under real Memprof sampling (20/20 clean runs), snippets = compiled code, 3 canaries caught; documents the memtrace 0.2.3 hang on OCaml ≥ 5.3 |
| `skills/public-record-analyst` (`trading-firm-public-record`) | practice | `research/business_public_data.md`, EDGAR 13F/X-17A-5, FINRA BrokerCheck, SEBI orders | `scripts/tests` (11): 13F unit boundary, kind split, CUSIP keying, cover-page reconciliation with a dropped-row canary; live check reconciles all 14,718 rows of the real Q2 2026 filing |
| `skills/hardcaml` (`hardcaml-design`) | practice | Jane Street's MIT agent prompts (vendored), template project, opam repos | `scripts/gate.sh`: linter tests, `examples/` compiled and run on Hardcaml v0.18 preview, SKILL.md snippets = compiled code (OxCaml-only templates reported as skipped), enable-removal canary caught |
| `skills/market-making` (`market-making-reasoning`) | practice | *Probability & Markets* guide, Figgie rules, Doss tech talk, 2 Signals and Threads episodes | quote gate: 41/41 verbatim, speaker-checked; `scripts/tests` (exact Figgie posterior vs 400k simulated deals; answer key vs brute-force enumeration) |
| `skills/expect-tests` (`expect-test-driven-development`) | practice | 6 blog posts (Minsky, Somers, Eastlund, Patti, Ray), ppx_expect README, Signals and Threads Ep. 23 | quote gate: 30/30 verbatim, speaker-checked; `scripts/gate.sh`: compiled examples, SKILL.md snippets = compiled code, 3 canary mutations caught |

## Quote gate

Every quotation in a persona must appear verbatim in its public source.

```sh
tools/fetch_corpus.sh /tmp/corpus $(cat skills/minsky/sources.txt)
python3 -I tools/verify_quotes.py /tmp/corpus skills/minsky/SKILL.md   # exit 0 = every quote found
```

`fetch_corpus.sh` always includes the Signals and Threads homepage, which embeds every episode transcript.
