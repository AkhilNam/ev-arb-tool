def extract_props(bookmakers_data):
    props = []
    
    # Iterate over the bookmaker data
    for bookmaker in bookmakers_data:
        bookmaker_name = bookmaker.get("title", "")
        
        # Check if 'markets' is in the bookmaker data
        if "markets" not in bookmaker:
            print(f"❌ Missing 'markets' for bookmaker {bookmaker_name}")
            continue  # Skip this bookmaker if 'markets' is missing
        
        # Handle new sportsbooks
        if bookmaker_name in ["Underdog", "PrizePicks"]:
            for market in bookmaker["markets"]:
                # Check if 'outcomes' is in the market data
                if "outcomes" not in market:
                    print(f"❌ Missing 'outcomes' for market {market.get('key', 'unknown')} from bookmaker {bookmaker_name}")
                    continue
                
                for outcome in market["outcomes"]:
                    prop = {
                        "bookmaker": bookmaker_name,
                        "market": market.get("key", "unknown"),
                        "player": outcome.get("description", "unknown"),
                        "side": outcome.get("name", "unknown"),
                        "line": outcome.get("point", None),  # Allow None if the line is missing
                        "odds": outcome.get("price", None),  # Allow None if the odds are missing
                    }
                    props.append(prop)
        else:
            # Existing logic for other sportsbooks
            for market in bookmaker["markets"]:
                if "outcomes" not in market:
                    print(f"❌ Missing 'outcomes' for market {market.get('key', 'unknown')} from bookmaker {bookmaker_name}")
                    continue

                for outcome in market["outcomes"]:
                    prop = {
                        "bookmaker": bookmaker_name,
                        "market": market.get("key", "unknown"),
                        "player": outcome.get("description", "unknown"),
                        "side": outcome.get("name", "unknown"),
                        "line": outcome.get("point", None),
                        "odds": outcome.get("price", None),
                    }
                    props.append(prop)

    return props
