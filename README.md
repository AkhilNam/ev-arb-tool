# EV-Arb-Tool

EV-Arb-Tool is a full-stack Python + React project that identifies and processes positive EV (expected value) bets across multiple sportsbooks and DFS (Daily Fantasy Sports) platforms. The tool calculates fair probabilities, expected values (EV), and applies platform-specific bet placement logic. It now includes a web dashboard for easy viewing of props and EV data, with dedicated pages for general props, DFS lines, and MLB props.

![EV Tool Screenshot](https://via.placeholder.com/1200x400.png?text=EV-Arb-Tool+Dashboard)

## Features

### 📊 EV Calculation Pipeline (Python Backend)
- Computes implied probabilities from odds.
- Uses average odds from non-DFS books to determine fair probabilities (removing the bookmaker's vig).
- Calculates EV using custom logic (via calculate_ev).
- Filters out extreme odds for cleaner, more reliable EV bets.
- Includes a dedicated MLB pipeline for baseball props.

### 🏀 DFS-Specific Strategy
- Separates DFS bets (e.g., Fliff, PrizePicks, Underdog) from sportsbook bets.
- Groups bets from PrizePicks and Underdog into parlays (since they do not support straight bets).
- Places bets as "straight" on all other platforms.
- Advanced DFS lineup optimization with customizable constraints.
- Real-time player pool updates and contest tracking.

### 🧩 Bet Selection & Duplicate Handling
- Ensures only one bet per unique player/market/line combination is placed.
- Prioritizes the bet with the highest EV (and higher fair probability in case of a tie).
- Prevents duplicate placements by checking against already placed bets.

### 🖥️ Web Dashboard (React Frontend)
- View EV bets in a clean, responsive dashboard.
- Dedicated pages:
  - DFS Lines: DFS-specific EV plays and lineup optimization.
  - All Props: Complete prop list across sports.
  - Baseball Props: MLB-only EV bets.
- Auto-formatted American odds.
- Color-coded EV % values (green for positive, red for negative).
- Persistent header and footer for smooth navigation.
- Dark mode support with modern UI components.

### 🗂️ Logging
- Logs every placed bet to placed_bets.csv.
- Records sportsbooks and DFS platforms bets separately.
- Tracks bets to avoid duplication.

## Installation

### 1. Clone the Repository

git clone <repository_url>
cd ev-arb-tool

### 2. Backend Setup (Python)

- Create virtual environment:

python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\\Scripts\\activate     # Windows

- Install dependencies:

pip install -r requirements.txt

- Run FastAPI server:

uvicorn app.app:app --reload --port 8001

Your backend will now be running at:
http://127.0.0.1:8001

### 3. Frontend Setup (React)

- Navigate to the frontend directory:

cd sports-betting
npm install
npm start

Your React app will run at:
http://localhost:3000

### 4. Access Web Dashboard

- Visit:
  - http://localhost:3000/ → DFS Lines
  - http://localhost:3000/props → All Props
  - http://localhost:3000/baseball → Baseball Props (MLB)

## API Routes (FastAPI)

| Endpoint           | Description                       |
|-------------------|-----------------------------------|
| /api/odds         | DFS lines EV bets                 |
| /api/props        | All props across sports           |
| /api/baseball     | MLB-only EV props                 |
| /api/dfs          | DFS contests and lineups          |

Access live API docs at:
http://127.0.0.1:8001/docs

## DFS API Endpoints

| Endpoint                      | Method | Description                          |
|------------------------------|--------|--------------------------------------|
| /api/dfs                     | GET    | List all available DFS contests      |
| /api/dfs/player-pool         | GET    | Get player pool for specific contest |
| /api/dfs/optimize            | POST   | Optimize lineup with constraints     |

## Roadmap 🚀

- [x] Auto-refresh frontend (Live odds updates)
- [x] Add dark mode support
- [x] Modern UI components with shadcn/ui
- [ ] CSV export from frontend dashboard
- [ ] Add filtering by market and EV %
- [ ] Add team logos for cleaner visuals
- [ ] Deployment to web hosting (Netlify / Vercel / Render)

## Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

## License

MIT License

## Contact

Questions or suggestions? Open an issue or reach out!