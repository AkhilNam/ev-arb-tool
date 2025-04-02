from odds_api import get_all_sports
from odds_api import list_bookmakers, get_active_sports, get_events_for_sport, get_player_props
from parser import extract_props

sports = get_active_sports()
# Pick a sport_key like "basketball_nba"
events = get_events_for_sport("basketball_nba")
# Pick an event index or ID
event_id = events[0]['id']
props = get_player_props(event_id, "basketball_nba")

print(extract_props(props))