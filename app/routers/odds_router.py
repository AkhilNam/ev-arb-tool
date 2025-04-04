from fastapi import APIRouter
from app.ev_dfs import run_dfs_ev_pipeline
import pandas as pd
import json

router = APIRouter()

# Convert decimal odds to American odds (+120, -150, etc.)
def decimal_to_american(decimal_odds):
    if decimal_odds >= 2:
        return f"+{int((decimal_odds - 1) * 100)}"
    else:
        return f"{int(-100 / (decimal_odds - 1))}"

@router.get("/")
def get_odds():
    SAVED_JSON = "data/last_live_pull.json"

    try:
        with open(SAVED_JSON, "r") as f:
            props_data = json.load(f)

        df = pd.DataFrame(props_data)
        valid_dfs = run_dfs_ev_pipeline(df, ev_threshold=0)
        valid_dfs = valid_dfs.sort_values(by="ev", ascending=False)

        valid_dfs["american_odds"] = valid_dfs["odds"].apply(decimal_to_american)

        return valid_dfs.to_dict(orient="records")

    except Exception as e:
        return {"error": str(e)}
