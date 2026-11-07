# Answers to the practice questions in *Probability & Markets*

These are the questions the guide poses without answering. They are for checking work, not for
handing over: in coaching mode, let the person attempt each one first (see SKILL.md, Coaching).

Every value in the table is recomputed by exact enumeration in
`scripts/tests/test_practice_answers.py`, which fails if a row and the brute-force answer disagree.
The `id` column is what the test keys on.

| id | Question (paraphrased) | Exact | ≈ | The idea it teaches |
|---|---|---|---|---|
| sum10 | P[two d6 sum to 10] | 1/12 | 0.0833 | [4,6], [5,5], [6,4]: the doubled pair has no mirror image |
| face_repl | P[two face cards], with replacement | 9/169 | 0.0533 | independence: (12/52)² |
| clubs_norepl | P[two clubs], without replacement | 1/17 | 0.0588 | the second draw is conditional: 13/52 · 12/51 |
| odd2 | P[product of two d6 is odd] | 1/4 | 0.25 | odd only if every factor is odd |
| odd3 | P[product of three d6 is odd] | 1/8 | 0.125 | same, one more factor |
| weighted6 | E[d6] when 6 comes up half the time | 9/2 | 4.5 | the other five faces share the remaining half: 1/10 each |
| six_to_12 | E[d6] with the 6 replaced by a 12 | 9/2 | 4.5 | EV moves by (12 − 6)/6 = 1 |
| prime_ev | E[d6 \| prime] | 10/3 | 3.3333 | condition, then average over {2, 3, 5} |
| prime_le3 | P[d6 ≤ 3 \| prime] | 2/3 | 0.6667 | two of the three primes |
| coins | P[exactly 2 heads \| at least 1 tail], 3 coins | 3/7 | 0.4286 | worked in the guide; included as a check on the test |
| ex2 | E[X·Y] ≠ E[X]·E[Y]: take Y = X = d6 | 91/6 vs 49/4 | 15.17 vs 12.25 | dependence breaks the product rule; linearity of sums survives it |
| three_heads | expected flips to see 3 heads in a row | 14 | 14 | recursion: E[n] = 2E[n−1] + 2, so 2, 6, 14 |
| d20 | EV of a d20 contract | 21/2 | 10.5 | midpoint of a symmetric distribution |
| max3d6 | EV of the max of 3d6 | 119/24 | 4.9583 | E[max] = Σₖ P[max ≥ k] = Σₖ (1 − ((k−1)/6)³) |
| reroll_holder | d6 with one reroll, the buyer chooses | 17/4 | 4.25 | reroll a 1, 2 or 3; keep 4, 5, 6 |
| reroll_writer | d6 with one reroll, the seller chooses | 11/4 | 2.75 | the seller rerolls a 4, 5 or 6: the option is worth 1.5 to whoever holds it |
| million | EV of 1,000,000 × d6 | 3500000 | 3500000 | same EV, but the worst case (−$2.5M if bought at EV) now matters against capital: quote smaller or wider |

Not computable here: **B+R and B·R** are dependent (B+R = 2 forces B·R = 1). **The NYC taxi
interval** and **the temperature in an hour** have no fixed answer: they are calibration
exercises, so score them by whether the interval contained the checked value, and track the hit
rate over many questions against the confidence you claimed.
