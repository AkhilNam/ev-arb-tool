import json
from collections import defaultdict

def find_arbitrage_bets(data, investment=100):
    grouped = defaultdict(lambda: {"Over": [], "Under": []})
    arb_opportunities = []

    for bet in data:
        key = (bet["player"], bet["market"], bet["line"])
        grouped[key][bet["side"]].append(bet)

    for (player, market, line), outcomes in grouped.items():
        if "Over" in outcomes and "Under" in outcomes:
            best_over = max(outcomes["Over"], key=lambda x: x["odds"], default=None)
            best_under = max(outcomes["Under"], key=lambda x: x["odds"], default=None)

            if not best_over or not best_under:
                continue

            inverse_sum = (1 / best_over["odds"]) + (1 / best_under["odds"])

            if inverse_sum < 1:
                payout = investment / inverse_sum
                profit = payout - investment

                if profit < 2:
                    continue  # Skip if profit is under $2

                bet_over_amt = (1 / best_over["odds"]) * payout
                bet_under_amt = (1 / best_under["odds"]) * payout

                arb_opportunities.append({
                    "player": player,
                    "market": market,
                    "line": line,
                    "profit": profit,
                    "payout": payout,
                    "bet_over": bet_over_amt,
                    "bet_under": bet_under_amt,
                    "book_over": best_over["bookmaker"],
                    "book_under": best_under["bookmaker"],
                    "odds_over": best_over["odds"],
                    "odds_under": best_under["odds"]
                })

    # Sort by biggest profit first
    arb_opportunities.sort(key=lambda x: x["profit"], reverse=True)

    for arb in arb_opportunities:
        print(f"\n🔥 Arbitrage opportunity for {arb['player']} | {arb['market']} | Line: {arb['line']}")
        print(f"  ➕ Over  @ {arb['book_over']}  | Odds: {arb['odds_over']}  | Bet: ${arb['bet_over']:.2f}")
        print(f"  ➖ Under @ {arb['book_under']} | Odds: {arb['odds_under']} | Bet: ${arb['bet_under']:.2f}")
        print(f"  📈 Profit: ${arb['profit']:.2f} on ${investment} investment")

if __name__ == "__main__":
    with open("data/last_live_pull.json") as f:
        odds_data = json.load(f)

    find_arbitrage_bets(odds_data)
