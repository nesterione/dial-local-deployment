from langchain_core.tools import tool

# These tools mock the real-world tools that would be used in the application.
# In the real-world, these tools would make API calls to external services to get the required data.


@tool
def get_weather(latitude: float, longitude: float) -> str:
    """This tool can get weather only based on latitude and longitude. The location """
    return "32C sunny."


@tool
def get_coordinates(city: str) -> str:
    """This tool can check actual coordinates (latitude, longitude) based on the city name."""
    mock_coordinates = {
        "vilnius": (40.7128, -74.0060),
        "london": (51.5074, -0.1278),
        "paris": (48.8566, 2.3522),
    }
    city_lower = city.lower().strip()
    if city_lower in mock_coordinates:
        lat, lon = mock_coordinates[city_lower]
        return f"{city} location is: latitude:{lat}, longitude:{lon}"
    return "Could not find coordinates for {city}"
