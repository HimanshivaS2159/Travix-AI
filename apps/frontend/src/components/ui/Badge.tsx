import React from 'react';
import { cn } from '../../lib/utils';

export interface BadgeProps extends React.HTMLAttributes<HTMLDivElement> {
  variant?: 'default' | 'success' | 'warning' | 'danger' | 'info';
}

export const Badge: React.FC<BadgeProps> = ({
  className,
  variant = 'default',
  ...props
}) => {
  const variants = {
    default: 'bg-slate-800 text-slate-200 border-slate-700',
    success: 'bg-emerald-950 text-emerald-300 border-emerald-800',
    warning: 'bg-amber-950 text-amber-300 border-amber-800',
    danger: 'bg-red-950 text-red-300 border-red-800',
    info: 'bg-blue-950 text-blue-300 border-blue-800',
  };

  return (
    <div
      className={cn(
        'inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2',
        variants[variant],
        className
      )}
      {...props}
    />
  );
};
