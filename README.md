# jane-skills

Agent skills and personas built from Jane Street's public technical record:
talks, papers, open source, and the Signals and Threads podcast.

- `research/` — sourced dossiers (people, GitHub, papers/talks, public business data)
- `skills/<name>/SKILL.md` — one skill per directory, Claude Code skill format

Personas encode a person's *published* engineering philosophy. Every principle
traces to a public source; nothing private is collected.

## Quote gate

Every quotation in a persona must appear verbatim in its public source.

```sh
tools/fetch_corpus.sh /tmp/corpus $(cat skills/minsky/sources.txt)
python3 -I tools/verify_quotes.py /tmp/corpus skills/minsky/SKILL.md   # exit 0 = every quote found
```

`fetch_corpus.sh` always includes the Signals and Threads homepage, which embeds every episode transcript.
