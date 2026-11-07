import contextlib
import io
import pathlib
import random
import sys
import unittest
from collections import Counter
from fractions import Fraction

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
import figgie_posterior as fp  # noqa: E402

HAND = {"spades": 5, "clubs": 2, "hearts": 2, "diamonds": 1}


def simulate(hand, trials, seed):
    """Deal real shuffled decks and keep the ones that produce `hand`: no shared code with fp.posterior."""
    rng = random.Random(seed)
    layouts = [(t, e) for t in fp.SUITS for e in fp.SUITS if t != e]
    size = sum(hand.values())
    hits = Counter()
    for _ in range(trials):
        twelve, eight = rng.choice(layouts)
        cards = [s for s in fp.SUITS for _ in range(12 if s == twelve else 8 if s == eight else 10)]
        dealt = Counter(rng.sample(cards, size))
        if all(dealt[s] == hand[s] for s in fp.SUITS):
            hits[twelve] += 1
    return hits


class Posterior(unittest.TestCase):
    def test_twelve_decks_summing_to_one(self):
        post = fp.posterior(HAND)
        self.assertEqual(len(post), 12)
        self.assertEqual(sum(p for _, _, p in post), 1)
        self.assertTrue(all(isinstance(p, Fraction) for _, _, p in post))

    def test_goal_is_same_color_as_twelve(self):
        for deck, goal in fp.decks():
            twelve = next(s for s in fp.SUITS if deck[s] == 12)
            self.assertEqual(goal, fp.SAME_COLOR[twelve])
            self.assertIn(deck[goal], (8, 10))
            self.assertEqual(sum(deck.values()), 40)

    def test_impossible_decks_get_zero(self):
        post = fp.posterior({"spades": 10, "clubs": 0, "hearts": 0, "diamonds": 0})
        self.assertTrue(all(p == 0 for d, _, p in post if d["spades"] == 8))
        self.assertGreater(sum(p for d, _, p in post if d["spades"] == 12), Fraction(1, 2))

    def test_color_swap_symmetry(self):
        a = fp.summary(HAND, 4)
        b = fp.summary({"spades": 2, "clubs": 5, "hearts": 1, "diamonds": 2}, 4)
        self.assertEqual(a["p_goal"]["clubs"], b["p_goal"]["spades"])
        self.assertEqual(a["p_goal"]["hearts"], b["p_goal"]["diamonds"])

    def test_long_suit_points_at_its_partner(self):
        s = fp.summary(HAND, 4)
        self.assertEqual(max(s["p_twelve"], key=s["p_twelve"].get), "spades")
        self.assertEqual(max(s["p_goal"], key=s["p_goal"].get), "clubs")

    def test_bonus_is_pot_minus_goal_payouts(self):
        for hand in (HAND, {"spades": 3, "clubs": 3, "hearts": 2, "diamonds": 2}):
            s = fp.summary(hand, 4)
            self.assertEqual(s["e_majority_bonus"], 200 - 10 * s["e_goal_cards_total"])


class MonteCarlo(unittest.TestCase):
    TRIALS = 400_000

    @classmethod
    def setUpClass(cls):
        cls.hits = simulate(HAND, cls.TRIALS, seed=20261107)
        cls.n = sum(cls.hits.values())

    def test_enough_accepted_deals(self):
        self.assertGreater(self.n, 2000)

    def _max_z(self, predicted):
        worst = 0.0
        for s in fp.SUITS:
            p = float(predicted[s])
            se = (p * (1 - p) / self.n) ** 0.5
            worst = max(worst, abs(self.hits[s] / self.n - p) / se)
        return worst

    def test_exact_posterior_matches_simulated_deals(self):
        self.assertLess(self._max_z(fp.summary(HAND, 4)["p_twelve"]), 4.0)

    def test_canary_uniform_prior_is_rejected(self):
        self.assertGreater(self._max_z({s: Fraction(1, 4) for s in fp.SUITS}), 4.0)


class Cli(unittest.TestCase):
    def run_cli(self, *args):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = fp.main(list(args))
        return code, out.getvalue(), err.getvalue()

    def test_ok(self):
        code, out, _ = self.run_cli("5", "2", "2", "1")
        self.assertEqual(code, 0)
        self.assertIn("clubs", out)

    def test_wrong_hand_size(self):
        self.assertEqual(self.run_cli("5", "2", "2", "2")[0], 2)
        self.assertEqual(self.run_cli("--players", "5", "5", "2", "2", "1")[0], 2)

    def test_bad_player_count(self):
        self.assertEqual(self.run_cli("--players", "6", "5", "2", "2", "1")[0], 2)

    def test_single_suit_hand(self):
        code, _, err = self.run_cli("--players", "4", "10", "0", "0", "0")
        self.assertEqual(code, 0)
        self.assertEqual(err, "")


if __name__ == "__main__":
    unittest.main()
