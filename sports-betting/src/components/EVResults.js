import React, { useEffect, useState } from 'react';
import { getOdds } from '../api'; // Adjust the import path as needed
import './EVResults.css'; // Optional: for extra styling

const EVResults = () => {
  const [odds, setOdds] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchOdds = async () => {
      try {
        const data = await getOdds();
        setOdds(data);
      } catch (error) {
        console.error('Error fetching odds:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchOdds();
  }, []);

  if (loading) return <div>Loading EV bets...</div>;
  if (odds.length === 0) return <div>No EV bets found.</div>;

  return (
    <div>
      <h2>DFS Lines</h2>
      <table>
        <thead>
          <tr>
            <th>Player</th>
            <th>Bookmaker</th>
            <th>Market</th>
            <th>Side</th>
            <th>Line</th>
            <th>Odds</th>
            <th>EV %</th>
          </tr>
        </thead>
        <tbody>
          {odds.map((odd, index) => (
            <tr key={index}>
              <td>{odd.player}</td>
              <td>{odd.bookmaker}</td>
              <td>{odd.market}</td>
              <td>{odd.side}</td>
              <td>{odd.line}</td>
              <td>{odd.american_odds}</td>
              <td style={{ color: odd.ev > 0 ? 'green' : 'red' }}>
                {(odd.ev * 100).toFixed(2)}%
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default EVResults;
