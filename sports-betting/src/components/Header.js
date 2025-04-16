import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { FaChartLine, FaBasketballBall, FaBaseballBall } from 'react-icons/fa';

const Header = () => {
  const location = useLocation();
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const navItems = [
    { path: '/', label: 'DFS Lines', icon: <FaChartLine /> },
    { path: '/props', label: 'NBA Props', icon: <FaBasketballBall /> },
    { path: '/baseball', label: 'Baseball Props', icon: <FaBaseballBall /> }
  ];

  return (
    <header>
      <div className="header-content">
        <h1>Sports Betting EV Tool</h1>
        <button 
          className="mobile-menu-button"
          onClick={() => setIsMenuOpen(!isMenuOpen)}
          aria-label="Toggle menu"
        >
          <span className={`menu-icon ${isMenuOpen ? 'open' : ''}`}></span>
        </button>
      </div>
      <nav className={`nav-menu ${isMenuOpen ? 'open' : ''}`}>
        <ul>
          {navItems.map((item) => (
            <li key={item.path}>
              <Link 
                to={item.path}
                className={location.pathname === item.path ? 'active' : ''}
              >
                <span className="nav-icon">{item.icon}</span>
                {item.label}
              </Link>
            </li>
          ))}
        </ul>
      </nav>
    </header>
  );
};

export default Header;
