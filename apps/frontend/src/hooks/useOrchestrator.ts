/**
 * useOrchestrator Hook
 * Manages orchestrator state and communication with backend
 */

import { useState, useCallback, useRef } from 'react';
import { apiService, OrchestratorResponse, AgentsResponse, OrchestratorRequest } from '../services/api';

export interface Message {
  role: 'user' | 'assistant' | 'system';
  content: string;
  agent?: string;
  action?: string;
  confidence?: number;
  timestamp: Date;
}

interface UseOrchestratorReturn {
  messages: Message[];
  loading: boolean;
  error: string | null;
  agents: any;
  agentsLoading: boolean;
  sendMessage: (message: string) => Promise<void>;
  loadAgents: () => Promise<void>;
  clearMessages: () => void;
  clearError: () => void;
}

export function useOrchestrator(): UseOrchestratorReturn {
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [agents, setAgents] = useState<any>(null);
  const [agentsLoading, setAgentsLoading] = useState(false);
  const conversationHistoryRef = useRef<Array<{ role: 'user' | 'assistant'; content: string }>>([]);

  /**
   * Load available agents
   */
  const loadAgents = useCallback(async () => {
    setAgentsLoading(true);
    setError(null);
    try {
      const response = await apiService.getAgents();
      setAgents(response.agents);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load agents');
    } finally {
      setAgentsLoading(false);
    }
  }, []);

  /**
   * Send message to orchestrator
   */
  const sendMessage = useCallback(async (userMessage: string) => {
    if (!userMessage.trim()) return;

    setLoading(true);
    setError(null);

    try {
      // Add user message to messages
      const userMessageObj: Message = {
        role: 'user',
        content: userMessage,
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, userMessageObj]);
      conversationHistoryRef.current.push({
        role: 'user',
        content: userMessage,
      });

      // Send to orchestrator
      const request: OrchestratorRequest = {
        user_message: userMessage,
        conversation_history: conversationHistoryRef.current,
      };

      const response = await apiService.analyzeRequest(request);

      // Add orchestrator response to messages
      const orchestratorMessage: Message = {
        role: 'assistant',
        content: response.reason,
        agent: response.agent,
        action: response.action,
        confidence: response.confidence,
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, orchestratorMessage]);
      conversationHistoryRef.current.push({
        role: 'assistant',
        content: response.reason,
      });
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to process message';
      setError(errorMessage);
      
      // Add error message
      const errorMessageObj: Message = {
        role: 'system',
        content: errorMessage,
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, errorMessageObj]);
    } finally {
      setLoading(false);
    }
  }, []);

  /**
   * Clear messages
   */
  const clearMessages = useCallback(() => {
    setMessages([]);
    conversationHistoryRef.current = [];
  }, []);

  /**
   * Clear error
   */
  const clearError = useCallback(() => {
    setError(null);
  }, []);

  return {
    messages,
    loading,
    error,
    agents,
    agentsLoading,
    sendMessage,
    loadAgents,
    clearMessages,
    clearError,
  };
}
