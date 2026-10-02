RANKS = '23456789TJQKA'
SUITS = 'cdhs'
RANK_VALUE = {rank: i + 1 for i, rank in enumerate(RANKS)}

def make_deck():
    return [rank + suit for rank in RANKS for suit in SUITS]

def card_rank(card):
    return RANK_VALUE[card[0]]

def card_suit(card):
    return card[1]