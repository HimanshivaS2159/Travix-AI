"""
Add sample flights for all Indian state capitals
This script adds flights connecting all 28 state capitals + 8 union territory capitals
"""
import psycopg2
from psycopg2.extras import execute_batch
import os
import random
from datetime import datetime, timedelta

# Database connection
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://travix:travix_password@localhost:5432/travix_db"
)

# All Indian State and UT Capitals
CAPITALS = [
    # States
    "Amaravati",      # Andhra Pradesh
    "Itanagar",       # Arunachal Pradesh
    "Dispur",         # Assam
    "Patna",          # Bihar
    "Raipur",         # Chhattisgarh
    "Panaji",         # Goa
    "Gandhinagar",    # Gujarat
    "Chandigarh",     # Haryana (also UT)
    "Shimla",         # Himachal Pradesh
    "Ranchi",         # Jharkhand
    "Bengaluru",      # Karnataka (already exists as Bangalore)
    "Thiruvananthapuram",  # Kerala
    "Bhopal",         # Madhya Pradesh
    "Mumbai",         # Maharashtra (already exists)
    "Imphal",         # Manipur
    "Shillong",       # Meghalaya
    "Aizawl",         # Mizoram
    "Kohima",         # Nagaland
    "Bhubaneswar",    # Odisha
    "Jaipur",         # Rajasthan
    "Gangtok",        # Sikkim
    "Chennai",        # Tamil Nadu (already exists)
    "Hyderabad",      # Telangana (already exists)
    "Agartala",       # Tripura
    "Lucknow",        # Uttar Pradesh
    "Dehradun",       # Uttarakhand
    "Kolkata",        # West Bengal (already exists)
    
    # Union Territories
    "Delhi",          # Delhi (already exists)
    "Chandigarh",     # Chandigarh (already added above)
    "Daman",          # Daman and Diu
    "Kavaratti",      # Lakshadweep
    "Puducherry",     # Puducherry
    "Port Blair",     # Andaman and Nicobar
    "Srinagar",       # Jammu and Kashmir
    "Leh",            # Ladakh
]

# Remove duplicates and cities already in dataset
EXISTING_CITIES = ["Delhi", "Mumbai", "Bangalore", "Chennai", "Kolkata", "Hyderabad"]
NEW_CAPITALS = [city for city in set(CAPITALS) if city not in EXISTING_CITIES and city != "Chandigarh"]
NEW_CAPITALS.append("Chandigarh")  # Add Chandigarh once
NEW_CAPITALS = list(set(NEW_CAPITALS))  # Remove final duplicates

# Airlines
AIRLINES = ["Air_India", "Indigo", "SpiceJet", "Vistara", "AirAsia", "GO_FIRST"]

# Departure times
DEPARTURE_TIMES = ["Early_Morning", "Morning", "Afternoon", "Evening", "Night", "Late_Night"]
ARRIVAL_TIMES = ["Early_Morning", "Morning", "Afternoon", "Evening", "Night", "Late_Night"]

# Stops
STOPS = ["zero", "one", "two_or_more"]

# Classes
CLASSES = ["Economy", "Business"]


def generate_flight_number(airline):
    """Generate realistic flight numbers"""
    prefixes = {
        "Air_India": "AI",
        "Indigo": "6E",
        "SpiceJet": "SG",
        "Vistara": "UK",
        "AirAsia": "I5",
        "GO_FIRST": "G8"
    }
    prefix = prefixes.get(airline, "XX")
    number = random.randint(100, 9999)
    return f"{prefix}-{number}"


def generate_price(distance_factor, stops, flight_class):
    """Generate realistic prices based on distance, stops, and class"""
    base_price = random.randint(3000, 8000)
    
    # Distance factor (1.0 to 3.0)
    base_price *= distance_factor
    
    # Stops factor
    if stops == "zero":
        base_price *= 1.0
    elif stops == "one":
        base_price *= 0.85
    else:
        base_price *= 0.70
    
    # Class factor
    if flight_class == "Business":
        base_price *= random.uniform(2.5, 4.0)
    
    # Random variation
    base_price *= random.uniform(0.9, 1.3)
    
    return round(base_price, 2)


def calculate_distance_factor(source, destination):
    """Estimate distance factor between cities (1.0 to 3.0)"""
    # Major hubs
    major_hubs = ["Delhi", "Mumbai", "Bangalore", "Chennai", "Kolkata", "Hyderabad"]
    
    # If both are major cities, medium distance
    if source in major_hubs and destination in major_hubs:
        return random.uniform(1.5, 2.5)
    
    # If one is major city, random distance
    if source in major_hubs or destination in major_hubs:
        return random.uniform(1.2, 2.8)
    
    # Smaller cities, random
    return random.uniform(1.0, 3.0)


def generate_flights():
    """Generate sample flights for all state capitals"""
    flights = []
    flight_id = 300154  # Continue from existing data
    
    # All cities (existing + new)
    all_cities = EXISTING_CITIES + NEW_CAPITALS
    
    print(f"Generating flights for {len(all_cities)} cities...")
    print(f"Total possible routes: {len(all_cities) * (len(all_cities) - 1)}")
    
    # Generate flights between all cities
    for source in all_cities:
        for destination in all_cities:
            if source == destination:
                continue
            
            # Generate 5-15 flights per route
            num_flights = random.randint(5, 15)
            
            for _ in range(num_flights):
                airline = random.choice(AIRLINES)
                flight_number = generate_flight_number(airline)
                departure_time = random.choice(DEPARTURE_TIMES)
                arrival_time = random.choice(ARRIVAL_TIMES)
                stops = random.choice(STOPS)
                flight_class = random.choice(CLASSES)
                
                # Calculate duration based on stops
                if stops == "zero":
                    duration = round(random.uniform(1.5, 4.0), 2)
                elif stops == "one":
                    duration = round(random.uniform(3.0, 8.0), 2)
                else:
                    duration = round(random.uniform(6.0, 15.0), 2)
                
                # Calculate price
                distance_factor = calculate_distance_factor(source, destination)
                price = generate_price(distance_factor, stops, flight_class)
                
                # Days left to book
                days_left = random.randint(1, 60)
                
                flights.append((
                    flight_id,
                    airline,
                    flight_number,
                    source,
                    departure_time,
                    stops,
                    arrival_time,
                    destination,
                    flight_class,
                    duration,
                    days_left,
                    price
                ))
                
                flight_id += 1
    
    return flights


def insert_flights(flights):
    """Insert flights into database"""
    conn = psycopg2.connect(DATABASE_URL)
    try:
        with conn.cursor() as cursor:
            # Check current count
            cursor.execute("SELECT COUNT(*) FROM flights")
            before_count = cursor.fetchone()[0]
            print(f"\nCurrent flights in database: {before_count}")
            
            # Insert new flights in batches
            print(f"\nInserting {len(flights)} new flights...")
            
            execute_batch(cursor, """
                INSERT INTO flights (
                    index_num, airline, flight, source_city, departure_time,
                    stops, arrival_time, destination_city, class, duration,
                    days_left, price
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, flights, page_size=1000)
            
            conn.commit()
            
            # Check new count
            cursor.execute("SELECT COUNT(*) FROM flights")
            after_count = cursor.fetchone()[0]
            print(f"\nFlights after insertion: {after_count}")
            print(f"New flights added: {after_count - before_count}")
            
            # Get city statistics
            cursor.execute("""
                SELECT DISTINCT city FROM (
                    SELECT source_city as city FROM flights
                    UNION
                    SELECT destination_city as city FROM flights
                ) cities ORDER BY city
            """)
            cities = [row[0] for row in cursor.fetchall()]
            print(f"\nTotal cities now covered: {len(cities)}")
            print(f"Cities: {', '.join(cities)}")
            
            # Get route statistics
            cursor.execute("""
                SELECT COUNT(DISTINCT (source_city, destination_city))
                FROM flights
            """)
            routes = cursor.fetchone()[0]
            print(f"\nTotal routes: {routes}")
            
    except Exception as e:
        conn.rollback()
        print(f"\nError inserting flights: {e}")
        raise
    finally:
        conn.close()


def main():
    print("=" * 70)
    print("TRAVIX AI - Adding State Capital Flights")
    print("=" * 70)
    
    print(f"\n📍 Indian State Capitals to be added:")
    for i, capital in enumerate(sorted(NEW_CAPITALS), 1):
        print(f"   {i:2d}. {capital}")
    
    print(f"\n✈️  Existing cities in database:")
    for city in EXISTING_CITIES:
        print(f"   • {city}")
    
    print(f"\n🔄 Generating flights...")
    flights = generate_flights()
    
    print(f"\n📊 Generated {len(flights)} flights")
    print(f"   • Routes: All state capitals connected")
    print(f"   • Airlines: {len(AIRLINES)} airlines")
    print(f"   • Classes: Economy and Business")
    print(f"   • Stops: Non-stop, 1 stop, 2+ stops")
    
    response = input("\n⚠️  Proceed with insertion? (yes/no): ")
    
    if response.lower() in ['yes', 'y']:
        insert_flights(flights)
        print("\n" + "=" * 70)
        print("✅ SUCCESS! All state capital flights have been added!")
        print("=" * 70)
        print("\n🎉 You can now search flights between ANY Indian state capitals!")
    else:
        print("\n❌ Operation cancelled.")


if __name__ == "__main__":
    main()
