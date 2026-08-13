import React from 'react';
import type { Flight } from '../../types';

interface FlightResultViewProps {
  flights: Flight[];
  from?: { name: string; code: string };
  to?: { name: string; code: string };
  onSelectFlight?: (flight: Flight) => void;
}

export function FlightResultView({ flights, from, to, onSelectFlight }: FlightResultViewProps) {
  if (!flights || flights.length === 0) {
    return (
      <div className="bg-white rounded-lg border border-gray-200 p-8 text-center">
        <svg
          className="w-16 h-16 mx-auto mb-4 text-gray-300"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={1.5}
            d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"
          />
        </svg>
        <p className="text-gray-600 font-medium">No flights found</p>
        <p className="text-sm text-gray-500 mt-1">Try searching for a different route</p>
      </div>
    );
  }

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
    <div className="space-y-4">
      {/* Header */}
      {from && to && (
        <div className="bg-white rounded-lg border border-gray-200 p-4 mb-4">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-xl font-semibold text-gray-900">
                {from.name} ({from.code}) → {to.name} ({to.code})
              </h2>
              <p className="text-sm text-gray-600 mt-1">
                {flights.length} flight{flights.length !== 1 ? 's' : ''} available • Sort by: Recommended
              </p>
            </div>
            <div className="flex items-center gap-2">
              <button className="px-3 py-1.5 text-sm border border-gray-300 rounded-lg hover:bg-gray-50">
                Filter
              </button>
              <button className="px-3 py-1.5 text-sm border border-gray-300 rounded-lg hover:bg-gray-50">
                Sort
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Flight Cards */}
      <div className="space-y-3">
        {flights.map((flight, index) => (
          <div
            key={flight.id}
            className="bg-white rounded-xl border border-gray-200 overflow-hidden hover:shadow-lg transition-shadow"
          >
            <div className="p-5">
              {/* Top Section - Airline Info and Price */}
              <div className="flex items-start justify-between mb-5">
                <div className="flex items-center gap-3">
                  <div className={`w-14 h-14 bg-gradient-to-br ${getAirlineColor(flight.airline)} rounded-xl flex items-center justify-center text-white font-bold text-lg shadow-md`}>
                    {getAirlineInitials(flight.airline)}
                  </div>
                  <div>
                    <h3 className="font-semibold text-gray-900 text-base">{flight.airline}</h3>
                    <p className="text-sm text-gray-500">{flight.flight_number}</p>
                    {flight.stops === 0 && (
                      <span className="inline-block mt-1 px-2 py-0.5 bg-green-100 text-green-700 text-xs font-medium rounded">
                        Non-stop
                      </span>
                    )}
                  </div>
                </div>
                <div className="text-right">
                  <div className="text-3xl font-bold text-gray-900">
                    ₹{flight.price.toLocaleString()}
                  </div>
                  <p className="text-xs text-gray-500 mt-0.5">per person</p>
                </div>
              </div>

              {/* Middle Section - Flight Times */}
              <div className="grid grid-cols-3 gap-4 mb-5 pb-5 border-b border-gray-100">
                {/* Departure */}
                <div>
                  <p className="text-xs text-gray-500 mb-1 uppercase tracking-wide">Departure</p>
                  <p className="text-3xl font-bold text-gray-900">{flight.departure_time}</p>
                  <p className="text-sm text-gray-600 mt-1 font-medium">{flight.from_city}</p>
                  <p className="text-xs text-gray-500">{flight.from_code}</p>
                </div>

                {/* Duration */}
                <div className="flex flex-col items-center justify-center">
                  <p className="text-xs text-gray-500 mb-2">{flight.duration}</p>
                  <div className="w-full relative flex items-center">
                    <div className="flex-1 h-px bg-gray-300"></div>
                    <svg
                      className="w-5 h-5 text-blue-500 mx-2"
                      fill="currentColor"
                      viewBox="0 0 20 20"
                    >
                      <path d="M10.894 2.553a1 1 0 00-1.788 0l-7 14a1 1 0 001.169 1.409l5-1.429A1 1 0 009 15.571V11a1 1 0 112 0v4.571a1 1 0 00.725.962l5 1.428a1 1 0 001.17-1.408l-7-14z" />
                    </svg>
                    <div className="flex-1 h-px bg-gray-300"></div>
                  </div>
                  <p className="text-xs text-gray-500 mt-2">
                    {flight.stops === 0 ? 'Direct' : `${flight.stops} stop${flight.stops > 1 ? 's' : ''}`}
                  </p>
                </div>

                {/* Arrival */}
                <div className="text-right">
                  <p className="text-xs text-gray-500 mb-1 uppercase tracking-wide">Arrival</p>
                  <p className="text-3xl font-bold text-gray-900">{flight.arrival_time}</p>
                  <p className="text-sm text-gray-600 mt-1 font-medium">{flight.to_city}</p>
                  <p className="text-xs text-gray-500">{flight.to_code}</p>
                </div>
              </div>

              {/* Bottom Section - Flight Details */}
              <div className="grid grid-cols-4 gap-4 mb-4">
                <div>
                  <p className="text-xs text-gray-500 mb-1">Class</p>
                  <div className="flex items-center gap-1.5">
                    <svg className="w-4 h-4 text-gray-600" fill="currentColor" viewBox="0 0 20 20">
                      <path d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" />
                    </svg>
                    <span className="text-sm font-medium text-gray-900">{flight.class_type}</span>
                  </div>
                </div>
                <div>
                  <p className="text-xs text-gray-500 mb-1">Baggage</p>
                  <div className="flex items-center gap-1.5">
                    <svg className="w-4 h-4 text-gray-600" fill="currentColor" viewBox="0 0 20 20">
                      <path d="M3 4a1 1 0 011-1h12a1 1 0 011 1v2a1 1 0 01-1 1H4a1 1 0 01-1-1V4zM3 10a1 1 0 011-1h6a1 1 0 011 1v6a1 1 0 01-1 1H4a1 1 0 01-1-1v-6zM14 9a1 1 0 00-1 1v6a1 1 0 001 1h2a1 1 0 001-1v-6a1 1 0 00-1-1h-2z" />
                    </svg>
                    <span className="text-sm font-medium text-gray-900">{flight.baggage}</span>
                  </div>
                </div>
                <div>
                  <p className="text-xs text-gray-500 mb-1">Seats</p>
                  <div className="flex items-center gap-1.5">
                    <svg className="w-4 h-4 text-gray-600" fill="currentColor" viewBox="0 0 20 20">
                      <path d="M9 6a3 3 0 11-6 0 3 3 0 016 0zM17 6a3 3 0 11-6 0 3 3 0 016 0zM12.93 17c.046-.327.07-.66.07-1a6.97 6.97 0 00-1.5-4.33A5 5 0 0119 16v1h-6.07zM6 11a5 5 0 015 5v1H1v-1a5 5 0 015-5z" />
                    </svg>
                    <span className="text-sm font-medium text-gray-900">{flight.available_seats} left</span>
                  </div>
                </div>
                <div>
                  <p className="text-xs text-gray-500 mb-1">Stops</p>
                  <span className="text-sm font-medium text-gray-900">
                    {flight.stops === 0 ? 'Non-stop' : `${flight.stops} stop${flight.stops > 1 ? 's' : ''}`}
                  </span>
                </div>
              </div>

              {/* Amenities */}
              {flight.amenities && flight.amenities.length > 0 && (
                <div className="flex flex-wrap gap-2 mb-4">
                  {flight.amenities.map((amenity, idx) => (
                    <span
                      key={idx}
                      className="px-3 py-1 bg-gray-100 text-gray-700 text-xs font-medium rounded-full border border-gray-200"
                    >
                      {amenity}
                    </span>
                  ))}
                </div>
              )}

              {/* Select Button */}
              <button
                onClick={() => onSelectFlight && onSelectFlight(flight)}
                className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-4 rounded-lg transition-colors shadow-sm hover:shadow-md flex items-center justify-center gap-2"
              >
                <span>Select Flight</span>
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                </svg>
              </button>
            </div>

            {/* Price Breakdown Toggle (Optional) */}
            <div className="bg-gray-50 px-5 py-3 border-t border-gray-100">
              <button className="text-sm text-blue-600 hover:text-blue-700 font-medium flex items-center gap-1">
                <span>View fare details</span>
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                </svg>
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
