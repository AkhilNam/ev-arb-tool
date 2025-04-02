def extract_props(data):
    props = []
    for bookmaker in data.get("bookmakers", []):
        book_name = bookmaker["title"]
        for market in bookmaker.get("markets", []):
            market_key = market["key"]
            for outcome in market.get("outcomes", []):
                props.append({
                    "bookmaker": book_name,
                    "market": market_key,
                    "player": outcome["name"],
                    "line": outcome.get("point"),
                    "odds": outcome["price"],
                    "side": "over" if "Over" in outcome["name"] else "under"
                })
    return props
