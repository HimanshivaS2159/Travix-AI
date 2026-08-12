/**
 * API Service
 * Handles all communication with the backend API
 */

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

export interface OrchestratorRequest {
  user_message: string;
  conversation_history?: Array<{
    role: 'user' | 'assistant';
    content: string;
  }>;
}

export interface OrchestratorResponse {
  agent: string;
  action: string;
  confidence: number;
  reason: string;
  tools?: string[];
}

export interface AgentInfo {
  name: string;
  description: string;
  capabilities: string[];
  icon: string;
}

export interface AgentsResponse {
  agents: Record<string, AgentInfo>;
  total: number;
}

export interface ToolsResponse {
  agent: string;
  tools: string[];
  tool_count: number;
}

class APIService {
  private baseURL: string;

  constructor(baseURL: string = API_BASE_URL) {
    this.baseURL = baseURL;
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseURL}${endpoint}`;
    
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
      ...options.headers,
    };

    try {
      const response = await fetch(url, {
        ...options,
        headers,
      });

      if (!response.ok) {
        const error = await response.json().catch(() => ({}));
        throw new Error(error.detail || `API Error: ${response.statusText}`);
      }

      return await response.json();
    } catch (error) {
      console.error('API request failed:', error);
      throw error;
    }
  }

  /**
   * Analyze user request and get orchestrator routing
   */
  async analyzeRequest(request: OrchestratorRequest): Promise<OrchestratorResponse> {
    return this.request<OrchestratorResponse>('/api/orchestrator/analyze', {
      method: 'POST',
      body: JSON.stringify(request),
    });
  }

  /**
   * Get list of available agents
   */
  async getAgents(): Promise<AgentsResponse> {
    return this.request<AgentsResponse>('/api/orchestrator/agents', {
      method: 'GET',
    });
  }

  /**
   * Get tools for a specific agent
   */
  async getAgentTools(agentName: string): Promise<ToolsResponse> {
    return this.request<ToolsResponse>(
      `/api/orchestrator/agents/${agentName}/tools`,
      {
        method: 'GET',
      }
    );
  }

  /**
   * Health check
   */
  async healthCheck(): Promise<any> {
    return this.request('/health', {
      method: 'GET',
    });
  }
}

export const apiService = new APIService();
