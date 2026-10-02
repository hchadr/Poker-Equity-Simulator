import random
from itertools import combinations

from poker.cards import RANK_VALUE, make_deck
from poker.evaluator import best_hand_score

HAND_WEIGHTS = {
    "AA": 1.0,
    "KK": 1.0,
    "QQ": 1.0,
    "JJ": 0.9,
    "TT": 0.8,
    "AKs": 0.9,
    "AKo": 0.8,
    "AQs": 0.8,
    "AQo": 0.6,
    "KQs": 0.7,
}

def hand_type(hand):
    rank1 = hand[0][0]
    rank2 = hand[1][0]

    suit1 = hand[0][1]
    suit2 = hand[1][1]

    if rank1 == rank2:
        return rank1 + rank2

    ranks = sorted([rank1, rank2], key = lambda r: RANK_VALUE[r], reverse = True)

    suffix = "s" if suit1 == suit2 else "o"

    return ranks[0] + ranks[1] + suffix

def generate_opponent_range(hero_hand, board):
    deck = make_deck()

    used_cards = set(hero_hand + board)

    available_cards = [card for card in deck if card not in used_cards]

    return list(combinations(available_cards, 2))

def hand_equity(hero_hand, opponent_range, board, trials=10_000):
    # Estimate hero's equity against a range of possible opponent hands.

    deck = make_deck()

    used_cards = hero_hand + board

    valid_opponent_hands = [hand for hand in opponent_range if not any(card in used_cards for card in hand)]

    if not valid_opponent_hands:
        raise ValueError("Opponent range contains no valid hands.")

    remaining_deck = [card for card in deck if card not in used_cards]

    wins = 0
    ties = 0
    losses = 0

    weights = [HAND_WEIGHTS.get(hand_type(hand), 0.1) for hand in valid_opponent_hands]


    for _ in range(trials):
        # Randomly choose an opponent hand from their possible range
        opponent_hand = random.choices(valid_opponent_hands, weights = weights, k = 1)[0]

        available = [card for card in remaining_deck if card not in opponent_hand]

        # Complete the board
        cards_needed = 5 - len(board)
        future_cards = random.sample(available, cards_needed)

        final_board = board + future_cards

        hero_score = best_hand_score(hero_hand + final_board)
        opponent_score = best_hand_score(list(opponent_hand) + final_board)

        if hero_score > opponent_score:
            wins += 1
        elif hero_score == opponent_score:
            ties += 1
        else:
            losses += 1

    total = wins + ties + losses

    return {
        "win_rate": wins / total,
        "tie_rate": ties / total,
        "loss_rate": losses / total,
        "equity": (wins + 0.5 * ties) / total
    }

