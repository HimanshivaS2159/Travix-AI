import React, { useState } from 'react';
import type { Flight } from '../../types';
import { Button } from '../ui/Button';
import { Input } from '../ui/Input';

interface FlightBookingModalProps {
  isOpen: boolean;
  onClose: () => void;
  flight: Flight | null;
  onConfirmBooking: (passengerName: string, email: string) => void;
}

export function FlightBookingModal({
  isOpen,
  onClose,
  flight,
  onConfirmBooking,
}: FlightBookingModalProps) {
  const [passengerName, setPassengerName] = useState('');
  const [email, setEmail] = useState('');
  const [phone, setPhone] = useState('');

  if (!isOpen || !flight) return null;

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (passengerName && email) {
      onConfirmBooking(passengerName, email);
      // Reset form
      setPassengerName('');
      setEmail('');
      setPhone('');
    }
  };

  const getAirlineColor = (airline: string) => {
    const colors: { [key: string]: string } = {
      'Vistara': 'from-purple-600 to-purple-700',
      'Air India': 'from-red-600 to-red-700',
      'IndiGo': 'from-blue-600 to-blue-700',
      'SpiceJet': 'from-orange-600 to-red-600',
      'Emirates': 'from-red-700 to-red-800',
      'FlyDubai': 'from-green-600 to-green-700',
    };
    return colors[airline] || 'from-blue-600 to-blue-700';
  };

  const getAirlineInitials = (airline: string) => {
    if (airline === 'Air India') return 'AI';
    if (airline === 'IndiGo') return '6E';
    if (airline === 'SpiceJet') return 'SG';
    if (airline === 'Vistara') return 'UK';
    if (airline === 'Emirates') return 'EK';
    if (airline === 'FlyDubai') return 'FZ';
    return airline.substring(0, 2).toUpperCase();
  };

  return (
    <div className="fixed inset-0 bg-gray-900/50 backdrop-blur-sm flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto shadow-2xl">
        {/* Header */}
        <div className="sticky top-0 bg-white border-b border-gray-200 px-6 py-4 flex items-center justify-between rounded-t-2xl z-10">
          <h2 className="text-xl font-semibold text-gray-900">Confirm Flight Booking</h2>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 transition-colors"
          >
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <div className="p-6">
          {/* Flight Summary Card */}
          <div className="bg-gradient-to-br from-blue-50 to-indigo-50 rounded-xl p-5 mb-6 border border-blue-100">
            <div className="flex items-start justify-between mb-4">
              <div className="flex items-center gap-3">
                <div className={`w-12 h-12 bg-gradient-to-br ${getAirlineColor(flight.airline)} rounded-lg flex items-center justify-center text-white font-bold text-base shadow-md`}>
                  {getAirlineInitials(flight.airline)}
                </div>
                <div>
                  <h3 className="font-semibold text-gray-900">{flight.airline}</h3>
                  <p className="text-sm text-gray-600">{flight.flight_number}</p>
                </div>
              </div>
              <div className="text-right">
                <div className="text-2xl font-bold text-gray-900">
                  ₹{flight.price.toLocaleString()}
                </div>
                <p className="text-xs text-gray-600">per person</p>
              </div>
            </div>

            <div className="grid grid-cols-3 gap-4">
              <div>
                <p className="text-xs text-gray-600 mb-1">Departure</p>
                <p className="text-xl font-bold text-gray-900">{flight.departure_time}</p>
                <p className="text-sm text-gray-700">{flight.from_city}</p>
                <p className="text-xs text-gray-600">{flight.from_code}</p>
              </div>
              <div className="flex flex-col items-center justify-center">
                <svg className="w-5 h-5 text-blue-600 mb-1" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M10.894 2.553a1 1 0 00-1.788 0l-7 14a1 1 0 001.169 1.409l5-1.429A1 1 0 009 15.571V11a1 1 0 112 0v4.571a1 1 0 00.725.962l5 1.428a1 1 0 001.17-1.408l-7-14z" />
                </svg>
                <p className="text-xs text-gray-600">{flight.duration}</p>
              </div>
              <div className="text-right">
                <p className="text-xs text-gray-600 mb-1">Arrival</p>
                <p className="text-xl font-bold text-gray-900">{flight.arrival_time}</p>
                <p className="text-sm text-gray-700">{flight.to_city}</p>
                <p className="text-xs text-gray-600">{flight.to_code}</p>
              </div>
            </div>

            <div className="mt-4 pt-4 border-t border-blue-200 grid grid-cols-3 gap-4 text-sm">
              <div>
                <span className="text-gray-600">Class:</span>
                <span className="ml-2 font-medium text-gray-900">{flight.class_type}</span>
              </div>
              <div>
                <span className="text-gray-600">Baggage:</span>
                <span className="ml-2 font-medium text-gray-900">{flight.baggage}</span>
              </div>
              <div className="text-right">
                <span className="text-gray-600">Seats:</span>
                <span className="ml-2 font-medium text-gray-900">{flight.available_seats} left</span>
              </div>
            </div>
          </div>

          {/* Passenger Details Form */}
          <form onSubmit={handleSubmit}>
            <div className="mb-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Passenger Details</h3>
              
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Full Name <span className="text-red-500">*</span>
                  </label>
                  <Input
                    type="text"
                    value={passengerName}
                    onChange={(e) => setPassengerName(e.target.value)}
                    placeholder="Enter full name as per ID"
                    required
                    className="w-full"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Email Address <span className="text-red-500">*</span>
                  </label>
                  <Input
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="your.email@example.com"
                    required
                    className="w-full"
                  />
                  <p className="text-xs text-gray-500 mt-1">Booking confirmation will be sent here</p>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Phone Number (Optional)
                  </label>
                  <Input
                    type="tel"
                    value={phone}
                    onChange={(e) => setPhone(e.target.value)}
                    placeholder="+91 XXXXX XXXXX"
                    className="w-full"
                  />
                </div>
              </div>
            </div>

            {/* Price Breakdown */}
            <div className="bg-gray-50 rounded-lg p-4 mb-6">
              <h3 className="text-sm font-semibold text-gray-900 mb-3">Price Breakdown</h3>
              <div className="space-y-2 text-sm">
                <div className="flex justify-between">
                  <span className="text-gray-600">Base Fare</span>
                  <span className="text-gray-900">₹{(flight.price * 0.85).toLocaleString()}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Taxes & Fees</span>
                  <span className="text-gray-900">₹{(flight.price * 0.15).toLocaleString()}</span>
                </div>
                <div className="border-t border-gray-200 pt-2 mt-2 flex justify-between font-semibold">
                  <span className="text-gray-900">Total Amount</span>
                  <span className="text-blue-600 text-lg">₹{flight.price.toLocaleString()}</span>
                </div>
              </div>
            </div>

            {/* Terms */}
            <div className="mb-6">
              <label className="flex items-start gap-2 cursor-pointer">
                <input
                  type="checkbox"
                  required
                  className="mt-1 w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
                />
                <span className="text-sm text-gray-600">
                  I agree to the <a href="#" className="text-blue-600 hover:underline">terms and conditions</a> and{' '}
                  <a href="#" className="text-blue-600 hover:underline">cancellation policy</a>
                </span>
              </label>
            </div>

            {/* Action Buttons */}
            <div className="flex gap-3">
              <button
                type="button"
                onClick={onClose}
                className="flex-1 px-6 py-3 border border-gray-300 text-gray-700 font-medium rounded-lg hover:bg-gray-50 transition-colors"
              >
                Cancel
              </button>
              <button
                type="submit"
                className="flex-1 px-6 py-3 bg-blue-600 text-white font-semibold rounded-lg hover:bg-blue-700 transition-colors shadow-md hover:shadow-lg"
              >
                Confirm Booking
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}
