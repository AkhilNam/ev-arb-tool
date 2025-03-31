from dotenv import load_dotenv
import os

load_dotenv()

THE_ODDS_API_KEY = os.getenv("THE_ODDS_API_KEY")
FETCH_INTERVAL_MINUTES = int(os.getenv("FETCH_INTERVAL_MINUTES", 5))
LOG_FILE = os.getenv("LOG_FILE", "data/logs.csv")
