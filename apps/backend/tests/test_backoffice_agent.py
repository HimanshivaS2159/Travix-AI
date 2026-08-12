"""
Tests for BackOffice Agent
Tests hotel search, booking, and booking history functionality
"""

import pytest
from app.services.backoffice_agent import BackOfficeAgent, Hotel, Booking, ToolResult


class TestBackOfficeAgent:
    """Test suite for BackOffice Agent"""

    @pytest.fixture
    def agent(self):
        """Create BackOffice agent instance"""
        return BackOfficeAgent()

    def test_list_hotels_delhi(self, agent):
        """Test listing hotels in Delhi"""
        result = agent.list_hotels("Delhi")
        
        assert result.action == "list_hotels"
        assert "hotels" in result.message.lower() or "found" in result.message.lower()
        assert isinstance(result.data, list)
        assert len(result.data) > 0
        assert len(result.trace) > 0
        
        # Verify hotel structure
        hotel = result.data[0]
        assert "id" in hotel
        assert "name" in hotel
        assert "city" in hotel
        assert "rating" in hotel
        assert "price_per_night" in hotel

    def test_list_hotels_mumbai(self, agent):
        """Test listing hotels in Mumbai"""
        result = agent.list_hotels("Mumbai")
        
        assert result.action == "list_hotels"
        assert isinstance(result.data, list)
        assert len(result.data) > 0

    def test_list_hotels_bangalore(self, agent):
        """Test listing hotels in Bangalore"""
        result = agent.list_hotels("Bangalore")
        
        assert result.action == "list_hotels"
        assert isinstance(result.data, list)
        assert len(result.data) > 0

    def test_list_hotels_bengaluru_alias(self, agent):
        """Test listing hotels in Bengaluru (alias for Bangalore)"""
        result = agent.list_hotels("Bengaluru")
        
        assert result.action == "list_hotels"
        assert isinstance(result.data, list)
        assert len(result.data) > 0

    def test_list_hotels_goa(self, agent):
        """Test listing hotels in Goa"""
        result = agent.list_hotels("Goa")
        
        assert result.action == "list_hotels"
        assert isinstance(result.data, list)
        assert len(result.data) > 0

    def test_list_hotels_unsupported_city(self, agent):
        """Test listing hotels in unsupported city"""
        result = agent.list_hotels("Paris")
        
        assert result.action == "list_hotels"
        assert isinstance(result.data, list)
        assert len(result.data) == 0
        assert "don't have" in result.message.lower() or "not" in result.message.lower()

    def test_book_hotel_within_budget(self, agent):
        """Test booking hotel within budget"""
        result = agent.book_hotel("Delhi", budget=5000)
        
        assert result.action == "book_hotel"
        assert result.data is not None
        
        # Verify booking structure
        booking = result.data
        assert "booking_id" in booking
        assert "hotel_name" in booking
        assert "city" in booking
        assert "total_price" in booking
        assert booking["price_per_night"] <= 5000

    def test_book_hotel_no_budget(self, agent):
        """Test booking hotel without providing budget"""
        result = agent.book_hotel("Delhi", budget=None)
        
        assert result.action == "book_hotel"
        assert result.data is None
        assert "budget" in result.message.lower()

    def test_book_hotel_budget_too_low(self, agent):
        """Test booking hotel with budget too low"""
        result = agent.book_hotel("Delhi", budget=500)
        
        assert result.action == "book_hotel"
        assert result.data is None
        assert "no hotels" in result.message.lower() or "increase" in result.message.lower()

    def test_book_hotel_unsupported_city(self, agent):
        """Test booking hotel in unsupported city"""
        result = agent.book_hotel("Tokyo", budget=5000)
        
        assert result.action == "book_hotel"
        assert result.data is None
        assert "don't have" in result.message.lower() or "supported" in result.message.lower()

    def test_list_bookings(self, agent):
        """Test listing bookings"""
        result = agent.list_bookings()
        
        assert result.action == "list_bookings"
        assert isinstance(result.data, list)
        assert len(result.data) > 0  # Pre-populated bookings exist
        
        # Verify booking structure
        booking = result.data[0]
        assert "booking_id" in booking
        assert "hotel_name" in booking
        assert "check_in" in booking
        assert "check_out" in booking

    def test_booking_appears_in_history(self, agent):
        """Test that new booking appears in booking history"""
        # Get initial booking count
        initial_result = agent.list_bookings()
        initial_count = len(initial_result.data)
        
        # Book a hotel
        book_result = agent.book_hotel("Mumbai", budget=5000)
        assert book_result.data is not None
        booking_id = book_result.data["booking_id"]
        
        # Check bookings again
        updated_result = agent.list_bookings()
        updated_count = len(updated_result.data)
        
        assert updated_count == initial_count + 1
        
        # Verify new booking is at the top (newest first)
        newest_booking = updated_result.data[0]
        assert newest_booking["booking_id"] == booking_id

    def test_trace_generation(self, agent):
        """Test that trace events are generated correctly"""
        result = agent.list_hotels("Delhi")
        
        assert len(result.trace) > 0
        
        # Verify trace structure
        for event in result.trace:
            assert "id" in event
            assert "type" in event
            assert "name" in event
            assert "agent" in event
            assert "status" in event
            assert "output_summary" in event

    def test_hotel_selection_prefers_highest_rating(self, agent):
        """Test that booking prefers highest-rated hotel within budget"""
        result = agent.book_hotel("Delhi", budget=10000)
        
        assert result.data is not None
        
        # Get all hotels in budget
        hotels_result = agent.list_hotels("Delhi")
        affordable_hotels = [
            h for h in hotels_result.data 
            if h["price_per_night"] <= 10000
        ]
        
        # Find highest rated
        max_rating = max(h["rating"] for h in affordable_hotels)
        
        # Booking should have high rating
        assert result.data["rating"] >= max_rating - 0.1  # Allow small tolerance


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
