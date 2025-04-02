import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("THE_ODDS_API_KEY")
BASE_URL = "https://api.the-odds-api.com/v4/sports"

def fetch_odds(sport_key="basketball_nba", regions="us", markets="h2h,spreads", odds_format="american"):
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
        "regions": "us",
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

