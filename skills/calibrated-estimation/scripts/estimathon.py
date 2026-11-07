"""Estimathon scoring, interval planning and calibration checks.

usage:
  python3 -I estimathon.py score <file.json>         [{"min":..,"max":..,"answer":..} | {"answer":..}, ...]
  python3 -I estimathon.py plan  <file.json>         [{"lo90":..,"hi90":..}, ...]   your 90% beliefs
  python3 -I estimathon.py calibration <file.csv>    rows: confidence,lo,hi,answer   (confidence in (0,1))

score: the official rule (estimathon.com/how-to-play, formula image read 2026-11-07):
    (10 + sum over good intervals of floor(max/min)) * 2^(13 - number of good intervals)
  A row without min/max is a blank. "Good" means min <= answer <= max.

plan (derived, not Jane Street's): treats each belief as lognormal with the given 90% interval and
the questions as independent. Then the expected score has a closed form,
    E = 2^N * prod_j (1 - p_j/2) * (10 + sum_i k_i * (p_i/2) / (1 - p_i/2))
  where k_i = floor(max/min) and p_i = P(answer in interval). Because of the floor, the best
  interval for a given k is as wide as possible while max/min stays below k+1. The planner picks
  each k_i (0 = leave blank) by coordinate descent on E, and prints log-centred intervals.

calibration: groups claims by stated confidence and reports the hit rate with a Wilson 95% interval.
  The verdict comes from an exact two-sided binomial test at 5%, not from the Wilson interval, which
  is not conservative for small n: 1 hit in 2 at a stated 95% is not evidence of overconfidence.
"""

import csv
import json
import math
import sys

N_PROBLEMS = 13
Z90 = 1.6448536269514722
MAX_K = 10_000
WIDTH_MARGIN = 0.999
ALPHA = 0.05


def score(rows, n=N_PROBLEMS):
    good = [r for r in rows if "min" in r and "max" in r and r["min"] <= r["answer"] <= r["max"]]
    for r in rows:
        if "min" in r and not 0 < r["min"] <= r["max"]:
            raise ValueError(f"interval must be positive and ordered: {r}")
    return (10 + sum(math.floor(r["max"] / r["min"]) for r in good)) * 2 ** (n - len(good))


def sigma_of(lo90, hi90):
    if not 0 < lo90 < hi90:
        raise ValueError(f"need 0 < lo90 < hi90, got {lo90}, {hi90}")
    return math.log(hi90 / lo90) / (2 * Z90)


def hit_probability(k, sigma):
    """P(answer inside the widest log-centred interval with floor(max/min) = k)."""
    if k == 0:
        return 0.0
    half_width = math.log((k + 1) * WIDTH_MARGIN) / 2
    return math.erf(half_width / (sigma * math.sqrt(2)))


def expected_score(ks, sigmas, n=N_PROBLEMS):
    ps = [hit_probability(k, s) for k, s in zip(ks, sigmas)]
    misses = math.prod(1 - p / 2 for p in ps)
    width = sum(k * (p / 2) / (1 - p / 2) for k, p in zip(ks, ps))
    return 2 ** n * misses * (10 + width)


def plan(beliefs, n=N_PROBLEMS):
    sigmas = [sigma_of(b["lo90"], b["hi90"]) for b in beliefs]
    ks = [1] * len(beliefs)
    for _ in range(100):
        changed = False
        for i in range(len(ks)):
            best = min(_candidates(ks[i]), key=lambda k: expected_score(ks[:i] + [k] + ks[i + 1:], sigmas, n))
            if expected_score(ks[:i] + [best] + ks[i + 1:], sigmas, n) < expected_score(ks, sigmas, n) - 1e-12:
                ks[i], changed = best, True
        if not changed:
            break
    out = []
    for b, k, s in zip(beliefs, ks, sigmas):
        centre = math.sqrt(b["lo90"] * b["hi90"])
        r = (k + 1) * WIDTH_MARGIN
        out.append({"k": k, "p_hit": hit_probability(k, s),
                    "min": centre / math.sqrt(r) if k else None, "max": centre * math.sqrt(r) if k else None})
    return out, expected_score(ks, sigmas, n)


def _candidates(current):
    grid = {0, 1, 2, 3, 4, 5, 6, 8, 10, 15, 20, 30, 50, 100, 200, 500, 1000, MAX_K}
    return sorted(grid | {max(0, current - 1), current, current + 1})


def wilson(hits, n, z=1.959963984540054):
    if n == 0:
        return 0.0, 1.0
    phat = hits / n
    centre = (phat + z * z / (2 * n)) / (1 + z * z / n)
    half = z * math.sqrt(phat * (1 - phat) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return max(0.0, centre - half), min(1.0, centre + half)


def _binom(n, k, p):
    return math.comb(n, k) * p**k * (1 - p) ** (n - k)


def calibration(rows):
    buckets = {}
    for conf, lo, hi, answer in rows:
        buckets.setdefault(conf, []).append(lo <= answer <= hi)
    report = []
    for conf in sorted(buckets):
        hits, n = sum(buckets[conf]), len(buckets[conf])
        low, high = wilson(hits, n)
        p_low = sum(_binom(n, j, conf) for j in range(hits + 1))
        p_high = sum(_binom(n, j, conf) for j in range(hits, n + 1))
        verdict = ("overconfident" if p_low < ALPHA / 2 else "underconfident" if p_high < ALPHA / 2
                   else "consistent with stated confidence")
        report.append({"confidence": conf, "n": n, "hits": hits, "hit_rate": hits / n,
                       "wilson95": [low, high], "p_too_few": p_low, "p_too_many": p_high,
                       "verdict": verdict})
    return report


def main(argv):
    if len(argv) != 2 or argv[0] not in ("score", "plan", "calibration"):
        print(__doc__.strip(), file=sys.stderr)
        return 2
    cmd, path = argv
    try:
        if cmd == "score":
            print(score(json.load(open(path))))
        elif cmd == "plan":
            intervals, e = plan(json.load(open(path)))
            for i, row in enumerate(intervals, 1):
                if row["k"] == 0:
                    print(f"Q{i:<2}  leave blank")
                else:
                    print(f"Q{i:<2}  [{row['min']:.3g}, {row['max']:.3g}]  max/min < {row['k'] + 1}  "
                          f"floor={row['k']}  P(hit)={row['p_hit']:.2f}")
            print(f"expected score {e:,.1f}  (lognormal beliefs, independent questions)")
        else:
            with open(path) as f:
                rows = [tuple(map(float, r)) for r in csv.reader(f) if r and not r[0].startswith("#")]
            for b in calibration(rows):
                lo, hi = b["wilson95"]
                print(f"stated {b['confidence']:.0%}: {b['hits']}/{b['n']} = {b['hit_rate']:.0%}  "
                      f"95% CI [{lo:.0%}, {hi:.0%}]  {b['verdict']}")
    except (ValueError, KeyError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
