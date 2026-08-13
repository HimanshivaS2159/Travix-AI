"""
Integration tests for new agents and tools
Tests the complete flow: schedule creation, display, rebooking, and revision
"""

import pytest
from app.services.itinerary_agent import ItineraryAgent
from app.services.rebooking_agent import RebookingAgent
from app.services.revising_agent import RevisingAgent
from app.services.groq_orchestrator import GroqOrchestrator, OrchestratorRequest


class TestItineraryAgent:
    """Test Itinerary Agent"""

    @pytest.fixture
    def agent(self):
        return ItineraryAgent()

    def test_create_schedule_form(self, agent):
        """Test schedule form creation"""
        result = agent.create_schedule_form([])
        assert result.action == "schedule_making_tool"
        assert "form_type" in result.data
        assert result.data["form_type"] == "schedule_creator"
        assert len(result.data["fields"]) > 0
        assert result.success is True

    def test_save_schedule(self, agent):
        """Test schedule saving"""
        schedule_data = {
            "trip_name": "Test Trip",
            "start_date": "2026-08-14",
            "end_date": "2026-08-16",
            "city": "Delhi",
            "daily_schedules": [
                {
                    "day": 1,
                    "title": "Day 1 - Exploration",
                    "items": [
                        {
                            "time": "08:00",
                            "activity": "Breakfast",
                            "location": "Hotel",
                            "duration": "1 hour",
                            "notes": "At hotel restaurant",
                        }
                    ],
                }
            ],
        }

        result = agent.save_schedule(schedule_data)
        assert result.success is True
        assert result.action == "schedule_saved"
        assert "schedule_id" in result.data
        assert result.data["trip_name"] == "Test Trip"
        assert result.data["city"] == "Delhi"

    def test_show_schedules_empty(self, agent):
        """Test showing empty schedules"""
        result = agent.show_schedules([])
        assert result.action == "show_schedule"
        assert len(result.data["schedules"]) == 0
        assert result.success is True

    def test_show_schedules_with_data(self, agent):
        """Test showing saved schedules"""
        # First save a schedule
        schedule_data = {
            "trip_name": "Test Trip",
            "start_date": "2026-08-14",
            "end_date": "2026-08-16",
            "city": "Mumbai",
            "daily_schedules": [],
        }
        agent.save_schedule(schedule_data)

        # Then show schedules
        result = agent.show_schedules([])
        assert result.action == "show_schedule"
        assert len(result.data["schedules"]) > 0
        assert result.success is True

    def test_execute_create_schedule_intent(self, agent):
        """Test execute method with create schedule intent"""
        result = agent.execute("create a day wise schedule")
        assert result.action == "schedule_making_tool"
        assert result.success is True

    def test_execute_show_schedule_intent(self, agent):
        """Test execute method with show schedule intent"""
        result = agent.execute("show me the schedule")
        assert result.action == "show_schedule"
        assert result.success is True


class TestRebookingAgent:
    """Test Rebooking Agent"""

    @pytest.fixture
    def agent(self):
        return RebookingAgent()

    def test_flight_delay_handling(self, agent):
        """Test flight delay handling"""
        result = agent.execute("my flight is delayed by 3 hours")
        assert result.action == "rebooking_tool"
        assert result.data["delay_hours"] == 3
        assert "compensation" in result.data
        assert result.success is True

    def test_flight_cancellation_handling(self, agent):
        """Test flight cancellation handling"""
        result = agent.execute("my flight is cancelled")
        assert result.action == "rebooking_tool"
        assert result.data["refund_amount"] is not None
        assert "rebooking_options" in result.data
        assert result.success is True

    def test_hotel_cancellation_handling(self, agent):
        """Test hotel cancellation handling"""
        result = agent.execute("cancel my hotel booking")
        assert result.action == "rebooking_tool"
        assert "refund_amount" in result.data
        assert "alternative_hotels" in result.data
        assert result.success is True

    def test_rebooking_options(self, agent):
        """Test rebooking options generation"""
        result = agent.handle_rebooking("rebook my flight", [])
        assert result.action == "rebooking_tool"
        assert "rebooking_options" in result.data
        assert len(result.data["rebooking_options"]) > 0
        assert result.success is True

    def test_rebooking_storage(self, agent):
        """Test rebooking storage"""
        initial_count = len(agent.rebookings)

        agent.execute("my flight is delayed")

        assert len(agent.rebookings) > initial_count


class TestRevisingAgent:
    """Test Revising Agent"""

    @pytest.fixture
    def agent(self):
        return RevisingAgent()

    def test_review_itinerary(self, agent):
        """Test itinerary review"""
        result = agent.review_itinerary([])
        assert result.action == "review_itinerary"
        assert "suggestions" in result.data
        assert len(result.data["suggestions"]) > 0
        assert result.success is True

    def test_review_booking(self, agent):
        """Test booking review"""
        result = agent.review_booking([])
        assert result.action == "review_booking"
        assert "bookings" in result.data
        assert result.success is True

    def test_optimize_schedule(self, agent):
        """Test schedule optimization"""
        result = agent.optimize_schedule([])
        assert result.action == "optimize_schedule"
        assert "optimized_schedule" in result.data
        assert result.success is True

    def test_check_budget(self, agent):
        """Test budget checking"""
        result = agent.check_budget([])
        assert result.action == "check_budget"
        assert "breakdown" in result.data
        assert "total_budget" in result.data
        assert result.success is True

    def test_execute_review_intent(self, agent):
        """Test execute method with review intent"""
        result = agent.execute("review my itinerary")
        assert result.action == "review_itinerary"
        assert result.success is True

    def test_execute_optimize_intent(self, agent):
        """Test execute method with optimize intent"""
        result = agent.execute("optimize my schedule")
        assert result.action == "optimize_schedule"
        assert result.success is True

    def test_execute_budget_intent(self, agent):
        """Test execute method with budget intent"""
        result = agent.execute("check my budget")
        assert result.action == "check_budget"
        assert result.success is True


class TestAgentIntegration:
    """Test integration between agents"""

    def test_complete_trip_planning_flow(self):
        """Test complete trip planning flow"""
        # Step 1: Create schedule with Itinerary Agent
        itinerary_agent = ItineraryAgent()
        schedule_data = {
            "trip_name": "Mumbai Adventure",
            "start_date": "2026-08-20",
            "end_date": "2026-08-22",
            "city": "Mumbai",
            "daily_schedules": [
                {
                    "day": 1,
                    "title": "Day 1 - Arrival",
                    "items": [
                        {
                            "time": "10:00",
                            "activity": "Arrival at airport",
                            "location": "Mumbai Airport",
                            "duration": "2 hours",
                            "notes": "",
                        }
                    ],
                }
            ],
        }
        save_result = itinerary_agent.save_schedule(schedule_data)
        assert save_result.success is True
        schedule_id = save_result.data["schedule_id"]

        # Step 2: Display saved schedules
        show_result = itinerary_agent.show_schedules([])
        assert len(show_result.data["schedules"]) > 0
        assert show_result.data["schedules"][0]["id"] == schedule_id

        # Step 3: Handle a delay with Rebooking Agent
        rebooking_agent = RebookingAgent()
        delay_result = rebooking_agent.execute("flight is delayed 2 hours")
        assert delay_result.success is True
        assert delay_result.data["delay_hours"] == 2

        # Step 4: Review the itinerary with Revising Agent
        revising_agent = RevisingAgent()
        review_result = revising_agent.execute("review my itinerary")
        assert review_result.success is True
        assert "suggestions" in review_result.data

    def test_agent_tool_availability(self):
        """Test that agents have correct tools"""
        itinerary = ItineraryAgent()
        rebooking = RebookingAgent()
        revising = RevisingAgent()

        # Verify agents can execute their respective operations
        assert itinerary.create_schedule_form([]).action == "schedule_making_tool"
        assert itinerary.show_schedules([]).action == "show_schedule"

        assert rebooking.handle_flight_delay("delay", []).action == "rebooking_tool"
        assert rebooking.handle_hotel_cancellation("cancel", []).action == "rebooking_tool"

        assert revising.review_itinerary([]).action == "review_itinerary"
        assert revising.check_budget([]).action == "check_budget"


# Run tests
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
