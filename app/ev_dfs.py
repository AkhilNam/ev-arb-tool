from app.ev_calc import implied_prob, no_vig_prob, calculate_ev, calculate_fair_prob
import json
import pandas as pd
from app.parser import extract_props

def run_dfs_ev_pipeline(df, ev_threshold=0):
    """
    Run a DFS-specific EV pipeline.
    
    This function takes a DataFrame (df) that contains all the bets across
    multiple bookmakers, then:
      1. Filters for DFS bets (bookmakers: Fliff, Underdog, PrizePicks).
      2. Uses non-DFS bets to compute the market’s fair probability by averaging odds.
      3. Merges the fair probabilities into the DFS bets.
      4. Calculates EV for each DFS bet using your calculate_ev function.
      5. Returns only those DFS bets with EV above the threshold.
    
    Parameters:
      df: DataFrame with columns such as player, market, line, side, bookmaker, odds.
      ev_threshold: Minimum EV to consider (default -0.4)
      
    Returns:
      DataFrame of valid DFS bets.
    """
    # List of DFS platforms
    dfs_platforms = ["Fliff", "Underdog", "PrizePicks"]
    
    # Step 1: Separate DFS bets and non-DFS bets
    dfs_df = df[df["bookmaker"].isin(dfs_platforms)].copy()
    non_dfs_df = df[~df["bookmaker"].isin(dfs_platforms)].copy()
    
    if dfs_df.empty:
        print("No DFS bets found in the data.")
        return dfs_df
    
    if non_dfs_df.empty:
        print("No non-DFS bets available to compute fair probabilities.")
        return dfs_df

    # Step 2: Compute implied probabilities on non-DFS bets (using your function)
    non_dfs_df["implied_prob"] = non_dfs_df["odds"].apply(implied_prob)
    
    # Step 3: For non-DFS bets, get average odds per side for each player/market/line
    group_cols = ["player", "market", "line", "side"]
    avg_odds_non_dfs = non_dfs_df.groupby(group_cols)["odds"].mean().reset_index()
    
    # Pivot so each row has an 'over' and 'under'
    pivot = avg_odds_non_dfs.pivot(index=["player", "market", "line"], columns="side", values="odds").reset_index()
    
    # Normalize pivot column names to lower-case
    pivot.columns = [col.lower() if isinstance(col, str) else col for col in pivot.columns]
    
    if "over" not in pivot.columns or "under" not in pivot.columns:
        print("Non-DFS pivot missing expected columns. Found:", pivot.columns)
        return dfs_df

    # Step 4: Calculate fair probability for 'over' using your no_vig_prob function
    pivot["fair_prob_over"] = pivot.apply(lambda row: no_vig_prob(row["over"], row["under"]), axis=1)
    
    # Step 5: Merge the fair probability back to the DFS bets using join keys
    dfs_df = dfs_df.merge(
        pivot[["player", "market", "line", "fair_prob_over"]],
        on=["player", "market", "line"],
        how="left"
    )
    
    # Assign fair probability based on bet side (for "under", take complement)
    dfs_df["fair_prob"] = dfs_df.apply(
        lambda row: row["fair_prob_over"] if row["side"].strip().lower() == "over" 
        else 1 - row["fair_prob_over"],
        axis=1
    )
    
    # Drop rows where fair_prob could not be merged
    dfs_df = dfs_df.dropna(subset=["fair_prob"])
    
    # Step 6: Calculate EV for DFS bets using your calculate_ev function
    dfs_df["ev"] = dfs_df.apply(lambda row: calculate_ev(row["odds"], row["fair_prob"]), axis=1)
    
    # Step 7: Filter for DFS bets that have EV above the threshold
    valid_dfs = dfs_df[dfs_df["ev"] > ev_threshold].copy()
    
    print(f"Found {len(valid_dfs)} DFS EV bets above threshold {ev_threshold}.")
    print(valid_dfs[["player", "market", "side", "line", "bookmaker", "odds", "fair_prob", "ev"]].head(10))
    
    return valid_dfs

# --- Main Execution ---
all_props = []

if __name__ == "__main__":
    SAVED_JSON = "data/last_live_pull.json"
    with open(SAVED_JSON, "r") as f:
        props_data = json.load(f)
        all_props.extend(props_data)
        
    df = pd.DataFrame(all_props)

    run_dfs_ev_pipeline(df)
