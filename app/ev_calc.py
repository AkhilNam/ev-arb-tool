def implied_prob(odds):
    return 1 / odds if odds > 0 else 0

def calculate_ev(odds, win_prob):
    return (win_prob * odds) - 1

def no_vig_prob(over_odds, under_odds):
    over_imp = implied_prob(over_odds)
    under_imp = implied_prob(under_odds)
    total = over_imp + under_imp
    if total == 0:
        return 0.5
    return over_imp / total
