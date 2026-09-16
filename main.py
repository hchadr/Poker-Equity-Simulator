import random
from itertools import combinations
from collections import Counter

RANKS = '23456789TJQKA'
SUITS = 'cdhs'
RANK_VALUE = {rank: i + 1 for i, rank in enumerate(RANKS)}

def make_deck():
    return [rank + suit for rank in RANKS for suit in SUITS]

def card_rank(card):
    return RANK_VALUE[card[0]]

def card_suit(card):
    return card[1]

def score_five_card_hand(hand):
    ranks = sorted([card_rank(card) for card in hand], reverse=True)
    suits = [card_suit(card) for card in hand]

    counts = Counter(ranks)
    count_groups = sorted(counts.items(), key=lambda x: (x[1], x[0]), reverse=True)

    is_flush = len(set(suits)) == 1

    unique_ranks = sorted(set(ranks), reverse=True)

    if set([14, 5, 4, 3, 2]).issubset(set(ranks)):
        is_straight = True
        straight_high = 5
    else:
        is_straight = len(unique_ranks) == 5 and unique_ranks[0] - unique_ranks[-1] == 4
        straight_high = unique_ranks[0] if is_straight else None
    if is_straight and is_flush:
        return (8, straight_high)
    
    if count_groups[0][1] == 4:
        four_rank = count_groups[0][0]
        kicker = max(rank for rank in ranks if rank != four_rank)
        return (7, four_rank, kicker)
    
    if count_groups[0][1] == 3 and count_groups[1][1] == 2:
        return (6, count_groups[0][0], count_groups[1][0])
    
    if is_flush:
        return (5, *ranks)
    
    if is_straight:
        return (4, straight_high)
    
    if count_groups[1][0] == 3:
        three_rank = count_groups[0][0]
        kickers = sorted([rank for rank in ranks if rank != three_rank], reverse=True)
        return (3, three_rank, *kickers)
    
    if count_groups[0][1] == 2 and count_groups[1][1] == 2:
        pair_high = max(count_groups[0][0], count_groups[1][0])
        pair_low = min(count_groups[0][0], count_groups[1][0])
        kicker = max(rank for rank in ranks if rank != pair_high and rank != pair_low)
        return (2, pair_high, pair_low, kicker)

    if count_groups[0][1] == 2:
        pair_rank = count_groups[0][0]
        kickers = sorted([rank for rank in ranks if rank != pair_rank], reverse=True)
        return (1, pair_rank, *kickers)

    return (0, *ranks)

def best_hand_score(seven_cards):
    best_score = None
    
    for five_card_hand in combinations(seven_cards, 5):
        score = score_five_card_hand(five_card_hand)

        if best_score is None or score > best_score:
            best_score = score

    return best_score

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

def main():
    hand1_input = input("Enter Hand 1, separated by spaces: ")
    hand2_input = input("Enter Hand 2, separated by spaces: ")

    hand1 = hand1_input.split()
    hand2 = hand2_input.split()

    simulate(hand1, hand2)

if __name__ == "__main__":
    main()
