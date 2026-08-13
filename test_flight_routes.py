#!/usr/bin/env python3
"""
Test script to verify all flight routes are working
"""

import sys
import os

# Add the backend app to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'apps', 'backend'))

from app.services.sbt_agent import SBTAgent

def test_route(agent, message):
    """Test a single route"""
    print(f"\n{'='*60}")
    print(f"Testing: {message}")
    print('='*60)
    
    result = agent.execute(message)
    
    if result.action == 'search_flights' and result.data:
        flights = result.data.get('flights', [])
        print(f"✓ Success! Found {len(flights)} flights")
        if flights:
            for i, flight in enumerate(flights[:3], 1):  # Show first 3
                print(f"  {i}. {flight['airline']} {flight['flight_number']}: ₹{flight['price']:,}")
    else:
        print(f"Action: {result.action}")
        print(f"Message: {result.message}")

def main():
    """Test all routes"""
    agent = SBTAgent()
    
    print("\n" + "="*60)
    print("FLIGHT ROUTES TEST")
    print("="*60)
    
    test_routes = [
        # Delhi routes
        "Search flights from Delhi to Mumbai",
        "Show flights from Delhi to Dubai",
        "Find flights Delhi to Bangalore",
        
        # Mumbai routes
        "Search flights Mumbai to Delhi",
        "Show flights from Mumbai to Dubai",
        
        # Dubai routes
        "Flights from Dubai to Delhi",
        "Search Dubai to Mumbai flights",
        
        # Bangalore routes
        "Show flights Bangalore to Delhi",
    ]
    
    for route in test_routes:
        test_route(agent, route)
    
    print("\n" + "="*60)
    print("TEST COMPLETE")
    print("="*60)

if __name__ == "__main__":
    main()
