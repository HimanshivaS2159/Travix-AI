"""
Script to initialize flights database
Run this once to load CSV data into PostgreSQL
"""
import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from app.services.flight_data_loader import FlightDataLoader


def main():
    print("=" * 60)
    print("TRAVIX AI - Flight Database Initialization")
    print("=" * 60)
    print()
    
    # Get database URL from environment
    database_url = os.getenv(
        "DATABASE_URL",
        "postgresql://travix:travix_password@localhost:5432/travix_db"
    )
    
    print(f"📊 Database: {database_url.split('@')[1] if '@' in database_url else 'unknown'}")
    print()
    
    # Initialize loader
    loader = FlightDataLoader(database_url)
    
    try:
        # Step 1: Create table
        print("Step 1: Creating flights table...")
        loader.create_table()
        print()
        
        # Step 2: Load CSV data
        print("Step 2: Loading CSV data...")
        print("📁 CSV Path:", loader.csv_path)
        
        if not loader.csv_path.exists():
            print(f"❌ ERROR: CSV file not found at {loader.csv_path}")
            print("Please ensure the CSV file is in the correct location:")
            print("  apps/Data set/airlines_flights_data.csv")
            return
        
        count = loader.load_csv_data(batch_size=1000)
        print()
        
        # Step 3: Get statistics
        print("Step 3: Gathering statistics...")
        stats = loader.get_statistics()
        print()
        
        # Display results
        print("=" * 60)
        print("✅ INITIALIZATION COMPLETE")
        print("=" * 60)
        print()
        print(f"📊 Total Flights Loaded: {stats['total_flights']:,}")
        print(f"✈️  Total Airlines: {stats['total_airlines']}")
        print(f"🗺️  Total Routes: {stats['total_routes']}")
        print()
        print(f"💰 Price Range:")
        print(f"   Minimum: ₹{stats['price_range']['min']:,.2f}")
        print(f"   Maximum: ₹{stats['price_range']['max']:,.2f}")
        print(f"   Average: ₹{stats['price_range']['avg']:,.2f}")
        print()
        print(f"🔝 Top 5 Airlines:")
        for i, airline in enumerate(stats['top_airlines'][:5], 1):
            print(f"   {i}. {airline['airline']}: {airline['flight_count']:,} flights")
        print()
        print(f"🌟 Popular Routes:")
        for i, route in enumerate(stats['popular_routes'][:5], 1):
            print(f"   {i}. {route['source']} → {route['destination']}: {route['flight_count']:,} flights")
        print()
        print("=" * 60)
        print("🚀 API is ready to use!")
        print("   - Search: http://localhost:8000/api/flights/search")
        print("   - Statistics: http://localhost:8000/api/flights/statistics")
        print("   - Filters: http://localhost:8000/api/flights/filters")
        print("   - API Docs: http://localhost:8000/docs")
        print("=" * 60)
        
    except Exception as e:
        print()
        print("=" * 60)
        print("❌ INITIALIZATION FAILED")
        print("=" * 60)
        print(f"Error: {e}")
        print()
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
