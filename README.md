# TimeReach

TimeReach is an API that helps users find places within a specified travel time using isochrones. It combines OpenRouteService for travel time calculations with Google Places API for location discovery.

## Features

- Find places within a specified travel time (1-60 minutes)
- Support for various place types (restaurants, cafes, bars, etc.)
- Integration with ChatGPT for natural language queries
- Detailed place information including ratings, price levels, and descriptions
- CORS support for web integration

## Prerequisites

- Python 3.8+
- OpenRouteService API key (get it from [OpenRouteService](https://openrouteservice.org/dev/#/signup))
- Google Places API key (get it from [Google Cloud Console](https://console.cloud.google.com/))

## Installation

1. Clone the repository:
```bash
git clone https://github.com/ClementV78/TimeReach.git
cd TimeReach
```

2. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file with your API keys:
```bash
ORS_API_KEY=your_openrouteservice_api_key
GOOGLE_API_KEY=your_google_places_api_key
```

## Running Locally

Start the development server:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

### Endpoints

#### GET /restaurants

Find places within a specified travel time.

Parameters:
- `lon` (float): Starting point longitude (-180 to 180)
- `lat` (float): Starting point latitude (-90 to 90)
- `minutes` (int): Travel time in minutes (1 to 60)
- `type` (string): Place type (restaurant, cafe, bar, fast_food_restaurant, bakery, any)
- `keyword` (string, optional): Filter results by keyword

Example Request:
```bash
curl "http://localhost:8000/restaurants?lon=2.3522&lat=48.8566&minutes=20&type=restaurant"
```

Example Response:
```json
{
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
            "description": "Restaurant description..."
        }
    ]
}
```

## ChatGPT Integration

To use TimeReach with ChatGPT, use the following system prompt:

```text
You are an assistant that helps users find interesting places. You have access to the TimeReach API that finds places within a travel time radius.

Endpoint: https://your-render-app.onrender.com/restaurants

Parameters:
- lat, lon: starting point coordinates (-90≤lat≤90, -180≤lon≤180)
- minutes: travel time (1-60)
- type: restaurant, cafe, bar, fast_food_restaurant, bakery, any
- keyword: optional search keyword

Example: "Find restaurants within 15 minutes of the Eiffel Tower"
You should:
1. Get Eiffel Tower coordinates (48.8584, 2.2945)
2. Call API with coordinates and desired time
3. Format response in a natural way
```

## Deployment

The API is designed to be deployed on Render.com. Follow these steps:

1. Create a new Web Service on Render
2. Connect your GitHub repository
3. Configure the environment variables:
   - `ORS_API_KEY`
   - `GOOGLE_API_KEY`
4. Set the build command: `pip install -r requirements.txt`
5. Set the start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

## Rate Limits and Quotas

Be aware of the following limits:

- OpenRouteService: Varies by plan (check your account)
- Google Places API: Pay-as-you-go based on:
  - Nearby Search requests
  - Basic vs. Contact vs. Atmosphere data
  - Check [Google Places API pricing](https://developers.google.com/maps/documentation/places/web-service/usage-and-billing)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- OpenRouteService for isochrone calculations
- Google Places API for location data
- FastAPI framework
