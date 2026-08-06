import { useState, useEffect } from 'react';

export type Theme = 'dark' | 'light';

export function useTheme() {
  const [theme] = useState<Theme>('dark');

  useEffect(() => {
    document.documentElement.classList.add('dark');
  }, [theme]);

  return { theme };
}
