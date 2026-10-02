import poker
from poker.opponent import hand_equity
from poker.strategy import choose_action

def main():
    hero_hand = ["As", "Ks"]

    board = ["Qs", "7s", "2c"]

    opponent_range = [
        ["Ah", "Kd"],
        ["Ac", "Kh"],
        ["Qh", "Jd"],
        ["Qc", "Jc"],
        ["9h", "9d"],
        ["8c", "8d"]
    ]

    result = hand_equity(hero_hand, opponent_range, board, trials=10000)

    equity = result["equity"]

    pot = 100
    call_amount = 50

    action, ev = poker.strategy.choose_action(equity, pot, call_amount)

    print(f"Hero: {hero_hand}")
    print(f"Board {board}")
    print(f"Equity: {equity:.2%}")
    print(f"Action: {action}")
    print(f"EV: ${ev:.2f}")

if __name__ == "__main__":
    main()




