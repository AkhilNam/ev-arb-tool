# EV-Arb-Tool

EV-Arb-Tool is a Python-based project that identifies and processes positive EV bets across multiple sportsbooks and DFS (Daily Fantasy Sports) platforms. The tool calculates fair probabilities, expected values (EV), and applies platform-specific bet placement logic (e.g., grouping bets into parlays when needed). All placed bets are logged for tracking and performance analysis.

## Features

- **EV Calculation Pipeline:**  
  - Computes implied probabilities from odds.  
  - Uses average odds from non-DFS books to determine fair probabilities (removing the bookmaker’s vig).  
  - Calculates EV using custom logic (via `calculate_ev`).

- **DFS-Specific Strategy:**  
  - Separates DFS bets (e.g., Fliff, PrizePicks, Underdog) from other markets.  
  - Automatically groups bets from PrizePicks and Underdog into parlays (since they do not support straight legs).  
  - Places bets as "straight" on all other platforms.

- **Bet Selection & Duplicate Handling:**  
  - Ensures that across all platforms, only one bet per unique player/market/line combination is placed. For example, if you take the over 24.5 points for a player, you will not take the under for the same line—even if the EV is the same, the bet with better fair odds is selected.  
  - If multiple bets exist for the same line (from different platforms), the one with the highest EV (and, if tied, the highest fair probability) is chosen.
  
- **Logging:**  
  - Logs every placed bet (with its bet type) to a CSV file (`placed_bets.csv`), including bets from normal sportsbooks that aren’t DFS.
  - Prevents duplicate placements by checking if a bet for the same player/market/line has already been placed on the same day.

## Installation

1. **Clone the Repository:**

   ```bash
   git clone <repository_url>
   cd ev-arb-tool
