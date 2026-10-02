import random

from poker.cards import make_deck
from poker.evaluator import best_hand_score
from poker.strategy import call_ev

def hand_equity(hero_hand, opponent_range, board, trials=10000):
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

    for _ in range(trials):
        # Randomly choose an opponent hand from their possible range
        opponent_hand = random.choice(valid_opponent_hands)

        available = [card for card in remaining_deck if card not in opponent_hand]

        # Complete the board
        cards_needed = 5 - len(board)
        future_cards = random.sample(available, cards_needed)

        final_board = board + future_cards

        hero_score = best_hand_score(hero_hand + final_board)
        opponent_score = best_hand_score(opponent_hand + final_board)

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

