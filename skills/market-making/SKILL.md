---
name: market-making-reasoning
description: Price uncertain contracts, quote two-sided markets, size against capital and update on every fill, the way Jane Street teaches it in its Probability & Markets guide, the Figgie card game and intern mock trading. Use when making a market or estimating expected value on any uncertain quantity, building or checking a confidence interval, asking what a fill or a counterparty's motive reveals, deciding whether an option-like choice (a reroll, an early exit) changes a price, playing or coaching Figgie, or practising for a trading interview. Ships an exact Figgie deck-posterior calculator and a brute-force-verified answer key.
---

# Market-Making Reasoning

## Overview

This skill is how Jane Street publicly teaches people to think about prices under uncertainty. It is built from four sources:

- the firm's 12-page trading-interview guide, *Probability & Markets* (revised August 2025);
- the official rules of Figgie, the trading card game "invented at Jane Street in 2013";
- the Signals and Threads podcast, where staff describe intern mock trading and client flow;
- Mark Doss's 2026 tech talk on production engineering, which shows the same reasoning used to run a live trading stack.

Two limits apply throughout:

- **This is teaching material, not anyone's trading strategy.** Nothing here describes how Jane Street actually trades, and none of it is investment advice.
- **Text marked *(derived)* is this skill's own reasoning, not Jane Street text.** That covers anything beyond what the sources say, and in particular all Figgie strategy past the official "basic strategy".

Every quotation below is verbatim from its cited source.

## Core Philosophy

"Probability provides a good framework for making decisions when uncertainty is involved." The guide builds everything else toward one rule: "If you know the expected value of something, you should be happy to buy for less or sell for more."

That rule is necessary, but it is not enough to make a market. Three further forces stop "quote at EV" from being the whole answer:

1. **Risk.** "It's bad to lose a lot of money, because that means in the future when there are great opportunities to trade, you won't have as much capital to do those trades."
2. **Edge versus volume.** "You will want to balance your likelihood of a trade and the expected profit."
3. **Selection.** "Adverse selection is the idea that the trades you get to do are worse than they would appear, because someone else is selecting into the trade against you."

The third is the deepest. Your counterparty chose to trade with you, and that choice is information. Doss describes the live-market version: "as soon as you decide you want to do a bad trade, every other market participant very eagerly wants to do that trade with you as fast as you or they possibly can."

## The Loop

Run these seven steps in order for every price you make. Steps 5–7 repeat after every trade.

### Step 1: Pin down the contract

Before any arithmetic, write down three things:
- what settles the contract;
- when it settles;
- who holds any choice inside it.

The guide's own warning about trading against someone as careful as you is that "there's a good chance you did your calculations wrong, or misunderstood the contract terms, or something."

Look for hidden options first. The guide's reroll contract comes with the hint "who gets to decide to re-roll? Does it matter?". It matters a great deal:
- If the buyer holds the reroll, the contract is worth 4.25.
- If the seller holds it, the contract is worth 2.75.

The same words describe a contract whose fair value shifts by 1.5 depending on who holds the choice. Ask about every embedded choice: who exercises it, and when.

### Step 2: Model the outcomes

Use the guide's counting tools, in this order:

| Tool | Rule | Classic trap it prevents |
|---|---|---|
| Distinct outcomes | Imagine a red die and a blue die: 36 outcomes, not 11 sums | "A common mistake is to say that there's one acceptable outcome (the sum is 7), out of 11" |
| Equally likely sub-outcomes | 30% / 20% / 50% becomes ten tickets: three, two and five | Weighting by hand and dropping a case |
| Independence | Multiply probabilities only when one outcome tells you nothing about the other | Multiplying draws made without replacement |
| Linearity | E[X+Y] = E X + E Y; "This is true even if X and Y are not independent!" | Enumerating a joint distribution you never needed |
| Indicators | E 1_A = P[A]; a bet paying x or y is worth y + (x−y)·P[A] | Treating a binary payout as a special case |
| Conditioning | P[A\|B] = P[A and B] / P[B]; update the prior when told something | Answering the unconditional question |
| Recursion | Memoryless processes: E = 1 + ½·0 + ½·E, so E = 2 | Summing an infinite series by hand |
| Edge and small cases | Try 0, 1, negatives, infinity; solve for 2 players, then add one | Shipping a formula that divides by zero |

### Step 3: Compute the expected value and the range

The guide names three ways to describe the range: the literal min and max, the average deviation, and a confidence interval.

Watch for overconfidence. People "tend to be overconfident. That is, if they gave a bunch of 95% confidence intervals, less than 95% of them would contain the actual outcome." The guide's correction is "It's important to try to correct for this, but also don't go overboard!". The way to practise is to quiz yourself "on easily verified facts" and score your hit rate against the confidence you claimed.

Then check orders of magnitude. The guide's interview section says numeracy is for "deciding if your answer is reasonable (e.g. check the order of magnitude!)".

### Step 4: Set the market

Put the quote around the expected value. Then adjust it for the three forces from Core Philosophy:

| Force | Pushes the quote | Guide's worked example (d6 contract, EV 3.5) |
|---|---|---|
| EV | centre | Bid below 3.5, offer above it |
| Worst case vs capital | wider, or smaller size | Losing $2.5 one time in six is fine on a small stake |
| Edge vs fill probability | narrower to trade more, wider to earn more per trade | Bidding 3.5 earns nothing; bidding 1 never trades |
| Difficulty of valuation | wider | A d6 is easy to value; the weather in a week against a meteorologist is not |

The guide's answer for the d6 is "3 at 4, 10 up". Scale is the test of whether you have absorbed step 4. On 1,000,000 × d6 the EV scales exactly, but the guide asks "How would you feel if I hit your bid and the roll ended up a 1?". At that size the worst case is a fraction of your capital, so you quote smaller or wider even though the per-unit math is unchanged.

### Step 5: Condition on the fill

After every fill, ask the guide's two questions: "Conditional on my order being filled, what do I think the expected value of the security is? Given this updated expected value, would I be happy to have done the trade?"

A fill is evidence, and it moves your estimate against you: "If you bought, the correct value of the security is probably a bit less than you initially believed." Re-quote from the updated value, not from the old one.

Figgie builds this into its rules: "After each trade, all quotes in all suits are automatically canceled". Nobody can stay posted at a price they set before the last piece of information arrived.

### Step 6: Ask why they are trading

The guide splits counterparties in two:

- **Price-sensitive and informed.** They are "just like you, trying to make a good expected value decision? This is scary". Widen your quote, shrink your size, and recheck your model.
- **Price-insensitive.** They trade for reasons other than price. The guide's examples are long-term investors, or an interviewer who commits to a trade "to make your scenario more interesting".

In Young Cho's account of client flow shows why identifying the counterparty pays for both sides. An anonymous stream of selling makes a market maker think "it might just be the case that I'm getting something very wrong and I'm going to make sure that I do something a little bit more conservative while I try to figure things out." Ron Minsky draws the conclusion: when the seller is a pension fund rebalancing, "knowing where it's coming from can allow you to provide better services—in particular just like a better price". Knowing who is on the other side of a trade has value. Price it rather than ignoring it.

### Step 7: Distrust a fill that looks too good

Doss calls the "fill-too-good" alert his favourite at Jane Street: "This means we made too much money." It earns that place because a windfall is usually a symptom. "If you have problems with market data, if you have problems with instrument generation, if you have problems with the order engine, if you have problems with your trading strategy, if you have a rogue trader, if a trader has fat-fingered something, anywhere in your trading stack, something can be caught by this one alert."

*(derived)* Apply this to your own reasoning too. When a trade looks unusually profitable, the first hypothesis is that your model, your data or your reading of the contract is wrong. That you have found an edge is the second hypothesis. In Doss's sample incident, the fill-too-good alerts traced back to market data that had silently gone stale while still being treated as live.

## Market Vocabulary

From the guide's Making Markets section:

| Say | Means |
|---|---|
| "I'm 2 bid for 10." | Buy up to 10 at 2 |
| "I have 10 at 4." | Sell up to 10 at 4 |
| "I'm 2 at 4, 10 up." | Both of the above at the same size |
| "Sold" / "take 'em" | Hit the whole bid / lift the whole offer |
| "I buy 5" / "I sell 5" | Trade part of the size |
| "I'm out." | Cancel your order |

A fill can be full or partial. A partially filled order keeps its remaining size live "unless otherwise specified".

## Figgie

### Rules (figgie.com)

- **Players and stakes.** 4 or 5 players start with $350 each. They ante a $200 pot, and the 40 cards are dealt evenly: 10 each with 4 players, 8 each with 5.
- **The deck.** It has "two 10-card suits", "one 8-card suit" and "one 12-card suit". Which suit gets which count is random and hidden until the end of the round.
- **The goal suit.** It "will always be the same color (black or red) as the 12-card suit", so it holds 8 or 10 cards. Spades and clubs are black; hearts and diamonds are red. No other suit is worth anything.
- **Trading.** Trading is open for 4 minutes with no turns, and one card changes hands per trade. You can "Penny" the best bid or offer by one. Every trade cancels every quote in every suit.
- **Payout.** Each goal card pays $10 from the pot. The holder of the most goal cards takes the remainder, $100 or $120, and ties split it.
- **Mindset.** "Most of the skill in Figgie is in negotiating trades that benefit both the buyer and seller." Play as if for money: "behave as if you are playing for real money and make decisions that maximize your long-term profits."

The official basic strategy has three parts: deduce the 12-card suit, collect goal cards while selling the others "as long as the prices seem worthwhile", and finish with the most goal cards.

### Your hand is a sample: `scripts/figgie_posterior.py`

The hand you were dealt is a random sample from the hidden deck, so it is evidence about which of the 12 possible decks you are in. The script computes the exact posterior: a uniform prior over the 12 decks and a multivariate hypergeometric likelihood, in rational arithmetic. Its tests cross-check it against 400,000 real shuffled deals, and a canary checks that the simulation would catch a wrong answer.

```sh
python3 -I scripts/figgie_posterior.py 5 2 2 1          # spades clubs hearts diamonds, 4 players
python3 -I scripts/figgie_posterior.py --players 5 4 1 2 1
python3 -I scripts/figgie_posterior.py --json 3 3 2 2
```

For the hand 5♠ 2♣ 2♥ 1♦, the script prints P(spades is the 12-card suit) = 0.494, so P(clubs is the goal) = 0.494 and P(spades is the goal) = 0.185. **A long suit points to its same-colour partner.** The five spades you hold are probably worth nothing, and the two clubs are your most valuable cards. Players who value their long suit have it backwards.

*(derived)* How to play from there:

- **Value one more goal card at $10·P(goal) plus its effect on the majority bonus.** That effect is near zero when you are far from the lead, and close to the whole $100–$120 when one card decides who holds the most. The same card is worth very different amounts to different players. That gap is why trades exist that "benefit both the buyer and seller".
- **Use only the dealt hand in the posterior.** A card you bought was chosen by its seller, so it is not a random sample. The script's likelihood assumes a random deal.
- **Treat order flow as evidence.** Mannes describes what Figgie trains: "you pay attention to what other people are doing, what information that they have that is probably causing them to behave in that way". Someone bidding hard for hearts probably holds many diamonds.
- **Re-quote only after updating.** The cancel-on-trade rule exists to make you do exactly that. If you have not updated since the last trade, wait before quoting again.
- **Sell the suits your hand rules out early.** Once the posterior puts a suit near zero, its cards are worth $0 to you but not yet to players who haven't done the arithmetic.

## Coaching Mode

Use this mode when someone is practising for an interview or learning, not asking for an answer.

- **Hold the answer key back.** `references/practice_answers.md` answers every question the guide poses. Keep it out of the conversation until the person has made an attempt. Then use it to check their work, and point them to the idea in its last column rather than just the number.
- **Value the process over the answer.** "We care about how you think about and approach tough problems, which includes how you take hints and respond to being wrong." A right answer "isn't enough" on its own, and a wrong answer is not a failure.
- **Reward simplicity.** "we often prefer the simple, intuitive answer to the one that involves a bunch of esoteric theorems."
- **Normalise uncertainty.** "It's totally fine to say that you're not sure about your answer". A better answer later beats a fast one now.
- **Use the trading-interview page's checklist.** "Approach the problem methodically. Communicate clearly. Correct your mistakes. Ask why."
- **Practise by trading, not only by reading.** Mannes on the intern program: "Doing it in a context where you kind of commit to something and there are consequences to what you choose I think provides useful feedback." Make real two-sided markets on the guide's contracts and have the person fill against them.

## Rules

**Always**
- Write down the contract's settlement and who holds each embedded choice before computing anything.
- Quote two-sided around EV, with the width justified by worst case, fill probability and how hard the value is to compute.
- Size so that the worst case does not cost you future opportunities.
- Ask "conditional on my order being filled" before celebrating a fill, and re-quote from the updated value.
- Ask why the counterparty is trading, and price informed and price-insensitive flow differently.
- Track how often your confidence intervals contain the answer.

**Never**
- Count sums or other aggregates as if they were equally likely outcomes.
- Multiply probabilities of dependent events.
- Leave a quote up after new information has arrived, including a fill of your own.
- Treat an unexpectedly good trade as skill before ruling out an error in your data, model or contract reading.
- Present this skill's derived Figgie strategy, or anything here, as Jane Street's actual trading practice.

**Prefer**
- Linearity and indicators over enumerating joint distributions.
- Recursion over infinite series.
- Small cases and extreme inputs before general formulas.
- The simple, intuitive argument over the clever one.

## Checklist before you quote

1. Can I state what settles the contract, when, and who holds every choice inside it?
2. Did I count distinct outcomes, not merely distinct totals?
3. What are the EV, the worst case, and my 90% interval, and have I checked the order of magnitude?
4. Is my worst-case loss at this size small relative to my capital?
5. Where would I be happy to be filled on each side, assuming the fill tells me something?
6. Who would trade against this quote, and why?
7. If this fills and looks great, what would I check first?

## Humility

Markets do not hold still. Mannes: "In finance, the things that you find, the patterns that you find often get discovered and competed away over time and the things that you knew stop being true or as important." A rule that worked yesterday is a hypothesis today. That includes every *(derived)* rule here.

## Sources

- **Probability & Markets** (Jane Street trading-interview guide, rev. Aug 2025). https://www.janestreet.com/static/pdfs/trading-interview.pdf. Used for the Randomness through Interview Thoughts sections, the market vocabulary and every practice contract.
- **Figgie: How to Play.** https://figgie.com/how-to-play. Used for the rules, the deck table, the basic strategy and the payout examples.
- **Trading Interviews.** https://www.janestreet.com/trading-interviews/. Used for the hiring signals and the four tips.
- **Mark Doss, "Production Engineering When Trading Billions of Dollars a Day"** (Jane Street tech talk, 2026). https://www.janestreet.com/tech-talks/production-engineering-when-trading-billions-of-dollars-a-day/. Adverse selection at (00:09:31) and fill-too-good at (00:27:11).
- **Signals and Threads, "Finding Signal in the Noise: Machine Learning and the Markets"** (In Young Cho with Ron Minsky, Ep. 22, 2025). https://signalsandthreads.com/finding-signal-in-the-noise/. Client flow and the value of knowing the counterparty: In Young Cho at 05:31, Ron Minsky at 08:27.
- **Signals and Threads, "Wrestling the World into Rows"** (Eric Mannes with Ron Minsky, Ep. 29, 2026). https://signalsandthreads.com/wrestling-the-world-into-rows/. Mock trading, Figgie and anti-inductive markets, 00:00:02–00:08:47.

Quote gate: `tools/fetch_corpus.sh <dir> $(cat skills/market-making/sources.txt)` then `python3 -I tools/verify_quotes.py <dir> skills/market-making/SKILL.md`. Script tests: `python3 -I -m unittest discover -s skills/market-making/scripts/tests`.
