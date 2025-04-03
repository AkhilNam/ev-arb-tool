import pandas as pd
import json
from datetime import datetime, timezone
from odds_api import get_events_for_sport, get_player_props
from parser import extract_props
from ev_calc import implied_prob, no_vig_prob, calculate_ev

SPORT_KEY = "basketball_nba"
DEV_MODE = True  # Set to True to use the saved JSON file
INCLUDE_LIVE = True  # Toggle this to True to include live bets
CSV_FILE = "data/props_ev.csv"
SAVED_JSON = "data/last_live_pull.json"

def run_ev_pipeline():
    all_props = []

    # Load data either from the saved JSON or live fetch
    if DEV_MODE:
        print("[DEV MODE] Loading props from saved JSON file...")
        all_props = []
        try:
            with open(SAVED_JSON, "r") as f:
                props_data = json.load(f)
                # Since props_data is already a list of props, no need to re-parse.
                all_props.extend(props_data)
        except FileNotFoundError:
            print(f"❌ No saved JSON file found at {SAVED_JSON}. Please fetch live data first.")
            return

        df = pd.DataFrame(all_props)
    else:
        print("[LIVE MODE] Pulling props from TheOddsAPI...")
        events = get_events_for_sport(SPORT_KEY)
        all_props = []  # Initialize an empty list to store all props

        for event in events[:3]:  # ⛔ LIMIT for credits
            event_id = event["id"]
            props_data = get_player_props(event_id, SPORT_KEY)
            if not props_data:
                continue
            
            # Accumulate all props into the list
            parsed = extract_props(props_data.get("bookmakers", []))
            all_props.extend(parsed)

        # After the loop, save all props into the JSON file
        with open(SAVED_JSON, "w") as f:
            json.dump(all_props, f, indent=2)


        # Create dataframe from all accumulated props
        df = pd.DataFrame(all_props)

    # Filter out live bets if INCLUDE_LIVE is False
    if not INCLUDE_LIVE and "commence_time" in df.columns:
        now_utc = datetime.now(timezone.utc)
        df["commence_time"] = pd.to_datetime(df["commence_time"])
        df = df[df["commence_time"] > now_utc]

    # Ensure required columns are present
    required_cols = ["player", "market", "line", "side", "odds", "bookmaker"]
    if not all(col in df.columns for col in required_cols):
        print("⚠️ Missing one or more required columns.")
        print("Available columns:", df.columns.tolist())
        return

    # Clean data: remove missing values and ensure correct data types
    df = df.dropna(subset=["line", "odds"])
    df["line"] = df["line"].astype(float)
    df["odds"] = df["odds"].astype(float)
    df["side"] = df["side"].str.lower()
    df["implied_prob"] = df["odds"].apply(implied_prob)

    if df.empty:
        print("No props found.")
        return

    # Step 1: Compute implied probabilities
    df["implied_prob"] = df["odds"].apply(implied_prob)

    # Step 2: Get best odds per side for each player/market/line combo
    group_cols = ["player", "market", "line", "side"]
    best_odds = df.groupby(group_cols)["odds"].max().reset_index()

    # Step 3: Pivot to put Over/Under odds side-by-side
    pivot = best_odds.pivot(index=["player", "market", "line"], columns="side", values="odds").reset_index()

    # Ensure we have both sides
    if "over" not in pivot.columns or "under" not in pivot.columns:
        print("❌ Pivot missing expected columns. Found:", pivot.columns)
        return

    # Step 4: Calculate no-vig odds (fair probability) for the "over" and "under"
    pivot["fair_prob_over"] = pivot.apply(lambda row: no_vig_prob(row["over"], row["under"]), axis=1)

    # Step 5: Merge fair probabilities back to the dataframe
    df = df.merge(pivot[["player", "market", "line", "fair_prob_over"]], on=["player", "market", "line"], how="left")
    df["fair_prob"] = df.apply(
        lambda row: row["fair_prob_over"] if row["side"] == "over" else 1 - row["fair_prob_over"], axis=1
    )

    # Step 6: Calculate EV
    df["ev"] = df.apply(lambda row: calculate_ev(row["odds"], row["fair_prob"]), axis=1)

    # Filter EV > 0.02 and flag value bets
    ev_df = df[df["ev"] > -0.02].copy()
    ev_df["flag"] = ev_df["ev"].apply(lambda x: "🔥 VALUE" if x > 0.05 else "")
    ev_df = ev_df.sort_values(by="ev", ascending=False)

    # Output results
    print(f"✅ Found {len(ev_df)} props with EV > 2%")
    print(ev_df[["player", "market", "side", "line", "bookmaker", "odds", "fair_prob", "ev", "flag"]].head(10))
    ev_df.to_csv("data/props_outlier_ev.csv", index=False)

    print("Bookmakers from data:", df["bookmaker"].unique())

if __name__ == "__main__":
    run_ev_pipeline()
