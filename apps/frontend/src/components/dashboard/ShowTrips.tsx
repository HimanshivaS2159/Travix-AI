import React from 'react';
import { MapPin, Calendar, FileText, DollarSign, Plane, CheckCircle2, Clock } from 'lucide-react';

interface Trip {
  trip_id: string;
  trip_name: string;
  start_date: string;
  end_date: string;
  destination: string;
  purpose: string;
  status: string;
  total_expenses: number;
  currency: string;
  created_at: string;
}

interface ShowTripsProps {
  trips: Trip[];
}

export function ShowTrips({ trips }: ShowTripsProps) {
  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'completed':
        return (
          <span className="flex items-center gap-1 bg-green-100 text-green-700 text-xs px-3 py-1 rounded-full">
            <CheckCircle2 size={14} />
            Completed
          </span>
        );
      case 'cancelled':
        return (
          <span className="flex items-center gap-1 bg-red-100 text-red-700 text-xs px-3 py-1 rounded-full">
            Cancelled
          </span>
        );
      default:
        return (
          <span className="flex items-center gap-1 bg-blue-100 text-blue-700 text-xs px-3 py-1 rounded-full">
            <Clock size={14} />
            Active
          </span>
        );
    }
  };

  const calculateDuration = (startDate: string, endDate: string) => {
    const start = new Date(startDate);
    const end = new Date(endDate);
    const days = Math.ceil((end.getTime() - start.getTime()) / (1000 * 60 * 60 * 24)) + 1;
    return days;
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
  };

  if (trips.length === 0) {
    return (
      <div className="text-center py-12">
        <div className="text-gray-400 mb-4">
          <Plane size={64} className="mx-auto" />
        </div>
        <h3 className="text-lg font-semibold text-gray-900 mb-2">No Trips Found</h3>
        <p className="text-gray-600">Create your first business trip to get started!</p>
      </div>
    );
  }

  return (
    <div>
      <div className="mb-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-2">Business Trips</h2>
        <p className="text-gray-600">Manage your business travel and track expenses</p>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-3 gap-4 mb-6">
        <div className="bg-gradient-to-br from-blue-500 to-blue-600 rounded-lg p-5 text-white">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm font-medium opacity-90">Total Trips</span>
            <Plane size={20} className="opacity-75" />
          </div>
          <p className="text-3xl font-bold">{trips.length}</p>
        </div>

        <div className="bg-gradient-to-br from-green-500 to-green-600 rounded-lg p-5 text-white">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm font-medium opacity-90">Active Trips</span>
            <Clock size={20} className="opacity-75" />
          </div>
          <p className="text-3xl font-bold">
            {trips.filter((t) => t.status === 'active').length}
          </p>
        </div>

        <div className="bg-gradient-to-br from-purple-500 to-purple-600 rounded-lg p-5 text-white">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm font-medium opacity-90">Total Expenses</span>
            <DollarSign size={20} className="opacity-75" />
          </div>
          <p className="text-3xl font-bold">
            ₹{trips.reduce((sum, t) => sum + t.total_expenses, 0).toLocaleString()}
          </p>
        </div>
      </div>

      {/* Trip Cards */}
      <div className="space-y-4">
        {trips.map((trip) => {
          const duration = calculateDuration(trip.start_date, trip.end_date);
          
          return (
            <div
              key={trip.trip_id}
              className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow"
            >
              <div className="flex items-start justify-between mb-4">
                <div className="flex items-start gap-4">
                  <div className="w-14 h-14 bg-gradient-to-br from-blue-500 to-blue-600 rounded-lg flex items-center justify-center flex-shrink-0">
                    <Plane className="w-7 h-7 text-white" />
                  </div>
                  <div>
                    <div className="flex items-center gap-3 mb-2">
                      <h3 className="text-xl font-bold text-gray-900">{trip.trip_name}</h3>
                      {getStatusBadge(trip.status)}
                    </div>
                    <div className="flex items-center gap-2 text-sm text-gray-600">
                      <span className="inline-block bg-blue-100 text-blue-700 px-2 py-0.5 rounded text-xs font-medium">
                        {trip.trip_id}
                      </span>
                      <span className="text-gray-400">•</span>
                      <span>{duration} days</span>
                    </div>
                  </div>
                </div>

                <div className="text-right">
                  <p className="text-sm text-gray-600 mb-1">Total Expenses</p>
                  <p className="text-2xl font-bold text-gray-900">
                    {trip.currency} {trip.total_expenses.toLocaleString()}
                  </p>
                </div>
              </div>

              <div className="grid grid-cols-3 gap-6 mb-4">
                <div className="flex items-start gap-3">
                  <div className="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center flex-shrink-0">
                    <Calendar className="w-5 h-5 text-blue-600" />
                  </div>
                  <div>
                    <p className="text-xs text-gray-600 mb-1">Travel Dates</p>
                    <p className="text-sm font-semibold text-gray-900">
                      {formatDate(trip.start_date)}
                    </p>
                    <p className="text-xs text-gray-500">to</p>
                    <p className="text-sm font-semibold text-gray-900">
                      {formatDate(trip.end_date)}
                    </p>
                  </div>
                </div>

                <div className="flex items-start gap-3">
                  <div className="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center flex-shrink-0">
                    <MapPin className="w-5 h-5 text-green-600" />
                  </div>
                  <div>
                    <p className="text-xs text-gray-600 mb-1">Destination</p>
                    <p className="text-sm font-semibold text-gray-900">{trip.destination}</p>
                  </div>
                </div>

                <div className="flex items-start gap-3">
                  <div className="w-10 h-10 bg-purple-100 rounded-lg flex items-center justify-center flex-shrink-0">
                    <FileText className="w-5 h-5 text-purple-600" />
                  </div>
                  <div>
                    <p className="text-xs text-gray-600 mb-1">Purpose</p>
                    <p className="text-sm font-semibold text-gray-900 line-clamp-2">
                      {trip.purpose}
                    </p>
                  </div>
                </div>
              </div>

              {trip.total_expenses > 0 && (
                <div className="pt-4 border-t border-gray-200">
                  <div className="flex items-center justify-between">
                    <p className="text-sm text-gray-600">
                      💰 Expenses tracked for this trip
                    </p>
                    <button className="text-sm text-blue-600 hover:text-blue-700 font-medium">
                      View Expenses →
                    </button>
                  </div>
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
