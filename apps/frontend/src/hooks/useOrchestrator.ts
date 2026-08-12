/**
 * useOrchestrator Hook
 * Manages orchestrator state and communication with backend
 */

import { useState, useCallback, useRef } from 'react';
import { apiService, OrchestratorResponse, AgentsResponse, OrchestratorRequest } from '../services/api';
import { ToolResult, TraceEvent } from '../types';

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
  currentResult: ToolResult | null;
  currentTrace: TraceEvent[];
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
  const [currentResult, setCurrentResult] = useState<ToolResult | null>(null);
  const [currentTrace, setCurrentTrace] = useState<TraceEvent[]>([]);
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

      // Execute through unified endpoint
      const request: OrchestratorRequest = {
        user_message: userMessage,
        conversation_history: conversationHistoryRef.current,
      };

      const response = await apiService.executeRequest(request);

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

      // Handle execution result
      if (response.result) {
        const result = response.result;
        setCurrentResult(result);
        setCurrentTrace(result.trace || []);

        // Add result message to conversation
        const resultMessage: Message = {
          role: 'assistant',
          content: result.message,
          agent: response.agent,
          action: result.action,
          timestamp: new Date(),
        };
        setMessages(prev => [...prev, resultMessage]);
      } else {
        // No result - clear views
        setCurrentResult(null);
        setCurrentTrace([]);
      }
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
      setCurrentResult(null);
      setCurrentTrace([]);
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
    setCurrentResult(null);
    setCurrentTrace([]);
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
    currentResult,
    currentTrace,
    sendMessage,
    loadAgents,
    clearMessages,
    clearError,
  };
}
