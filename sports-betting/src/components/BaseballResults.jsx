import React, { useState, useEffect } from 'react';
import { FaSearch, FaFilter, FaSort, FaSortUp, FaSortDown, FaChartLine, FaInfoCircle } from 'react-icons/fa';
import { useTheme } from '../context/ThemeContext';
import { Button } from './ui/button';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { cn } from '../lib/utils';
import { fetchBaseballOdds } from '../api';

const BaseballResults = () => {
  const { theme } = useTheme();
  const [odds, setOdds] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedBookmakers, setSelectedBookmakers] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [itemsPerPage] = useState(10);
  const [showFilters, setShowFilters] = useState(false);
  const [sortConfig, setSortConfig] = useState({ key: 'ev', direction: 'desc' });

  useEffect(() => {
    const fetchData = async () => {
      try {
        const data = await fetchBaseballOdds();
        setOdds(data);
        setLoading(false);
      } catch (err) {
        setError('Failed to fetch baseball odds data');
        setLoading(false);
      }
    };

    fetchData();
    const interval = setInterval(fetchData, 30000);
    return () => clearInterval(interval);
  }, []);

  const handleSort = (key) => {
    setSortConfig(prev => ({
      key,
      direction: prev.key === key && prev.direction === 'asc' ? 'desc' : 'asc'
    }));
  };

  const filteredOdds = odds
    .filter(odd => 
      odd.player.toLowerCase().includes(searchTerm.toLowerCase()) &&
      (selectedBookmakers.length === 0 || selectedBookmakers.includes(odd.bookmaker))
    )
    .sort((a, b) => {
      if (a[sortConfig.key] < b[sortConfig.key]) return sortConfig.direction === 'asc' ? -1 : 1;
      if (a[sortConfig.key] > b[sortConfig.key]) return sortConfig.direction === 'asc' ? 1 : -1;
      return 0;
    });

  const totalPages = Math.ceil(filteredOdds.length / itemsPerPage);
  const currentOdds = filteredOdds.slice(
    (currentPage - 1) * itemsPerPage,
    currentPage * itemsPerPage
  );

  const bookmakers = [...new Set(odds.map(odd => odd.bookmaker))];
  const positiveEVCount = filteredOdds.filter(odd => odd.ev > 0).length;
  const averageEV = filteredOdds.reduce((acc, odd) => acc + odd.ev, 0) / filteredOdds.length || 0;

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <Card className="w-full max-w-md">
          <CardHeader>
            <CardTitle className="text-destructive">Error</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-muted-foreground">{error}</p>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 mb-6">
        <div>
          <h1 className="text-2xl font-bold tracking-tight">Baseball EV Opportunities</h1>
          <p className="text-muted-foreground">Real-time baseball betting opportunities</p>
        </div>
        <div className="flex gap-4 w-full md:w-auto">
          <div className="relative flex-1 md:flex-none">
            <FaSearch className="absolute left-3 top-1/2 transform -translate-y-1/2 text-muted-foreground" />
            <input
              type="text"
              placeholder="Search players..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="pl-10 pr-4 py-2 w-full rounded-md border border-input bg-background text-sm"
            />
          </div>
          <Button
            variant="outline"
            onClick={() => setShowFilters(!showFilters)}
            className="flex items-center gap-2"
          >
            <FaFilter />
            Filters
          </Button>
        </div>
      </div>

      {showFilters && (
        <Card className="mb-6">
          <CardHeader>
            <CardTitle className="text-sm">Bookmakers</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex flex-wrap gap-2">
              {bookmakers.map(bookmaker => (
                <Button
                  key={bookmaker}
                  variant={selectedBookmakers.includes(bookmaker) ? "default" : "outline"}
                  size="sm"
                  onClick={() => {
                    setSelectedBookmakers(prev =>
                      prev.includes(bookmaker)
                        ? prev.filter(b => b !== bookmaker)
                        : [...prev, bookmaker]
                    );
                    setCurrentPage(1);
                  }}
                >
                  {bookmaker}
                </Button>
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center gap-4">
              <div className="p-3 rounded-full bg-primary/10">
                <FaChartLine className="text-primary" />
              </div>
              <div>
                <p className="text-sm text-muted-foreground">Positive EV Bets</p>
                <p className="text-2xl font-bold">{positiveEVCount}</p>
              </div>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center gap-4">
              <div className="p-3 rounded-full bg-primary/10">
                <FaInfoCircle className="text-primary" />
              </div>
              <div>
                <p className="text-sm text-muted-foreground">Average EV</p>
                <p className="text-2xl font-bold">{averageEV.toFixed(2)}%</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      <Card className="overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-input">
                <th
                  className="px-4 py-3 text-left text-sm font-medium text-muted-foreground cursor-pointer"
                  onClick={() => handleSort('player')}
                >
                  Player
                  {sortConfig.key === 'player' && (
                    sortConfig.direction === 'asc' ? <FaSortUp className="inline ml-1" /> : <FaSortDown className="inline ml-1" />
                  )}
                </th>
                <th
                  className="px-4 py-3 text-left text-sm font-medium text-muted-foreground cursor-pointer"
                  onClick={() => handleSort('bookmaker')}
                >
                  Bookmaker
                  {sortConfig.key === 'bookmaker' && (
                    sortConfig.direction === 'asc' ? <FaSortUp className="inline ml-1" /> : <FaSortDown className="inline ml-1" />
                  )}
                </th>
                <th
                  className="px-4 py-3 text-left text-sm font-medium text-muted-foreground cursor-pointer"
                  onClick={() => handleSort('ev')}
                >
                  EV
                  {sortConfig.key === 'ev' && (
                    sortConfig.direction === 'asc' ? <FaSortUp className="inline ml-1" /> : <FaSortDown className="inline ml-1" />
                  )}
                </th>
              </tr>
            </thead>
            <tbody>
              {currentOdds.map((odd, index) => (
                <tr
                  key={index}
                  className={cn(
                    "border-b border-input last:border-0",
                    odd.ev > 0 ? "bg-green-50 dark:bg-green-900/20" : "bg-red-50 dark:bg-red-900/20"
                  )}
                >
                  <td className="px-4 py-3">{odd.player}</td>
                  <td className="px-4 py-3">{odd.bookmaker}</td>
                  <td className={cn(
                    "px-4 py-3 font-medium",
                    odd.ev > 0 ? "text-green-600 dark:text-green-400" : "text-red-600 dark:text-red-400"
                  )}>
                    {odd.ev.toFixed(2)}%
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>

      {totalPages > 1 && (
        <div className="flex justify-center items-center gap-2 mt-6">
          <Button
            variant="outline"
            onClick={() => setCurrentPage(prev => Math.max(prev - 1, 1))}
            disabled={currentPage === 1}
          >
            Previous
          </Button>
          <span className="text-sm text-muted-foreground">
            Page {currentPage} of {totalPages}
          </span>
          <Button
            variant="outline"
            onClick={() => setCurrentPage(prev => Math.min(prev + 1, totalPages))}
            disabled={currentPage === totalPages}
          >
            Next
          </Button>
        </div>
      )}
    </div>
  );
};

export default BaseballResults; 