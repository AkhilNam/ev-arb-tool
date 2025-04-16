import React from 'react';
import { useTheme } from '../context/ThemeContext';
import { Button } from './ui/button';
import { FaSun, FaMoon } from 'react-icons/fa';

const ThemeToggle = () => {
  const { theme, toggleTheme } = useTheme();

  return (
    <Button
      variant="ghost"
      size="icon"
      onClick={toggleTheme}
      className="fixed bottom-4 right-4"
    >
      {theme === 'light' ? (
        <FaMoon className="h-5 w-5" />
      ) : (
        <FaSun className="h-5 w-5" />
      )}
      <span className="sr-only">Toggle theme</span>
    </Button>
  );
};

export default ThemeToggle; 