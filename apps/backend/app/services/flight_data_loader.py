"""
Flight Data Loader Service
Loads CSV data into PostgreSQL database and provides search functionality
"""
import csv
import psycopg2
from psycopg2.extras import execute_batch
from typing import List, Dict, Optional
import os
from pathlib import Path


class FlightDataLoader:
    """Service to load and manage flight data from CSV"""
    
    def __init__(self, database_url: str):
        self.database_url = database_url
        # Update path for Docker container - CSV is copied to /app/dataset/
        csv_in_container = Path("/app/dataset/airlines_flights_data.csv")
        # For local development
        csv_local = Path(__file__).parent.parent.parent.parent / "Data set" / "airlines_flights_data.csv"
        
        # Use container path if it exists, otherwise local
        self.csv_path = csv_in_container if csv_in_container.exists() else csv_local
    
    def get_connection(self):
        """Create database connection"""
        return psycopg2.connect(self.database_url)
    
    def create_table(self):
        """Create flights table with proper schema"""
        conn = self.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS flights (
                        id SERIAL PRIMARY KEY,
                        index_num INTEGER,
                        airline VARCHAR(100),
                        flight VARCHAR(50),
                        source_city VARCHAR(100),
                        departure_time VARCHAR(50),
                        stops VARCHAR(20),
                        arrival_time VARCHAR(50),
                        destination_city VARCHAR(100),
                        class VARCHAR(50),
                        duration DECIMAL(10,2),
                        days_left INTEGER,
                        price DECIMAL(10,2),
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                    
                    -- Create indexes for faster searches
                    CREATE INDEX IF NOT EXISTS idx_flights_source ON flights(source_city);
                    CREATE INDEX IF NOT EXISTS idx_flights_destination ON flights(destination_city);
                    CREATE INDEX IF NOT EXISTS idx_flights_airline ON flights(airline);
                    CREATE INDEX IF NOT EXISTS idx_flights_price ON flights(price);
                    CREATE INDEX IF NOT EXISTS idx_flights_stops ON flights(stops);
                    CREATE INDEX IF NOT EXISTS idx_flights_departure ON flights(departure_time);
                """)
                conn.commit()
                print("✅ Flights table created successfully")
        except Exception as e:
            conn.rollback()
            print(f"❌ Error creating table: {e}")
            raise
        finally:
            conn.close()
    
    def load_csv_data(self, batch_size: int = 1000):
        """Load CSV data into database in batches"""
        if not self.csv_path.exists():
            raise FileNotFoundError(f"CSV file not found: {self.csv_path}")
        
        conn = self.get_connection()
        try:
            with conn.cursor() as cursor:
                # Check if data already loaded
                cursor.execute("SELECT COUNT(*) FROM flights")
                count = cursor.fetchone()[0]
                if count > 0:
                    print(f"ℹ️  Data already loaded ({count} records)")
                    return count
                
                # Read and insert CSV data
                with open(self.csv_path, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    batch = []
                    total_loaded = 0
                    
                    for row in reader:
                        batch.append((
                            int(row['index']),
                            row['airline'],
                            row['flight'],
                            row['source_city'],
                            row['departure_time'],
                            row['stops'],
                            row['arrival_time'],
                            row['destination_city'],
                            row['class'],
                            float(row['duration']),
                            int(row['days_left']),
                            float(row['price'])
                        ))
                        
                        if len(batch) >= batch_size:
                            execute_batch(cursor, """
                                INSERT INTO flights (
                                    index_num, airline, flight, source_city, departure_time,
                                    stops, arrival_time, destination_city, class, duration,
                                    days_left, price
                                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                            """, batch)
                            total_loaded += len(batch)
                            print(f"📦 Loaded {total_loaded} records...")
                            batch = []
                    
                    # Insert remaining records
                    if batch:
                        execute_batch(cursor, """
                            INSERT INTO flights (
                                index_num, airline, flight, source_city, departure_time,
                                stops, arrival_time, destination_city, class, duration,
                                days_left, price
                            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        """, batch)
                        total_loaded += len(batch)
                
                conn.commit()
                print(f"✅ Successfully loaded {total_loaded} flight records")
                return total_loaded
                
        except Exception as e:
            conn.rollback()
            print(f"❌ Error loading data: {e}")
            raise
        finally:
            conn.close()
    
    def search_flights(
        self,
        source_city: Optional[str] = None,
        destination_city: Optional[str] = None,
        airline: Optional[str] = None,
        max_price: Optional[float] = None,
        stops: Optional[str] = None,
        departure_time: Optional[str] = None,
        flight_class: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[Dict]:
        """Search flights with multiple filters"""
        conn = self.get_connection()
        try:
            with conn.cursor() as cursor:
                # Build dynamic query
                query = "SELECT * FROM flights WHERE 1=1"
                params = []
                
                if source_city:
                    query += " AND LOWER(source_city) = LOWER(%s)"
                    params.append(source_city)
                
                if destination_city:
                    query += " AND LOWER(destination_city) = LOWER(%s)"
                    params.append(destination_city)
                
                if airline:
                    query += " AND LOWER(airline) LIKE LOWER(%s)"
                    params.append(f"%{airline}%")
                
                if max_price:
                    query += " AND price <= %s"
                    params.append(max_price)
                
                if stops:
                    query += " AND LOWER(stops) = LOWER(%s)"
                    params.append(stops)
                
                if departure_time:
                    query += " AND LOWER(departure_time) = LOWER(%s)"
                    params.append(departure_time)
                
                if flight_class:
                    query += " AND LOWER(class) = LOWER(%s)"
                    params.append(flight_class)
                
                # Add ordering and pagination
                query += " ORDER BY price ASC LIMIT %s OFFSET %s"
                params.extend([limit, offset])
                
                cursor.execute(query, params)
                columns = [desc[0] for desc in cursor.description]
                results = cursor.fetchall()
                
                # Convert to list of dictionaries
                flights = []
                for row in results:
                    flight_dict = dict(zip(columns, row))
                    # Convert Decimal to float for JSON serialization
                    if flight_dict.get('duration'):
                        flight_dict['duration'] = float(flight_dict['duration'])
                    if flight_dict.get('price'):
                        flight_dict['price'] = float(flight_dict['price'])
                    flights.append(flight_dict)
                
                return flights
        finally:
            conn.close()
    
    def get_statistics(self) -> Dict:
        """Get database statistics"""
        conn = self.get_connection()
        try:
            with conn.cursor() as cursor:
                stats = {}
                
                # Total flights
                cursor.execute("SELECT COUNT(*) FROM flights")
                stats['total_flights'] = cursor.fetchone()[0]
                
                # Unique airlines
                cursor.execute("SELECT COUNT(DISTINCT airline) FROM flights")
                stats['total_airlines'] = cursor.fetchone()[0]
                
                # Unique routes
                cursor.execute("SELECT COUNT(DISTINCT (source_city, destination_city)) FROM flights")
                stats['total_routes'] = cursor.fetchone()[0]
                
                # Price range
                cursor.execute("SELECT MIN(price), MAX(price), AVG(price) FROM flights")
                min_price, max_price, avg_price = cursor.fetchone()
                stats['price_range'] = {
                    'min': float(min_price) if min_price else 0,
                    'max': float(max_price) if max_price else 0,
                    'avg': float(avg_price) if avg_price else 0
                }
                
                # Top airlines
                cursor.execute("""
                    SELECT airline, COUNT(*) as flight_count 
                    FROM flights 
                    GROUP BY airline 
                    ORDER BY flight_count DESC 
                    LIMIT 10
                """)
                stats['top_airlines'] = [
                    {'airline': row[0], 'flight_count': row[1]}
                    for row in cursor.fetchall()
                ]
                
                # Popular routes
                cursor.execute("""
                    SELECT source_city, destination_city, COUNT(*) as flight_count 
                    FROM flights 
                    GROUP BY source_city, destination_city 
                    ORDER BY flight_count DESC 
                    LIMIT 10
                """)
                stats['popular_routes'] = [
                    {
                        'source': row[0],
                        'destination': row[1],
                        'flight_count': row[2]
                    }
                    for row in cursor.fetchall()
                ]
                
                return stats
        finally:
            conn.close()
    
    def get_unique_values(self) -> Dict:
        """Get unique values for filters"""
        conn = self.get_connection()
        try:
            with conn.cursor() as cursor:
                values = {}
                
                # Unique cities (both source and destination)
                cursor.execute("""
                    SELECT DISTINCT city FROM (
                        SELECT source_city as city FROM flights
                        UNION
                        SELECT destination_city as city FROM flights
                    ) cities ORDER BY city
                """)
                values['cities'] = [row[0] for row in cursor.fetchall()]
                
                # Unique airlines
                cursor.execute("SELECT DISTINCT airline FROM flights ORDER BY airline")
                values['airlines'] = [row[0] for row in cursor.fetchall()]
                
                # Unique stops
                cursor.execute("SELECT DISTINCT stops FROM flights ORDER BY stops")
                values['stops'] = [row[0] for row in cursor.fetchall()]
                
                # Unique departure times
                cursor.execute("SELECT DISTINCT departure_time FROM flights ORDER BY departure_time")
                values['departure_times'] = [row[0] for row in cursor.fetchall()]
                
                # Unique classes
                cursor.execute("SELECT DISTINCT class FROM flights ORDER BY class")
                values['classes'] = [row[0] for row in cursor.fetchall()]
                
                return values
        finally:
            conn.close()
