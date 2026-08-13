import React, { useState } from 'react';

type TabType = 'all' | 'agents' | 'tools';

interface Agent {
  id: string;
  name: string;
  description: string;
  color: string;
  icon: string;
}

interface Tool {
  id: string;
  name: string;
  agent: string;
  description: string;
  icon: string;
}

const agents: Agent[] = [
  {
    id: 'orchestrator',
    name: 'Orchestrator',
    description: 'Routes users across flight, hotel, and expense workflows',
    color: 'bg-blue-500',
    icon: 'O',
  },
  {
    id: 'sbt-agent',
    name: 'SBT Agent',
    description: 'Flight search, booking, and management',
    color: 'bg-cyan-500',
    icon: 'S',
  },
  {
    id: 'expense-agent',
    name: 'Expense Agent',
    description: 'Handles trips, approvals, invoices and expense tracking',
    color: 'bg-emerald-500',
    icon: 'E',
  },
  {
    id: 'backoffice-agent',
    name: 'BackOffice Agent',
    description: 'Hotel search, booking, and management',
    color: 'bg-blue-600',
    icon: 'B',
  },
  {
    id: 'itinerary-agent',
    name: 'Itinerary Agent',
    description: 'Creates day-wise schedules and itineraries',
    color: 'bg-purple-500',
    icon: 'I',
  },
  {
    id: 'rebooking-agent',
    name: 'Rebooking Agent',
    description: 'Handles cancellations, delays, and rebooking',
    color: 'bg-red-500',
    icon: 'R',
  },
  {
    id: 'revising-agent',
    name: 'Revising Agent',
    description: 'Reviews, optimizes schedules and budgets',
    color: 'bg-violet-500',
    icon: 'V',
  },
];

const tools: Tool[] = [
  // SBT Agent Tools
  {
    id: 'search_flights',
    name: 'Search Flights',
    agent: 'SBT Agent',
    description: 'Search available flights between cities',
    icon: '✈️',
  },
  {
    id: 'book_flight',
    name: 'Book Flight',
    agent: 'SBT Agent',
    description: 'Book a flight with passenger details',
    icon: '🎫',
  },
  {
    id: 'list_flight_bookings',
    name: 'List Flight Bookings',
    agent: 'SBT Agent',
    description: 'View all flight booking history',
    icon: '📋',
  },
  // BackOffice Agent Tools
  {
    id: 'list_hotels',
    name: 'List Hotels',
    agent: 'BackOffice Agent',
    description: 'Search hotels in a city',
    icon: '🏨',
  },
  {
    id: 'book_hotel',
    name: 'Book Hotel',
    agent: 'BackOffice Agent',
    description: 'Book a hotel room',
    icon: '🛏️',
  },
  {
    id: 'list_bookings',
    name: 'List Hotel Bookings',
    agent: 'BackOffice Agent',
    description: 'View hotel booking history',
    icon: '📝',
  },
  // Expense Agent Tools
  {
    id: 'create_expense',
    name: 'Create Expense',
    agent: 'Expense Agent',
    description: 'Create a new expense entry',
    icon: '💰',
  },
  {
    id: 'approve_expense',
    name: 'Approve Expense',
    agent: 'Expense Agent',
    description: 'Approve or reject expenses',
    icon: '✅',
  },
  {
    id: 'generate_invoice',
    name: 'Generate Invoice',
    agent: 'Expense Agent',
    description: 'Create invoices for expenses',
    icon: '🧾',
  },
  {
    id: 'create_trip',
    name: 'Create Trip',
    agent: 'Expense Agent',
    description: 'Create a new business trip',
    icon: '🗺️',
  },
  // Itinerary Agent Tools
  {
    id: 'schedule_making_tool',
    name: 'Create Schedule',
    agent: 'Itinerary Agent',
    description: 'Create day-wise itinerary',
    icon: '📅',
  },
  {
    id: 'show_schedule',
    name: 'Show Schedules',
    agent: 'Itinerary Agent',
    description: 'View saved schedules',
    icon: '📖',
  },
  // Rebooking Agent Tools
  {
    id: 'rebooking_tool',
    name: 'Rebooking Tool',
    agent: 'Rebooking Agent',
    description: 'Handle rebooking requests',
    icon: '🔄',
  },
  {
    id: 'handle_cancellation',
    name: 'Handle Cancellation',
    agent: 'Rebooking Agent',
    description: 'Process cancellations',
    icon: '❌',
  },
  {
    id: 'handle_delay',
    name: 'Handle Delay',
    agent: 'Rebooking Agent',
    description: 'Manage flight/hotel delays',
    icon: '⏰',
  },
  // Revising Agent Tools
  {
    id: 'review_itinerary',
    name: 'Review Itinerary',
    agent: 'Revising Agent',
    description: 'Analyze and suggest improvements',
    icon: '🔍',
  },
  {
    id: 'optimize_schedule',
    name: 'Optimize Schedule',
    agent: 'Revising Agent',
    description: 'Optimize travel schedules',
    icon: '⚡',
  },
  {
    id: 'check_budget',
    name: 'Check Budget',
    agent: 'Revising Agent',
    description: 'Analyze budget breakdown',
    icon: '💵',
  },
  // Orchestrator Tools
  {
    id: 'route_request',
    name: 'Route Request',
    agent: 'Orchestrator',
    description: 'Intelligently route user requests',
    icon: '🎯',
  },
];

export function SubagentsSidebar() {
  const [activeTab, setActiveTab] = useState<TabType>('all');
  const [searchQuery, setSearchQuery] = useState('');

  const filteredAgents = agents.filter((agent) =>
    agent.name.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const filteredTools = tools.filter((tool) =>
    tool.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    tool.agent.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div className="w-80 bg-[#f5f5f5] border-l border-gray-300 flex flex-col">
      {/* Header */}
      <div className="px-4 py-3 border-b border-gray-300">
        <div className="flex items-center justify-between mb-3">
          <h2 className="text-gray-800 text-sm font-semibold italic">
            Subagents & Tools
          </h2>
          <span className="text-gray-500 text-xs">{agents.length} · {tools.length}</span>
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
          <div className={`p-4 ${activeTab === 'all' ? 'border-t border-gray-300' : ''}`}>
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
                Orchestrator Tools
              </h3>
              <span className="ml-auto text-xs text-gray-500">{filteredTools.length}</span>
            </div>

            <div className="space-y-2">
              {filteredTools.map((tool) => (
                <div
                  key={tool.id}
                  className="bg-white rounded-lg p-3 shadow-sm border border-gray-200 hover:shadow-md cursor-pointer transition-shadow"
                >
                  <div className="flex items-start gap-3">
                    {/* Tool Icon */}
                    <div className="w-8 h-8 bg-gray-100 rounded-lg flex items-center justify-center flex-shrink-0 text-lg">
                      {tool.icon}
                    </div>

                    {/* Tool Info */}
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center justify-between mb-1">
                        <h4 className="text-sm font-semibold text-gray-900">
                          {tool.name}
                        </h4>
                      </div>
                      <p className="text-xs text-gray-600 mb-1">
                        {tool.description}
                      </p>
                      <div className="flex items-center gap-1">
                        <span className="text-xs text-gray-500">by</span>
                        <span className="text-xs font-medium text-blue-600">
                          {tool.agent}
                        </span>
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
