def calculate_ev(odds, win_prob):
    if odds > 0:
        payout = odds / 100
    else:
        payout = 100 / abs(odds)
    return (win_prob * payout) - (1 - win_prob)
