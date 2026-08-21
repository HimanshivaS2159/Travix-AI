"""
Flight Search API Endpoints
Provides REST API for searching and filtering flight data
"""
from fastapi import APIRouter, Query, HTTPException
from typing import Optional, List
from pydantic import BaseModel, Field
import os

from app.services.flight_data_loader import FlightDataLoader

router = APIRouter(prefix="/api/flights", tags=["flights"])

# Initialize data loader
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://travix:travix_password@localhost:5432/travix_db")
flight_loader = FlightDataLoader(DATABASE_URL)


# Response Models
class FlightResponse(BaseModel):
    id: int
    index_num: Optional[int] = None
    airline: str
    flight: str
    source_city: str
    departure_time: str
    stops: str
    arrival_time: str
    destination_city: str
    class_: str = Field(alias="class")
    duration: float
    days_left: int
    price: float
    
    class Config:
        populate_by_name = True


class FlightSearchResponse(BaseModel):
    total: int
    flights: List[dict]
    page: int
    page_size: int


class StatisticsResponse(BaseModel):
    total_flights: int
    total_airlines: int
    total_routes: int
    price_range: dict
    top_airlines: List[dict]
    popular_routes: List[dict]


class FilterOptionsResponse(BaseModel):
    cities: List[str]
    airlines: List[str]
    stops: List[str]
    departure_times: List[str]
    classes: List[str]


# API Endpoints
@router.get("/search", response_model=dict)
async def search_flights(
    source_city: Optional[str] = Query(None, description="Source city (e.g., Delhi, Mumbai)"),
    destination_city: Optional[str] = Query(None, description="Destination city"),
    airline: Optional[str] = Query(None, description="Airline name (partial match)"),
    max_price: Optional[float] = Query(None, description="Maximum price"),
    stops: Optional[str] = Query(None, description="Number of stops (zero, one, two_or_more)"),
    departure_time: Optional[str] = Query(None, description="Departure time (Morning, Afternoon, Evening, Night, Early_Morning)"),
    flight_class: Optional[str] = Query(None, description="Flight class (Economy, Business)"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(50, ge=1, le=500, description="Results per page")
):
    """
    Search flights with multiple filters
    
    Returns paginated flight results sorted by price (lowest first)
    """
    try:
        offset = (page - 1) * page_size
        
        flights = flight_loader.search_flights(
            source_city=source_city,
            destination_city=destination_city,
            airline=airline,
            max_price=max_price,
            stops=stops,
            departure_time=departure_time,
            flight_class=flight_class,
            limit=page_size,
            offset=offset
        )
        
        # Get total count for pagination
        # Note: This is approximate for performance
        total = len(flights)
        
        return {
            "success": True,
            "total": total,
            "page": page,
            "page_size": page_size,
            "flights": flights
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")


@router.get("/statistics", response_model=StatisticsResponse)
async def get_statistics():
    """
    Get flight database statistics
    
    Returns:
    - Total flights, airlines, routes
    - Price range (min, max, avg)
    - Top 10 airlines by flight count
    - Top 10 popular routes
    """
    try:
        stats = flight_loader.get_statistics()
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get statistics: {str(e)}")


@router.get("/filters", response_model=FilterOptionsResponse)
async def get_filter_options():
    """
    Get all unique values for filter dropdowns
    
    Returns lists of:
    - Cities (source and destination)
    - Airlines
    - Stop options
    - Departure times
    - Flight classes
    """
    try:
        filters = flight_loader.get_unique_values()
        return filters
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get filters: {str(e)}")


@router.post("/initialize")
async def initialize_database():
    """
    Initialize database and load CSV data
    
    This endpoint:
    1. Creates the flights table
    2. Loads all CSV data into PostgreSQL
    3. Creates indexes for fast searching
    
    Only needs to be called once or when resetting the database
    """
    try:
        # Create table
        flight_loader.create_table()
        
        # Load data
        count = flight_loader.load_csv_data()
        
        # Get statistics
        stats = flight_loader.get_statistics()
        
        return {
            "success": True,
            "message": "Database initialized successfully",
            "records_loaded": count,
            "statistics": stats
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Initialization failed: {str(e)}")


@router.get("/health")
async def health_check():
    """Check if flight service is operational"""
    try:
        stats = flight_loader.get_statistics()
        return {
            "status": "healthy",
            "total_flights": stats.get("total_flights", 0)
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }


@router.get("/cheapest")
async def get_cheapest_flights(
    source_city: str = Query(..., description="Source city"),
    destination_city: str = Query(..., description="Destination city"),
    limit: int = Query(10, ge=1, le=50, description="Number of results")
):
    """
    Get cheapest flights for a route
    
    Returns the cheapest flights sorted by price
    """
    try:
        flights = flight_loader.search_flights(
            source_city=source_city,
            destination_city=destination_city,
            limit=limit,
            offset=0
        )
        
        return {
            "success": True,
            "route": f"{source_city} → {destination_city}",
            "total": len(flights),
            "flights": flights
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")


@router.get("/by-airline/{airline}")
async def get_flights_by_airline(
    airline: str,
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=200)
):
    """Get all flights for a specific airline"""
    try:
        offset = (page - 1) * page_size
        
        flights = flight_loader.search_flights(
            airline=airline,
            limit=page_size,
            offset=offset
        )
        
        return {
            "success": True,
            "airline": airline,
            "page": page,
            "page_size": page_size,
            "total": len(flights),
            "flights": flights
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")
