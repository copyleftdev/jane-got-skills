import contextlib
import io
import itertools
import json
import math
import pathlib
import random
import sys
import tempfile
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
import estimathon as est  # noqa: E402


def interval(k, centre=100.0):
    r = (k + 1) * est.WIDTH_MARGIN
    return {"min": centre / math.sqrt(r), "max": centre * math.sqrt(r)}


class Score(unittest.TestCase):
    def test_all_blank(self):
        self.assertEqual(est.score([{"answer": 1}] * 13), 10 * 2**13)

    def test_all_good(self):
        self.assertEqual(est.score([{"min": 1, "max": 2, "answer": 1.5}] * 13), 10 + 13 * 2)

    def test_each_miss_doubles(self):
        rows = [{"min": 1, "max": 2, "answer": 1.5}] * 12 + [{"min": 1, "max": 2, "answer": 3}]
        self.assertEqual(est.score(rows), (10 + 12 * 2) * 2)

    def test_floor_not_ceiling(self):
        self.assertEqual(est.score([{"min": 1, "max": 1.99, "answer": 1.5}] * 13), 10 + 13 * 1)

    def test_resubmission_is_callers_job_but_bad_interval_rejected(self):
        with self.assertRaises(ValueError):
            est.score([{"min": 0, "max": 2, "answer": 1}])


def simulate(ks, sigmas, n, trials, seed, rule=math.floor):
    """Play real contests: draw answers from the beliefs, score with the official rule."""
    rng = random.Random(seed)
    total = 0.0
    sq = 0.0
    for _ in range(trials):
        rows = []
        for k, s in zip(ks, sigmas):
            answer = 100.0 * math.exp(rng.gauss(0, s))
            rows.append({**interval(k), "answer": answer} if k else {"answer": answer})
        good = [r for r in rows if "min" in r and r["min"] <= r["answer"] <= r["max"]]
        x = (10 + sum(rule(r["max"] / r["min"]) for r in good)) * 2 ** (n - len(good))
        total += x
        sq += x * x
    mean = total / trials
    return mean, math.sqrt((sq / trials - mean * mean) / trials)


class ExpectedScore(unittest.TestCase):
    KS = [1, 2, 3, 0, 5]
    SIGMAS = [0.3, 0.6, 1.0, 1.5, 0.8]
    N = 5

    def test_closed_form_matches_simulated_contests(self):
        mean, se = simulate(self.KS, self.SIGMAS, self.N, 40_000, seed=7)
        self.assertLess(abs(est.expected_score(self.KS, self.SIGMAS, self.N) - mean), 4 * se)

    def test_canary_ceiling_rule_is_rejected(self):
        mean, se = simulate(self.KS, self.SIGMAS, self.N, 40_000, seed=7, rule=math.ceil)
        self.assertGreater(abs(est.expected_score(self.KS, self.SIGMAS, self.N) - mean), 4 * se)

    def test_hit_probability_matches_lognormal_90(self):
        s = est.sigma_of(10, 1000)
        z = math.log(100) / s
        self.assertAlmostEqual(z, 2 * est.Z90)
        self.assertAlmostEqual(math.erf(est.Z90 / math.sqrt(2)), 0.90, places=6)


class BlankOrNot(unittest.TestCase):
    def test_adding_an_interval_helps_iff_k_below_10_plus_s(self):
        rng = random.Random(3)
        seen = set()
        for _ in range(2000):
            m = rng.randint(1, 6)
            sigmas = [rng.uniform(0.1, 3) for _ in range(m + 1)]
            ks = [rng.choice([0, 1, 2, 5, 20, 100]) for _ in range(m)]
            k = rng.choice([1, 3, 10, 30, 100, 300, 1000])
            ps = [est.hit_probability(kj, sj) for kj, sj in zip(ks, sigmas)]
            s = sum(kj * (pj / 2) / (1 - pj / 2) for kj, pj in zip(ks, ps))
            if abs(k - (10 + s)) < 1e-9:
                continue
            helps = est.expected_score(ks + [k], sigmas, m + 1) < est.expected_score(ks + [0], sigmas, m + 1)
            self.assertEqual(helps, k < 10 + s)
            seen.add(helps)
        self.assertEqual(seen, {True, False}, "both outcomes must occur for the test to mean anything")

    def test_k1_always_beats_blank(self):
        for sigma in (0.01, 0.5, 5.0):
            self.assertLess(est.expected_score([1], [sigma], 1), est.expected_score([0], [sigma], 1))


class Plan(unittest.TestCase):
    def test_coordinate_descent_finds_brute_force_optimum(self):
        beliefs = [{"lo90": 10, "hi90": 30}, {"lo90": 1, "hi90": 1000}, {"lo90": 50, "hi90": 60}]
        sigmas = [est.sigma_of(b["lo90"], b["hi90"]) for b in beliefs]
        grid = est._candidates(1)
        brute = min(est.expected_score(list(ks), sigmas, 3) for ks in itertools.product(grid, repeat=3))
        _, planned = est.plan(beliefs, n=3)
        self.assertAlmostEqual(planned, brute, places=6)

    def test_planned_intervals_respect_the_floor(self):
        rows, _ = est.plan([{"lo90": 5, "hi90": 500}] * 13)
        for r in rows:
            if r["k"]:
                self.assertEqual(math.floor(r["max"] / r["min"]), r["k"])

    def test_wider_belief_gets_wider_interval(self):
        rows, _ = est.plan([{"lo90": 90, "hi90": 110}, {"lo90": 1, "hi90": 10_000}] + [{"lo90": 10, "hi90": 100}] * 11)
        self.assertLess(rows[0]["k"], rows[1]["k"])


class Calibration(unittest.TestCase):
    def test_wilson_known_value(self):
        lo, hi = est.wilson(9, 10)
        self.assertAlmostEqual(lo, 0.5958, places=3)
        self.assertAlmostEqual(hi, 0.9821, places=3)

    def test_verdicts_need_evidence(self):
        rows = ([(0.9, 0, 1, 0.5)] * 9 + [(0.9, 0, 1, 2)]
                + [(0.8, 0, 1, 0.5)] * 5 + [(0.8, 0, 1, 2)] * 15
                + [(0.5, 0, 1, 0.5)] * 20)
        verdicts = {b["confidence"]: b["verdict"] for b in est.calibration(rows)}
        self.assertEqual(verdicts[0.9], "consistent with stated confidence")
        self.assertEqual(verdicts[0.8], "overconfident")
        self.assertEqual(verdicts[0.5], "underconfident")

    def test_small_samples_never_convict(self):
        b = est.calibration([(0.95, 0, 1, 2), (0.95, 0, 1, 0.5)])[0]
        self.assertLess(b["wilson95"][1], 0.95, "Wilson alone would have convicted")
        self.assertAlmostEqual(b["p_too_few"], 1 - 0.95**2)
        self.assertEqual(b["verdict"], "consistent with stated confidence")


class Cli(unittest.TestCase):
    def run_cli(self, *args):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = est.main(list(args))
        return code, out.getvalue(), err.getvalue()

    def test_plan_cli(self):
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
            json.dump([{"lo90": 10, "hi90": 1000}] * 13, f)
        code, out, _ = self.run_cli("plan", f.name)
        self.assertEqual(code, 0)
        self.assertIn("expected score", out)

    def test_bad_input(self):
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
            json.dump([{"lo90": 10, "hi90": 5}], f)
        self.assertEqual(self.run_cli("plan", f.name)[0], 2)
        self.assertEqual(self.run_cli("nope", f.name)[0], 2)


if __name__ == "__main__":
    unittest.main()
