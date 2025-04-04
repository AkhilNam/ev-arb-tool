from fastapi import APIRouter
from app.ev_pipeline import run_ev_pipeline
from app.odds_api import get_events_for_sport, get_player_props

router = APIRouter()

def decimal_to_american(decimal_odds: float) -> str:
    if decimal_odds >= 2.0:
        return f"+{int((decimal_odds - 1) * 100)}"
    else:
        return f"-{int(100 / (decimal_odds - 1))}"


@router.get("/")
async def get_all_props():
    try:
        props_df = run_ev_pipeline()
        props_df = props_df.sort_values(by="ev", ascending=False)
        if props_df is None or props_df.empty:
            return []

        # Convert decimal odds to American odds
        props_df["american_odds"] = props_df["odds"].apply(decimal_to_american)

        # Convert to list of dicts
        props_list = props_df.to_dict(orient="records")
        return props_list

    except Exception as e:
        import traceback
        traceback.print_exc()
        return []


