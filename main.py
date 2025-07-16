# main.py
from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.openapi.utils import get_openapi
from shapely.geometry import shape, Point
import requests
from geopy.distance import geodesic
from typing import Optional, List, Dict, Union
from config import settings
from enum import Enum
from pydantic import BaseModel, Field

app = FastAPI()

def custom_openapi():
    """Customize OpenAPI documentation for ChatGPT"""
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="TimeReach API",
        version="1.0.0",
        description="""
        API for finding places within a specified travel time using isochrones.
        
        ChatGPT Integration:
        1. Input format: lat=48.8566,lon=2.3522
        2. Travel time in minutes: 1-60
        3. Supported types: restaurant, cafe, bar, fast_food_restaurant, bakery, any
        4. Optional keyword filtering
        
        ChatGPT Example:
        "Find restaurants within 20 minutes of the Eiffel Tower"
        → /restaurants?lat=48.8584&lon=2.2945&minutes=20
        """,
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

@app.get("/")
async def root():
    """Root endpoint providing API information"""
    return {
        "name": "TimeReach API",
        "description": "Find places within travel time using isochrones",
        "version": "1.0.0",
        "documentation": "/docs",
        "openapi": "/openapi.json"
    }

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PlaceType(str, Enum):
    """Place types supported by the API"""
    RESTAURANT = "restaurant"
    CAFE = "cafe"
    BAR = "bar"
    FAST_FOOD = "fast_food_restaurant"
    BAKERY = "bakery"
    ANY = "any"

class Location(BaseModel):
    """Geographic coordinates model"""
    lat: float = Field(..., ge=-90, le=90, description="Latitude")
    lng: float = Field(..., ge=-180, le=180, description="Longitude")

class Place(BaseModel):
    """Place model"""
    name: str = Field(..., description="Place name")
    address: str = Field(None, description="Formatted address")
    rating: Optional[float] = Field(None, description="Average rating out of 5")
    location: Location = Field(..., description="Geographic coordinates")
    place_id: str = Field(..., description="Unique Google Places identifier")
    types: List[str] = Field(default_list=[], description="Place types")
    price_level: Optional[str] = Field(None, description="Price level")
    description: Optional[str] = Field(None, description="Editorial description")

class SearchResponse(BaseModel):
    """API response model"""
    average_radius: int = Field(..., description="Average reachable radius in meters")
    places: List[Place] = Field(..., description="List of found places")

def custom_openapi():
    """Customize OpenAPI documentation for ChatGPT"""
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="TimeReach API",
        version="1.0.0",
        description="""
        API for finding places within a specified travel time using isochrones.
        
        ChatGPT Integration:
        1. Input format: lat=48.8566,lon=2.3522
        2. Travel time in minutes: 1-60
        3. Supported types: restaurant, cafe, bar, fast_food_restaurant, bakery, any
        4. Optional keyword filtering
        
        ChatGPT Example:
        "Find restaurants within 20 minutes of the Eiffel Tower"
        → /restaurants?lat=48.8584&lon=2.2945&minutes=20
        
        Responses include:
        - Average reachable radius
        - List of places with details (name, address, rating, etc.)
        """,
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema

# CORS middleware configuration already applied above

@app.get("/restaurants", 
         summary="Find places within a reachable area",
         response_description="List of places and average radius",
         response_model=SearchResponse,
         responses={
             200: {
                 "description": "Search successful",
                 "content": {
                     "application/json": {
                         "example": {
                             "average_radius": 5000,
                             "places": [
                                 {
                                     "name": "Sample Restaurant",
                                     "address": "1 Example St, City",
                                     "rating": 4.5,
                                     "location": {"lat": 48.8566, "lng": 2.3522},
                                     "place_id": "ChIJ...",
                                     "types": ["restaurant", "food"],
                                     "price_level": "PRICE_LEVEL_MODERATE",
                                     "description": "Traditional restaurant..."
                                 }
                             ]
                         }
                     }
                 }
             },
             503: {
                 "description": "Error accessing external services",
                 "content": {
                     "application/json": {
                         "example": {"detail": "Error accessing external API"}
                     }
                 }
             }
         })
async def find_restaurants(
    lon: float = Query(..., ge=-180, le=180, description="Starting point longitude"),
    lat: float = Query(..., ge=-90, le=90, description="Starting point latitude"),
    minutes: int = Query(20, ge=1, le=60, description="Travel time in minutes"),
    type: PlaceType = Query(PlaceType.RESTAURANT, description="Type of place to search for"),
    keyword: Optional[str] = Query(None, description="Keyword to filter results")
):
    """
    Find places within a specified travel time using isochrones.
    
    - Uses OpenRouteService to calculate the reachable area
    - Calculates average radius from the isochrone polygon
    - Searches for places using Google Places API
    """
    try:
        # 1. ORS Isochrone
        ors_url = "https://api.openrouteservice.org/v2/isochrones/driving-car"
        headers = {"Authorization": f"Bearer {settings.ORS_API_KEY}"}
        params = {"locations": f"{lon},{lat}", "range": minutes * 60}
        response = requests.post(ors_url, headers=headers, json={"locations": [[lon, lat]], "range": [minutes * 60]})
        response.raise_for_status()
        poly = shape(response.json()['features'][0]['geometry'])
    except requests.RequestException as e:
        raise HTTPException(status_code=503, detail="Error accessing OpenRouteService API")
    # 2. Rayon moyen
    center = Point(lon, lat)
    distances = [geodesic((center.y, center.x), (p[1], p[0])).meters for p in poly.exterior.coords]
    average_radius = int(sum(distances) / len(distances))
    
    try:
        # 3. Google Places Nearby (New API)
        gplaces_url = "https://places.googleapis.com/v1/places:searchNearby"
        headers = {
            "Content-Type": "application/json",
            "X-Goog-Api-Key": settings.GOOGLE_API_KEY,
            "X-Goog-FieldMask": "places.displayName,places.formattedAddress,places.rating,places.location,places.id,places.types,places.priceLevel,places.editorialSummary"
        }
        
        places_data = {
            "includedTypes": [type] if type != "any" else [],
            "maxResultCount": 20,
            "locationRestriction": {
                "circle": {
                    "center": {
                        "latitude": lat,
                        "longitude": lon
                    },
                    "radius": min(float(average_radius), 50000.0)
                }
            },
            "rankPreference": "DISTANCE"
        }
        
        if keyword:
            # Note: keyword filtering will be handled in python as the new API doesn't support keywords directly
            places_data["maxResultCount"] = 20  # Request max to filter after
            
        places_resp = requests.post(gplaces_url, headers=headers, json=places_data)
        places_resp.raise_for_status()
        response_data = places_resp.json()
        
        # Filter results if keyword was provided
        places = response_data.get("places", [])
        if keyword:
            keyword = keyword.lower()
            places = [
                p for p in places 
                if keyword in p.get("displayName", {}).get("text", "").lower()
            ]
            
        return {
            "average_radius": average_radius,
            "places": [
                {
                    "name": p.get("displayName", {}).get("text"),
                    "address": p.get("formattedAddress"),
                    "rating": p.get("rating", {}).get("rating") if isinstance(p.get("rating"), dict) else p.get("rating"),
                    "location": {
                        "lat": p.get("location", {}).get("latitude"),
                        "lng": p.get("location", {}).get("longitude")
                    },
                    "place_id": p.get("id"),
                    "types": p.get("types", []),
                    "price_level": p.get("priceLevel"),
                    "description": p.get("editorialSummary", {}).get("text")
                }
                for p in places[:min(len(places), 20)]  # Limit to 20 results
            ]
        }
    except requests.RequestException as e:
        raise HTTPException(
            status_code=503,
            detail="Error accessing Google Places API"
        )
