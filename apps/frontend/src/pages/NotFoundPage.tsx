import React from 'react';

export const NotFoundPage: React.FC = () => {
  return (
    <div className="flex-1 flex flex-col items-center justify-center text-center py-16">
      <h1 className="text-3xl font-bold tracking-tight text-white">404</h1>
      <p className="mt-2 text-base text-slate-400">Page Not Found</p>
    </div>
  );
};
