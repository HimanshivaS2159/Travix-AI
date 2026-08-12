import React, { useState, useEffect, useRef } from 'react';
import { useOrchestrator } from '../../hooks/useOrchestrator';

export function ConversationPanel() {
  const { 
    messages, 
    loading, 
    error, 
    sendMessage, 
    clearMessages 
  } = useOrchestrator();
  const [inputValue, setInputValue] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputValue.trim() || loading) return;

    await sendMessage(inputValue);
    setInputValue('');
  };

  const getAgentColor = (agent: string): string => {
    const colors: Record<string, string> = {
      orchestrator: 'bg-blue-600',
      sbt_agent: 'bg-cyan-500',
      expense_agent: 'bg-emerald-500',
      backoffice_agent: 'bg-blue-600',
    };
    return colors[agent] || 'bg-gray-600';
  };

  return (
    <div className="w-96 bg-[#1e1e1e] border-r border-gray-700 flex flex-col">
      {/* Header */}
      <div className="px-4 py-3 border-b border-gray-700">
        <h2 className="text-white text-sm font-medium mb-2">Conversation</h2>
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3 text-xs text-gray-400">
            <span className="flex items-center gap-1">
              <span className="w-2 h-2 bg-green-500 rounded-full"></span>
              4 agents
            </span>
            <span>·</span>
            <span>19 tools</span>
          </div>
          {messages.length > 0 && (
            <button
              onClick={clearMessages}
              className="text-xs text-gray-500 hover:text-gray-300 transition-colors"
              title="Clear conversation"
            >
              Clear
            </button>
          )}
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4 dashboard-scroll">
        {messages.length === 0 ? (
          <div className="flex items-center justify-center h-full text-gray-500 text-sm">
            <p>No messages yet. Start a conversation!</p>
          </div>
        ) : (
          messages.map((msg, idx) => (
            <div key={idx} className="space-y-2">
              {msg.role === 'user' && (
                <div className="text-gray-300 text-sm">
                  <span className="text-gray-500">You:</span> {msg.content}
                  <div className="text-gray-600 text-xs mt-1">
                    {new Date(msg.timestamp).toLocaleTimeString()}
                  </div>
                </div>
              )}
              {msg.role === 'assistant' && (
                <div className={`${getAgentColor(msg.agent || '')} rounded-lg p-3 shadow-lg`}>
                  <div className="text-white font-medium text-sm mb-1">
                    {msg.agent?.replace(/_/g, ' ').toUpperCase() || 'Orchestrator'}
                  </div>
                  <div className="text-white text-xs mb-2">{msg.content}</div>
                  {msg.action && (
                    <div className="flex items-center justify-between">
                      <span className="text-white/70 text-xs">Action: {msg.action}</span>
                      <span className="text-white/50 text-xs">
                        {(msg.confidence ? msg.confidence * 100 : 0).toFixed(0)}%
                      </span>
                    </div>
                  )}
                  <div className="text-white/50 text-xs mt-1">
                    {new Date(msg.timestamp).toLocaleTimeString()}
                  </div>
                </div>
              )}
              {msg.role === 'system' && (
                <div className="bg-red-900/30 rounded-lg p-3 border border-red-700">
                  <div className="text-red-300 text-xs">{msg.content}</div>
                  <div className="text-red-500 text-xs mt-1">
                    {new Date(msg.timestamp).toLocaleTimeString()}
                  </div>
                </div>
              )}
            </div>
          ))
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Error Message */}
      {error && (
        <div className="px-4 py-2 bg-red-900/20 border-t border-red-700">
          <p className="text-red-300 text-xs">{error}</p>
        </div>
      )}

      {/* Input Area */}
      <form onSubmit={handleSubmit} className="p-4 border-t border-gray-700">
        <div className="flex items-center gap-2 bg-[#2a2a2a] rounded-lg px-3 py-2 border border-gray-600 focus-within:border-blue-500 transition-colors">
          <button
            type="button"
            disabled={loading}
            className="text-gray-400 hover:text-gray-300 disabled:opacity-50 transition-colors"
          >
            <svg
              className="w-5 h-5"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M12 4v16m8-8H4"
              />
            </svg>
          </button>
          <input
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            disabled={loading}
            placeholder={loading ? "Processing..." : "Ask AI..."}
            className="flex-1 bg-transparent text-white text-sm placeholder-gray-500 outline-none disabled:opacity-50"
          />
          <button
            type="submit"
            disabled={loading || !inputValue.trim()}
            className="text-gray-400 hover:text-gray-300 disabled:opacity-50 transition-colors"
          >
            {loading ? (
              <svg
                className="w-5 h-5 animate-spin"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8z"
                />
              </svg>
            ) : (
              <svg
                className="w-5 h-5"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"
                />
              </svg>
            )}
          </button>
        </div>
      </form>
    </div>
  );
}
