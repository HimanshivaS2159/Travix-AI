export type ComponentVariant = 'default' | 'primary' | 'secondary' | 'outline' | 'ghost' | 'danger';
export type ComponentSize = 'sm' | 'md' | 'lg';

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
