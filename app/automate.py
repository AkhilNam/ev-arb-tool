from ev_pipeline import run_ev_pipeline
from bet_planner import process_and_place_bets
from ev_dfs import run_dfs_ev_pipeline
import json
import pandas as pd
all_props = []
def auto():
    ev_df = run_ev_pipeline()
    process_and_place_bets(ev_df)
    SAVED_JSON = "data/last_live_pull.json"
    with open(SAVED_JSON, "r") as f:
        props_data = json.load(f)
        all_props.extend(props_data)
        
    df = pd.DataFrame(all_props)

    valid_dfs = run_dfs_ev_pipeline(df)
    process_and_place_bets(valid_dfs)

if __name__ == "__main__":
    auto()