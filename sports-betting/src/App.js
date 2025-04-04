// src/App.js
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Header from './components/Header';
import PropList from './components/PropList';
import EVResults from './components/EVResults';
import BaseballProps from './components/BaseballProps';
import Footer from './components/Footer';
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        <Header />
        <main>
          <Routes>
            <Route path="/" element={<EVResults />} />
            <Route path="/props" element={<PropList />} />
            <Route path="/baseball" element={<BaseballProps />} />
          </Routes>
        </main>
        <Footer />
      </div>
    </Router>
  );
}

export default App;
