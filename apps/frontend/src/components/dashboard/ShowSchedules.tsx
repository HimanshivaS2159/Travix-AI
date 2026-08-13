import React, { useState, useEffect } from 'react';
import { Button } from '../ui/Button';

interface ScheduleItem {
  time: string;
  activity: string;
  location: string;
  duration: string;
  notes: string;
}

interface DailySchedule {
  day: number;
  title: string;
  items: ScheduleItem[];
}

interface Schedule {
  id: string;
  trip_name: string;
  city: string;
  start_date: string;
  end_date: string;
  daily_schedules: DailySchedule[];
  created_at: string;
  status: string;
}

interface ShowSchedulesProps {
  schedules?: Schedule[];
  loading?: boolean;
  onRefresh?: () => Promise<void>;
  onEdit?: (schedule: Schedule) => void;
  onDelete?: (scheduleId: string) => Promise<void>;
}

export function ShowSchedules({
  schedules = [],
  loading = false,
  onRefresh,
  onEdit,
  onDelete,
}: ShowSchedulesProps) {
  const [expandedSchedule, setExpandedSchedule] = useState<string | null>(null);
  const [expandedDay, setExpandedDay] = useState<string | null>(null);
  const [localSchedules, setLocalSchedules] = useState<Schedule[]>(schedules);

  useEffect(() => {
    setLocalSchedules(schedules);
  }, [schedules]);

  const handleDelete = async (scheduleId: string) => {
    if (window.confirm('Are you sure you want to delete this schedule?')) {
      if (onDelete) {
        await onDelete(scheduleId);
        setLocalSchedules(localSchedules.filter((s) => s.id !== scheduleId));
      }
    }
  };

  const toggleSchedule = (scheduleId: string) => {
    setExpandedSchedule(expandedSchedule === scheduleId ? null : scheduleId);
    setExpandedDay(null);
  };

  const toggleDay = (dayId: string) => {
    setExpandedDay(expandedDay === dayId ? null : dayId);
  };

  if (loading) {
    return (
      <div className="w-full bg-[#1e1e1e] rounded-lg border border-gray-700 p-6 flex items-center justify-center min-h-96">
        <div className="text-center space-y-4">
          <div className="w-12 h-12 border-4 border-gray-600 border-t-blue-500 rounded-full animate-spin mx-auto"></div>
          <p className="text-gray-400">Loading schedules...</p>
        </div>
      </div>
    );
  }

  if (localSchedules.length === 0) {
    return (
      <div className="w-full bg-[#1e1e1e] rounded-lg border border-gray-700 p-8 flex flex-col items-center justify-center min-h-96">
        <div className="text-center space-y-4">
          <div className="text-4xl">📅</div>
          <h3 className="text-lg font-medium text-white">No Schedules Found</h3>
          <p className="text-gray-400">
            Create your first schedule by asking "create a day wise schedule"
          </p>
          {onRefresh && (
            <Button onClick={onRefresh} variant="outline" size="sm">
              Refresh
            </Button>
          )}
        </div>
      </div>
    );
  }

  return (
    <div className="w-full bg-[#1e1e1e] rounded-lg border border-gray-700 p-6">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-xl font-semibold text-white">
          Saved Schedules ({localSchedules.length})
        </h2>
        {onRefresh && (
          <button
            onClick={onRefresh}
            disabled={loading}
            className="px-3 py-2 bg-blue-600 hover:bg-blue-700 text-white text-sm rounded-lg transition-colors disabled:opacity-50"
          >
            ↻ Refresh
          </button>
        )}
      </div>

      <div className="space-y-3">
        {localSchedules.map((schedule) => (
          <div
            key={schedule.id}
            className="bg-[#2a2a2a] border border-gray-600 rounded-lg overflow-hidden"
          >
            {/* Schedule Header */}
            <button
              onClick={() => toggleSchedule(schedule.id)}
              className="w-full px-4 py-4 flex items-center justify-between hover:bg-[#333333] transition-colors"
            >
              <div className="flex items-center gap-4 flex-1">
                <div className="flex-shrink-0">
                  <div className="w-10 h-10 bg-blue-600 rounded-lg flex items-center justify-center text-white font-medium">
                    {schedule.trip_name.charAt(0).toUpperCase()}
                  </div>
                </div>
                <div className="text-left flex-1">
                  <h3 className="text-white font-medium">{schedule.trip_name}</h3>
                  <div className="flex items-center gap-3 text-gray-400 text-xs mt-1">
                    <span>📍 {schedule.city}</span>
                    <span>•</span>
                    <span>
                      📅 {new Date(schedule.start_date).toLocaleDateString()} -{' '}
                      {new Date(schedule.end_date).toLocaleDateString()}
                    </span>
                    <span>•</span>
                    <span>🕐 {schedule.daily_schedules.length} days</span>
                  </div>
                </div>
              </div>
              <div className="flex items-center gap-2">
                <span
                  className={`px-2 py-1 text-xs font-medium rounded-full ${
                    schedule.status === 'active'
                      ? 'bg-green-500/20 text-green-400'
                      : 'bg-gray-500/20 text-gray-400'
                  }`}
                >
                  {schedule.status}
                </span>
                <svg
                  className={`w-5 h-5 text-gray-400 transition-transform ${
                    expandedSchedule === schedule.id ? 'rotate-180' : ''
                  }`}
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M19 14l-7 7m0 0l-7-7m7 7V3"
                  />
                </svg>
              </div>
            </button>

            {/* Schedule Details */}
            {expandedSchedule === schedule.id && (
              <div className="border-t border-gray-600 px-4 py-4 space-y-3 bg-[#1e1e1e]">
                {/* Daily Schedules */}
                {schedule.daily_schedules.map((day) => {
                  const dayId = `${schedule.id}-day-${day.day}`;
                  return (
                    <div key={dayId} className="space-y-2">
                      {/* Day Header */}
                      <button
                        onClick={() => toggleDay(dayId)}
                        className="w-full px-3 py-2 bg-[#2a2a2a] hover:bg-[#333333] border border-gray-600 rounded-lg flex items-center justify-between transition-colors"
                      >
                        <div className="text-left flex-1">
                          <h4 className="text-white font-medium text-sm">
                            {day.title}
                          </h4>
                          <p className="text-gray-400 text-xs mt-1">
                            {day.items.length} activities
                          </p>
                        </div>
                        <svg
                          className={`w-4 h-4 text-gray-400 transition-transform ${
                            expandedDay === dayId ? 'rotate-180' : ''
                          }`}
                          fill="none"
                          stroke="currentColor"
                          viewBox="0 0 24 24"
                        >
                          <path
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            strokeWidth={2}
                            d="M19 14l-7 7m0 0l-7-7m7 7V3"
                          />
                        </svg>
                      </button>

                      {/* Day Activities */}
                      {expandedDay === dayId && (
                        <div className="ml-4 space-y-2 pl-3 border-l-2 border-blue-500">
                          {day.items.map((item, itemIndex) => (
                            <div
                              key={itemIndex}
                              className="bg-[#2a2a2a] border border-gray-600 rounded-lg p-3 space-y-2"
                            >
                              <div className="flex items-start justify-between">
                                <div className="flex-1">
                                  <div className="flex items-center gap-2">
                                    <span className="text-blue-400 font-semibold text-sm">
                                      {item.time}
                                    </span>
                                    <span className="text-gray-400 text-xs">
                                      ({item.duration})
                                    </span>
                                  </div>
                                  <h5 className="text-white font-medium text-sm mt-1">
                                    {item.activity}
                                  </h5>
                                  <p className="text-gray-400 text-xs mt-1">
                                    📍 {item.location}
                                  </p>
                                  {item.notes && (
                                    <p className="text-gray-500 text-xs mt-2 italic">
                                      Note: {item.notes}
                                    </p>
                                  )}
                                </div>
                              </div>
                            </div>
                          ))}
                        </div>
                      )}
                    </div>
                  );
                })}

                {/* Actions */}
                <div className="flex gap-2 pt-4 border-t border-gray-600">
                  {onEdit && (
                    <Button
                      onClick={() => onEdit(schedule)}
                      variant="secondary"
                      size="sm"
                      className="flex-1"
                    >
                      ✏️ Edit
                    </Button>
                  )}
                  {onDelete && (
                    <Button
                      onClick={() => handleDelete(schedule.id)}
                      variant="danger"
                      size="sm"
                      className="flex-1"
                    >
                      🗑️ Delete
                    </Button>
                  )}
                  <Button
                    onClick={() => {
                      const text = `${schedule.trip_name}\n${schedule.city}\n${schedule.start_date} to ${schedule.end_date}\n\n${schedule.daily_schedules
                        .map(
                          (day) =>
                            `${day.title}\n${day.items
                              .map(
                                (item) =>
                                  `  ${item.time} - ${item.activity} (${item.location})`
                              )
                              .join('\n')}`
                        )
                        .join('\n\n')}`;
                      navigator.clipboard.writeText(text);
                      alert('Schedule copied to clipboard!');
                    }}
                    variant="secondary"
                    size="sm"
                    className="flex-1"
                  >
                    📋 Copy
                  </Button>
                </div>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
