
# Sports Betting Odds Analysis

This project extracts player prop odds from different sportsbooks, calculates implied probabilities, and evaluates value bets based on the Expected Value (EV) of the bets. The goal is to help identify profitable player prop bets using odds data from various bookmakers.

## Features

- **Data Extraction**: Fetches live odds data from different sportsbooks and saves it in a JSON file.
- **Data Processing**: Parses the data to extract player props, markets, and odds.
- **Implied Probabilities**: Calculates implied probabilities for both "Over" and "Under" bets based on the odds.
- **Fair Odds Calculation**: Computes no-vig odds (fair odds) to determine the true probability of an event.
- **EV Calculation**: Evaluates bets based on their expected value (EV), helping to identify value bets with higher potential returns.
- **CSV Output**: Exports filtered bets with a high EV to a CSV file for further analysis.

## Requirements

- Python 3.6+
- Pandas
- Requests
- JSON
- [TheOddsAPI](https://theoddsapi.com/) for fetching live odds data

## Setup Instructions

1. **Clone the repository**:

   ```bash
   git clone https://github.com/yourusername/sports-betting-odds-analysis.git
   cd sports-betting-odds-analysis
   ```

2. **Create a virtual environment** (optional but recommended):

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # For macOS/Linux
   venv\Scriptsctivate     # For Windows
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **API Key for TheOddsAPI**: Sign up at [TheOddsAPI](https://theoddsapi.com/) and get an API key. 
   
   - Create a `.env` file in the root of the project directory and add your API key:
     
     ```bash
     THEODDSAPI_KEY=your_api_key_here
     ```

5. **Run the Script**: 

   To fetch live data and process the props:

   ```bash
   python sports_betting_pipeline.py
   ```

   The script will pull player props data, process it, calculate EV, and save results to `props_outlier_ev.csv`.

## How It Works

1. **Data Fetching**: 
   The script uses TheOddsAPI to fetch live event data for NBA games. It retrieves player props from bookmakers like FanDuel, DraftKings, and others.

2. **Data Extraction**: 
   The `extract_props()` function parses the raw event data and extracts relevant information such as the player name, market (e.g., points, assists), side (Over/Under), odds, and bookmaker.

3. **Implied Probability Calculation**:
   The implied probability of a bet is calculated using the formula:

   \[
   	ext{Implied Probability} = rac{1}{	ext{Odds}}
   \]

4. **No-Vig Odds**: 
   The `no_vig_prob()` function removes the vig (house edge) from odds and calculates the "true" probability of each bet.

5. **Expected Value (EV) Calculation**: 
   The expected value is computed using the formula:

   \[
   	ext{EV} = (	ext{Win Probability} 	imes 	ext{Odds}) - 1
   \]

   The script filters out bets with a negative EV and identifies "value bets" with a high positive EV.

6. **Output**: 
   The filtered results with a high EV are saved to a CSV file (`props_outlier_ev.csv`), which includes details like player, market, odds, fair probability, and EV.

## Configuration

- **DEV_MODE**: Set to `True` to load data from a saved JSON file for testing or development. Set to `False` to fetch live data.
- **INCLUDE_LIVE**: Set to `True` to include live bets, or `False` to exclude live bets from the analysis.
- **SAVED_JSON**: Path to the JSON file that contains the saved data if `DEV_MODE` is enabled.

## Example Output

The output CSV file (`props_outlier_ev.csv`) will look like this:

| player       | market          | side | line  | bookmaker   | odds | fair_prob | ev     | flag  |
|--------------|-----------------|------|-------|-------------|------|-----------|--------|-------|
| Jordan Poole | player_points   | Over | 12.5  | FanDuel     | 1.96 | 0.5125    | 0.022  | 🔥 VALUE |
| AJ Johnson   | player_points   | Under| 16.5  | DraftKings  | 1.78 | 0.5334    | 0.018  |       |

## Contributing

Feel free to fork the repository and submit pull requests. Contributions are welcome!

### How to Contribute:

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature-name`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add new feature'`).
5. Push to the branch (`git push origin feature-name`).
6. Create a new Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [TheOddsAPI](https://theoddsapi.com/) for providing the live odds data.
- Various sportsbooks for their player props data.
