from poker.opponent import hand_equity
from poker.strategy import choose_action
from poker.opponent import (generate_opponent_range, hand_type, HAND_WEIGHTS)

def main():
    hero_hand = ["As", "Ks"]

    board = ["Qs", "7s", "2c"]

    opponent_range = generate_opponent_range(hero_hand, board)

    for hand in opponent_range[:20]:
        print(hand, hand_type(hand), HAND_WEIGHTS.get(hand_type(hand), 0.1))

    result = hand_equity(hero_hand, opponent_range, board, trials=10_000)

    equity = result["equity"]

    pot = 100
    call_amount = 50

    action, ev = choose_action(equity, pot, call_amount)

    print(f"Hero: {hero_hand}")
    print(f"Board {board}")
    print(f"Equity: {equity:.2%}")
    print(f"Action: {action}")
    print(f"EV: ${ev:.2f}")

if __name__ == "__main__":
    main()




