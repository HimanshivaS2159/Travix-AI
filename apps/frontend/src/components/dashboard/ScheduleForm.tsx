import React, { useState } from 'react';
import { Button } from '../ui/Button';
import { Input } from '../ui/Input';

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

interface ScheduleFormData {
  trip_name: string;
  start_date: string;
  end_date: string;
  city: string;
  daily_schedules: DailySchedule[];
}

interface ScheduleFormProps {
  onSubmit: (data: ScheduleFormData) => Promise<void>;
  loading?: boolean;
}

export function ScheduleForm({ onSubmit, loading = false }: ScheduleFormProps) {
  const [formData, setFormData] = useState<ScheduleFormData>({
    trip_name: '',
    start_date: '',
    end_date: '',
    city: 'Delhi',
    daily_schedules: [
      {
        day: 1,
        title: 'Day 1',
        items: [
          {
            time: '08:00',
            activity: 'Breakfast',
            location: 'Hotel',
            duration: '1 hour',
            notes: '',
          },
        ],
      },
    ],
  });

  const handleTripChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, trip_name: e.target.value });
  };

  const handleDateChange = (
    e: React.ChangeEvent<HTMLInputElement>,
    field: 'start_date' | 'end_date'
  ) => {
    setFormData({ ...formData, [field]: e.target.value });
  };

  const handleCityChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setFormData({ ...formData, city: e.target.value });
  };

  const handleDailyScheduleChange = (
    dayIndex: number,
    field: string,
    value: any
  ) => {
    const updatedSchedules = [...formData.daily_schedules];
    if (field === 'title') {
      updatedSchedules[dayIndex].title = value;
    }
    setFormData({ ...formData, daily_schedules: updatedSchedules });
  };

  const handleScheduleItemChange = (
    dayIndex: number,
    itemIndex: number,
    field: keyof ScheduleItem,
    value: string
  ) => {
    const updatedSchedules = [...formData.daily_schedules];
    updatedSchedules[dayIndex].items[itemIndex][field] = value;
    setFormData({ ...formData, daily_schedules: updatedSchedules });
  };

  const addDay = () => {
    const newDay = {
      day: formData.daily_schedules.length + 1,
      title: `Day ${formData.daily_schedules.length + 1}`,
      items: [
        {
          time: '08:00',
          activity: 'Activity',
          location: 'Location',
          duration: '1 hour',
          notes: '',
        },
      ],
    };
    setFormData({
      ...formData,
      daily_schedules: [...formData.daily_schedules, newDay],
    });
  };

  const removeDay = (dayIndex: number) => {
    if (formData.daily_schedules.length > 1) {
      const updatedSchedules = formData.daily_schedules.filter(
        (_, idx) => idx !== dayIndex
      );
      setFormData({ ...formData, daily_schedules: updatedSchedules });
    }
  };

  const addScheduleItem = (dayIndex: number) => {
    const updatedSchedules = [...formData.daily_schedules];
    updatedSchedules[dayIndex].items.push({
      time: '12:00',
      activity: 'Activity',
      location: 'Location',
      duration: '1 hour',
      notes: '',
    });
    setFormData({ ...formData, daily_schedules: updatedSchedules });
  };

  const removeScheduleItem = (dayIndex: number, itemIndex: number) => {
    const updatedSchedules = [...formData.daily_schedules];
    updatedSchedules[dayIndex].items = updatedSchedules[dayIndex].items.filter(
      (_, idx) => idx !== itemIndex
    );
    setFormData({ ...formData, daily_schedules: updatedSchedules });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!formData.trip_name || !formData.start_date || !formData.end_date) {
      alert('Please fill in all required fields');
      return;
    }
    await onSubmit(formData);
  };

  return (
    <div className="w-full bg-[#1e1e1e] rounded-lg border border-gray-700 p-6">
      <h2 className="text-xl font-semibold text-white mb-6">Create Day-Wise Schedule</h2>

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Basic Info */}
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              Trip Name *
            </label>
            <Input
              type="text"
              value={formData.trip_name}
              onChange={handleTripChange}
              placeholder="e.g., Delhi Adventure 2026"
              disabled={loading}
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Start Date *
              </label>
              <Input
                type="date"
                value={formData.start_date}
                onChange={(e) => handleDateChange(e, 'start_date')}
                disabled={loading}
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                End Date *
              </label>
              <Input
                type="date"
                value={formData.end_date}
                onChange={(e) => handleDateChange(e, 'end_date')}
                disabled={loading}
              />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              City *
            </label>
            <select
              value={formData.city}
              onChange={handleCityChange}
              disabled={loading}
              className="w-full bg-[#2a2a2a] text-white border border-gray-600 rounded-lg px-3 py-2 focus:border-blue-500 outline-none transition-colors disabled:opacity-50"
            >
              <option>Delhi</option>
              <option>Mumbai</option>
              <option>Bangalore</option>
              <option>Goa</option>
              <option>Jaipur</option>
            </select>
          </div>
        </div>

        {/* Daily Schedules */}
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-lg font-medium text-white">Daily Schedules</h3>
            <button
              type="button"
              onClick={addDay}
              disabled={loading}
              className="px-3 py-1 bg-blue-600 hover:bg-blue-700 text-white text-sm rounded-lg transition-colors disabled:opacity-50"
            >
              + Add Day
            </button>
          </div>

          {formData.daily_schedules.map((schedule, dayIndex) => (
            <div
              key={dayIndex}
              className="bg-[#2a2a2a] border border-gray-600 rounded-lg p-4 space-y-4"
            >
              <div className="flex items-center justify-between">
                <div className="flex-1">
                  <label className="block text-sm font-medium text-gray-300 mb-1">
                    Day Title
                  </label>
                  <Input
                    type="text"
                    value={schedule.title}
                    onChange={(e) =>
                      handleDailyScheduleChange(dayIndex, 'title', e.target.value)
                    }
                    placeholder="e.g., Day 1 - City Exploration"
                    disabled={loading}
                  />
                </div>
                {formData.daily_schedules.length > 1 && (
                  <button
                    type="button"
                    onClick={() => removeDay(dayIndex)}
                    disabled={loading}
                    className="ml-3 px-3 py-2 bg-red-600/20 hover:bg-red-600/30 text-red-400 rounded-lg transition-colors disabled:opacity-50"
                  >
                    Remove
                  </button>
                )}
              </div>

              {/* Schedule Items */}
              <div className="space-y-3 pl-4 border-l-2 border-gray-600">
                {schedule.items.map((item, itemIndex) => (
                  <div
                    key={itemIndex}
                    className="bg-[#1e1e1e] rounded-lg p-3 space-y-3"
                  >
                    <div className="grid grid-cols-2 gap-3">
                      <div>
                        <label className="block text-xs font-medium text-gray-400 mb-1">
                          Time
                        </label>
                        <Input
                          type="time"
                          value={item.time}
                          onChange={(e) =>
                            handleScheduleItemChange(
                              dayIndex,
                              itemIndex,
                              'time',
                              e.target.value
                            )
                          }
                          disabled={loading}
                        />
                      </div>
                      <div>
                        <label className="block text-xs font-medium text-gray-400 mb-1">
                          Duration
                        </label>
                        <Input
                          type="text"
                          value={item.duration}
                          onChange={(e) =>
                            handleScheduleItemChange(
                              dayIndex,
                              itemIndex,
                              'duration',
                              e.target.value
                            )
                          }
                          placeholder="e.g., 1 hour"
                          disabled={loading}
                        />
                      </div>
                    </div>

                    <div>
                      <label className="block text-xs font-medium text-gray-400 mb-1">
                        Activity
                      </label>
                      <Input
                        type="text"
                        value={item.activity}
                        onChange={(e) =>
                          handleScheduleItemChange(
                            dayIndex,
                            itemIndex,
                            'activity',
                            e.target.value
                          )
                        }
                        placeholder="e.g., Visit Red Fort"
                        disabled={loading}
                      />
                    </div>

                    <div>
                      <label className="block text-xs font-medium text-gray-400 mb-1">
                        Location
                      </label>
                      <Input
                        type="text"
                        value={item.location}
                        onChange={(e) =>
                          handleScheduleItemChange(
                            dayIndex,
                            itemIndex,
                            'location',
                            e.target.value
                          )
                        }
                        placeholder="e.g., New Delhi"
                        disabled={loading}
                      />
                    </div>

                    <div>
                      <label className="block text-xs font-medium text-gray-400 mb-1">
                        Notes
                      </label>
                      <textarea
                        value={item.notes}
                        onChange={(e) =>
                          handleScheduleItemChange(
                            dayIndex,
                            itemIndex,
                            'notes',
                            e.target.value
                          )
                        }
                        placeholder="Any additional notes"
                        disabled={loading}
                        className="w-full bg-[#2a2a2a] text-white border border-gray-600 rounded-lg px-3 py-2 focus:border-blue-500 outline-none transition-colors disabled:opacity-50 text-xs"
                        rows={2}
                      />
                    </div>

                    {schedule.items.length > 1 && (
                      <button
                        type="button"
                        onClick={() => removeScheduleItem(dayIndex, itemIndex)}
                        disabled={loading}
                        className="w-full px-3 py-1 bg-red-600/20 hover:bg-red-600/30 text-red-400 text-xs rounded transition-colors disabled:opacity-50"
                      >
                        Remove Item
                      </button>
                    )}
                  </div>
                ))}

                <button
                  type="button"
                  onClick={() => addScheduleItem(dayIndex)}
                  disabled={loading}
                  className="w-full px-3 py-2 bg-green-600/20 hover:bg-green-600/30 text-green-400 text-sm rounded-lg transition-colors disabled:opacity-50"
                >
                  + Add Activity
                </button>
              </div>
            </div>
          ))}
        </div>

        {/* Submit Button */}
        <div className="flex gap-3 pt-4">
          <Button
            type="submit"
            disabled={loading}
            className="flex-1"
          >
            {loading ? 'Saving...' : 'Save Schedule'}
          </Button>
        </div>
      </form>
    </div>
  );
}
