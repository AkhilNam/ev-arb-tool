import React, { useEffect, useState } from 'react';
import { getBaseballProps } from '../api'; 
import './EVResults.css'; // Reuse styling

const BaseballProps = () => {
  const [props, setProps] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchProps = async () => {
      try {
        const data = await getBaseballProps(); 
        setProps(data);
      } catch (error) {
        console.error('Error fetching baseball props:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchProps();
  }, []);

  if (loading) return <div>Loading baseball props...</div>;
  if (props.length === 0) return <div>No baseball props found.</div>;

  return (
    <div>
      <h2>Baseball Props</h2>
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
          {props.map((prop, index) => (
            <tr key={index}>
              <td>{prop.player}</td>
              <td>{prop.bookmaker}</td>
              <td>{prop.market}</td>
              <td>{prop.side}</td>
              <td>{prop.line}</td>
              <td>{prop.american_odds}</td>
              <td style={{ color: prop.ev > 0 ? 'green' : 'red' }}>
                {(prop.ev * 100).toFixed(2)}%
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default BaseballProps;
