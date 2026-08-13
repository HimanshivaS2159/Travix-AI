import React from 'react';
import { Card } from '../ui/Card';
import { Badge } from '../ui/Badge';
import type { FlightBooking } from '../../types';

interface ShowFlightBookingsProps {
  bookings: FlightBooking[];
}

export function ShowFlightBookings({ bookings }: ShowFlightBookingsProps) {
  if (!bookings || bookings.length === 0) {
    return (
      <Card className="p-8">
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
              d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
            />
          </svg>
          <p className="text-sm font-medium">No flight bookings found</p>
          <p className="text-xs mt-1">Your flight bookings will appear here</p>
        </div>
      </Card>
    );
  }

  return (
    <div className="space-y-4">
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-4 mb-4">
        <h2 className="text-xl font-semibold text-gray-800">Flight Bookings</h2>
        <p className="text-sm text-gray-600 mt-1">{bookings.length} booking{bookings.length !== 1 ? 's' : ''} found</p>
      </div>

      <div className="space-y-3">
        {bookings.map((booking) => (
          <Card key={booking.booking_id} className="hover:shadow-md transition-shadow">
            <div className="p-5">
              {/* Header */}
              <div className="flex items-start justify-between mb-4">
                <div>
                  <div className="flex items-center gap-2 mb-1">
                    <h3 className="font-semibold text-gray-900">{booking.airline}</h3>
                    <Badge variant="primary" size="sm">
                      {booking.flight_number}
                    </Badge>
                  </div>
                  <p className="text-sm text-gray-600">Booking ID: {booking.booking_id}</p>
                </div>
                <Badge variant={booking.status === 'Confirmed' ? 'default' : 'secondary'}>
                  {booking.status}
                </Badge>
              </div>

              {/* Route Information */}
              <div className="bg-gray-50 rounded-lg p-4 mb-4">
                <div className="grid grid-cols-3 gap-4">
                  <div>
                    <p className="text-xs text-gray-500 mb-1">From</p>
                    <p className="font-semibold text-gray-900">{booking.from_city}</p>
                    <p className="text-sm text-gray-600">{booking.from_code}</p>
                    <p className="text-sm text-blue-600 mt-1">{booking.departure_time}</p>
                  </div>
                  <div className="flex flex-col items-center justify-center">
                    <svg
                      className="w-8 h-8 text-gray-400 mb-1"
                      fill="currentColor"
                      viewBox="0 0 20 20"
                    >
                      <path d="M10.894 2.553a1 1 0 00-1.788 0l-7 14a1 1 0 001.169 1.409l5-1.429A1 1 0 009 15.571V11a1 1 0 112 0v4.571a1 1 0 00.725.962l5 1.428a1 1 0 001.17-1.408l-7-14z" />
                    </svg>
                    <p className="text-xs text-gray-500">{booking.duration}</p>
                  </div>
                  <div className="text-right">
                    <p className="text-xs text-gray-500 mb-1">To</p>
                    <p className="font-semibold text-gray-900">{booking.to_city}</p>
                    <p className="text-sm text-gray-600">{booking.to_code}</p>
                    <p className="text-sm text-blue-600 mt-1">{booking.arrival_time}</p>
                  </div>
                </div>
              </div>

              {/* Booking Details */}
              <div className="grid grid-cols-2 gap-4 mb-4">
                <div>
                  <p className="text-xs text-gray-500 mb-1">Passenger</p>
                  <p className="text-sm font-medium text-gray-900">{booking.passenger_name}</p>
                </div>
                <div>
                  <p className="text-xs text-gray-500 mb-1">Class</p>
                  <p className="text-sm font-medium text-gray-900">{booking.class_type}</p>
                </div>
                <div>
                  <p className="text-xs text-gray-500 mb-1">Booking Date</p>
                  <p className="text-sm font-medium text-gray-900">
                    {new Date(booking.booking_date).toLocaleDateString()}
                  </p>
                </div>
                <div>
                  <p className="text-xs text-gray-500 mb-1">Total Price</p>
                  <p className="text-sm font-bold text-green-600">
                    {booking.currency} {booking.price.toLocaleString()}
                  </p>
                </div>
              </div>

              {/* Actions */}
              <div className="flex gap-2 pt-4 border-t border-gray-200">
                <button className="flex-1 bg-gray-100 hover:bg-gray-200 text-gray-700 font-medium py-2 px-4 rounded-lg transition-colors text-sm">
                  View Details
                </button>
                <button className="flex-1 bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-lg transition-colors text-sm">
                  Download Ticket
                </button>
              </div>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
}
