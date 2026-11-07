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
| `skills/hardcaml` (`hardcaml-design`) | practice | Jane Street's MIT agent prompts (vendored), template project, opam repos | `scripts/tests/test_lint.py`; linter clean on template + own examples |
| `skills/market-making` (`market-making-reasoning`) | practice | *Probability & Markets* guide, Figgie rules, Doss tech talk, 2 Signals and Threads episodes | quote gate: 41/41 verbatim, speaker-checked; `scripts/tests` (exact Figgie posterior vs 400k simulated deals; answer key vs brute-force enumeration) |

## Quote gate

Every quotation in a persona must appear verbatim in its public source.

```sh
tools/fetch_corpus.sh /tmp/corpus $(cat skills/minsky/sources.txt)
python3 -I tools/verify_quotes.py /tmp/corpus skills/minsky/SKILL.md   # exit 0 = every quote found
```

`fetch_corpus.sh` always includes the Signals and Threads homepage, which embeds every episode transcript.
