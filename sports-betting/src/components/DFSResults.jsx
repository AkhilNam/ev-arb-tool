import React, { useState, useEffect } from 'react';
import { FaSearch, FaFilter, FaSort, FaSortUp, FaSortDown, FaChartLine, FaInfoCircle } from 'react-icons/fa';
import { useTheme } from '../context/ThemeContext';
import { Button } from './ui/button';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { cn } from '../lib/utils';
import { fetchDfsData } from '../api';

const DFSResults = () => {
  const { theme } = useTheme();
  const [dfsData, setDfsData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [currentPage, setCurrentPage] = useState(1);
  const [itemsPerPage] = useState(10);
  const [showFilters, setShowFilters] = useState(false);
  const [sortConfig, setSortConfig] = useState({ key: 'value', direction: 'desc' });

  useEffect(() => {
    const fetchData = async () => {
      try {
        const data = await fetchDfsData();
        setDfsData(Array.isArray(data) ? data : []);
        setLoading(false);
      } catch (err) {
        setError('Failed to fetch DFS data');
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

  const filteredData = (dfsData || [])
    .filter(item => 
      item.player.toLowerCase().includes(searchTerm.toLowerCase())
    )
    .sort((a, b) => {
      if (a[sortConfig.key] < b[sortConfig.key]) return sortConfig.direction === 'asc' ? -1 : 1;
      if (a[sortConfig.key] > b[sortConfig.key]) return sortConfig.direction === 'asc' ? 1 : -1;
      return 0;
    });

  const totalPages = Math.ceil(filteredData.length / itemsPerPage);
  const currentItems = filteredData.slice(
    (currentPage - 1) * itemsPerPage,
    currentPage * itemsPerPage
  );

  const averageValue = filteredData.length > 0
    ? filteredData.reduce((acc, item) => acc + item.value, 0) / filteredData.length
    : 0;
  const highValueCount = filteredData.filter(item => item.value > averageValue).length;

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
          <h1 className="text-2xl font-bold tracking-tight">DFS Value Plays</h1>
          <p className="text-muted-foreground">Daily Fantasy Sports value opportunities</p>
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

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center gap-4">
              <div className="p-3 rounded-full bg-primary/10">
                <FaChartLine className="text-primary" />
              </div>
              <div>
                <p className="text-sm text-muted-foreground">High Value Players</p>
                <p className="text-2xl font-bold">{highValueCount}</p>
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
                <p className="text-sm text-muted-foreground">Average Value</p>
                <p className="text-2xl font-bold">{averageValue.toFixed(2)}</p>
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
                  className="px-4 py-3 text-left text-sm font-medium text-muted-foreground cursor-pointer hover:text-foreground transition-colors"
                  onClick={() => handleSort('player')}
                >
                  Player
                  {sortConfig.key === 'player' && (
                    sortConfig.direction === 'asc' ? <FaSortUp className="inline ml-1" /> : <FaSortDown className="inline ml-1" />
                  )}
                </th>
                <th
                  className="px-4 py-3 text-left text-sm font-medium text-muted-foreground cursor-pointer hover:text-foreground transition-colors"
                  onClick={() => handleSort('salary')}
                >
                  Salary
                  {sortConfig.key === 'salary' && (
                    sortConfig.direction === 'asc' ? <FaSortUp className="inline ml-1" /> : <FaSortDown className="inline ml-1" />
                  )}
                </th>
                <th
                  className="px-4 py-3 text-left text-sm font-medium text-muted-foreground cursor-pointer hover:text-foreground transition-colors"
                  onClick={() => handleSort('projection')}
                >
                  Projection
                  {sortConfig.key === 'projection' && (
                    sortConfig.direction === 'asc' ? <FaSortUp className="inline ml-1" /> : <FaSortDown className="inline ml-1" />
                  )}
                </th>
                <th
                  className="px-4 py-3 text-left text-sm font-medium text-muted-foreground cursor-pointer hover:text-foreground transition-colors"
                  onClick={() => handleSort('value')}
                >
                  Value
                  {sortConfig.key === 'value' && (
                    sortConfig.direction === 'asc' ? <FaSortUp className="inline ml-1" /> : <FaSortDown className="inline ml-1" />
                  )}
                </th>
              </tr>
            </thead>
            <tbody>
              {currentItems.map((item, index) => (
                <tr
                  key={index}
                  className={cn(
                    "border-b border-input last:border-0 transition-colors",
                    item.value > averageValue 
                      ? "bg-green-50/50 hover:bg-green-100/50 dark:bg-green-900/10 dark:hover:bg-green-900/20" 
                      : "bg-red-50/50 hover:bg-red-100/50 dark:bg-red-900/10 dark:hover:bg-red-900/20"
                  )}
                >
                  <td className="px-4 py-3 text-foreground">{item.player}</td>
                  <td className="px-4 py-3 text-foreground">${item.salary.toLocaleString()}</td>
                  <td className="px-4 py-3 text-foreground">{item.projection.toFixed(1)}</td>
                  <td className={cn(
                    "px-4 py-3 font-medium",
                    item.value > averageValue 
                      ? "text-green-700 dark:text-green-400" 
                      : "text-red-700 dark:text-red-400"
                  )}>
                    {item.value.toFixed(2)}
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

export default DFSResults; 