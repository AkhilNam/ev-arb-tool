import React from 'react';
import { Link } from 'react-router-dom';

const Header = () => {
  return (
    <header>
      <h1>Sports Betting EV Tool</h1>
      <nav>
        <ul>
          <li><Link to="/">DFS Lines</Link></li>
          <li><Link to="/props">NBA Props</Link></li>
          <li><Link to="/baseball">Baseball Props</Link></li>
        </ul>
      </nav>
    </header>
  );
};

export default Header;
