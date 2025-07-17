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
import logging
from datetime import datetime

# Endpoint GET /places_test compatible OpenAPI 3.0.3

# ...existing code...

# Place this endpoint after app = FastAPI(...)

# ...existing code...

# After app = FastAPI(...)

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

@app.get("/places_test", tags=["Places"], summary="Test endpoint for OpenAPI 3.0.3 compatibility", description="Returns a static example response compatible with OpenAPI 3.0.3.")
async def places_test():
    """
    Test endpoint for OpenAPI 3.0.3 compatibility. Returns a static response.
    """
    example_response = {
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
            }
        ]
    }
    return JSONResponse(content=example_response)
# Endpoint GET /places_test compatible OpenAPI 3.0.3


# ...existing code...

# Endpoint GET /places_test compatible OpenAPI 3.0.3
from fastapi.responses import JSONResponse

# Place this endpoint after app = FastAPI(...)


# ...existing code...

# Place this endpoint after app = FastAPI(...)

# ...existing code...

# After app = FastAPI(...)

@app.get("/places_test", tags=["Places"], summary="Test endpoint for OpenAPI 3.0.3 compatibility", description="Returns a static example response compatible with OpenAPI 3.0.3.")
async def places_test():
    """
    Test endpoint for OpenAPI 3.0.3 compatibility. Returns a static response.
    """
    example_response = {
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
            }
        ]
    }
    return JSONResponse(content=example_response)
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
import logging
from datetime import datetime

# Configuration des logs
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

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
        # TimeReach API - Find Places Within Travel Time

        This API finds places reachable within a specific travel time from a starting point (address or coordinates).

        ## Integration with ChatGPT

        - For most queries, use the `keyword` parameter to describe what you are looking for (e.g., 'pizzeria', 'auberge traditionnelle', 'bistro').
        - If you know or can deduce the Google Places type (see [Google Place Types](https://developers.google.com/maps/documentation/places/web-service/place-types)), use the `type` parameter as well (e.g., 'restaurant', 'museum', 'park').
        - Combining `type` and `keyword` increases relevance: `type` restricts results to a category, `keyword` refines the search within that category.
        - If only `keyword` is provided, the API will search for places matching the text in the specified area.

        ## Supported Parameters

        - `location`: Name of the starting place (e.g., "Eiffel Tower, Paris")
        - `lat`, `lon`: Latitude and longitude (if no location name)
        - `minutes`: Travel time (1-60 minutes)
        - `mode`: Transport mode (car, cycling-regular, foot-walking, etc.)
        - `type`: Google Places type (optional, e.g., 'restaurant', 'museum')
        - `keyword`: Free text search (optional, e.g., 'pizzeria', 'bistro')
        - `priceLevels`: Filter by price level (optional, e.g., 'PRICE_LEVEL_MODERATE')

        ## Example Queries

        - "Find pizzerias within 10 minutes by bike from GiFi Plaisir"
          → `/places?location=GiFi Plaisir&minutes=10&mode=cycling-regular&type=restaurant&keyword=pizzeria`

        - "Find bakeries near Notre Dame Paris"
          → `/places?location=Notre Dame, Paris&minutes=10&type=bakery`

        - "Find traditional inns around Dax"
          → `/places?location=Dax, France&minutes=20&keyword=auberge`

        ## Request Format

        - GET `/places`
        - Parameters: as described above

        ## Response Format

        ```json
        {
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
            }
          ]
        }
        ```

        ## Error Handling

        - 503: External service unavailable
        - 422: Invalid parameters

        ## Tips for ChatGPT

        - Always use `keyword` for free text queries or when the type is unknown.
        - Use `type` if you know the Google Places type for more precise results.
        - You can combine both for best relevance.
        - For price filtering, use `priceLevels` (e.g., 'PRICE_LEVEL_MODERATE').

        For testing: Try the interactive docs at `/docs`
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

# Enum for transport modes
class TransportMode(str, Enum):
    """Available transport modes (OpenRouteService profiles)"""
    CAR = "driving-car"
    HGV = "driving-hgv"
    BIKE = "cycling-regular"
    ROADBIKE = "cycling-road"
    MTB = "cycling-mountain"
    EBIKE = "cycling-electric"
    WALKING = "foot-walking"
    HIKING = "foot-hiking"
    WHEELCHAIR = "wheelchair"

class Location(BaseModel):
    """Geographic coordinates model"""
    lat: float = Field(..., ge=-90, le=90, description="Latitude")
    lng: float = Field(..., ge=-180, le=180, description="Longitude")

class Place(BaseModel):
    """Place model"""
    name: str = Field(..., description="Place name")
    address: str = Field("", description="Formatted address")
    rating: Optional[float] = Field(None, description="Average rating out of 5")
    location: Location = Field(..., description="Geographic coordinates")
    place_id: str = Field(..., description="Unique Google Places identifier")
    types: List[str] = Field(default_factory=list, description="Place types")
    price_level: Optional[str] = Field(None, description="Price level")
    description: Optional[str] = Field(None, description="Editorial description")

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
    mode: TransportMode = Query(
        TransportMode.CAR,
        description="Mode of transportation",
        example="car",
        title="Transport Mode",
    ),
    type: str = Query(
        "restaurant",
        description="Type of place to search for (e.g., restaurant, museum, park, etc.)",
        example="restaurant",
        title="Place Type",
        min_length=2,
        max_length=50
    ),
    keyword: Optional[str] = Query(
        None,
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
    logger.info(f"[LOG] /places endpoint called (GET or POST)")
    # Dump requête utilisateur
    logger.debug(f"[API Request] location={location}, lat={lat}, lon={lon}, minutes={minutes}, mode={mode}, type={type}, keyword={keyword}")
    # Verify that either location or coordinates are provided
    if location is None and (lat is None or lon is None):
        raise HTTPException(
            status_code=422,
            detail="Either location name or both latitude and longitude must be provided"
        )

    # ---[ Google Geocoding API ]---
    if location and (lat is None or lon is None):
        geocode_url = "https://maps.googleapis.com/maps/api/geocode/json"
        params = {
            "address": location,
            "key": settings.GOOGLE_API_KEY
        }
        logger.info("\n==================== [CALL] Google Geocoding API ====================")
        logger.info(f"Request: address='{location}'")
        logger.debug(f"[Google Geocoding] Request params: {params}")
        try:
            start_time = datetime.now()
            geocode_resp = requests.get(geocode_url, params=params)
            duration = (datetime.now() - start_time).total_seconds()
            logger.info(f"[Google Geocoding] Response time: {duration:.2f}s")
            geocode_resp.raise_for_status()
            response_data = geocode_resp.json()
            logger.debug(f"[Google Geocoding] Response JSON: {response_data}")
            logger.info(f"[Google Geocoding] Status: {response_data.get('status')}")
            if response_data["status"] != "OK":
                logger.error(f"[Google Geocoding] Error: {response_data['status']}")
                raise HTTPException(
                    status_code=422,
                    detail=f"Geocoding error: {response_data['status']}"
                )
            location_data = response_data["results"][0]["geometry"]["location"]
            lat = location_data["lat"]
            lon = location_data["lng"]
            logger.info(f"[Google Geocoding] Found: lat={lat}, lon={lon}")
            logger.info("====================================================================\n")
        except requests.RequestException as e:
            error_message = f"Error accessing Google Geocoding API: {str(e)}"
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_details = e.response.json()
                    error_message += f" - Details: {error_details}"
                except:
                    error_message += f" - Status: {e.response.status_code}"
            logger.error(f"[Google Geocoding] Exception: {error_message}")
            logger.info("====================================================================\n")
            raise HTTPException(status_code=503, detail=error_message)

    # ---[ OpenRouteService Isochrone API ]---
    try:
        ors_url = f"https://api.openrouteservice.org/v2/isochrones/{mode.value}"
        headers = {"Authorization": f"Bearer {settings.ORS_API_KEY}"}
        params = {"locations": f"{lon},{lat}", "range": minutes * 60}
        logger.info("\n==================== [CALL] OpenRouteService Isochrone API ====================")
        logger.info(f"Request: mode={mode}, lat={lat}, lon={lon}, minutes={minutes}")
        logger.debug(f"[ORS Isochrone] Request JSON: {{'locations': [[{lon}, {lat}]], 'range': [{minutes * 60}]}}")
        start_time = datetime.now()
        response = requests.post(ors_url, headers=headers, json={"locations": [[lon, lat]], "range": [minutes * 60]})
        duration = (datetime.now() - start_time).total_seconds()
        logger.info(f"[ORS Isochrone] Response time: {duration:.2f}s")
        response.raise_for_status()
        ors_json = response.json()
        logger.debug(f"[ORS Isochrone] Response JSON: {ors_json}")
        poly = shape(ors_json['features'][0]['geometry'])
        logger.info(f"[ORS Isochrone] Polygon received, calculating average radius...")
        logger.info("==========================================================================\n")
    except requests.RequestException as e:
        logger.error(f"[ORS Isochrone] Exception: {str(e)}")
        logger.info("==========================================================================\n")
        raise HTTPException(status_code=503, detail="Error accessing OpenRouteService API")
    # 2. Rayon moyen
    center = Point(lon, lat)
    distances = [geodesic((center.y, center.x), (p[1], p[0])).meters for p in poly.exterior.coords]
    average_radius = int(sum(distances) / len(distances))
    
    # ---[ Google Places API ]---
    try:
        gplaces_url = "https://places.googleapis.com/v1/places:searchText"
        headers = {
            "Content-Type": "application/json",
            "X-Goog-Api-Key": settings.GOOGLE_API_KEY,
            "X-Goog-FieldMask": "places.displayName,places.formattedAddress,places.rating,places.location,places.id,places.types,places.priceLevel,places.editorialSummary"
        }
        # Construction de la requête Text Search
        text_query = keyword if keyword else type
        places_data = {
            "textQuery": text_query,
            "maxResultCount": 20,
            "locationBias": {
                "circle": {
                    "center": {
                        "latitude": lat,
                        "longitude": lon
                    },
                    "radius": min(float(average_radius), 50000.0)
                }
            },
            "includedType": type,
            "strictTypeFiltering": True,
            # "priceLevels": ["PRICE_LEVEL_MODERATE", "PRICE_LEVEL_EXPENSIVE"] # à adapter si paramètre prix
        }
        logger.info("\n==================== [CALL] Google Places Text Search API ====================")
        logger.info(f"Request: textQuery={text_query}, type={type}, lat={lat}, lon={lon}, radius={average_radius}m")
        logger.debug(f"[Google Places] Request JSON: {places_data}")
        try:
            start_time = datetime.now()
            places_resp = requests.post(gplaces_url, headers=headers, json=places_data)
            duration = (datetime.now() - start_time).total_seconds()
            logger.info(f"[Google Places] Response time: {duration:.2f}s")
            places_resp.raise_for_status()
            response_data = places_resp.json()
            logger.debug(f"[Google Places] Response JSON: {response_data}")
            places_count = len(response_data.get("places", []))
            logger.info(f"[Google Places] Found {places_count} places matching the criteria")
            logger.info("==================================================================\n")
        except requests.RequestException as e:
            error_message = f"Error accessing Google Places API: {str(e)}"
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_details = e.response.json()
                    error_message += f" - Details: {error_details}"
                    logger.error(f"[Google Places] Error details: {error_details}")
                except:
                    logger.error(f"[Google Places] Error status: {e.response.status_code}")
            logger.info("==================================================================\n")
            raise HTTPException(status_code=503, detail=error_message)
        return {
            "average_radius": average_radius,
            "places": [
                {
                    "name": p.get("displayName", {}).get("text", "Unknown"),
                    "address": p.get("formattedAddress", ""),
                    "rating": float(p.get("rating", {}).get("rating")) if isinstance(p.get("rating"), dict) and p.get("rating", {}).get("rating") is not None else p.get("rating", None),
                    "location": {
                        "lat": float(p.get("location", {}).get("latitude", 0)),
                        "lng": float(p.get("location", {}).get("longitude", 0))
                    },
                    "place_id": p.get("id", ""),
                    "types": p.get("types", []),
                    "price_level": p.get("priceLevel") if p.get("priceLevel") else None,
                    "description": p.get("editorialSummary", {}).get("text") if p.get("editorialSummary") else None
                }
                for p in response_data.get("places", [])[:20]
            ]
        }
    except requests.RequestException as e:
        error_message = "Error accessing Google Places API"
        if hasattr(e, 'response') and e.response is not None:
            try:
                error_details = e.response.json()
                error_message += f" - Details: {error_details}"
            except:
                error_message += f" - Status: {e.response.status_code}"
        raise HTTPException(status_code=503, detail=error_message)

