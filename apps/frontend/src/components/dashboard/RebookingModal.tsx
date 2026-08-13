import React, { useState } from 'react';
import { Button } from '../ui/Button';

interface RebookingModalProps {
  isOpen: boolean;
  onClose: () => void;
  data?: {
    rebooking_id: string;
    type: 'flight_cancellation' | 'flight_delay' | 'hotel_cancellation';
    delay_hours?: number;
    compensation?: string;
    refund_amount?: string;
    original_flight?: string;
    original_booking?: string;
    refund_policy?: string;
    options?: string[];
    rebooking_options?: any[];
    alternative_hotels?: any[];
  };
  onAction?: (action: string, data: any) => void;
  loading?: boolean;
}

export function RebookingModal({
  isOpen,
  onClose,
  data,
  onAction,
  loading = false,
}: RebookingModalProps) {
  const [selectedOption, setSelectedOption] = useState<number | null>(null);
  const [actionType, setActionType] = useState<string>('');

  if (!isOpen || !data) return null;

  const handleAction = (action: string, value?: any) => {
    if (onAction) {
      onAction(action, value || selectedOption);
    }
    setActionType(action);
  };

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div className="bg-[#1e1e1e] border border-gray-700 rounded-lg shadow-xl max-w-2xl w-full mx-4 max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="sticky top-0 px-6 py-4 border-b border-gray-700 bg-[#1e1e1e] flex items-center justify-between">
          <div className="flex items-center gap-3">
            {data.type === 'flight_delay' && <span className="text-2xl">⏱️</span>}
            {data.type === 'flight_cancellation' && <span className="text-2xl">✈️</span>}
            {data.type === 'hotel_cancellation' && <span className="text-2xl">🏨</span>}
            <div>
              <h2 className="text-xl font-semibold text-white">
                {data.type === 'flight_delay' && 'Flight Delay Notification'}
                {data.type === 'flight_cancellation' && 'Flight Cancellation'}
                {data.type === 'hotel_cancellation' && 'Hotel Cancellation'}
              </h2>
              <p className="text-gray-400 text-sm mt-1">ID: {data.rebooking_id}</p>
            </div>
          </div>
          <button
            onClick={onClose}
            disabled={loading}
            className="text-gray-400 hover:text-gray-200 transition-colors disabled:opacity-50"
          >
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        {/* Content */}
        <div className="px-6 py-6 space-y-6">
          {/* Flight Delay */}
          {data.type === 'flight_delay' && (
            <div className="space-y-4">
              <div className="bg-yellow-900/20 border border-yellow-700 rounded-lg p-4">
                <p className="text-yellow-300 font-semibold">
                  Your flight is delayed by {data.delay_hours} hours
                </p>
                <p className="text-yellow-200 text-sm mt-2">
                  Flight: {data.original_flight}
                </p>
              </div>

              <div className="bg-blue-900/20 border border-blue-700 rounded-lg p-4">
                <h3 className="text-blue-300 font-semibold mb-2">Compensation & Rights</h3>
                <ul className="text-blue-200 text-sm space-y-2">
                  <li>✓ You are entitled to compensation: {data.compensation}</li>
                  <li>✓ Complimentary meals and refreshments provided</li>
                  <li>✓ Hotel accommodation if overnight delay</li>
                  <li>✓ Communication costs reimbursement</li>
                </ul>
              </div>

              <div>
                <h3 className="text-white font-semibold mb-3">What would you like to do?</h3>
                <div className="space-y-2">
                  <label className="flex items-center p-3 bg-[#2a2a2a] border border-gray-600 rounded-lg cursor-pointer hover:border-blue-500 transition-colors">
                    <input
                      type="radio"
                      name="flight_delay_action"
                      value="take_delayed"
                      checked={selectedOption === 0}
                      onChange={() => setSelectedOption(0)}
                      disabled={loading}
                      className="w-4 h-4"
                    />
                    <span className="ml-3 text-white text-sm">
                      Take the delayed flight with compensation (₹3,000)
                    </span>
                  </label>
                  <label className="flex items-center p-3 bg-[#2a2a2a] border border-gray-600 rounded-lg cursor-pointer hover:border-blue-500 transition-colors">
                    <input
                      type="radio"
                      name="flight_delay_action"
                      value="rebook"
                      checked={selectedOption === 1}
                      onChange={() => setSelectedOption(1)}
                      disabled={loading}
                      className="w-4 h-4"
                    />
                    <span className="ml-3 text-white text-sm">
                      Rebook on next available flight
                    </span>
                  </label>
                  <label className="flex items-center p-3 bg-[#2a2a2a] border border-gray-600 rounded-lg cursor-pointer hover:border-blue-500 transition-colors">
                    <input
                      type="radio"
                      name="flight_delay_action"
                      value="cancel_refund"
                      checked={selectedOption === 2}
                      onChange={() => setSelectedOption(2)}
                      disabled={loading}
                      className="w-4 h-4"
                    />
                    <span className="ml-3 text-white text-sm">
                      Cancel and get full refund
                    </span>
                  </label>
                </div>
              </div>
            </div>
          )}

          {/* Flight Cancellation */}
          {data.type === 'flight_cancellation' && (
            <div className="space-y-4">
              <div className="bg-red-900/20 border border-red-700 rounded-lg p-4">
                <p className="text-red-300 font-semibold">
                  Your flight has been cancelled
                </p>
                <p className="text-red-200 text-sm mt-2">
                  Flight: {data.original_flight}
                </p>
              </div>

              <div className="bg-green-900/20 border border-green-700 rounded-lg p-4">
                <h3 className="text-green-300 font-semibold mb-2">Your Rights</h3>
                <ul className="text-green-200 text-sm space-y-2">
                  <li>✓ Full refund: {data.refund_amount}</li>
                  <li>✓ Re-route on another flight at no cost</li>
                  <li>✓ Claim compensation if applicable</li>
                </ul>
              </div>

              <div>
                <h3 className="text-white font-semibold mb-3">Available Rebooking Options</h3>
                <div className="space-y-2">
                  {data.rebooking_options && data.rebooking_options.map((option: any, idx: number) => (
                    <label
                      key={idx}
                      className="flex items-start p-4 bg-[#2a2a2a] border border-gray-600 rounded-lg cursor-pointer hover:border-blue-500 transition-colors"
                    >
                      <input
                        type="radio"
                        name="flight_rebook"
                        value={idx}
                        checked={selectedOption === idx}
                        onChange={() => setSelectedOption(idx)}
                        disabled={loading}
                        className="w-4 h-4 mt-1 flex-shrink-0"
                      />
                      <div className="ml-3 flex-1">
                        <div className="text-white text-sm font-medium">
                          {option.airline} - {option.departure} to {option.arrival}
                        </div>
                        <div className="text-gray-400 text-xs mt-1">
                          {option.notes}
                        </div>
                        {option.price > 0 && (
                          <div className="text-yellow-400 text-sm mt-1">
                            +₹{option.price}
                          </div>
                        )}
                      </div>
                    </label>
                  ))}
                </div>
              </div>
            </div>
          )}

          {/* Hotel Cancellation */}
          {data.type === 'hotel_cancellation' && (
            <div className="space-y-4">
              <div className="bg-orange-900/20 border border-orange-700 rounded-lg p-4">
                <p className="text-orange-300 font-semibold">
                  Hotel Cancellation
                </p>
                <p className="text-orange-200 text-sm mt-2">
                  Booking: {data.original_booking}
                </p>
                <p className="text-orange-200 text-sm mt-1">
                  Policy: {data.refund_policy}
                </p>
              </div>

              <div className="bg-blue-900/20 border border-blue-700 rounded-lg p-4">
                <h3 className="text-blue-300 font-semibold mb-2">Refund Details</h3>
                <div className="text-blue-200 text-sm space-y-1">
                  <p>Refund Amount: <span className="font-semibold">{data.refund_amount}</span></p>
                  <p>Processing Time: 5-7 business days</p>
                </div>
              </div>

              <div>
                <h3 className="text-white font-semibold mb-3">Alternative Hotels</h3>
                <div className="space-y-2">
                  {data.alternative_hotels && data.alternative_hotels.map((hotel: any, idx: number) => (
                    <label
                      key={idx}
                      className="flex items-start p-4 bg-[#2a2a2a] border border-gray-600 rounded-lg cursor-pointer hover:border-blue-500 transition-colors"
                    >
                      <input
                        type="radio"
                        name="hotel_alternative"
                        value={idx}
                        checked={selectedOption === idx}
                        onChange={() => setSelectedOption(idx)}
                        disabled={loading}
                        className="w-4 h-4 mt-1 flex-shrink-0"
                      />
                      <div className="ml-3 flex-1">
                        <div className="text-white text-sm font-medium">
                          {hotel.name}
                        </div>
                        <div className="text-yellow-400 text-sm mt-1">
                          ₹{hotel.price}/night • ⭐ {hotel.rating}
                        </div>
                      </div>
                    </label>
                  ))}
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="sticky bottom-0 px-6 py-4 border-t border-gray-700 bg-[#1e1e1e] flex gap-3">
          <Button
            onClick={onClose}
            variant="secondary"
            disabled={loading}
            className="flex-1"
          >
            Cancel
          </Button>
          <Button
            onClick={() => {
              if (data.type === 'flight_delay') {
                handleAction('flight_delay_action', ['take_delayed', 'rebook', 'cancel_refund'][selectedOption || 0]);
              } else if (data.type === 'flight_cancellation') {
                handleAction('flight_rebook', selectedOption);
              } else if (data.type === 'hotel_cancellation') {
                handleAction('hotel_alternative', selectedOption);
              }
            }}
            disabled={loading || selectedOption === null}
            className="flex-1"
          >
            {loading ? 'Processing...' : 'Confirm'}
          </Button>
        </div>
      </div>
    </div>
  );
}
