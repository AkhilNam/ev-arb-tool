// src/App.js
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider } from './context/ThemeContext';
import EVResults from './components/EVResults';
import BaseballResults from './components/BaseballResults';
import NcaabResults from './components/NcaabResults';
import DFSResults from './components/DFSResults';
import Navbar from './components/Navbar';
import './index.css';

function App() {
  return (
    <ThemeProvider>
      <Router basename={process.env.PUBLIC_URL}>
        <div className="min-h-screen bg-background text-foreground">
          <Navbar />
          <main className="container mx-auto px-4 py-8">
            <Routes>
              <Route path="/" element={<EVResults />} />
              <Route path="/sports-betting" element={<EVResults />} />
              <Route path="/baseball" element={<BaseballResults />} />
              <Route path="/ncaab" element={<NcaabResults />} />
              <Route path="/dfs" element={<DFSResults />} />
              <Route path="/featured" element={<div className="text-xl font-semibold">Featured Section Coming Soon</div>} />
              <Route path="/calculator" element={<div className="text-xl font-semibold">Calculator Coming Soon</div>} />
              <Route path="/history" element={<div className="text-xl font-semibold">History Coming Soon</div>} />
            </Routes>
          </main>
        </div>
      </Router>
    </ThemeProvider>
  );
}

export default App;
