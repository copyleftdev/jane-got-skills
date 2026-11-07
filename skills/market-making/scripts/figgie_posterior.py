"""Exact posterior over the 12 Figgie decks given the hand you were dealt.

usage: python3 -I figgie_posterior.py [--players 4|5] [--json] <spades> <clubs> <hearts> <diamonds>

The counts are your hand at the deal, before any trade: cards you bought were chosen by the
seller, so they are not a random sample and do not fit this likelihood. The prior is uniform
over the 12 decks (figgie.com: the suit matching each count is random). The likelihood is
multivariate hypergeometric, so the numbers are exact fractions, rounded only for display.

Card values printed here are the $10-per-card part only. The majority bonus is not included,
because it depends on what every other player ends up holding.
"""

import json
import sys
from fractions import Fraction
from math import comb

SUITS = ("spades", "clubs", "hearts", "diamonds")
SAME_COLOR = {"spades": "clubs", "clubs": "spades", "hearts": "diamonds", "diamonds": "hearts"}
POT = 200
PER_CARD = 10


def decks():
    for twelve in SUITS:
        for eight in SUITS:
            if eight != twelve:
                yield {s: 12 if s == twelve else 8 if s == eight else 10 for s in SUITS}, SAME_COLOR[twelve]


def posterior(hand):
    weights = [(deck, goal, Fraction(_likelihood(deck, hand))) for deck, goal in decks()]
    total = sum(w for _, _, w in weights)
    if total == 0:
        raise ValueError("no Figgie deck can produce this hand")
    return [(deck, goal, w / total) for deck, goal, w in weights]


def _likelihood(deck, hand):
    out = 1
    for s in SUITS:
        out *= comb(deck[s], hand[s])
    return out


def summary(hand, players):
    if players not in (4, 5):
        raise ValueError("Figgie is played by 4 or 5 players")
    if sum(hand.values()) != 40 // players:
        raise ValueError(f"a {players}-player hand has {40 // players} cards, got {sum(hand.values())}")
    post = posterior(hand)
    p_goal = {s: sum(p for _, g, p in post if g == s) for s in SUITS}
    p_twelve = {s: sum(p for d, _, p in post if d[s] == 12) for s in SUITS}
    e_goal_total = sum(p * d[g] for d, g, p in post)
    e_goal_others = sum(p * (d[g] - hand[g]) for d, g, p in post)
    e_bonus = sum(p * (POT - PER_CARD * d[g]) for d, g, p in post)
    return {
        "hand": hand,
        "players": players,
        "decks": [{"counts": d, "goal": g, "p": p} for d, g, p in sorted(post, key=lambda x: -x[2])],
        "p_goal": p_goal,
        "p_twelve": p_twelve,
        "card_value": {s: PER_CARD * p_goal[s] for s in SUITS},
        "e_goal_cards_total": e_goal_total,
        "e_goal_cards_held_by_others": e_goal_others,
        "e_majority_bonus": e_bonus,
    }


def _render(x):
    if isinstance(x, Fraction):
        return round(float(x), 4)
    if isinstance(x, dict):
        return {k: _render(v) for k, v in x.items()}
    if isinstance(x, list):
        return [_render(v) for v in x]
    return x


def main(argv):
    as_json = "--json" in argv
    argv = [a for a in argv if a != "--json"]
    players = 4
    if "--players" in argv:
        i = argv.index("--players")
        players = int(argv[i + 1])
        argv = argv[:i] + argv[i + 2:]
    if len(argv) != 4 or not all(a.isdigit() for a in argv):
        print(__doc__.strip(), file=sys.stderr)
        return 2
    hand = dict(zip(SUITS, map(int, argv)))
    try:
        result = _render(summary(hand, players))
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    if as_json:
        print(json.dumps(result, indent=2))
        return 0
    print(f"hand {hand}  ({players} players)")
    print(f"{'suit':<9} {'P(12-card)':>10} {'P(goal)':>8} {'$/card':>7}")
    for s in SUITS:
        print(f"{s:<9} {result['p_twelve'][s]:>10.4f} {result['p_goal'][s]:>8.4f} {result['card_value'][s]:>7.2f}")
    print(f"E[goal cards in deck] {result['e_goal_cards_total']:.3f}   "
          f"E[goal cards held by others] {result['e_goal_cards_held_by_others']:.3f}   "
          f"E[majority bonus] ${result['e_majority_bonus']:.2f}")
    print("most likely decks:")
    for d in result["decks"][:4]:
        print(f"  {d['p']:.4f}  {' '.join(f'{s[0].upper()}{d['counts'][s]}' for s in SUITS)}  goal={d['goal']}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
