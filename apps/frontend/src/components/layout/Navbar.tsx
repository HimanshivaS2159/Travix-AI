import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Badge } from '../ui/Badge';

export const Navbar: React.FC = () => {
  const location = useLocation();
  
  return (
    <header className="sticky top-0 z-50 w-full border-b border-slate-800 bg-slate-950/80 backdrop-blur-md">
      <div className="mx-auto flex h-14 max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">
        <div className="flex items-center space-x-6">
          <div className="flex items-center space-x-3">
            <span className="text-lg font-bold tracking-tight text-white">
              Travix AI
            </span>
            <Badge variant="info">Shell Ready</Badge>
          </div>
          
          <nav className="flex items-center space-x-4">
            <Link
              to="/"
              className={`text-sm font-medium transition-colors hover:text-white ${
                location.pathname === '/' ? 'text-white' : 'text-slate-400'
              }`}
            >
              Home
            </Link>
            <Link
              to="/dashboard"
              className={`text-sm font-medium transition-colors hover:text-white ${
                location.pathname === '/dashboard' ? 'text-white' : 'text-slate-400'
              }`}
            >
              Dashboard
            </Link>
          </nav>
        </div>
      </div>
    </header>
  );
};
