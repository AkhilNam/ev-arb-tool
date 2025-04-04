import os
import json
import pandas as pd
from datetime import datetime
from app.ev_calc import implied_prob, no_vig_prob, calculate_ev, calculate_fair_prob
from app.parser import extract_props

LOG_FILE = "placed_bets.csv"

# ---------------------------
# 1. Bet Selection Functions
# ---------------------------

def select_bets(ev_df, min_ev=0.015):
    """
    From the EV DataFrame, filter bets with EV greater than min_ev.
    For each unique combination of player/market/line (regardless of platform),
    choose the bet with the highest EV (and, if equal, the highest fair_prob).
    """
    # Filter bets above the EV threshold
    valid_bets = ev_df[ev_df["ev"] > min_ev].copy()
    
    # Sort descending by EV and then by fair_prob
    valid_bets.sort_values(by=["ev", "fair_prob"], ascending=False, inplace=True)
    
    # Drop duplicates based on player, market, and line.
    # This ensures that if we already bet on (say) the over 24.5, we won't bet on the under 24.5.
    selected = valid_bets.drop_duplicates(subset=["player", "market", "line"], keep="first")
    return selected

def already_placed(selected_bets, log_file=LOG_FILE):
    """
    Checks the log file to see if a bet for the same player/market/line has already
    been placed today (regardless of platform). Returns only the bets that are new.
    """
    if not os.path.exists(log_file):
        return selected_bets  # No log exists, so all bets are new

    log_df = pd.read_csv(log_file)
    # Parse the timestamp and extract the date
    log_df["timestamp"] = pd.to_datetime(log_df["timestamp"])
    log_df["date"] = log_df["timestamp"].dt.date
    today = datetime.now().date()

    # We check by the unique key: player, market, line
    placed_today = log_df[log_df["date"] == today][["player", "market", "line"]]

    merged = pd.merge(
        selected_bets,
        placed_today,
        on=["player", "market", "line"],
        how="left",
        indicator=True
    )
    
    new_bets = merged[merged["_merge"] == "left_only"]
    new_bets = new_bets[selected_bets.columns]  # retain original columns
    return new_bets

def log_bets(bets, log_file=LOG_FILE):
    """
    Appends the new bets to a CSV log with a timestamp.
    """
    bets = bets.copy()
    bets["timestamp"] = pd.Timestamp.now()
    
    if os.path.exists(log_file):
        existing = pd.read_csv(log_file)
        bets = pd.concat([existing, bets], ignore_index=True)
    bets.to_csv(log_file, index=False)

# ---------------------------
# 2. Parlay Construction
# ---------------------------

def place_parlay(bets, parlay_books=["PrizePicks", "Underdog"]):
    """
    Combines bets from PrizePicks and Underdog into a single parlay.
    The parlay odds is the product of the individual odds,
    the parlay fair probability is the product of the individual fair probabilities,
    and the parlay EV is computed as: (parlay_odds * parlay_fair_prob) - 1.
    
    Returns a dictionary with parlay details (including a DataFrame for logging)
    if at least 2 legs exist; otherwise, returns None.
    """
    parlay_bets = bets[bets["bookmaker"].isin(parlay_books)].copy()
    if parlay_bets.empty:
        print("No parlay bets available.")
        return None
    if len(parlay_bets) < 2:
        print("Only one bet from PrizePicks/Underdog available; cannot form a parlay.")
        return None
    
    parlay_odds = parlay_bets["odds"].prod()
    parlay_fair_prob = parlay_bets["fair_prob"].prod()
    parlay_ev = parlay_odds * parlay_fair_prob - 1
    
    print(f"Parlay composed of {len(parlay_bets)} legs:")
    print(parlay_bets[["player", "market", "side", "line", "bookmaker", "odds", "fair_prob", "ev"]])
    print(f"Parlay Odds: {parlay_odds:.3f}, Fair Probability: {parlay_fair_prob:.3f}, EV: {parlay_ev:.3f}")
    
    # Create a log DataFrame for the parlay bet
    parlay_log = pd.DataFrame({
        "bet_type": ["parlay"],
        "platforms": [", ".join(parlay_bets["bookmaker"].unique())],
        "legs": [len(parlay_bets)],
        "parlay_odds": [parlay_odds],
        "parlay_fair_prob": [parlay_fair_prob],
        "parlay_ev": [parlay_ev],
        "player": [", ".join(parlay_bets["player"].unique())],
        "market": [", ".join(parlay_bets["market"].unique())],
        "line": [", ".join(parlay_bets["line"].astype(str).unique())]
    })
    
    return {
        "legs": parlay_bets,
        "parlay_odds": parlay_odds,
        "parlay_fair_prob": parlay_fair_prob,
        "parlay_ev": parlay_ev,
        "log_df": parlay_log
    }

# ---------------------------
# 3. Processing and Placing Bets
# ---------------------------

def process_and_place_bets(ev_df, min_ev=0.01):
    """
    Processes bets from the EV DataFrame and places them according to these rules:
      - Across all platforms, only one bet per unique player/market/line is allowed.
      - If a bet is placed (e.g. over 24.5), the opposite (under 24.5) is not placed.
      - If multiple bets exist for the same line (from different platforms), the one with
        the highest EV (and, if tied, the best fair probability) is selected.
      - Bets from PrizePicks and Underdog must be placed as a parlay (they don't support straight legs).
      - All other bets are placed as straight bets.
      - Every placed bet is logged, with its bet type noted.
    """
    # First, select the best bet per unique player/market/line across all platforms.
    selected = select_bets(ev_df, min_ev=min_ev)
    
    # Remove any bets already placed today (based on player/market/line).
    new_bets = already_placed(selected)
    
    if new_bets.empty:
        print("No new bets to place today.")
        return
    
    print("Selected bets for placement:")
    print(new_bets[["player", "market", "side", "line", "bookmaker", "odds", "fair_prob", "ev"]])
    
    # Group bets into two sets:
    # - Parlay group: bets from PrizePicks and Underdog (must be combined into a parlay).
    # - Straight group: all bets from other platforms.
    parlay_bets = new_bets[new_bets["bookmaker"].isin(["PrizePicks", "Underdog"])].copy()
    straight_bets = new_bets[~new_bets["bookmaker"].isin(["PrizePicks", "Underdog"])].copy()
    
    # Process parlay bets: only place if at least 2 bets are available.
    if not parlay_bets.empty:
        if len(parlay_bets) >= 2:
            parlay_result = place_parlay(parlay_bets, parlay_books=["PrizePicks", "Underdog"])
            if parlay_result:
                # Replace the print statement with your actual parlay placement API call.
                print("Placing parlay bet with the following details:")
                print(parlay_result)
                # Log the parlay bet.
                log_bets(parlay_result["log_df"])
        else:
            print("Not enough parlay bets from PrizePicks/Underdog to form a parlay. Skipping parlay placement.")
    
    # Process straight bets: mark them as "straight" and place individually.
    if not straight_bets.empty:
        straight_bets["bet_type"] = "straight"
        for idx, row in straight_bets.iterrows():
            # Replace the print statement with your actual straight bet placement API call.
            print("Placing straight bet:")
            print(row)
        log_bets(straight_bets)

# ---------------------------
# Example Usage After EV Pipeline
# ---------------------------
if __name__ == "__main__":
    # For demonstration, we assume ev_df is built from your EV pipeline.
    # It should have columns: player, market, line, side, bookmaker, odds, fair_prob, ev, etc.
    # Here we load a JSON file that contains the raw bet props and then create a DataFrame.
    
    SAVED_JSON = "data/last_live_pull.json"
    all_props = []
    with open(SAVED_JSON, "r") as f:
        props_data = json.load(f)
        all_props.extend(props_data)
        
    ev_df = pd.DataFrame(all_props)
    
    # Process and place bets according to the rules.
    process_and_place_bets(ev_df, min_ev=0.015)
