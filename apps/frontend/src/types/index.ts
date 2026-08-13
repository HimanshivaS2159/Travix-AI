export type ComponentVariant = 'default' | 'primary' | 'secondary' | 'outline' | 'ghost' | 'danger';
export type ComponentSize = 'sm' | 'md' | 'lg';

// Flight Types
export interface Flight {
  id: string;
  airline: string;
  flight_number: string;
  from_city: string;
  from_code: string;
  to_city: string;
  to_code: string;
  departure_time: string;
  arrival_time: string;
  duration: string;
  price: number;
  currency: string;
  class_type: string;
  stops: number;
  available_seats: number;
  baggage: string;
  amenities: string[];
}

export interface FlightBooking {
  booking_id: string;
  flight_id: string;
  airline: string;
  flight_number: string;
  from_city: string;
  from_code: string;
  to_city: string;
  to_code: string;
  departure_time: string;
  arrival_time: string;
  duration: string;
  price: number;
  currency: string;
  class_type: string;
  passenger_name: string;
  booking_date: string;
  status: string;
}

// Hotel Types
export interface Hotel {
  id: string;
  name: string;
  city: string;
  address: string;
  rating: number;
  price_per_night: number;
  currency: string;
  room_types: string[];
  amenities: string[];
}

export interface Booking {
  booking_id: string;
  hotel_id: string;
  hotel_name: string;
  city: string;
  address: string;
  rating: number;
  price_per_night: number;
  currency: string;
  room_type: string;
  check_in: string;
  check_out: string;
  nights: number;
  total_price: number;
  booked_at: string;
}

export interface TraceEvent {
  id: string;
  type: string;
  name: string;
  agent: string;
  status: string;
  input: any;
  output_summary: string;
  duration_ms: number;
  timestamp: string;
}

export interface ToolResult {
  action: string;
  message: string;
  data: any;
  trace: TraceEvent[];
}

// Schedule Types
export interface ScheduleItem {
  time: string;
  activity: string;
  location: string;
  duration: string;
  notes: string;
}

export interface DailySchedule {
  day: number;
  title: string;
  items: ScheduleItem[];
}

export interface Schedule {
  id: string;
  trip_name: string;
  city: string;
  start_date: string;
  end_date: string;
  daily_schedules: DailySchedule[];
  created_at: string;
  status: string;
}

// Rebooking Types
export interface Rebooking {
  id: string;
  type: 'flight_cancellation' | 'flight_delay' | 'hotel_cancellation';
  status: string;
  original_flight?: string;
  original_booking?: string;
  delay_hours?: number;
  compensation?: string;
  refund_amount?: string;
  created_at: string;
}
