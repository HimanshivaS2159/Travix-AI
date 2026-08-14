"""
Test Local Guide Agent Integration
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.services.local_guide_agent import LocalGuideAgent


def test_local_guide_agent():
    """Test Local Guide Agent"""
    print("\n" + "="*60)
    print("Testing Local Guide Agent")
    print("="*60)
    
    agent = LocalGuideAgent()
    
    # Test 1: Get attractions for Delhi
    print("\n1. Testing: Get attractions for Delhi")
    print("-" * 60)
    result = agent.execute("Show me attractions in Delhi")
    print(f"Action: {result.action}")
    print(f"Message: {result.message}")
    print(f"City: {result.data.get('city')}")
    print(f"Attractions found: {result.data.get('count')}")
    if result.data.get('attractions'):
        for attr in result.data['attractions'][:2]:  # Show first 2
            print(f"  - {attr['name']} ({attr['rating']}⭐) - {attr['entry_fee']}")
    
    # Test 2: Get restaurants for Mumbai
    print("\n2. Testing: Get restaurants for Mumbai")
    print("-" * 60)
    result = agent.execute("Where can I eat in Mumbai?")
    print(f"Action: {result.action}")
    print(f"Message: {result.message}")
    print(f"City: {result.data.get('city')}")
    print(f"Restaurants found: {result.data.get('count')}")
    if result.data.get('restaurants'):
        for rest in result.data['restaurants'][:2]:  # Show first 2
            print(f"  - {rest['name']} ({rest['cuisine']}) - {rest['price_range']}")
    
    # Test 3: Get travel tips for Dubai
    print("\n3. Testing: Get travel tips for Dubai")
    print("-" * 60)
    result = agent.execute("Give me travel tips for Dubai")
    print(f"Action: {result.action}")
    print(f"Message: {result.message}")
    print(f"City: {result.data.get('city')}")
    print(f"Tips found: {result.data.get('count')}")
    if result.data.get('tips'):
        for tip in result.data['tips'][:3]:  # Show first 3
            print(f"  [{tip['importance'].upper()}] {tip['category']}: {tip['tip']}")
    
    # Test 4: Get hidden gems for Bangalore
    print("\n4. Testing: Get hidden gems for Bangalore")
    print("-" * 60)
    result = agent.execute("Show me hidden gems in Bangalore")
    print(f"Action: {result.action}")
    print(f"Message: {result.message}")
    print(f"City: {result.data.get('city')}")
    print(f"Hidden gems found: {result.data.get('count')}")
    if result.data.get('gems'):
        for gem in result.data['gems'][:3]:  # Show first 3
            print(f"  💎 {gem}")
    
    # Test 5: Complete local guide for Delhi
    print("\n5. Testing: Complete local guide for Delhi")
    print("-" * 60)
    result = agent.execute("Complete local guide for Delhi")
    print(f"Action: {result.action}")
    print(f"Message: {result.message}")
    print(f"City: {result.data.get('city')}")
    if result.data.get('summary'):
        summary = result.data['summary']
        print(f"Summary:")
        print(f"  - Attractions: {summary['attractions_count']}")
        print(f"  - Restaurants: {summary['restaurants_count']}")
        print(f"  - Travel Tips: {summary['tips_count']}")
        print(f"  - Hidden Gems: {summary['hidden_gems_count']}")
    
    # Test 6: Unknown city
    print("\n6. Testing: Unknown city")
    print("-" * 60)
    result = agent.execute("Show me attractions in Paris")
    print(f"Action: {result.action}")
    print(f"Message: {result.message}")
    
    # Test 7: No city specified
    print("\n7. Testing: No city specified")
    print("-" * 60)
    result = agent.execute("Show me some attractions")
    print(f"Action: {result.action}")
    print(f"Message: {result.message}")
    if result.data.get('available_cities'):
        print(f"Available cities: {', '.join(result.data['available_cities'])}")
    
    print("\n" + "="*60)
    print("✓ All tests completed successfully!")
    print("="*60 + "\n")


if __name__ == "__main__":
    test_local_guide_agent()
