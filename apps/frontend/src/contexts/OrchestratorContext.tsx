/**
 * Orchestrator Context
 * Provides shared orchestrator state across the application
 */

import React, { createContext, useContext, ReactNode } from 'react';
import { useOrchestrator } from '../hooks/useOrchestrator';
import type { Message } from '../hooks/useOrchestrator';
import type { ToolResult, TraceEvent } from '../types';

interface OrchestratorContextValue {
  messages: Message[];
  loading: boolean;
  error: string | null;
  agents: any;
  agentsLoading: boolean;
  currentResult: ToolResult | null;
  currentTrace: TraceEvent[];
  sendMessage: (message: string) => Promise<void>;
  loadAgents: () => Promise<void>;
  clearMessages: () => void;
  clearError: () => void;
}

const OrchestratorContext = createContext<OrchestratorContextValue | null>(null);

export function OrchestratorProvider({ children }: { children: ReactNode }) {
  const orchestrator = useOrchestrator();

  return (
    <OrchestratorContext.Provider value={orchestrator}>
      {children}
    </OrchestratorContext.Provider>
  );
}

export function useOrchestratorContext(): OrchestratorContextValue {
  const context = useContext(OrchestratorContext);
  if (!context) {
    throw new Error('useOrchestratorContext must be used within OrchestratorProvider');
  }
  return context;
}
