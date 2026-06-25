import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { FaBars, FaTimes } from 'react-icons/fa';

interface HeaderProps {
  onLogout: () => void;
}

/**
 * Header component with brand logo, navigation links, and logout button.
 * Includes a mobile hamburger menu.
 */
const Header: React.FC<HeaderProps> = ({ onLogout }) => {
  const [mobileOpen, setMobileOpen] = useState(false);

  const toggleMenu = () => setMobileOpen(!mobileOpen);

  return (
    <header className="bg-white shadow-sm">
      <nav className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8" aria-label="Main navigation">
        <div className="flex justify-between h-16 items-center">
          <Link to="/dashboard" className="text-xl font-bold text-primary">
            RealTimeRoomChat
          </Link>
          <div className="hidden md:flex space-x-4">
            <Link to="/dashboard" className="text-gray-700 hover:text-primary">
              Dashboard
            </Link>
            <button
              onClick={onLogout}
              className="text-gray-700 hover:text-primary"
            >
              Logout
            </button>
          </div>
          <div className="md:hidden flex items-center">
            <button
              onClick={toggleMenu}
              aria-label={mobileOpen ? 'Close menu' : 'Open menu'}
              className="text-gray-700 focus:outline-none focus:ring-2 focus:ring-primary"
            >
              {mobileOpen ? <FaTimes size={24} /> : <FaBars size={24} />}
            </button>
          </div>
        </div>
        {mobileOpen && (
          <div className="md:hidden mt-2 space-y-2">
            <Link to="/dashboard" className="block text-gray-700 hover:text-primary" onClick={toggleMenu}>
              Dashboard
            </Link>
            <button
              onClick={() => { onLogout(); toggleMenu(); }}
              className="block w-full text-left text-gray-700 hover:text-primary"
            >
              Logout
            </button>
          </div>
        )}
      </nav>
    </header>
  );
};

export default Header;
