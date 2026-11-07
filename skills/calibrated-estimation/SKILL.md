---
name: calibrated-estimation
description: Make and score interval estimates the way Jane Street teaches it, using the confidence-interval section of its Probability & Markets guide and the official Estimathon rules. Use when estimating an unknown quantity with no references (Fermi problems, back-of-envelope sizing, interview estimation questions), giving a confidence interval, playing, coaching or hosting an Estimathon, or checking whether your own stated confidence matches your hit rate. Ships a tool that scores by the official formula, plans the expected-score-optimal intervals, and tests calibration with an exact binomial test.
---

# Calibrated Estimation

## Overview

Jane Street teaches interval estimation in two places:

- **The "Confidence Intervals" section** of its trading-interview guide, *Probability & Markets*.
- **The Estimathon.** This is "a team-based contest that combines trivia, game theory, and mathematical thinking". "Since debuting the Estimathon in 2013, Jane Street has run hundreds of Estimathon contests." The rules are published at estimathon.com.

This skill combines those sources with a tool, `scripts/estimathon.py`, which has three subcommands:

| Subcommand | What it does |
|---|---|
| `score` | Applies the official scoring formula |
| `plan` | Turns your beliefs into the intervals that minimise expected score |
| `calibration` | Checks your stated confidence against your actual hit rate |

What comes from where:

- **Jane Street:** the rules, the guide's advice and the quotations.
- **This skill *(derived)*:** the decomposition method, the expected-score analysis and every strategy rule. The derived strategy rests on the tool's closed form, which the tests check against simulated contests.

## Core Philosophy

**People are overconfident, and the fix is measurement, not a vague humility.** From the guide:
- "Often times, people tend to be overconfident. That is, if they gave a bunch of 95% confidence intervals, less than 95% of them would contain the actual outcome."
- "It's important to try to correct for this, but also don't go overboard!"

The guide's remedy is to practise: "If you want to practice, you can try quizzing yourself on easily verified facts." Its worked exercise asks for a 95% interval for the number of New York City taxis, and then says to check your interval after you build it.

**An answer is a range, and its width is a decision.** A confidence interval is "any continuous range of numbers that contains some predefined percentage of the possible outcomes". The Estimathon prices that decision explicitly:
- a wide interval costs you its width;
- a miss doubles your score.

**Sanity beats arithmetic.** The guide's interview advice says numeracy matters for "deciding if your answer is reasonable (e.g. check the order of magnitude!)".

## Method *(derived)*

1. **Decompose.** Build the quantity from factors you know better than the whole. For example, NYC taxis = trips per day ÷ trips per cab per day. Estimate each factor as a central value plus a factor of uncertainty, such as "×/÷ 2".
2. **Work in logs.** Multiply the central values. For independent factors, the log-uncertainties combine in quadrature. Two factors that are each "×/÷ 3" give about ×/÷ 4.7, not ×/÷ 9: exp(√2 · ln 3) ≈ 4.7.
3. **State the interval in multiplicative terms.** Use a log-centred interval, [x/f, x·f]. Quantities that span orders of magnitude are roughly lognormal, and the Estimathon scores a max/min ratio, which is itself multiplicative.
4. **Check the order of magnitude** against one independent reference point before committing.
5. **Record the claim.** Write down the confidence, the interval and, later, the answer. Calibration you never measure is just a feeling.

## The Estimathon

### Official rules (estimathon.com)

- **Format.** "Your team will have 30 minutes to work on 13 estimation problems." Each answer is a positive number. You submit intervals that may not contain zero or negative numbers. No internet, calculators or references are allowed.
- **Scoring.** An interval is good if it contains the correct answer. The formula, published on the site as an image (transcribed here; read 2026-11-07), is

  **score = (10 + Σ over good intervals of ⌊max / min⌋) · 2^(13 − number of good intervals)**

  The rules page explains it as: "for every problem you get wrong (or leave blank), your score doubles." Lowest score wins.
- **Slips.** "Every team can submit up to 18 total intervals". Only the last submission for a problem counts. The host grades in real time, but warns that feedback near the end may be slow.
- **Notation.** Scientific notation is allowed, but nothing more complicated.

Note that the formula uses a **floor**. Some third-party write-ups give it as a ceiling, and they are wrong.

### Strategy *(derived from the formula, verified by `plan`)*

Under the tool's model, the expected score has an exact closed form. The model assumes lognormal beliefs, given as your 90% interval, and independent questions:

  E = 2^13 · Π (1 − pᵢ/2) · (10 + Σ kᵢ · (pᵢ/2) / (1 − pᵢ/2))

Here kᵢ = ⌊max/min⌋ and pᵢ is your probability of hitting question i. Four rules follow:

- **Use the floor.** A ratio of 1.99 scores exactly like a ratio of 1, so every interval should sit just below an integer ratio. Aim for max/min just under k+1 rather than at k. `plan` prints intervals that do this.
- **Never leave a problem blank.** A blank is a guaranteed miss. Under the closed form, adding an interval with floor k lowers the expected score exactly when k < 10 + S, where S = Σ kⱼ·(pⱼ/2)/(1 − pⱼ/2) over the other problems. A narrow interval (k = 1) therefore always beats a blank, but an enormous one can be worse than leaving the problem empty.
- **Don't buy certainty on hopeless questions.** Suppose your honest 90% belief spans a factor of 1,000:

  | max/min below | P(hit) |
  |---|---|
  | 2 | 0.13 |
  | 16 | 0.49 |
  | 1,000 | 0.90 |

  A ratio of 1,000 adds about 1,000 to the sum whenever it hits. A miss only doubles the score, which for a typical 13-question set is a few hundred. So `plan` settles near a ratio of 15 and about a coin flip. Spend width where it buys a lot of probability, which means the questions you understand moderately well.
- **Spend the 5 spare slips on feedback.** Submit early, because the host grades in real time, and resubmit the misses with wider intervals. Only the last slip counts, so a revision never hurts. Leave margin before the end, when grading slows.

```sh
python3 -I scripts/estimathon.py plan beliefs.json      # [{"lo90": 8000, "hi90": 20000}, ...] one per problem
python3 -I scripts/estimathon.py score sheet.json       # [{"min": .., "max": .., "answer": ..} | {"answer": ..}]
```

## Measuring Your Calibration

```sh
python3 -I scripts/estimathon.py calibration log.csv    # rows: confidence,lo,hi,answer
```

The tool groups claims by stated confidence, then reports the hit rate with a Wilson 95% interval. It gives a verdict only when an **exact binomial test** rejects the stated level at 5%. It does not base the verdict on the Wilson interval. With 1 hit in 2 at a stated 95%, Wilson's upper bound is 0.91, which would convict you, yet an honest 95% estimator misses at least once in two tries nearly 10% of the time. The test suite pins exactly this case.

You also need enough questions before a verdict means anything. Here is the chance of detecting a true hit rate of 80% when you claim 95%, with a two-sided test at 5%:

| Questions per bucket | 10 | 20 | 30 | 50 | 100 |
|---|---|---|---|---|---|
| Power | 0.32 | 0.59 | 0.74 | 0.90 | 0.99 |

Telling 90% from a true 80% needs about 100 questions (power 0.81). So score yourself in batches of 50 or more per confidence level before you change your behaviour, which is the guide's "don't go overboard" in numbers.

## Rules

**Always**
- Give an interval and a confidence level, not a point estimate.
- Decompose into factors and combine their uncertainties in log space.
- Check the order of magnitude against something independent.
- Log claims and outcomes, and score them in batches large enough to mean something.
- In an Estimathon, set each max/min just below an integer and answer every problem.

**Never**
- Call yourself (or someone else) overconfident on a handful of misses.
- Widen every interval by reflex. Width costs points in the Estimathon and credibility everywhere else.
- Use a calculator, phone or reference during an Estimathon (official rule).

**Prefer**
- Multiplicative (×/÷) intervals for anything spanning orders of magnitude.
- A coin-flip interval on a hopeless question over a huge "safe" one.
- Early submissions and real-time feedback over one final batch.

## Checklist

1. What exactly is being estimated (units, date, scope)?
2. Which factors did I multiply, and what is the ×/÷ uncertainty on each?
3. Is the combined interval log-centred, with the stated confidence written down?
4. Did I check the order of magnitude against one independent anchor?
5. In an Estimathon: are all 13 answered, does each max/min sit just below an integer, and are slips left for resubmissions?
6. Over my last 50+ claims at this confidence level, what was the hit rate?

## Verification

`python3 -I -m unittest discover -s skills/calibrated-estimation/scripts/tests` runs 18 tests:

- The official formula is checked on hand-built sheets, including the floor.
- The closed-form expected score matches 40,000 simulated contests within 4 standard errors, and a canary using a ceiling rule falls outside that band.
- The coordinate-descent planner matches brute force on a 3-question instance.
- The blank-versus-interval condition (k < 10 + S) holds on random instances, both ways round.
- The Wilson interval matches a known value.
- The exact-test verdicts are checked, including the small-sample case above.

## Sources

- **Probability & Markets** (Jane Street, rev. Aug 2025), sections Confidence Intervals and Interview Thoughts. https://www.janestreet.com/static/pdfs/trading-interview.pdf
- **Estimathon: How to Play**, plus the rules PDF and the formula image. https://estimathon.com/how-to-play, https://estimathon.com/static/estimathon-rules.pdf
- **Estimathon: About.** https://estimathon.com/about
- **Trading Interviews.** https://www.janestreet.com/trading-interviews/

Quote gate: `tools/fetch_corpus.sh <dir> $(cat skills/calibrated-estimation/sources.txt)` then `python3 -I tools/verify_quotes.py <dir> skills/calibrated-estimation/SKILL.md`.
