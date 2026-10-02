def call_ev(equity, pot, call_amount):
    # Approximate EV of calling a bet.

    final_pot = pot + call_amount

    return equity * final_pot - call_amount

def choose_action(equity, pot, call_amount):
    fold_ev = 0

    call_ev_value = call_ev(equity, pot, call_amount)

    if call_ev_value > fold_ev:
        return "Call", call_ev_value

    return "Fold", fold_ev

