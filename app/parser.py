def extract_props(bookmakers_data):
    props = []
    
    # Iterate over the bookmaker data
    for bookmaker in bookmakers_data:
        bookmaker_name = bookmaker.get("title", "")
        
        if bookmaker_name in ["Underdog", "PrizePicks"]:  # Handle new sportsbooks
            for market in bookmaker["markets"]:
                for outcome in market["outcomes"]:
                    prop = {
                        "bookmaker": bookmaker_name,
                        "market": market["key"],
                        "player": outcome["description"],
                        "side": outcome["name"],
                        "line": outcome["point"],
                        "odds": outcome["price"],
                    }
                    props.append(prop)
        else:
            # Existing logic for other sportsbooks
            for market in bookmaker["markets"]:
                for outcome in market["outcomes"]:
                    prop = {
                        "bookmaker": bookmaker_name,
                        "market": market["key"],
                        "player": outcome["description"],
                        "side": outcome["name"],
                        "line": outcome["point"],
                        "odds": outcome["price"],
                    }
                    props.append(prop)
    return props
