
# TimeReach

TimeReach is an API that helps users find places within a specified travel time using isochrones. It combines OpenRouteService for travel time calculations with Google Places API for location discovery.

## Features

- Find places within a specified travel time (1-60 minutes)
- Support for various place types (see below for valid types)
- Use both place type and keyword for precise searches (e.g. type=restaurant & keyword=pizzeria)
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

### Endpoint

#### GET /places

Find places within a specified travel time.

Parameters:
- `location` (string, optional): Name of the starting point (e.g. "Eiffel Tower, Paris")
- `lat` (float, optional): Latitude (-90 to 90)
- `lon` (float, optional): Longitude (-180 to 180)
- `minutes` (int): Travel time in minutes (1 to 60)
- `type` (string): Place type (see below for valid types)
- `mode` (string, optional): Transport mode (driving-car, cycling-regular, foot-walking, foot-hiking, etc.)
- `keyword` (string, optional): Filter results by keyword (e.g. "pizza", "sushi", "vegan")

### How to use `type` and `keyword`

- **type**: Must be a valid Google Places type (e.g. restaurant, cafe, bar, bakery, museum, park, etc.). See [Google Places Types](https://developers.google.com/maps/documentation/places/web-service/place-types) for the full list.
- **keyword**: Any free text to refine the search (e.g. "pizzeria", "sushi", "vegan", "bistro").
- You can use **type** alone, **keyword** alone, or both together for more precise results.
- If you want a specific kind of place not in the official types (e.g. "pizzeria"), use type=restaurant and keyword=pizzeria.

#### Examples

```bash
# Find restaurants within 20 minutes by car
curl "http://localhost:8000/places?location=Paris&minutes=20&type=restaurant"

# Find pizzerias within 10 minutes by bike (type=restaurant, keyword=pizzeria)
curl "http://localhost:8000/places?location=Paris&minutes=10&type=restaurant&mode=cycling-regular&keyword=pizzeria"

# Find vegan places within 15 minutes walking
curl "http://localhost:8000/places?location=Paris&minutes=15&type=restaurant&mode=foot-walking&keyword=vegan"

# Find museums within 30 minutes
curl "http://localhost:8000/places?location=Paris&minutes=30&type=museum"

# Find any place with keyword only
curl "http://localhost:8000/places?location=Paris&minutes=20&keyword=bistro"
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

### Valid Place Types

Some common valid types:

- restaurant
- cafe
- bar
- bakery
- museum
- park
- tourist_attraction
- supermarket
- pharmacy
- hotel
- library
- gym
- movie_theater

For the full list, see [Google Places Types](https://developers.google.com/maps/documentation/places/web-service/place-types).

## ChatGPT Integration & Best Practices

When integrating with ChatGPT or any assistant:

- Always specify a valid `type` (see above) for best results.
- Use `keyword` for more precise queries (e.g. "pizzeria", "sushi", "vegan", "bistro").
- You can use both together: `type=restaurant&keyword=pizzeria`.
- If the user asks for something not in the official types, map to the closest type and use the keyword.
- Example: "Trouve-moi des pizzerias à Paris dans les 10 minutes en vélo" → `type=restaurant&keyword=pizzeria&mode=cycling-regular`

### Example ChatGPT Prompt

```text
You are an assistant that helps users find interesting places. You have access to the TimeReach API that finds places within a travel time radius.

Endpoint: https://your-render-app.onrender.com/places

Parameters:
- location (or lat/lon): starting point
- minutes: travel time (1-60)
- type: valid Google Places type (see doc)
- keyword: optional search keyword for more precision
- mode: transport mode (driving-car, cycling-regular, foot-walking, etc.)

Examples:
- "Find pizzerias within 10 minutes by bike from Paris"
- "Find vegan restaurants within 15 minutes walking from the Eiffel Tower"
- "Find museums within 30 minutes from my hotel"
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
