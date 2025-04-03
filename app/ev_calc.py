def implied_prob(odds):
    """ Calculate implied probability from decimal odds. """
    return 1 / odds

def no_vig_prob(over_odds, under_odds):
    """ Calculate no-vig probability from over and under odds. """
    over_imp = implied_prob(over_odds)
    under_imp = implied_prob(under_odds)
    total_imp = over_imp + under_imp
    
    # To handle division by zero in case the odds are invalid or equal
    if total_imp == 0:
        return 0.5  # or some default value like 0.5 for an uncertain outcome
    
    return over_imp / total_imp

def calculate_fair_prob(df):
    """Calculate fair probabilities for all rows in the dataframe"""
    # Calculate implied probabilities
    df["implied_prob_over"] = df["over"].apply(implied_prob)
    df["implied_prob_under"] = df["under"].apply(implied_prob)
    
    # Calculate no-vig fair probabilities
    df["fair_prob_over"] = df.apply(lambda row: no_vig_prob(row["over"], row["under"]), axis=1)
    
    # Assign fair probability to "under" side
    df["fair_prob"] = df.apply(lambda row: row["fair_prob_over"] if row["side"] == "over" else 1 - row["fair_prob_over"], axis=1)
    
    return df

def calculate_ev(odds, win_prob):
    return (win_prob * odds) - 1
