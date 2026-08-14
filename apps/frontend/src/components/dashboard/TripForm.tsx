import React, { useState } from 'react';
import { X, ArrowLeft, MapPin, Calendar, FileText } from 'lucide-react';
import { apiService } from '../../services/api';
import { useOrchestratorContext } from '../../contexts/OrchestratorContext';

interface TripFormProps {
  onSubmit: (data: any) => void;
  onCancel: () => void;
}

export function TripForm({ onSubmit, onCancel }: TripFormProps) {
  const { sendMessage } = useOrchestratorContext();
  const [trip, setTrip] = useState({
    trip_name: '',
    start_date: '',
    end_date: '',
    destination: '',
    purpose: ''
  });

  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitError, setSubmitError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    setSubmitError(null);

    try {
      // Submit to backend
      const result = await apiService.saveTrip(trip);
      
      // Show success message
      if (result.success) {
        onSubmit(trip);
        // Trigger a refresh of the trips list
        await sendMessage('Show my trips');
      } else {
        setSubmitError(result.message || 'Failed to save trip');
      }
    } catch (error) {
      console.error('Error saving trip:', error);
      setSubmitError(error instanceof Error ? error.message : 'Failed to save trip');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="h-full overflow-y-auto" style={{ backgroundColor: '#F5F3EF' }}>
      {/* Header */}
      <div className="bg-white border-b border-gray-200 px-6 py-4 sticky top-0 z-10">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-4">
            <button
              onClick={onCancel}
              className="text-blue-600 hover:text-blue-700 flex items-center gap-2"
            >
              <ArrowLeft size={20} />
              <span className="text-sm">Back to Summary</span>
            </button>
            <span className="text-gray-300">•</span>
            <span className="text-sm text-gray-600">Form Mode</span>
          </div>
          <div className="flex items-center gap-3">
            <button
              onClick={onCancel}
              className="flex items-center gap-2 px-4 py-2 text-gray-700 hover:bg-gray-100 rounded-lg transition-colors border border-gray-300"
            >
              <X size={18} />
              Cancel
            </button>
            <button
              onClick={handleSubmit}
              className="flex items-center gap-2 bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg disabled:bg-gray-400 disabled:cursor-not-allowed"
              disabled={isSubmitting}
            >
              {isSubmitting ? '⏳ Saving...' : '💾 Save Trip'}
            </button>
          </div>
        </div>
        
        {submitError && (
          <div className="mx-6 mb-4 bg-red-50 border border-red-200 rounded-lg p-3">
            <p className="text-sm text-red-800">❌ {submitError}</p>
          </div>
        )}
        
        <div className="mt-3 px-6">
          <h1 className="text-2xl font-bold text-gray-900">Create Business Trip</h1>
          <p className="text-sm text-gray-600 mt-1">Plan your business travel and track expenses</p>
        </div>
      </div>

      <form onSubmit={handleSubmit} className="p-6 max-w-4xl mx-auto">
        {/* Trip Details Card */}
        <div className="bg-white rounded-lg p-6">
          <div className="flex items-center gap-2 mb-6">
            <div className="w-8 h-8 bg-blue-600 rounded flex items-center justify-center">
              <span className="text-white text-xs">✈️</span>
            </div>
            <h3 className="text-base font-semibold text-gray-900">Trip Information</h3>
          </div>

          <div className="space-y-5">
            {/* Trip Name */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                🎯 Trip Name <span className="text-red-500">*</span>
              </label>
              <input
                type="text"
                value={trip.trip_name}
                onChange={(e) => setTrip({ ...trip, trip_name: e.target.value })}
                placeholder="e.g., Mumbai Client Meeting • August 2026"
                className="w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                required
              />
              <p className="text-xs text-gray-500 mt-1.5">Give your trip a descriptive name</p>
            </div>

            {/* Date Range */}
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  <Calendar className="inline w-4 h-4 mr-1" />
                  Start Date <span className="text-red-500">*</span>
                </label>
                <input
                  type="date"
                  value={trip.start_date}
                  onChange={(e) => setTrip({ ...trip, start_date: e.target.value })}
                  className="w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  <Calendar className="inline w-4 h-4 mr-1" />
                  End Date <span className="text-red-500">*</span>
                </label>
                <input
                  type="date"
                  value={trip.end_date}
                  onChange={(e) => setTrip({ ...trip, end_date: e.target.value })}
                  className="w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  required
                />
              </div>
            </div>

            {/* Destination */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                <MapPin className="inline w-4 h-4 mr-1" />
                Destination <span className="text-red-500">*</span>
              </label>
              <input
                type="text"
                value={trip.destination}
                onChange={(e) => setTrip({ ...trip, destination: e.target.value })}
                placeholder="e.g., Mumbai, Maharashtra, India"
                className="w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                required
              />
              <p className="text-xs text-gray-500 mt-1.5">City and country of your destination</p>
            </div>

            {/* Purpose */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                <FileText className="inline w-4 h-4 mr-1" />
                Business Purpose <span className="text-red-500">*</span>
              </label>
              <textarea
                value={trip.purpose}
                onChange={(e) => setTrip({ ...trip, purpose: e.target.value })}
                placeholder="Describe the purpose of this business trip..."
                rows={4}
                className="w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
                required
              />
              <p className="text-xs text-gray-500 mt-1.5">
                Include details like client meetings, conferences, training, etc.
              </p>
            </div>
          </div>

          {/* Info Box */}
          <div className="mt-6 p-4 bg-blue-50 border border-blue-100 rounded-lg">
            <div className="flex gap-3">
              <div className="flex-shrink-0">
                <div className="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center">
                  <span className="text-white text-sm">💡</span>
                </div>
              </div>
              <div>
                <h4 className="text-sm font-semibold text-blue-900 mb-1">Trip Benefits</h4>
                <ul className="text-xs text-blue-800 space-y-1">
                  <li>• Associate all expenses with this trip for easy tracking</li>
                  <li>• View total trip costs in one place</li>
                  <li>• Generate trip reports for reimbursement</li>
                  <li>• Keep business travel organized</li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </form>
    </div>
  );
}
