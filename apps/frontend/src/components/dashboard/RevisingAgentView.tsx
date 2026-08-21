import React, { useState } from 'react';
import { AlertCircle, CheckCircle, TrendingUp, DollarSign, Save, Calendar } from 'lucide-react';
import { showToast } from '../ui/Toast';

interface Suggestion {
  issue: string;
  current: string;
  suggestion: string;
  impact: string;
  priority: 'High' | 'Medium' | 'Low';
}

interface ItineraryReviewData {
  suggestions: Suggestion[];
  overall_score: number;
  score_breakdown: {
    pacing: number;
    routing: number;
    meal_breaks: number;
    activities: number;
  };
  recommendation: string;
}

interface BookingReviewData {
  booking_status: string;
  bookings: Array<{
    type: string;
    name?: string;
    flight?: string;
    route?: string;
    check_in?: string;
    check_out?: string;
    departure?: string;
    price: string;
    status: string;
  }>;
  issues: string[];
  total_cost: string;
  recommendations: string[];
}

interface OptimizeScheduleData {
  optimized_schedule: Record<string, {
    original: string;
    optimized: string;
    time_saved: string;
    comfort_improvement: string;
  }>;
  time_saved: string;
  improvements: string[];
}

interface BudgetCheckData {
  total_budget: string;
  breakdown: Record<string, {
    amount: string;
    details: string;
    percentage: number;
  }>;
  spent: string;
  remaining: string;
  status: string;
}

interface RevisingAgentViewProps {
  action: string;
  data: ItineraryReviewData | BookingReviewData | OptimizeScheduleData | BudgetCheckData | any;
  message: string;
}

export function RevisingAgentView({ action, data, message }: RevisingAgentViewProps) {
  if (action === 'review_itinerary') {
    return <ItineraryReviewView data={data as ItineraryReviewData} message={message} />;
  } else if (action === 'review_booking') {
    return <BookingReviewView data={data as BookingReviewData} message={message} />;
  } else if (action === 'optimize_schedule') {
    return <OptimizeScheduleView data={data as OptimizeScheduleData} message={message} />;
  } else if (action === 'check_budget') {
    return <BudgetCheckView data={data as BudgetCheckData} message={message} />;
  }

  return null;
}

// Itinerary Review View
function ItineraryReviewView({ data, message }: { data: ItineraryReviewData; message: string }) {
  const [selectedSuggestions, setSelectedSuggestions] = useState<Set<number>>(new Set());

  const toggleSuggestion = (index: number) => {
    const newSelected = new Set(selectedSuggestions);
    if (newSelected.has(index)) {
      newSelected.delete(index);
    } else {
      newSelected.add(index);
    }
    setSelectedSuggestions(newSelected);
  };

  const handleApplyChanges = () => {
    if (selectedSuggestions.size === 0) {
      showToast('Please select at least one suggestion to apply', 'info');
      return;
    }

    // Simulate saving changes
    showToast(
      `Successfully applied ${selectedSuggestions.size} suggestion${selectedSuggestions.size > 1 ? 's' : ''} to your itinerary!`,
      'success'
    );
    setSelectedSuggestions(new Set());
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'High':
        return 'bg-red-100 text-red-700 border-red-200';
      case 'Medium':
        return 'bg-yellow-100 text-yellow-700 border-yellow-200';
      case 'Low':
        return 'bg-blue-100 text-blue-700 border-blue-200';
      default:
        return 'bg-gray-100 text-gray-700 border-gray-200';
    }
  };

  const getScoreColor = (score: number) => {
    if (score >= 8) return 'text-green-600';
    if (score >= 6) return 'text-yellow-600';
    return 'text-red-600';
  };

  return (
    <div className="p-6">
      <div className="max-w-5xl mx-auto">
        {/* Header */}
        <div className="mb-6">
          <h2 className="text-2xl font-bold text-gray-900 mb-2">{message}</h2>
          <p className="text-gray-600">Review the suggestions below and apply the changes you want</p>
        </div>

        {/* Overall Score */}
        <div className="bg-white rounded-lg shadow-md border border-gray-200 p-6 mb-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-gray-900">Overall Score</h3>
            <div className={`text-3xl font-bold ${getScoreColor(data.overall_score)}`}>
              {data.overall_score}/10
            </div>
          </div>

          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {Object.entries(data.score_breakdown).map(([key, value]) => (
              <div key={key} className="text-center">
                <div className="text-xs text-gray-500 mb-1 capitalize">{key.replace('_', ' ')}</div>
                <div className={`text-xl font-bold ${getScoreColor(value)}`}>{value}/10</div>
              </div>
            ))}
          </div>

          <div className="mt-4 p-3 bg-blue-50 border border-blue-100 rounded-lg">
            <p className="text-sm text-blue-800">💡 {data.recommendation}</p>
          </div>
        </div>

        {/* Suggestions */}
        <div className="space-y-4 mb-6">
          {data.suggestions.map((suggestion, index) => (
            <div
              key={index}
              className={`bg-white rounded-lg shadow-md border-2 transition-all cursor-pointer ${
                selectedSuggestions.has(index) ? 'border-blue-500 bg-blue-50' : 'border-gray-200'
              }`}
              onClick={() => toggleSuggestion(index)}
            >
              <div className="p-6">
                <div className="flex items-start justify-between mb-3">
                  <div className="flex items-center gap-3">
                    <input
                      type="checkbox"
                      checked={selectedSuggestions.has(index)}
                      onChange={() => toggleSuggestion(index)}
                      className="w-5 h-5 text-blue-600 rounded cursor-pointer"
                      onClick={(e) => e.stopPropagation()}
                    />
                    <div>
                      <h4 className="text-lg font-semibold text-gray-900">{suggestion.issue}</h4>
                      <span
                        className={`inline-block text-xs px-2 py-1 rounded border mt-1 ${getPriorityColor(
                          suggestion.priority
                        )}`}
                      >
                        {suggestion.priority} Priority
                      </span>
                    </div>
                  </div>
                  <AlertCircle className="w-5 h-5 text-gray-400 flex-shrink-0" />
                </div>

                <div className="ml-8 space-y-3">
                  <div>
                    <div className="text-xs font-medium text-gray-500 mb-1">Current:</div>
                    <div className="text-sm text-gray-700 bg-gray-50 p-2 rounded">
                      {suggestion.current}
                    </div>
                  </div>

                  <div>
                    <div className="text-xs font-medium text-gray-500 mb-1">Suggestion:</div>
                    <div className="text-sm text-gray-900 bg-green-50 p-2 rounded border border-green-200">
                      {suggestion.suggestion}
                    </div>
                  </div>

                  <div className="flex items-center gap-2 text-sm text-blue-600">
                    <TrendingUp className="w-4 h-4" />
                    <span className="font-medium">Impact:</span>
                    <span>{suggestion.impact}</span>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Action Button */}
        <div className="flex items-center justify-end gap-4">
          <div className="text-sm text-gray-600">
            {selectedSuggestions.size} suggestion{selectedSuggestions.size !== 1 ? 's' : ''} selected
          </div>
          <button
            onClick={handleApplyChanges}
            disabled={selectedSuggestions.size === 0}
            className="flex items-center gap-2 px-6 py-3 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
          >
            <Save className="w-5 h-5" />
            Apply Selected Changes
          </button>
        </div>
      </div>
    </div>
  );
}

// Booking Review View
function BookingReviewView({ data, message }: { data: BookingReviewData; message: string }) {
  const handleSaveBooking = () => {
    showToast('Booking details saved successfully!', 'success');
  };

  return (
    <div className="p-6">
      <div className="max-w-4xl mx-auto">
        <div className="mb-6">
          <h2 className="text-2xl font-bold text-gray-900 mb-2">{message}</h2>
        </div>

        {/* Status Banner */}
        <div className="bg-green-50 border border-green-200 rounded-lg p-4 mb-6">
          <div className="flex items-center gap-2">
            <CheckCircle className="w-5 h-5 text-green-600" />
            <span className="text-green-800 font-medium">Status: {data.booking_status}</span>
          </div>
        </div>

        {/* Bookings */}
        <div className="space-y-4 mb-6">
          {data.bookings.map((booking, index) => (
            <div key={index} className="bg-white rounded-lg shadow-md border border-gray-200 p-6">
              <div className="flex items-start justify-between mb-4">
                <div>
                  <span className="inline-block bg-blue-100 text-blue-700 text-xs px-2 py-1 rounded mb-2">
                    {booking.type}
                  </span>
                  <h3 className="text-lg font-semibold text-gray-900">
                    {booking.name || booking.flight}
                  </h3>
                  {booking.route && (
                    <p className="text-sm text-gray-600 mt-1">{booking.route}</p>
                  )}
                </div>
                <div className="text-right">
                  <div className="text-xs text-gray-500 mb-1">Price</div>
                  <div className="text-xl font-bold text-gray-900">{booking.price}</div>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                {booking.check_in && (
                  <div>
                    <div className="text-xs text-gray-500 mb-1">Check-in</div>
                    <div className="text-sm font-medium text-gray-900">{booking.check_in}</div>
                  </div>
                )}
                {booking.check_out && (
                  <div>
                    <div className="text-xs text-gray-500 mb-1">Check-out</div>
                    <div className="text-sm font-medium text-gray-900">{booking.check_out}</div>
                  </div>
                )}
                {booking.departure && (
                  <div>
                    <div className="text-xs text-gray-500 mb-1">Departure</div>
                    <div className="text-sm font-medium text-gray-900">{booking.departure}</div>
                  </div>
                )}
                <div>
                  <div className="text-xs text-gray-500 mb-1">Status</div>
                  <div className="text-sm font-medium text-green-600">{booking.status}</div>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Total Cost */}
        <div className="bg-white rounded-lg shadow-md border border-gray-200 p-6 mb-6">
          <div className="flex items-center justify-between">
            <span className="text-lg font-semibold text-gray-900">Total Cost</span>
            <span className="text-2xl font-bold text-gray-900">{data.total_cost}</span>
          </div>
        </div>

        {/* Recommendations */}
        {data.recommendations.length > 0 && (
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6">
            <h4 className="text-sm font-semibold text-blue-900 mb-2">Recommendations:</h4>
            <ul className="space-y-1">
              {data.recommendations.map((rec, index) => (
                <li key={index} className="text-sm text-blue-800 flex items-start gap-2">
                  <span className="text-blue-600 mt-0.5">•</span>
                  <span>{rec}</span>
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Save Button */}
        <div className="flex justify-end">
          <button
            onClick={handleSaveBooking}
            className="flex items-center gap-2 px-6 py-3 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 transition-colors"
          >
            <Save className="w-5 h-5" />
            Save Booking Details
          </button>
        </div>
      </div>
    </div>
  );
}

// Optimize Schedule View
function OptimizeScheduleView({ data, message }: { data: OptimizeScheduleData; message: string }) {
  const handleSaveSchedule = () => {
    showToast('Optimized schedule saved successfully!', 'success');
  };

  return (
    <div className="p-6">
      <div className="max-w-4xl mx-auto">
        <div className="mb-6">
          <h2 className="text-2xl font-bold text-gray-900 mb-2">{message}</h2>
          <p className="text-gray-600">Your schedule has been optimized for better timing and comfort</p>
        </div>

        {/* Time Saved Banner */}
        <div className="bg-green-50 border border-green-200 rounded-lg p-4 mb-6">
          <div className="flex items-center gap-2">
            <Calendar className="w-5 h-5 text-green-600" />
            <span className="text-green-800 font-medium">
              Total Time Saved: {data.time_saved}
            </span>
          </div>
        </div>

        {/* Schedule Comparison */}
        <div className="space-y-4 mb-6">
          {Object.entries(data.optimized_schedule).map(([day, schedule]) => (
            <div key={day} className="bg-white rounded-lg shadow-md border border-gray-200 p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">{day}</h3>

              <div className="space-y-4">
                <div>
                  <div className="text-xs font-medium text-gray-500 mb-2">Original Schedule:</div>
                  <div className="text-sm text-gray-700 bg-gray-50 p-3 rounded">
                    {schedule.original}
                  </div>
                </div>

                <div>
                  <div className="text-xs font-medium text-gray-500 mb-2">Optimized Schedule:</div>
                  <div className="text-sm text-gray-900 bg-green-50 p-3 rounded border border-green-200">
                    {schedule.optimized}
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4 pt-3 border-t border-gray-200">
                  <div>
                    <div className="text-xs text-gray-500 mb-1">Time Saved</div>
                    <div className="text-sm font-medium text-green-600">{schedule.time_saved}</div>
                  </div>
                  <div>
                    <div className="text-xs text-gray-500 mb-1">Improvement</div>
                    <div className="text-sm font-medium text-blue-600">
                      {schedule.comfort_improvement}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Improvements */}
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6">
          <h4 className="text-sm font-semibold text-blue-900 mb-2">Key Improvements:</h4>
          <ul className="space-y-1">
            {data.improvements.map((improvement, index) => (
              <li key={index} className="text-sm text-blue-800 flex items-start gap-2">
                <CheckCircle className="w-4 h-4 text-blue-600 mt-0.5 flex-shrink-0" />
                <span>{improvement}</span>
              </li>
            ))}
          </ul>
        </div>

        {/* Save Button */}
        <div className="flex justify-end">
          <button
            onClick={handleSaveSchedule}
            className="flex items-center gap-2 px-6 py-3 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 transition-colors"
          >
            <Save className="w-5 h-5" />
            Save Optimized Schedule
          </button>
        </div>
      </div>
    </div>
  );
}

// Budget Check View
function BudgetCheckView({ data, message }: { data: BudgetCheckData; message: string }) {
  const handleSaveBudget = () => {
    showToast('Budget details saved successfully!', 'success');
  };

  const getStatusColor = (status: string) => {
    if (status.includes('Within')) return 'text-green-600';
    if (status.includes('Close')) return 'text-yellow-600';
    return 'text-red-600';
  };

  return (
    <div className="p-6">
      <div className="max-w-4xl mx-auto">
        <div className="mb-6">
          <h2 className="text-2xl font-bold text-gray-900 mb-2">{message}</h2>
          <p className="text-gray-600">Detailed breakdown of your trip expenses</p>
        </div>

        {/* Budget Overview */}
        <div className="bg-white rounded-lg shadow-md border border-gray-200 p-6 mb-6">
          <div className="grid grid-cols-3 gap-6">
            <div>
              <div className="text-xs text-gray-500 mb-1">Total Budget</div>
              <div className="text-2xl font-bold text-gray-900">{data.total_budget}</div>
            </div>
            <div>
              <div className="text-xs text-gray-500 mb-1">Spent</div>
              <div className="text-2xl font-bold text-red-600">{data.spent}</div>
            </div>
            <div>
              <div className="text-xs text-gray-500 mb-1">Remaining</div>
              <div className="text-2xl font-bold text-green-600">{data.remaining}</div>
            </div>
          </div>

          <div className="mt-4 pt-4 border-t border-gray-200">
            <div className={`text-lg font-semibold ${getStatusColor(data.status)}`}>
              {data.status}
            </div>
          </div>
        </div>

        {/* Budget Breakdown */}
        <div className="bg-white rounded-lg shadow-md border border-gray-200 p-6 mb-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Expense Breakdown</h3>

          <div className="space-y-4">
            {Object.entries(data.breakdown).map(([category, details]) => (
              <div key={category} className="border-b border-gray-200 pb-4 last:border-0 last:pb-0">
                <div className="flex items-center justify-between mb-2">
                  <div className="flex items-center gap-3">
                    <DollarSign className="w-5 h-5 text-gray-400" />
                    <span className="font-semibold text-gray-900">{category}</span>
                  </div>
                  <div className="text-right">
                    <div className="text-lg font-bold text-gray-900">{details.amount}</div>
                    <div className="text-xs text-gray-500">{details.percentage.toFixed(1)}%</div>
                  </div>
                </div>
                <div className="ml-8 text-sm text-gray-600">{details.details}</div>

                {/* Progress Bar */}
                <div className="ml-8 mt-2">
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div
                      className="bg-blue-600 h-2 rounded-full transition-all"
                      style={{ width: `${details.percentage}%` }}
                    />
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Save Button */}
        <div className="flex justify-end">
          <button
            onClick={handleSaveBudget}
            className="flex items-center gap-2 px-6 py-3 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 transition-colors"
          >
            <Save className="w-5 h-5" />
            Save Budget Details
          </button>
        </div>
      </div>
    </div>
  );
}
