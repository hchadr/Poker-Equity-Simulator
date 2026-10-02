import random

from poker.cards import make_deck
from poker.evaluator import best_hand_score

def simulate(hand1, hand2, trials=100_000):
    deck = make_deck()
    used_cards = hand1 + hand2

    remaining_deck = [card for card in deck if card not in used_cards]

    wins1 = 0
    wins2 = 0
    ties = 0

    for _ in range(trials):
        board = random.sample(remaining_deck, 5)

        score1 = best_hand_score(hand1 + board)
        score2 = best_hand_score(hand2 + board)

        if score1 > score2:
            wins1 += 1
        elif score2 > score1:
            wins2 += 1
        else:
            ties += 1

    p1 = wins1 / trials
    p2 = wins2 / trials
    ptie = ties / trials

    margin = 1.96 * ((p1 * (1 - p1)) / trials) ** 0.5
    margin2 = 1.96 * ((p2 * (1 - p2)) / trials) ** 0.5
    
    print(f"Hand 1: {hand1}")
    print(f"Hand 2: {hand2}")
    print(f"Trials: {trials:,}")
    print()
    print(f"Hand 1 win rate: {p1:.2%}")
    print(f"95% CI: [{p1 - margin:.2%}, {p1 + margin:.2%}]")
    print(f"Hand 2 win rate: {p2:.2%}")
    print(f"95% CI: [{p2 - margin2:.2%}, {p2 + margin2:.2%}]")
    print(f"Tie rate: {ptie:.2%}")

