import React from 'react';

interface LogoProps {
  className?: string;
  size?: 'sm' | 'md' | 'lg';
}

export function Logo({ className = '', size = 'md' }: LogoProps) {
  const sizes = {
    sm: 'w-8 h-8',
    md: 'w-10 h-10',
    lg: 'w-12 h-12',
  };

  return (
    <div className={`${sizes[size]} ${className}`}>
      <svg
        viewBox="0 0 100 100"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
        className="w-full h-full"
      >
        {/* Background Circle - Blue gradient */}
        <circle cx="50" cy="50" r="48" fill="url(#blueGradient)" />
        
        {/* Airplane icon in black */}
        <path
          d="M 75 35 L 50 25 L 25 35 L 30 45 L 45 40 L 50 60 L 55 40 L 70 45 Z"
          fill="#000000"
          stroke="#000000"
          strokeWidth="2"
          strokeLinejoin="round"
        />
        
        {/* Travel path line */}
        <path
          d="M 20 70 Q 35 60 50 65 T 80 70"
          stroke="#000000"
          strokeWidth="2"
          fill="none"
          strokeLinecap="round"
        />
        
        {/* Dots on path */}
        <circle cx="20" cy="70" r="3" fill="#000000" />
        <circle cx="50" cy="65" r="3" fill="#000000" />
        <circle cx="80" cy="70" r="3" fill="#000000" />
        
        {/* Gradient definition */}
        <defs>
          <linearGradient id="blueGradient" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="#3B82F6" />
            <stop offset="100%" stopColor="#1E40AF" />
          </linearGradient>
        </defs>
      </svg>
    </div>
  );
}

export function LogoWithText({ className = '', size = 'md' }: LogoProps) {
  const textSizes = {
    sm: 'text-lg',
    md: 'text-xl',
    lg: 'text-2xl',
  };

  return (
    <div className={`flex items-center gap-3 ${className}`}>
      <Logo size={size} />
      <div className="flex flex-col">
        <span className={`${textSizes[size]} font-bold tracking-tight bg-gradient-to-r from-blue-500 to-blue-700 bg-clip-text text-transparent`}>
          TRAVIX
        </span>
        <span className="text-xs text-gray-500 -mt-1">AI Travel Assistant</span>
      </div>
    </div>
  );
}
