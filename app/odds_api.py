import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("THE_ODDS_API_KEY")
BASE_URL = "https://api.the-odds-api.com/v4/sports"

def fetch_odds(sport_key="basketball_nba", regions="us,us2,us_dfs,us_ex",  markets="h2h,spreads", odds_format="american"):
    url = f"{BASE_URL}/{sport_key}/odds"
    params = {
        "apiKey": API_KEY,
        "regions": regions,
        "markets": markets,
        "oddsFormat": odds_format
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        print("Error:", response.status_code, response.text)
        return []
def list_bookmakers(sport_key="basketball_nba"):
    url = f"https://api.the-odds-api.com/v4/sports/{sport_key}/odds"
    params = {
        "apiKey": API_KEY,
        "regions": "us,us2,us_dfs,us_ex",
        "markets": "h2h",
    }   
    res = requests.get(url, params=params)

    seen = set()
    for game in res.json():
        for book in game.get("bookmakers", []):
            if book['key'] not in seen:
                seen.add(book['key'])
                print(f"{book['title']} ({book['key']})")


def get_all_sports():
    url = "https://api.the-odds-api.com/v4/sports"
    params = {
        "apiKey": API_KEY
    }
    res = requests.get(url, params=params)

    if res.status_code != 200:
        print(f"Failed to fetch sports. Status code: {res.status_code}")
        return []

    sports = res.json()
    print(f"{'Sport':35} | {'Key':30} | {'Active'}")
    print("-" * 75)
    for s in sports:
        title = s['title'][:35]
        key = s['key'][:30]
        active = 'Yes' if s['active'] else 'No'
        print(f"{title:35} | {key:30} | {active}")

    return sports

def get_active_sports():
    url = "https://api.the-odds-api.com/v4/sports"
    params = { "apiKey": API_KEY }

    res = requests.get(url, params=params)
    if res.status_code != 200:
        print(f"Error fetching sports: {res.status_code}")
        return []

    sports = [s for s in res.json() if s['active']]
    print(f"\n{'Sport':30} | {'Key'}")
    print("-" * 60)
    for s in sports:
        print(f"{s['title'][:30]:30} | {s['key']}")
    return sports

def get_events_for_sport(sport_key):
    url = f"https://api.the-odds-api.com/v4/sports/{sport_key}/events"
    params = { "apiKey": API_KEY }

    res = requests.get(url, params=params)
    if res.status_code != 200:
        print(f"Failed to fetch events: {res.status_code}")
        return []

    events = res.json()
    print(f"\nEvents for {sport_key}:\n")
    for i, event in enumerate(events):
        print(f"{i}: {event['id']} | {event['home_team']} vs {event['away_team']} | {event['commence_time']}")
    return events

def get_player_props(event_id, sport_key):
    url = f"https://api.the-odds-api.com/v4/sports/{sport_key}/events/{event_id}/odds"

    markets = [
        "player_points", "player_rebounds", "player_assists", "player_threes", "player_blocks", "player_points_rebounds_assists", "player_points_rebounds", "player_points_assists", "player_rebounds_assists"
    ]

    params = {
        "apiKey": API_KEY,
        "regions": "us,us2,us_dfs",
        "markets": ",".join(markets),
        "oddsFormat": "decimal"
    }

    res = requests.get(url, params=params)
    if res.status_code != 200:
        print(f"❌ Failed to fetch odds: {res.status_code}")
        print(res.text)
        return None

    return res.json()

def get_player_props_mlb(event_id, sport_key):
    url = f"https://api.the-odds-api.com/v4/sports/{sport_key}/events/{event_id}/odds"

    markets = [
    "batter_home_runs",
    "batter_first_home_run",
    "batter_hits",
    "batter_total_bases",
    "batter_rbis",
    "batter_runs_scored",
    "batter_hits_runs_rbis",
    "batter_singles",
    "batter_doubles",
    "batter_triples",
    "batter_walks",
    "batter_strikeouts",
    "batter_stolen_bases",
    "pitcher_strikeouts",
    "pitcher_record_a_win",
    "pitcher_hits_allowed",
    "pitcher_walks",
    "pitcher_earned_runs",
    "pitcher_outs"
    ]


    params = {
        "apiKey": API_KEY,
        "regions": "us,us2,us_dfs",
        "markets": ",".join(markets),
        "oddsFormat": "decimal"
    }

    res = requests.get(url, params=params)
    if res.status_code != 200:
        print(f"❌ Failed to fetch odds: {res.status_code}")
        print(res.text)
        return None

    return res.json()

def game_props(event_id, sport_key):
    url = f"https://api.the-odds-api.com/v4/sports/{sport_key}/events/{event_id}/odds"

    markets = [
        "h2h", "spreads", "totals", "h2h_lay"
    ]

    params = {
        "apiKey": API_KEY,
        "regions": "us,us2,us_dfs",
        "markets": ",".join(markets),
        "oddsFormat": "decimal"
    }

    res = requests.get(url, params=params)
    if res.status_code != 200:
        print(f"❌ Failed to fetch odds: {res.status_code}")
        print(res.text)
        return None

    return res.json()