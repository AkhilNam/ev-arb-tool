import pandas as pd
import json
from datetime import datetime, timezone
from app.odds_api import get_events_for_sport, game_props
from app.parser import extract_game_props
from app.ev_calc import implied_prob

SPORT_KEYS = ["basketball_nba", "americanfootball_nfl", "soccer_epl", "soccer_uefa_champs_league"]  # Add sports here
DEV_MODE = False  # Toggle between live and dev mode
INCLUDE_LIVE = True  # Include live games or not

def run_ev_pipeline():
    all_sports_ev = []

    for sport_key in SPORT_KEYS:
        print(f"\n=== Processing sport: {sport_key} ===")
        all_props = []

        saved_json = f"data/{sport_key}_last_live_pull_game_data.json"

        # Load data
        if DEV_MODE:
            print(f"[DEV MODE] Loading props from saved JSON file: {saved_json}")
            try:
                with open(saved_json, "r") as f:
                    props_data = json.load(f)
                    all_props.extend(props_data)
            except FileNotFoundError:
                print(f"❌ No saved JSON file found at {saved_json}. Please fetch live data first.")
                continue
            df = pd.DataFrame(all_props)
        else:
            print("[LIVE MODE] Pulling props from TheOddsAPI...")
            events = get_events_for_sport(sport_key)
            for event in events:
                event_id = event["id"]
                props_data = game_props(event_id, sport_key)
                if not props_data:
                    continue

                event_name = f"{event.get('home_team')} vs {event.get('away_team')}"
                parsed = extract_game_props(props_data.get("bookmakers", []), event_name)
                all_props.extend(parsed)

            # Save JSON for dev mode reuse
            with open(saved_json, "w") as f:
                json.dump(all_props, f, indent=2)

            df = pd.DataFrame(all_props)

        if df.empty:
            print("❌ DataFrame is empty after fetching props.")
            continue

        if not INCLUDE_LIVE and "commence_time" in df.columns:
            now_utc = datetime.now(timezone.utc)
            df["commence_time"] = pd.to_datetime(df["commence_time"])
            df = df[df["commence_time"] > now_utc]

        required_cols = ["team", "market", "line", "side", "odds", "bookmaker"]
        if not all(col in df.columns for col in required_cols):
            print("⚠️ Missing one or more required columns.")
            print("Available columns:", df.columns.tolist())
            continue

        df = df.dropna(subset=["line", "odds"])
        df["line"] = df["line"].astype(float)
        df["odds"] = df["odds"].astype(float)
        df["side"] = df["side"].str.lower()
        df["implied_prob"] = df["odds"].apply(implied_prob)

        if df.empty:
            print("❌ No props left after cleaning.")
            continue

        totals_df = df[df["market"] == "totals"].copy()
        spreads_df = df[df["market"] == "spreads"].copy()

        ev_totals = process_binary_market(totals_df, "team")

        ev_spreads = []
        if not spreads_df.empty:
            for event_name, df_event in spreads_df.groupby("event_name"):
                print(f"📊 Processing spreads for event: {event_name}")
                ev_event = process_binary_market(df_event, "team")
                if ev_event is not None and not ev_event.empty:
                    ev_spreads.append(ev_event)
            ev_spreads = pd.concat(ev_spreads, ignore_index=True) if ev_spreads else pd.DataFrame()
        else:
            ev_spreads = pd.DataFrame()

        sport_ev_df = pd.concat([ev_totals, ev_spreads], ignore_index=True)
        if sport_ev_df.empty:
            print(f"✅ Found 0 props with EV > 2% for sport {sport_key}")
            continue

        print(f"✅ Found {len(sport_ev_df)} props with EV > 2% for sport {sport_key}")

        sport_ev_df["sport"] = sport_key
        all_sports_ev.append(sport_ev_df)

    if all_sports_ev:
        final_ev_df = pd.concat(all_sports_ev, ignore_index=True)
        final_ev_df = final_ev_df.sort_values(by="ev", ascending=False)

        print(final_ev_df[["sport", "event_name", "team", "market", "side", "line", "bookmaker", "odds", "fair_prob", "ev", "flag"]].head(20))
        final_ev_df.to_csv("data/props_outlier_ev_combined.csv", index=False)
        print("📁 Saved combined results to data/props_outlier_ev_combined.csv")
        return final_ev_df
    else:
        print("❌ No positive EV props found across all sports.")
        return None


def process_binary_market(df_market, id_col):
    if df_market.empty:
        return pd.DataFrame()

    df_market["side"] = df_market["side"].str.lower()

    group_cols = ["event_name", "market", "side"]
    best_odds = df_market.sort_values(by="odds", ascending=False).drop_duplicates(subset=group_cols)

    pivot = best_odds.pivot(index=["event_name", "market"], columns="side", values="odds").reset_index()

    sides = list(df_market["side"].unique())
    if len(sides) != 2:
        print(f"❌ Market '{df_market['market'].iloc[0]}' does not have exactly 2 sides: found {sides}")
        return pd.DataFrame()

    side1, side2 = sides

    if side1 not in pivot.columns or side2 not in pivot.columns:
        print(f"❌ Pivot missing expected sides for market '{df_market['market'].iloc[0]}'. Found columns: {pivot.columns.tolist()}")
        return pd.DataFrame()

    pivot[f"implied_prob_{side1}"] = 1 / pivot[side1]
    pivot[f"implied_prob_{side2}"] = 1 / pivot[side2]

    total_implied = pivot[f"implied_prob_{side1}"] + pivot[f"implied_prob_{side2}"]

    pivot[f"fair_prob_{side1}"] = pivot[f"implied_prob_{side1}"] / total_implied
    pivot[f"fair_prob_{side2}"] = pivot[f"implied_prob_{side2}"] / total_implied

    merge_cols = ["event_name", "market"]
    df_market = df_market.merge(
        pivot[merge_cols + [f"fair_prob_{side1}", f"fair_prob_{side2}"]],
        on=merge_cols,
        how="left"
    )

    df_market["fair_prob"] = df_market.apply(
        lambda row: row.get(f"fair_prob_{row['side']}", None),
        axis=1
    )

    df_market["ev"] = df_market["odds"] * df_market["fair_prob"] - 1

    ev_df = df_market[df_market["ev"] > 0.02].copy()
    ev_df["flag"] = ev_df["ev"].apply(lambda x: "🔥 VALUE" if x > 0.05 else "")
    ev_df = ev_df.sort_values(by="ev", ascending=False)

    return ev_df


if __name__ == "__main__":
    #run_ev_pipeline()
    
    #This is for getting FLIFF odds only 
    df = run_ev_pipeline()
    if not df.empty and (df["bookmaker"].str.lower() == "fliff").any():
        fliff_df = df[df["bookmaker"].str.lower() == "fliff"]
        fliff_df = fliff_df[["bookmaker", "market" , "team" ,"side" , "line", "odds", "event_name" ,"implied_prob","fair_prob","ev", "flag"]]
        print(fliff_df)
        fliff_df.to_csv("data/props_outlier_ev_fliff.csv", index=False)
    else:
        print("No Fliff value props found.")
    