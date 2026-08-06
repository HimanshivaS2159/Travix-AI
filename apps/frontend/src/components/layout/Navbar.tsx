import React from 'react';
import { Badge } from '../ui/Badge';

export const Navbar: React.FC = () => {
  return (
    <header className="sticky top-0 z-50 w-full border-b border-slate-800 bg-slate-950/80 backdrop-blur-md">
      <div className="mx-auto flex h-14 max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">
        <div className="flex items-center space-x-3">
          <span className="text-lg font-bold tracking-tight text-white">
            Travix AI
          </span>
          <Badge variant="info">Shell Ready</Badge>
        </div>
      </div>
    </header>
  );
};
