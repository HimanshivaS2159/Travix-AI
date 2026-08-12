import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { LogOut } from 'lucide-react';
import { ConversationPanel } from '../components/dashboard/ConversationPanel';
import { ResultView } from '../components/dashboard/ResultView';
import { SubagentsSidebar } from '../components/dashboard/SubagentsSidebar';
import { OrchestratorProvider, useOrchestratorContext } from '../contexts/OrchestratorContext';

type ViewTab = 'trace' | 'flow' | 'result';

function DashboardContent() {
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState<ViewTab>('result');
  const { currentTrace, currentResult } = useOrchestratorContext();

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
                {currentTrace.length > 0 && (
                  <span className="bg-gray-400 text-white text-xs px-1.5 py-0.5 rounded">
                    {currentTrace.length}
                  </span>
                )}
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
                {currentResult && (
                  <span className="bg-gray-400 text-white text-xs px-1.5 py-0.5 rounded">1</span>
                )}
              </button>
            </div>

            {/* Tab Content */}
            <div className="flex-1 overflow-auto dashboard-scroll">
              {activeTab === 'trace' && <TraceView trace={currentTrace} />}
              {activeTab === 'flow' && <FlowView trace={currentTrace} />}
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

// Trace View Component
function TraceView({ trace }: { trace: any[] }) {
  if (!trace || trace.length === 0) {
    return (
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
    );
  }

  return (
    <div className="p-6">
      <div className="space-y-3">
        {trace.map((event, idx) => (
          <div key={event.id} className="bg-white rounded-lg shadow-sm border border-gray-200 p-4">
            <div className="flex items-start justify-between mb-2">
              <div className="flex items-center gap-3">
                <div className="bg-blue-100 text-blue-700 text-xs font-mono px-2 py-1 rounded">
                  {event.type}
                </div>
                <h4 className="font-semibold text-gray-800">{event.name}</h4>
              </div>
              <div className={`text-xs px-2 py-1 rounded ${
                event.status === 'completed' ? 'bg-green-100 text-green-700' :
                event.status === 'processing' ? 'bg-yellow-100 text-yellow-700' :
                event.status === 'failed' ? 'bg-red-100 text-red-700' :
                'bg-gray-100 text-gray-700'
              }`}>
                {event.status}
              </div>
            </div>
            <p className="text-sm text-gray-600 mb-2">{event.output_summary}</p>
            <div className="flex items-center gap-4 text-xs text-gray-500">
              <span>Agent: {event.agent}</span>
              <span>•</span>
              <span>Duration: {event.duration_ms}ms</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

// Flow View Component
function FlowView({ trace }: { trace: any[] }) {
  if (!trace || trace.length === 0) {
    return (
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
    );
  }

  const getNodeStyle = (type: string) => {
    const styles = {
      orchestrator: {
        bg: 'bg-gradient-to-br from-blue-500 to-blue-600',
        border: 'border-blue-700',
        icon: '◉',
        shadow: 'shadow-blue-200'
      },
      agent: {
        bg: 'bg-gradient-to-br from-purple-500 to-purple-600',
        border: 'border-purple-700',
        icon: 'B',
        shadow: 'shadow-purple-200'
      },
      tool: {
        bg: 'bg-gradient-to-br from-emerald-500 to-emerald-600',
        border: 'border-emerald-700',
        icon: '🔧',
        shadow: 'shadow-emerald-200'
      },
      booking: {
        bg: 'bg-gradient-to-br from-amber-500 to-amber-600',
        border: 'border-amber-700',
        icon: '📝',
        shadow: 'shadow-amber-200'
      },
      result: {
        bg: 'bg-gradient-to-br from-green-500 to-green-600',
        border: 'border-green-700',
        icon: '✓',
        shadow: 'shadow-green-200'
      }
    };
    return styles[type as keyof typeof styles] || styles.agent;
  };

  const getStatusBadge = (status: string) => {
    const badges = {
      completed: { text: '✓ Success', style: 'bg-green-100 text-green-800' },
      processing: { text: '⟳ Processing', style: 'bg-yellow-100 text-yellow-800' },
      failed: { text: '✗ Failed', style: 'bg-red-100 text-red-800' }
    };
    return badges[status as keyof typeof badges] || badges.completed;
  };

  return (
    <div className="h-full overflow-auto bg-gradient-to-br from-gray-50 to-gray-100" 
         style={{
           backgroundImage: 'radial-gradient(circle, #e5e7eb 1px, transparent 1px)',
           backgroundSize: '20px 20px'
         }}>
      <div className="p-12 flex justify-center">
        <div className="inline-flex flex-col items-center gap-6">
          {trace.map((event, idx) => {
            const style = getNodeStyle(event.type);
            const statusBadge = getStatusBadge(event.status);
            
            return (
              <React.Fragment key={event.id}>
                {/* Node */}
                <div className={`relative ${style.bg} ${style.border} border-2 rounded-xl p-6 min-w-[280px] shadow-lg ${style.shadow} transform transition-all hover:scale-105`}>
                  {/* Icon */}
                  <div className="absolute -top-4 -left-4 w-12 h-12 bg-white rounded-full shadow-lg flex items-center justify-center text-2xl border-2 border-gray-200">
                    {style.icon}
                  </div>
                  
                  {/* Content */}
                  <div className="ml-8">
                    <h3 className="text-white font-bold text-lg mb-1">{event.name}</h3>
                    <p className="text-white/80 text-xs mb-3">{event.type}</p>
                    
                    {/* Status Badge */}
                    <div className="flex items-center gap-2 mb-2">
                      <span className={`${statusBadge.style} text-xs px-2 py-1 rounded-full font-medium`}>
                        {statusBadge.text}
                      </span>
                      {event.duration_ms && (
                        <span className="bg-white/20 text-white text-xs px-2 py-1 rounded-full">
                          {event.duration_ms}ms
                        </span>
                      )}
                    </div>
                    
                    {/* Output Summary */}
                    {event.output_summary && (
                      <p className="text-white/90 text-sm mt-2 italic">
                        {event.output_summary}
                      </p>
                    )}
                  </div>
                </div>
                
                {/* Connector Arrow */}
                {idx < trace.length - 1 && (
                  <div className="flex flex-col items-center">
                    <div className="w-1 h-8 bg-gradient-to-b from-gray-400 to-gray-500"></div>
                    <svg className="w-8 h-8 text-gray-500" fill="currentColor" viewBox="0 0 24 24">
                      <path d="M12 16l-6-6h12z" />
                    </svg>
                  </div>
                )}
              </React.Fragment>
            );
          })}
        </div>
      </div>
    </div>
  );
}

export default function DashboardPage() {
  return (
    <OrchestratorProvider>
      <DashboardContent />
    </OrchestratorProvider>
  );
}
