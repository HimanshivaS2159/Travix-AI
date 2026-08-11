import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { LogOut } from 'lucide-react';
import { ConversationPanel } from '../components/dashboard/ConversationPanel';
import { ResultView } from '../components/dashboard/ResultView';
import { SubagentsSidebar } from '../components/dashboard/SubagentsSidebar';

type ViewTab = 'trace' | 'flow' | 'result';

export default function DashboardPage() {
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState<ViewTab>('result');

  const handleLogout = () => {
    // Clear any stored authentication data
    localStorage.removeItem('authToken');
    sessionStorage.clear();
    
    // Redirect to login page
    navigate('/', { replace: true });
  };

  return (
    <div className="flex h-screen bg-[#2a2a2a]">
      {/* Main Content Area */}
      <div className="flex flex-1 flex-col">
        {/* Header */}
        <header className="bg-[#1e1e1e] border-b border-gray-700 px-6 py-3">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="flex items-center gap-2">
                <div className="w-8 h-8 bg-gradient-to-br from-blue-500 via-purple-500 to-pink-500 rounded"></div>
                <span className="text-white font-semibold text-lg">AgenticBox</span>
              </div>
              <span className="text-gray-400">/</span>
              <span className="text-gray-300">Admin</span>
              <span className="text-gray-400">/</span>
              <span className="text-gray-300">Travel & Expense</span>
            </div>

            {/* Logout Button */}
            <button
              onClick={handleLogout}
              className="flex items-center gap-2 px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg transition-colors duration-200 font-medium text-sm"
              title="Logout"
            >
              <LogOut size={18} />
              <span>Logout</span>
            </button>
          </div>
        </header>

        {/* Content Area */}
        <div className="flex flex-1 overflow-hidden">
          {/* Left Panel - Conversation */}
          <ConversationPanel />

          {/* Right Panel - Views */}
          <div className="flex-1 flex flex-col bg-[#e8e4d9]">
            {/* Tab Navigation */}
            <div className="flex items-center gap-6 px-6 py-3 bg-[#e8e4d9] border-b border-gray-300">
              <button
                onClick={() => setActiveTab('trace')}
                className={`px-3 py-2 text-sm font-medium transition-colors ${
                  activeTab === 'trace'
                    ? 'text-blue-600 border-b-2 border-blue-600'
                    : 'text-gray-600 hover:text-gray-800'
                }`}
              >
                Trace View
              </button>
              <button
                onClick={() => setActiveTab('flow')}
                className={`px-3 py-2 text-sm font-medium transition-colors flex items-center gap-2 ${
                  activeTab === 'flow'
                    ? 'text-blue-600 border-b-2 border-blue-600'
                    : 'text-gray-600 hover:text-gray-800'
                }`}
              >
                Flow View
                <span className="bg-gray-400 text-white text-xs px-1.5 py-0.5 rounded">3</span>
              </button>
              <button
                onClick={() => setActiveTab('result')}
                className={`px-3 py-2 text-sm font-medium transition-colors flex items-center gap-2 ${
                  activeTab === 'result'
                    ? 'text-blue-600 border-b-2 border-blue-600'
                    : 'text-gray-600 hover:text-gray-800'
                }`}
              >
                Result View
                <span className="bg-gray-400 text-white text-xs px-1.5 py-0.5 rounded">1</span>
              </button>
            </div>

            {/* Tab Content */}
            <div className="flex-1 overflow-auto dashboard-scroll">
              {activeTab === 'trace' && (
                <div className="h-full flex items-center justify-center p-6">
                  <div className="text-center text-gray-500">
                    <svg
                      className="w-16 h-16 mx-auto mb-4 text-gray-400"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={1.5}
                        d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"
                      />
                    </svg>
                    <p className="text-sm font-medium">No trace data available</p>
                    <p className="text-xs mt-1">Execution traces will appear here</p>
                  </div>
                </div>
              )}
              {activeTab === 'flow' && (
                <div className="h-full flex items-center justify-center p-6">
                  <div className="text-center text-gray-500">
                    <svg
                      className="w-16 h-16 mx-auto mb-4 text-gray-400"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={1.5}
                        d="M13 10V3L4 14h7v7l9-11h-7z"
                      />
                    </svg>
                    <p className="text-sm font-medium">No flow data available</p>
                    <p className="text-xs mt-1">Agent workflow will be visualized here</p>
                  </div>
                </div>
              )}
              {activeTab === 'result' && <ResultView />}
            </div>
          </div>
        </div>
      </div>

      {/* Right Sidebar - Subagents & Tools */}
      <SubagentsSidebar />
    </div>
  );
}
