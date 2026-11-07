import pathlib
import re
import unittest
from fractions import Fraction as F
from itertools import product

TABLE = pathlib.Path(__file__).resolve().parents[2] / "references" / "practice_answers.md"
D6 = range(1, 7)


def mean(xs):
    xs = list(xs)
    return F(sum(xs), len(xs))


def prob(pred, space):
    return mean(1 if pred(*o) else 0 for o in space)


def flips_until_run(n):
    """Expected flips to see n heads in a row, by solving the absorbing chain on run length."""
    # E_k = expected remaining flips with a current run of k: E_k = 1 + E_{k+1}/2 + E_0/2, E_n = 0.
    # Write E_k = a_k + b_k * E_0 and back-substitute from k = n.
    a, b = F(0), F(0)
    for _ in range(n):
        a, b = 1 + a / 2, b / 2 + F(1, 2)
    return a / (1 - b)


def reroll(holder_maximizes):
    """Best value over all 64 keep/reroll policies, for whichever side holds the choice."""
    policies = product((True, False), repeat=6)
    values = [mean(x if keep else mean(D6) for x, keep in zip(D6, policy)) for policy in policies]
    return max(values) if holder_maximizes else min(values)


def deck():
    return [(rank, suit) for suit in "SHDC" for rank in range(1, 14)]


def two_draws(replace):
    cards = deck()
    if replace:
        return list(product(cards, cards))
    return [(a, b) for a in cards for b in cards if a != b]


EXPECTED = {
    "sum10": prob(lambda a, b: a + b == 10, product(D6, D6)),
    "face_repl": prob(lambda a, b: a[0] > 10 and b[0] > 10, two_draws(True)),
    "clubs_norepl": prob(lambda a, b: a[1] == b[1] == "C", two_draws(False)),
    "odd2": prob(lambda a, b: a * b % 2 == 1, product(D6, D6)),
    "odd3": prob(lambda a, b, c: a * b * c % 2 == 1, product(D6, D6, D6)),
    "weighted6": sum(F(1, 10) * x for x in range(1, 6)) + F(1, 2) * 6,
    "six_to_12": mean([1, 2, 3, 4, 5, 12]),
    "prime_ev": mean(x for x in D6 if x in (2, 3, 5)),
    "prime_le3": prob(lambda x: x <= 3, [(x,) for x in D6 if x in (2, 3, 5)]),
    "coins": prob(lambda *c: c.count("H") == 2, [c for c in product("HT", repeat=3) if "T" in c]),
    "ex2": (mean(x * x for x in D6), mean(D6) ** 2),
    "three_heads": flips_until_run(3),
    "d20": mean(range(1, 21)),
    "max3d6": mean(max(t) for t in product(D6, D6, D6)),
    "reroll_holder": reroll(True),
    "reroll_writer": reroll(False),
    "million": 1_000_000 * mean(D6),
}


def parse_exact(cell):
    parts = [F(p.strip()) for p in cell.split(" vs ")]
    return tuple(parts) if len(parts) > 1 else parts[0]


class PracticeAnswers(unittest.TestCase):
    def setUp(self):
        self.rows = {}
        for line in TABLE.read_text().splitlines():
            cells = [c.strip() for c in re.split(r"(?<!\\)\|", line)[1:-1]]
            if len(cells) == 5 and cells[0] in EXPECTED:
                self.rows[cells[0]] = parse_exact(cells[2])

    def test_every_row_is_checked(self):
        self.assertEqual(set(self.rows), set(EXPECTED))

    def test_table_matches_enumeration(self):
        for key, value in EXPECTED.items():
            with self.subTest(key):
                self.assertEqual(self.rows[key], value)

    def test_recursion_matches_closed_form(self):
        for n in range(1, 8):
            self.assertEqual(flips_until_run(n), 2 ** (n + 1) - 2)

    def test_canary_wrong_dice_count_is_caught(self):
        wrong_1_over_11 = F(1, 11)
        self.assertNotEqual(prob(lambda a, b: a + b == 7, product(D6, D6)), wrong_1_over_11)


if __name__ == "__main__":
    unittest.main()
