import React, { useState } from 'react';

type TabType = 'all' | 'agents' | 'tools';

interface Agent {
  id: string;
  name: string;
  description: string;
  color: string;
  icon: string;
}

const agents: Agent[] = [
  {
    id: 'orchestrator',
    name: 'Orchestrator',
    description: 'Routes users across flight and preference workflows',
    color: 'bg-blue-500',
    icon: 'O',
  },
  {
    id: 'sbt-agent',
    name: 'SBT Agent',
    description: 'Collects flight search route preference-aware guidance',
    color: 'bg-cyan-500',
    icon: 'S',
  },
  {
    id: 'expense-agent',
    name: 'Expense Agent',
    description: 'Handles trips, approvals, invoices and expense mutation tools',
    color: 'bg-emerald-500',
    icon: 'E',
  },
  {
    id: 'backoffice-agent',
    name: 'BackOffice Agent',
    description: 'Handles hotel search, booking, and booking history',
    color: 'bg-blue-600',
    icon: 'B',
  },
];

export function SubagentsSidebar() {
  const [activeTab, setActiveTab] = useState<TabType>('all');
  const [searchQuery, setSearchQuery] = useState('');

  const filteredAgents = agents.filter((agent) =>
    agent.name.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div className="w-80 bg-[#f5f5f5] border-l border-gray-300 flex flex-col">
      {/* Header */}
      <div className="px-4 py-3 border-b border-gray-300">
        <div className="flex items-center justify-between mb-3">
          <h2 className="text-gray-800 text-sm font-semibold italic">
            Subagents & Tools
          </h2>
          <span className="text-gray-500 text-xs">4 · 19</span>
        </div>

        {/* Tab Navigation */}
        <div className="flex items-center gap-4 mb-3">
          <button
            onClick={() => setActiveTab('all')}
            className={`text-sm font-medium pb-1 transition-colors ${
              activeTab === 'all'
                ? 'text-blue-600 border-b-2 border-blue-600'
                : 'text-gray-600 hover:text-gray-800'
            }`}
          >
            All
          </button>
          <button
            onClick={() => setActiveTab('agents')}
            className={`text-sm font-medium pb-1 transition-colors ${
              activeTab === 'agents'
                ? 'text-blue-600 border-b-2 border-blue-600'
                : 'text-gray-600 hover:text-gray-800'
            }`}
          >
            Agents
          </button>
          <button
            onClick={() => setActiveTab('tools')}
            className={`text-sm font-medium pb-1 transition-colors ${
              activeTab === 'tools'
                ? 'text-blue-600 border-b-2 border-blue-600'
                : 'text-gray-600 hover:text-gray-800'
            }`}
          >
            Tools
          </button>
        </div>

        {/* Search Input */}
        <div className="relative">
          <input
            type="text"
            placeholder="Search agents and tools..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full px-3 py-2 pr-8 text-sm bg-white border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 placeholder-gray-400"
          />
          <svg
            className="w-4 h-4 text-gray-400 absolute right-3 top-1/2 -translate-y-1/2"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
            />
          </svg>
        </div>
      </div>

      {/* Content */}
      <div className="flex-1 overflow-y-auto dashboard-scroll">
        {/* Subagents Section */}
        {(activeTab === 'all' || activeTab === 'agents') && (
          <div className="p-4">
            <div className="flex items-center gap-2 mb-3">
              <svg
                className="w-4 h-4 text-gray-600"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M19 9l-7 7-7-7"
                />
              </svg>
              <h3 className="text-xs font-semibold text-gray-700 uppercase tracking-wide">
                Subagents
              </h3>
            </div>

            <div className="space-y-3">
              {filteredAgents.map((agent) => (
                <div
                  key={agent.id}
                  className="agent-card bg-white rounded-lg p-3 shadow-sm border border-gray-200 hover:shadow-md cursor-pointer"
                >
                  <div className="flex items-start gap-3">
                    {/* Agent Icon */}
                    <div
                      className={`${agent.color} w-10 h-10 rounded-lg flex items-center justify-center flex-shrink-0`}
                    >
                      <span className="text-white font-bold text-lg">
                        {agent.icon}
                      </span>
                    </div>

                    {/* Agent Info */}
                    <div className="flex-1 min-w-0">
                      <h4 className="text-sm font-semibold text-gray-900 mb-1">
                        {agent.name}
                      </h4>
                      <p className="text-xs text-gray-600 leading-relaxed">
                        {agent.description}
                      </p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Tools Section */}
        {(activeTab === 'all' || activeTab === 'tools') && (
          <div className="p-4 border-t border-gray-300">
            <div className="flex items-center gap-2 mb-3">
              <svg
                className="w-4 h-4 text-gray-600"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M19 9l-7 7-7-7"
                />
              </svg>
              <h3 className="text-xs font-semibold text-gray-700 uppercase tracking-wide">
                Tools
              </h3>
            </div>
            <div className="text-xs text-gray-500 italic">19 tools available</div>
          </div>
        )}
      </div>
    </div>
  );
}
