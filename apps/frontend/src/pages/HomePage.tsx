import React from 'react';

export const HomePage: React.FC = () => {
  return (
    <div className="flex-1 flex flex-col items-center justify-center text-center py-16">
      <h1 className="text-3xl font-extrabold tracking-tight text-white sm:text-4xl">
        Travix AI
      </h1>
      <p className="mt-3 text-lg text-slate-400 font-medium">
        Application Shell Ready
      </p>
    </div>
  );
};
