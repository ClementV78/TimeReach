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

app = FastAPI(
    title="TimeReach API",
    description="Find places within travel time using isochrones",
    version="1.0.0",
    openapi_version="3.1.0",
    openapi_tags=[{
        "name": "Places",
        "description": "Operations for finding places within travel time"
    }],
    terms_of_service="https://timereach.onrender.com/terms",
    contact={
        "name": "TimeReach API Support",
        "url": "https://timereach.onrender.com/support",
    },
    swagger_ui_parameters={"defaultModelsExpandDepth": -1}
)

def custom_openapi():
    """Customize OpenAPI documentation for ChatGPT"""
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="TimeReach API",
        version="1.0.0",
        openapi_version="3.1.0",
        servers=[{"url": "https://timereach.onrender.com"}],
        description="""
        TimeReach API - Find Places Within Travel Time

        This API helps find places that are reachable within a specific travel time from a starting point. 
        You can search using either a location name or GPS coordinates.

        Base Endpoint: https://timereach.onrender.com

        Main Parameters:
           - location: Name of the place (e.g., "Eiffel Tower, Paris")
           OR
           - lat: Latitude (-90 to 90)
           - lon: Longitude (-180 to 180)
           
           AND
           - minutes: Travel time (1-60 minutes)
           - type: Type of place to search for (e.g., "restaurant", "museum", "park", etc.)
           - keyword: Optional search term

        3. Common Use Cases:
           "Find restaurants within 20 minutes of the Eiffel Tower"
           → /places?location=Eiffel Tower, Paris&minutes=20&type=restaurant

           "Find cafes within 15 minutes of Central Park"
           → /places?location=Central Park, New York&minutes=15&type=cafe

           "Find bakeries near Notre Dame Paris"
           → /places?location=Notre Dame, Paris&minutes=10&type=bakery

           "Find traditional inns around Dax"
           → /places?location=Dax, France&minutes=20&type=auberge&keyword=restaurant

        4. Response Format:
           - average_radius: Reachable distance in meters
           - places: Array of found locations with:
             * name: Place name
             * address: Full address
             * rating: Rating out of 5
             * location: {lat, lng}
             * types: Place categories
             * price_level: Price category
             * description: Place description

        5. Error Handling:
           - 503: External service unavailable
           - 422: Invalid parameters

        For testing: Try the interactive docs at /docs
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
    allow_origins=[
        "https://timereach.onrender.com",
        "https://chat.openai.com",
        "*"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=[
        "Content-Type",
        "Authorization",
        "X-Goog-Api-Key",
        "X-Goog-FieldMask",
        "*"
    ],
    expose_headers=["*"]
)

# Removed PlaceType enum to allow more flexible place types

class Location(BaseModel):
    """Geographic coordinates model"""
    lat: float = Field(..., ge=-90, le=90, description="Latitude")
    lng: float = Field(..., ge=-180, le=180, description="Longitude")

class Place(BaseModel):
    """Place model"""
    name: str = Field(..., description="Place name")
    address: str = Field("", description="Formatted address")
    rating: float = Field(0.0, description="Average rating out of 5")
    location: Location = Field(..., description="Geographic coordinates")
    place_id: str = Field(..., description="Unique Google Places identifier")
    types: List[str] = Field(default_factory=list, description="Place types")
    price_level: str = Field("", description="Price level")
    description: str = Field("", description="Editorial description")

class SearchResponse(BaseModel):
    """API response model"""
    average_radius: int = Field(..., description="Average reachable radius in meters")
    places: List[Place] = Field(..., description="List of found places")

# CORS middleware configuration already applied above

@app.get("/places", 
         operation_id="find_places",
         tags=["Places"],
         summary="Find places within a reachable area",
         description="Search for places (restaurants, cafes, etc.) that are reachable within a specified travel time from a starting point",
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
                                     "name": "Le Bistrot Parisien",
                                     "address": "12 Avenue des Champs-Élysées, 75008 Paris, France",
                                     "rating": 4.5,
                                     "location": {"lat": 48.8584, "lng": 2.2945},
                                     "place_id": "ChIJxxx...",
                                     "types": ["restaurant", "french_restaurant"],
                                     "price_level": "PRICE_LEVEL_MODERATE",
                                     "description": "Traditional French bistro with Eiffel Tower views"
                                 },
                                 {
                                     "name": "Café de Paris",
                                     "address": "10 Rue de la Paix, 75002 Paris, France",
                                     "rating": 4.2,
                                     "location": {"lat": 48.8566, "lng": 2.3522},
                                     "place_id": "ChIJyyy...",
                                     "types": ["cafe", "restaurant"],
                                     "price_level": "PRICE_LEVEL_EXPENSIVE",
                                     "description": "Historic Parisian café serving French cuisine"
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
async def find_places(
    location: str = Query(
        None,
        description="Name of the location (e.g., 'Eiffel Tower, Paris')",
        example="Eiffel Tower, Paris",
        title="Location Name",
    ),
    lon: float = Query(
        None,
        ge=-180,
        le=180,
        description="Starting point longitude (optional if location is provided)",
        example=2.2945,
        title="Longitude",
    ),
    lat: float = Query(
        None,
        ge=-90,
        le=90,
        description="Starting point latitude (optional if location is provided)",
        example=48.8584,
        title="Latitude",
    ),
    minutes: int = Query(
        20,
        ge=1,
        le=60,
        description="Travel time in minutes",
        example=20,
        title="Travel Time",
    ),
    type: str = Query(
        "restaurant",
        description="Type of place to search for (e.g., restaurant, museum, park, etc.)",
        example="restaurant",
        title="Place Type",
        min_length=2,
        max_length=50
    ),
    keyword: str = Query(
        "",
        description="Optional keyword to filter results (e.g., 'bistro', 'pizza', etc.)",
        example="bistro",
        title="Search Keyword",
        min_length=2,
        max_length=50,
        regex="^[a-zA-Z0-9 ]*$"
    )
):
    """
    Find places within a specified travel time using isochrones.
    
    - Uses OpenRouteService to calculate the reachable area
    - Calculates average radius from the isochrone polygon
    - Searches for places using Google Places API
    """
    # Verify that either location or coordinates are provided
    if location is None and (lat is None or lon is None):
        raise HTTPException(
            status_code=422,
            detail="Either location name or both latitude and longitude must be provided"
        )

    # If location is provided but no coordinates, use Google Geocoding API
    if location and (lat is None or lon is None):
        try:
            geocode_url = "https://places.googleapis.com/v1/places:searchText"
            headers = {
                "Content-Type": "application/json",
                "X-Goog-Api-Key": settings.GOOGLE_API_KEY,
                "X-Goog-FieldMask": "places.location"
            }
            geocode_data = {"textQuery": location}
            geocode_resp = requests.post(geocode_url, headers=headers, json=geocode_data)
            geocode_resp.raise_for_status()
            
            place_data = geocode_resp.json().get("places", [])
            if not place_data:
                raise HTTPException(status_code=422, detail="Location not found")
            
            lat = place_data[0]["location"]["latitude"]
            lon = place_data[0]["location"]["longitude"]
        except requests.RequestException as e:
            raise HTTPException(status_code=503, detail="Error accessing Google Geocoding API")

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
            "textQuery": type,  # Use textQuery instead of includedTypes for more flexibility
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
