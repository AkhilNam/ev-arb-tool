def extract_props(bookmakers):
    props = []
    for book in bookmakers:
        bookmaker = book["title"]
        for market in book.get("markets", []):
            market_key = market.get("key")
            for outcome in market.get("outcomes", []):
                props.append({
                    "bookmaker": bookmaker,
                    "market": market_key,
                    "player": outcome.get("description", "Unknown Player"),
                    "side": outcome.get("name", ""),
                    "line": outcome.get("point"),
                    "odds": outcome.get("price")
                })
    return props
