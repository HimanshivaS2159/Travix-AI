import React from 'react';
import { useOrchestratorContext } from '../../contexts/OrchestratorContext';
import { Hotel, Booking, Flight, FlightBooking } from '../../types';
import { Star, MapPin, Wifi, Coffee, Dumbbell, Waves, Plane } from 'lucide-react';
import { FlightResultView } from './FlightResultView';
import { ShowFlightBookings } from './ShowFlightBookings';
import { LocalGuideView } from './LocalGuideView';
import { ExpenseForm } from './ExpenseForm';
import { ShowExpenses } from './ShowExpenses';
import { TripForm } from './TripForm';
import { ShowTrips } from './ShowTrips';

interface ResultViewProps {
  onSelectFlight?: (flight: Flight) => void;
}

export function ResultView({ onSelectFlight }: ResultViewProps) {
  const { currentResult } = useOrchestratorContext();

  if (!currentResult) {
    return (
      <div className="p-6 h-full flex items-center justify-center">
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
              d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
            />
          </svg>
          <p className="text-sm font-medium">No results to display</p>
          <p className="text-xs mt-1">Results will appear here when available</p>
        </div>
      </div>
    );
  }

  // Render based on action type
  if (currentResult.action === 'search_flights') {
    const handleSelectFlight = (flight: Flight) => {
      if (onSelectFlight) {
        onSelectFlight(flight);
      }
    };

    return (
      <div className="p-6">
        <FlightResultView
          flights={currentResult.data?.flights || []}
          from={currentResult.data?.from}
          to={currentResult.data?.to}
          onSelectFlight={handleSelectFlight}
        />
      </div>
    );
  } else if (currentResult.action === 'book_flight') {
    return <FlightBookingConfirmationView booking={currentResult.data?.booking} message={currentResult.message} />;
  } else if (currentResult.action === 'list_flight_bookings') {
    return (
      <div className="p-6">
        <ShowFlightBookings bookings={currentResult.data?.bookings || []} />
      </div>
    );
  } else if (currentResult.action === 'list_hotels') {
    return <HotelListView hotels={currentResult.data || []} message={currentResult.message} />;
  } else if (currentResult.action === 'book_hotel') {
    return <BookingConfirmationView booking={currentResult.data} message={currentResult.message} />;
  } else if (currentResult.action === 'list_bookings') {
    return <BookingsListView bookings={currentResult.data || []} message={currentResult.message} />;
  } else if (
    currentResult.action === 'get_attractions' ||
    currentResult.action === 'get_restaurants' ||
    currentResult.action === 'get_local_tips' ||
    currentResult.action === 'get_hidden_gems' ||
    currentResult.action === 'complete_local_guide'
  ) {
    return <LocalGuideView data={currentResult.data} message={currentResult.message} />;
  } else if (currentResult.action === 'create_expense') {
    return (
      <div className="p-6">
        <ExpenseForm
          formData={currentResult.data}
          onSubmit={(data) => {
            console.log('Expense submitted:', data);
            // Form will handle API call internally
          }}
          onCancel={() => {
            console.log('Cancelled');
            // Could add a message or clear current result
          }}
        />
      </div>
    );
  } else if (currentResult.action === 'show_expenses') {
    return (
      <div className="p-6">
        <ShowExpenses
          expenses={currentResult.data?.expenses || []}
          statistics={currentResult.data?.statistics}
        />
      </div>
    );
  } else if (currentResult.action === 'expense_created') {
    return <ExpenseCreatedView expense={currentResult.data?.expense} message={currentResult.message} />;
  } else if (currentResult.action === 'create_trip') {
    return (
      <div className="h-full">
        <TripForm
          onSubmit={(data) => {
            console.log('Trip submitted:', data);
            // Form will handle API call internally
          }}
          onCancel={() => {
            console.log('Cancelled');
            // Could add a message or clear current result
          }}
        />
      </div>
    );
  } else if (currentResult.action === 'show_trips') {
    return (
      <div className="p-6">
        <ShowTrips trips={currentResult.data?.trips || []} />
      </div>
    );
  } else if (currentResult.action === 'trip_created') {
    return <TripCreatedView trip={currentResult.data?.trip} message={currentResult.message} />;
  }

  return (
    <div className="p-6">
      <div className="text-gray-700">
        <p className="text-sm">{currentResult.message}</p>
      </div>
    </div>
  );
}

// Hotel List View Component
function HotelListView({ hotels, message }: { hotels: Hotel[]; message: string }) {
  const getAmenityIcon = (amenity: string) => {
    const lower = amenity.toLowerCase();
    if (lower.includes('wifi')) return <Wifi size={14} />;
    if (lower.includes('breakfast') || lower.includes('coffee')) return <Coffee size={14} />;
    if (lower.includes('gym')) return <Dumbbell size={14} />;
    if (lower.includes('pool') || lower.includes('spa')) return <Waves size={14} />;
    return null;
  };

  return (
    <div className="p-6">
      <div className="mb-4">
        <h2 className="text-xl font-semibold text-gray-800">{message}</h2>
      </div>

      {hotels.length === 0 ? (
        <div className="text-center text-gray-500 py-8">
          <p>{message}</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {hotels.map((hotel) => (
            <div
              key={hotel.id}
              className="bg-white rounded-lg shadow-md border border-gray-200 p-4 hover:shadow-lg transition-shadow"
            >
              <div className="flex items-start justify-between mb-2">
                <h3 className="text-lg font-semibold text-gray-800">{hotel.name}</h3>
                <div className="flex items-center gap-1 bg-yellow-100 px-2 py-1 rounded">
                  <Star size={14} className="text-yellow-600 fill-yellow-600" />
                  <span className="text-sm font-medium text-yellow-700">{hotel.rating}</span>
                </div>
              </div>

              <div className="flex items-start gap-1 text-gray-600 text-sm mb-3">
                <MapPin size={14} className="mt-0.5 flex-shrink-0" />
                <span>{hotel.address}</span>
              </div>

              <div className="mb-3">
                <div className="text-2xl font-bold text-gray-900">
                  {hotel.currency} {hotel.price_per_night.toLocaleString()}
                </div>
                <div className="text-xs text-gray-500">per night</div>
              </div>

              <div className="mb-3">
                <div className="text-xs font-medium text-gray-600 mb-1">Room Types</div>
                <div className="flex flex-wrap gap-1">
                  {hotel.room_types.map((type, idx) => (
                    <span
                      key={idx}
                      className="bg-blue-100 text-blue-700 text-xs px-2 py-1 rounded"
                    >
                      {type}
                    </span>
                  ))}
                </div>
              </div>

              <div>
                <div className="text-xs font-medium text-gray-600 mb-1">Amenities</div>
                <div className="flex flex-wrap gap-2">
                  {hotel.amenities.slice(0, 5).map((amenity, idx) => (
                    <span
                      key={idx}
                      className="flex items-center gap-1 bg-gray-100 text-gray-700 text-xs px-2 py-1 rounded"
                    >
                      {getAmenityIcon(amenity)}
                      {amenity}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

// Booking Confirmation View Component
function BookingConfirmationView({ booking, message }: { booking: Booking | null; message: string }) {
  if (!booking) {
    return (
      <div className="p-6">
        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
          <p className="text-yellow-800">{message}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="p-6">
      <div className="max-w-2xl mx-auto">
        <div className="bg-green-50 border border-green-200 rounded-lg p-4 mb-6">
          <div className="flex items-center gap-2 mb-2">
            <svg
              className="w-6 h-6 text-green-600"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M5 13l4 4L19 7"
              />
            </svg>
            <h2 className="text-lg font-semibold text-green-800">Hotel Booked Successfully!</h2>
          </div>
          <p className="text-sm text-green-700">{message}</p>
        </div>

        <div className="bg-white rounded-lg shadow-md border border-gray-200 p-6">
          <div className="mb-4 pb-4 border-b border-gray-200">
            <h3 className="text-xl font-bold text-gray-900">{booking.hotel_name}</h3>
            <div className="flex items-center gap-2 mt-1">
              <MapPin size={16} className="text-gray-500" />
              <span className="text-sm text-gray-600">{booking.address}</span>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4 mb-4">
            <div>
              <div className="text-xs font-medium text-gray-500 mb-1">Rating</div>
              <div className="flex items-center gap-1">
                <Star size={16} className="text-yellow-600 fill-yellow-600" />
                <span className="text-sm font-medium text-gray-900">{booking.rating}</span>
              </div>
            </div>
            <div>
              <div className="text-xs font-medium text-gray-500 mb-1">Room Type</div>
              <div className="text-sm font-medium text-gray-900">{booking.room_type}</div>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4 mb-4">
            <div>
              <div className="text-xs font-medium text-gray-500 mb-1">Check-in</div>
              <div className="text-sm font-medium text-gray-900">{booking.check_in}</div>
            </div>
            <div>
              <div className="text-xs font-medium text-gray-500 mb-1">Check-out</div>
              <div className="text-sm font-medium text-gray-900">{booking.check_out}</div>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4 mb-4 pb-4 border-b border-gray-200">
            <div>
              <div className="text-xs font-medium text-gray-500 mb-1">Price per night</div>
              <div className="text-sm font-medium text-gray-900">
                {booking.currency} {booking.price_per_night.toLocaleString()}
              </div>
            </div>
            <div>
              <div className="text-xs font-medium text-gray-500 mb-1">Nights</div>
              <div className="text-sm font-medium text-gray-900">{booking.nights}</div>
            </div>
          </div>

          <div className="flex items-center justify-between">
            <div>
              <div className="text-xs font-medium text-gray-500 mb-1">Total Price</div>
              <div className="text-2xl font-bold text-gray-900">
                {booking.currency} {booking.total_price.toLocaleString()}
              </div>
            </div>
            <div>
              <div className="text-xs font-medium text-gray-500 mb-1">Booking ID</div>
              <div className="text-sm font-mono font-medium text-blue-600">{booking.booking_id}</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

// Bookings List View Component
function BookingsListView({ bookings, message }: { bookings: Booking[]; message: string }) {
  return (
    <div className="p-6">
      <div className="mb-4">
        <h2 className="text-xl font-semibold text-gray-800">{message}</h2>
      </div>

      {bookings.length === 0 ? (
        <div className="text-center text-gray-500 py-8">
          <p>No bookings found.</p>
        </div>
      ) : (
        <div className="space-y-4">
          {bookings.map((booking) => (
            <div
              key={booking.booking_id}
              className="bg-white rounded-lg shadow-md border border-gray-200 p-4"
            >
              <div className="flex items-start justify-between mb-3">
                <div>
                  <h3 className="text-lg font-semibold text-gray-800">{booking.hotel_name}</h3>
                  <div className="flex items-center gap-2 mt-1">
                    <MapPin size={14} className="text-gray-500" />
                    <span className="text-sm text-gray-600">{booking.city}</span>
                    <span className="text-gray-400">•</span>
                    <span className="text-xs font-mono text-blue-600">{booking.booking_id}</span>
                  </div>
                </div>
                <div className="flex items-center gap-1 bg-yellow-100 px-2 py-1 rounded">
                  <Star size={14} className="text-yellow-600 fill-yellow-600" />
                  <span className="text-sm font-medium text-yellow-700">{booking.rating}</span>
                </div>
              </div>

              <div className="grid grid-cols-4 gap-4 text-sm">
                <div>
                  <div className="text-xs text-gray-500 mb-1">Check-in</div>
                  <div className="font-medium text-gray-900">{booking.check_in}</div>
                </div>
                <div>
                  <div className="text-xs text-gray-500 mb-1">Check-out</div>
                  <div className="font-medium text-gray-900">{booking.check_out}</div>
                </div>
                <div>
                  <div className="text-xs text-gray-500 mb-1">Room</div>
                  <div className="font-medium text-gray-900">{booking.room_type}</div>
                </div>
                <div className="text-right">
                  <div className="text-xs text-gray-500 mb-1">Total</div>
                  <div className="font-bold text-gray-900">
                    {booking.currency} {booking.total_price.toLocaleString()}
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

// Flight Booking Confirmation View Component
function FlightBookingConfirmationView({ booking, message }: { booking: FlightBooking | null; message: string }) {
  if (!booking) {
    return (
      <div className="p-6">
        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
          <p className="text-yellow-800">{message}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="p-6">
      <div className="max-w-2xl mx-auto">
        <div className="bg-green-50 border border-green-200 rounded-lg p-4 mb-6">
          <div className="flex items-center gap-2 mb-2">
            <svg
              className="w-6 h-6 text-green-600"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M5 13l4 4L19 7"
              />
            </svg>
            <h2 className="text-lg font-semibold text-green-800">Flight Booked Successfully!</h2>
          </div>
          <p className="text-sm text-green-700">{message}</p>
        </div>

        <div className="bg-white rounded-lg shadow-md border border-gray-200 p-6">
          <div className="mb-4 pb-4 border-b border-gray-200">
            <div className="flex items-center gap-3 mb-2">
              <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-blue-600 rounded-lg flex items-center justify-center">
                <Plane className="w-6 h-6 text-white" />
              </div>
              <div>
                <h3 className="text-xl font-bold text-gray-900">{booking.airline}</h3>
                <p className="text-sm text-gray-600">{booking.flight_number}</p>
              </div>
            </div>
          </div>

          <div className="bg-gray-50 rounded-lg p-4 mb-4">
            <div className="grid grid-cols-3 gap-4">
              <div>
                <p className="text-xs text-gray-500 mb-1">From</p>
                <p className="font-semibold text-gray-900">{booking.from_city}</p>
                <p className="text-sm text-gray-600">{booking.from_code}</p>
                <p className="text-sm text-blue-600 mt-1">{booking.departure_time}</p>
              </div>
              <div className="flex flex-col items-center justify-center">
                <Plane className="w-6 h-6 text-gray-400 mb-1" />
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

          <div className="grid grid-cols-2 gap-4 mb-4">
            <div>
              <div className="text-xs font-medium text-gray-500 mb-1">Passenger</div>
              <div className="text-sm font-medium text-gray-900">{booking.passenger_name}</div>
            </div>
            <div>
              <div className="text-xs font-medium text-gray-500 mb-1">Class</div>
              <div className="text-sm font-medium text-gray-900">{booking.class_type}</div>
            </div>
            <div>
              <div className="text-xs font-medium text-gray-500 mb-1">Booking Date</div>
              <div className="text-sm font-medium text-gray-900">
                {new Date(booking.booking_date).toLocaleDateString()}
              </div>
            </div>
            <div>
              <div className="text-xs font-medium text-gray-500 mb-1">Status</div>
              <div className="text-sm font-medium text-green-600">{booking.status}</div>
            </div>
          </div>

          <div className="pt-4 border-t border-gray-200">
            <div className="flex items-center justify-between">
              <div>
                <div className="text-xs font-medium text-gray-500 mb-1">Total Price</div>
                <div className="text-2xl font-bold text-gray-900">
                  {booking.currency} {booking.price.toLocaleString()}
                </div>
              </div>
              <div className="text-right">
                <div className="text-xs font-medium text-gray-500 mb-1">Booking ID</div>
                <div className="text-sm font-mono font-medium text-blue-600">{booking.booking_id}</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

// Expense Created View Component
function ExpenseCreatedView({ expense, message }: { expense: any; message: string }) {
  if (!expense) {
    return (
      <div className="p-6">
        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
          <p className="text-yellow-800">{message}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="p-6">
      <div className="max-w-2xl mx-auto">
        <div className="bg-green-50 border border-green-200 rounded-lg p-4 mb-6">
          <div className="flex items-center gap-2 mb-2">
            <svg
              className="w-6 h-6 text-green-600"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M5 13l4 4L19 7"
              />
            </svg>
            <h2 className="text-lg font-semibold text-green-800">Expense Created Successfully!</h2>
          </div>
          <p className="text-sm text-green-700">{message}</p>
        </div>

        <div className="bg-white rounded-lg shadow-md border border-gray-200 p-6">
          <div className="mb-4 pb-4 border-b border-gray-200">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="text-xl font-bold text-gray-900">{expense.merchant}</h3>
                <p className="text-sm text-gray-600">{expense.category}</p>
              </div>
              <div className="text-2xl font-bold text-gray-900">
                {expense.currency} {expense.amount.toLocaleString()}
              </div>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4 mb-4">
            <div>
              <div className="text-xs font-medium text-gray-500 mb-1">Expense ID</div>
              <div className="text-sm font-mono font-medium text-blue-600">{expense.expense_id}</div>
            </div>
            <div>
              <div className="text-xs font-medium text-gray-500 mb-1">Date</div>
              <div className="text-sm font-medium text-gray-900">
                {new Date(expense.date).toLocaleDateString()}
              </div>
            </div>
            <div>
              <div className="text-xs font-medium text-gray-500 mb-1">Payment Method</div>
              <div className="text-sm font-medium text-gray-900">{expense.payment_method}</div>
            </div>
            <div>
              <div className="text-xs font-medium text-gray-500 mb-1">Status</div>
              <div className="text-sm font-medium text-yellow-600">{expense.status}</div>
            </div>
          </div>

          {expense.gst_amount && (
            <div className="mb-4">
              <div className="text-xs font-medium text-gray-500 mb-1">GST Amount</div>
              <div className="text-sm font-medium text-gray-900">₹{expense.gst_amount}</div>
            </div>
          )}

          {expense.notes && (
            <div className="bg-gray-50 rounded-lg p-3">
              <div className="text-xs font-medium text-gray-500 mb-1">Notes</div>
              <p className="text-sm text-gray-700">{expense.notes}</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

// Trip Created View Component
function TripCreatedView({ trip, message }: { trip: any; message: string }) {
  if (!trip) {
    return (
      <div className="p-6">
        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
          <p className="text-yellow-800">{message}</p>
        </div>
      </div>
    );
  }

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric' });
  };

  const calculateDuration = () => {
    const start = new Date(trip.start_date);
    const end = new Date(trip.end_date);
    const days = Math.ceil((end.getTime() - start.getTime()) / (1000 * 60 * 60 * 24)) + 1;
    return days;
  };

  return (
    <div className="p-6">
      <div className="max-w-2xl mx-auto">
        <div className="bg-green-50 border border-green-200 rounded-lg p-4 mb-6">
          <div className="flex items-center gap-2 mb-2">
            <svg
              className="w-6 h-6 text-green-600"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M5 13l4 4L19 7"
              />
            </svg>
            <h2 className="text-lg font-semibold text-green-800">Trip Created Successfully!</h2>
          </div>
          <p className="text-sm text-green-700">{message}</p>
        </div>

        <div className="bg-white rounded-lg shadow-md border border-gray-200 p-6">
          <div className="mb-4 pb-4 border-b border-gray-200">
            <div className="flex items-center gap-3 mb-2">
              <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-blue-600 rounded-lg flex items-center justify-center">
                <Plane className="w-6 h-6 text-white" />
              </div>
              <div>
                <h3 className="text-xl font-bold text-gray-900">{trip.trip_name}</h3>
                <p className="text-sm text-gray-600">{trip.trip_id}</p>
              </div>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4 mb-4">
            <div>
              <div className="text-xs font-medium text-gray-500 mb-1">Start Date</div>
              <div className="text-sm font-medium text-gray-900">{formatDate(trip.start_date)}</div>
            </div>
            <div>
              <div className="text-xs font-medium text-gray-500 mb-1">End Date</div>
              <div className="text-sm font-medium text-gray-900">{formatDate(trip.end_date)}</div>
            </div>
            <div>
              <div className="text-xs font-medium text-gray-500 mb-1">Duration</div>
              <div className="text-sm font-medium text-gray-900">{calculateDuration()} days</div>
            </div>
            <div>
              <div className="text-xs font-medium text-gray-500 mb-1">Status</div>
              <div className="text-sm font-medium text-blue-600">{trip.status}</div>
            </div>
          </div>

          <div className="mb-4">
            <div className="text-xs font-medium text-gray-500 mb-1">Destination</div>
            <div className="text-sm font-medium text-gray-900">{trip.destination}</div>
          </div>

          {trip.purpose && (
            <div className="bg-gray-50 rounded-lg p-3">
              <div className="text-xs font-medium text-gray-500 mb-1">Business Purpose</div>
              <p className="text-sm text-gray-700">{trip.purpose}</p>
            </div>
          )}

          <div className="mt-4 p-3 bg-blue-50 border border-blue-100 rounded-lg">
            <p className="text-xs text-blue-800">
              💡 You can now associate expenses with this trip when creating new expenses
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
