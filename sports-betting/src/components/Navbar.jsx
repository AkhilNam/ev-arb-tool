import React from 'react';
import { Link } from 'react-router-dom';
import { 
  FaChartLine, 
  FaCalculator, 
  FaHistory, 
  FaCog, 
  FaBaseballBall, 
  FaChartBar, 
  FaFootballBall, 
  FaBasketballBall 
} from 'react-icons/fa';
import ThemeToggle from './ThemeToggle';
import { Button } from './ui/button';

const Navbar = () => {
  return (
    <nav className="sticky top-0 z-50 w-full border-b border-border/40 bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container flex h-16 items-center px-4">
        <div className="mr-4 hidden md:flex">
          <Link to="/" className="mr-6 flex items-center space-x-2">
            <FaChartLine className="h-6 w-6 text-primary" />
            <span className="hidden font-bold sm:inline-block">
              EV Betting Tool
            </span>
          </Link>
          <nav className="flex items-center space-x-4 text-sm font-medium">
            <Link
              to="/"
              className="transition-colors hover:text-foreground/80 text-foreground flex items-center space-x-1"
            >
              <FaChartLine className="h-4 w-4" />
              <span>Dashboard</span>
            </Link>
            <Link
              to="/baseball"
              className="transition-colors hover:text-foreground/80 text-foreground/60 flex items-center space-x-1"
            >
              <FaBaseballBall className="h-4 w-4" />
              <span>Baseball</span>
            </Link>
            <Link
              to="/ncaab"
              className="transition-colors hover:text-foreground/80 text-foreground/60 flex items-center space-x-1"
            >
              <FaBasketballBall className="h-4 w-4" />
              <span>NCAAB</span>
            </Link>
            <Link
              to="/dfs"
              className="transition-colors hover:text-foreground/80 text-foreground/60 flex items-center space-x-1"
            >
              <FaChartBar className="h-4 w-4" />
              <span>DFS</span>
            </Link>
            <Link
              to="/featured"
              className="transition-colors hover:text-foreground/80 text-foreground/60 flex items-center space-x-1"
            >
              <FaFootballBall className="h-4 w-4" />
              <span>Featured</span>
            </Link>
            <Link
              to="/calculator"
              className="transition-colors hover:text-foreground/80 text-foreground/60 flex items-center space-x-1"
            >
              <FaCalculator className="h-4 w-4" />
              <span>Calculator</span>
            </Link>
            <Link
              to="/history"
              className="transition-colors hover:text-foreground/80 text-foreground/60 flex items-center space-x-1"
            >
              <FaHistory className="h-4 w-4" />
              <span>History</span>
            </Link>
          </nav>
        </div>
        
        {/* Mobile Navigation */}
        <div className="md:hidden">
          <Button variant="ghost" className="mr-2" size="icon">
            <FaChartLine className="h-5 w-5" />
          </Button>
        </div>

        <div className="flex flex-1 items-center justify-between space-x-2 md:justify-end">
          <div className="w-full flex-1 md:w-auto md:flex-none">
            <div className="relative">
              <input
                type="search"
                placeholder="Search bets..."
                className="block h-9 w-full rounded-md border border-input bg-background px-3 py-1 text-sm shadow-sm transition-colors placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring"
              />
            </div>
          </div>
          <nav className="flex items-center">
            <Button variant="ghost" size="icon" className="mr-2">
              <FaCog className="h-5 w-5" />
              <span className="sr-only">Settings</span>
            </Button>
            <ThemeToggle />
          </nav>
        </div>
      </div>
    </nav>
  );
};

export default Navbar; 