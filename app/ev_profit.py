import pandas as pd

def calculate_expected_profit(log_file="placed_bets.csv", stake=10):
    """
    Reads the placed bets log, assumes a fixed stake per bet,
    and calculates the expected profit for each bet.
    
    For straight bets, it uses the 'ev' column.
    For parlay bets, it uses the 'parlay_ev' column if available.
    
    Expected profit per bet = stake * EV.
    
    A summary is printed, including:
      - Total number of bets
      - Total expected profit
      - Average EV across bets
      - Breakdown by bet type (if 'bet_type' column exists)
    
    Parameters:
      log_file: Path to the CSV file with placed bets.
      stake: Dollar amount assumed to be placed on each bet.
    
    Returns:
      The DataFrame with an added 'expected_profit' column.
    """
    try:
        df = pd.read_csv(log_file)
    except FileNotFoundError:
        print(f"Log file {log_file} not found.")
        return

    # Function to compute expected profit per row
    def compute_profit(row):
        # Check if a bet type is logged. Default to straight if missing.
        bet_type = row.get("bet_type", "straight")
        if isinstance(bet_type, str) and bet_type.lower() == "parlay":
            # Use parlay_ev if available; otherwise, fallback to ev.
            ev = row.get("parlay_ev")
            if pd.isna(ev):
                ev = row.get("ev", 0)
        else:
            ev = row.get("ev", 0)
        return stake * ev

    df["expected_profit"] = df.apply(compute_profit, axis=1)

    # Overall summary
    total_bets = len(df)
    total_expected_profit = df["expected_profit"].sum()
    avg_ev = df["expected_profit"].mean() / stake if total_bets > 0 else 0

    print("=== Expected Profit Summary ===")
    print(f"Total bets placed: {total_bets}")
    print(f"Total expected profit (assuming ${stake} per bet): ${total_expected_profit:.2f}")
    print(f"Average EV: {avg_ev:.3f}")

    # Optional breakdown by bet type if the column exists
    if "bet_type" in df.columns:
        print("\nBreakdown by bet type:")
        summary = df.groupby("bet_type")["expected_profit"].agg(["count", "sum", "mean"])
        summary["average_ev"] = summary["mean"] / stake
        print(summary)

    return df

if __name__ == "__main__":
    calculate_expected_profit(log_file="placed_bets.csv", stake=10)
