import { useState, useEffect } from 'react';
import { Card } from '../ui/Card';
import { Button } from '../ui/Button';

interface Flight {
  id: number;
  airline: string;
  flight: string;
  source_city: string;
  destination_city: string;
  departure_time: string;
  arrival_time: string;
  stops: string;
  duration: number;
  price: number;
  days_left: number;
  class: string;
}

interface FilterOptions {
  cities: string[];
  airlines: string[];
  stops: string[];
  departure_times: string[];
  classes: string[];
}

interface SearchFilters {
  source_city: string;
  destination_city: string;
  airline: string;
  max_price: string;
  stops: string;
  departure_time: string;
  flight_class: string;
}

export function FlightSearch() {
  const [flights, setFlights] = useState<Flight[]>([]);
  const [filterOptions, setFilterOptions] = useState<FilterOptions | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [totalFlights, setTotalFlights] = useState(0);
  const [currentPage, setCurrentPage] = useState(1);
  const pageSize = 20;

  const [filters, setFilters] = useState<SearchFilters>({
    source_city: '',
    destination_city: '',
    airline: '',
    max_price: '',
    stops: '',
    departure_time: '',
    flight_class: ''
  });

  // Load filter options on component mount
  useEffect(() => {
    fetchFilterOptions();
  }, []);

  const fetchFilterOptions = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/flights/filters');
      const data = await response.json();
      setFilterOptions(data);
    } catch (err) {
      console.error('Failed to load filter options:', err);
    }
  };

  const searchFlights = async () => {
    setLoading(true);
    setError(null);

    try {
      const params = new URLSearchParams();
      
      // Add only non-empty filters
      if (filters.source_city) params.append('source_city', filters.source_city);
      if (filters.destination_city) params.append('destination_city', filters.destination_city);
      if (filters.airline) params.append('airline', filters.airline);
      if (filters.max_price) params.append('max_price', filters.max_price);
      if (filters.stops) params.append('stops', filters.stops);
      if (filters.departure_time) params.append('departure_time', filters.departure_time);
      if (filters.flight_class) params.append('flight_class', filters.flight_class);
      
      params.append('page', currentPage.toString());
      params.append('page_size', pageSize.toString());

      const response = await fetch(`http://localhost:8000/api/flights/search?${params}`);
      
      if (!response.ok) {
        throw new Error('Failed to search flights');
      }

      const data = await response.json();
      setFlights(data.flights);
      setTotalFlights(data.total);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
      setFlights([]);
    } finally {
      setLoading(false);
    }
  };

  const handleFilterChange = (key: keyof SearchFilters, value: string) => {
    setFilters(prev => ({ ...prev, [key]: value }));
    setCurrentPage(1); // Reset to first page when filters change
  };

  const handleSearch = () => {
    searchFlights();
  };

  const handleClearFilters = () => {
    setFilters({
      source_city: '',
      destination_city: '',
      airline: '',
      max_price: '',
      stops: '',
      departure_time: '',
      flight_class: ''
    });
    setCurrentPage(1);
  };

  const formatPrice = (price: number) => {
    return new Intl.NumberFormat('en-IN', {
      style: 'currency',
      currency: 'INR',
      maximumFractionDigits: 0
    }).format(price);
  };

  const formatDuration = (hours: number) => {
    const h = Math.floor(hours);
    const m = Math.round((hours - h) * 60);
    return `${h}h ${m}m`;
  };

  const getStopsLabel = (stops: string) => {
    switch (stops) {
      case 'zero': return 'Non-stop';
      case 'one': return '1 Stop';
      case 'two_or_more': return '2+ Stops';
      default: return stops;
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h2 className="text-2xl font-bold text-gray-900">Flight Search</h2>
        <p className="text-gray-600 mt-1">Search from 300,000+ flights across India</p>
      </div>

      {/* Search Filters */}
      <Card className="p-6">
        <h3 className="text-lg font-semibold mb-4">Search Filters</h3>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {/* Source City */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              From
            </label>
            <select
              value={filters.source_city}
              onChange={(e) => handleFilterChange('source_city', e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">All Cities</option>
              {filterOptions?.cities.map(city => (
                <option key={city} value={city}>{city}</option>
              ))}
            </select>
          </div>

          {/* Destination City */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              To
            </label>
            <select
              value={filters.destination_city}
              onChange={(e) => handleFilterChange('destination_city', e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">All Cities</option>
              {filterOptions?.cities.map(city => (
                <option key={city} value={city}>{city}</option>
              ))}
            </select>
          </div>

          {/* Airline */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Airline
            </label>
            <select
              value={filters.airline}
              onChange={(e) => handleFilterChange('airline', e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">All Airlines</option>
              {filterOptions?.airlines.map(airline => (
                <option key={airline} value={airline}>{airline}</option>
              ))}
            </select>
          </div>

          {/* Max Price */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Max Price
            </label>
            <input
              type="number"
              value={filters.max_price}
              onChange={(e) => handleFilterChange('max_price', e.target.value)}
              placeholder="e.g., 10000"
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          {/* Stops */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Stops
            </label>
            <select
              value={filters.stops}
              onChange={(e) => handleFilterChange('stops', e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">All</option>
              {filterOptions?.stops.map(stop => (
                <option key={stop} value={stop}>{getStopsLabel(stop)}</option>
              ))}
            </select>
          </div>

          {/* Departure Time */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Departure Time
            </label>
            <select
              value={filters.departure_time}
              onChange={(e) => handleFilterChange('departure_time', e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">Any Time</option>
              {filterOptions?.departure_times.map(time => (
                <option key={time} value={time}>{time.replace('_', ' ')}</option>
              ))}
            </select>
          </div>

          {/* Class */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Class
            </label>
            <select
              value={filters.flight_class}
              onChange={(e) => handleFilterChange('flight_class', e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">All</option>
              {filterOptions?.classes.map(cls => (
                <option key={cls} value={cls}>{cls}</option>
              ))}
            </select>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex gap-3 mt-6">
          <Button onClick={handleSearch} disabled={loading}>
            {loading ? 'Searching...' : 'Search Flights'}
          </Button>
          <Button variant="outline" onClick={handleClearFilters}>
            Clear Filters
          </Button>
        </div>
      </Card>

      {/* Error Message */}
      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
          <p className="font-medium">Error</p>
          <p className="text-sm">{error}</p>
        </div>
      )}

      {/* Results Summary */}
      {flights.length > 0 && (
        <div className="text-sm text-gray-600">
          Found {totalFlights} flight{totalFlights !== 1 ? 's' : ''} 
          {currentPage > 1 && ` - Page ${currentPage}`}
        </div>
      )}

      {/* Flight Results */}
      {loading ? (
        <div className="text-center py-12">
          <div className="inline-block h-8 w-8 animate-spin rounded-full border-4 border-solid border-blue-600 border-r-transparent"></div>
          <p className="mt-4 text-gray-600">Searching flights...</p>
        </div>
      ) : flights.length > 0 ? (
        <div className="space-y-4">
          {flights.map((flight) => (
            <Card key={flight.id} className="p-5 hover:shadow-lg transition-shadow">
              <div className="flex items-center justify-between">
                {/* Flight Info */}
                <div className="flex-1">
                  <div className="flex items-center gap-3 mb-3">
                    <h3 className="text-lg font-semibold text-gray-900">
                      {flight.airline}
                    </h3>
                    <span className="text-sm text-gray-500">
                      {flight.flight}
                    </span>
                    <span className={`text-xs px-2 py-1 rounded-full ${
                      flight.class === 'Business' 
                        ? 'bg-purple-100 text-purple-700' 
                        : 'bg-blue-100 text-blue-700'
                    }`}>
                      {flight.class}
                    </span>
                  </div>

                  <div className="flex items-center gap-6 text-sm">
                    {/* Route */}
                    <div className="flex items-center gap-3">
                      <div className="text-center">
                        <div className="font-semibold text-gray-900">
                          {flight.source_city}
                        </div>
                        <div className="text-xs text-gray-500">
                          {flight.departure_time.replace('_', ' ')}
                        </div>
                      </div>
                      
                      <div className="flex flex-col items-center">
                        <div className="text-xs text-gray-500 mb-1">
                          {formatDuration(flight.duration)}
                        </div>
                        <div className="w-24 h-px bg-gray-300 relative">
                          <div className="absolute -top-1 left-1/2 transform -translate-x-1/2">
                            ✈️
                          </div>
                        </div>
                        <div className="text-xs text-gray-500 mt-1">
                          {getStopsLabel(flight.stops)}
                        </div>
                      </div>

                      <div className="text-center">
                        <div className="font-semibold text-gray-900">
                          {flight.destination_city}
                        </div>
                        <div className="text-xs text-gray-500">
                          {flight.arrival_time.replace('_', ' ')}
                        </div>
                      </div>
                    </div>
                  </div>

                  {flight.days_left <= 7 && (
                    <div className="mt-2 text-xs text-orange-600">
                      ⚠️ Only {flight.days_left} days left to book
                    </div>
                  )}
                </div>

                {/* Price & Book Button */}
                <div className="text-right ml-6">
                  <div className="text-2xl font-bold text-gray-900 mb-2">
                    {formatPrice(flight.price)}
                  </div>
                  <Button size="sm">
                    Book Now
                  </Button>
                </div>
              </div>
            </Card>
          ))}

          {/* Pagination */}
          {totalFlights > pageSize && (
            <div className="flex justify-center gap-2 mt-6">
              <Button
                variant="outline"
                size="sm"
                onClick={() => setCurrentPage(p => Math.max(1, p - 1))}
                disabled={currentPage === 1}
              >
                Previous
              </Button>
              <span className="px-4 py-2 text-sm text-gray-700">
                Page {currentPage}
              </span>
              <Button
                variant="outline"
                size="sm"
                onClick={() => setCurrentPage(p => p + 1)}
                disabled={flights.length < pageSize}
              >
                Next
              </Button>
            </div>
          )}
        </div>
      ) : !loading ? (
        <Card className="p-12 text-center">
          <div className="text-gray-400 text-5xl mb-4">✈️</div>
          <h3 className="text-lg font-medium text-gray-900 mb-2">
            No flights found
          </h3>
          <p className="text-gray-600">
            Try adjusting your search filters to find more results
          </p>
        </Card>
      ) : null}
    </div>
  );
}
