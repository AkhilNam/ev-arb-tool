from fastapi import APIRouter
from app.baseball_pipeline import run_mlb_ev_pipeline  # Make sure this matches your function name
import pandas as pd
import json

router = APIRouter()

def decimal_to_american(decimal_odds: float) -> str:
    if decimal_odds >= 2.0:
        return f"+{int((decimal_odds - 1) * 100)}"
    else:
        return f"-{int(100 / (decimal_odds - 1))}"

@router.get("/")
async def get_baseball_props():
    try:
        props_df = run_mlb_ev_pipeline()
        props_df = props_df.sort_values(by="ev", ascending=False)

        if props_df is None or props_df.empty:
            return []

        # Convert decimal odds to American odds
        props_df["american_odds"] = props_df["odds"].apply(decimal_to_american)

        # Optional: if you added team mapping, it's already in df
        props_list = props_df.to_dict(orient="records")
        return props_list

    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"error": str(e)}
