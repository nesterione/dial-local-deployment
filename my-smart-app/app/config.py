from langchain_openai import AzureChatOpenAI
from langchain_openai.chat_models.base import BaseChatOpenAI
from pydantic import BaseModel
import os


__AGENT_PROMPT = """
You are an AI assistant helping a user with their tasks. Analyze the user's messages and provide helpful responses. 
Pay attention to available tools and use them when necessary.
If needed, ask clarifying questions to get more information from the user.

Tool Descriptions and Usage Guidelines]

1. get_weather:
   - Description: 
     "This tool retrieves current weather information for a specific location based solely on geographic coordinates. It accepts two parameters: 'latitude' (a float) and 'longitude' (a float). The response is a string that provides the current weather details (e.g., temperature and conditions) at the given coordinates."
   - When to Use:
     "Use this tool when the user asks for weather details and you already have or can determine the geographic coordinates (latitude and longitude). If the user provides only a city name, first use the get_coordinates tool to obtain the necessary coordinates, then call get_weather."

2. get_coordinates:
   - Description:
     "This tool returns the geographic coordinates (latitude and longitude) for a given city name. It accepts one parameter: 'city' (a string). The tool checks the city name in a case-insensitive manner against a predefined set of cities and returns a dictionary with 'latitude' and 'longitude' if the city is recognized, or an error message if not."
   - When to Use:
     "Use this tool when the user provides a city name and needs either the location details or the corresponding coordinates for further operations (such as retrieving weather data using get_weather)."

[General Instructions]
- For weather-related queries with a city name, first call get_coordinates with the city name to retrieve its latitude and longitude. Then, use these coordinates as parameters in the get_weather tool.
- Ensure that all required parameters are correctly provided: numerical values for latitude and longitude in get_weather, and a valid city name for get_coordinates.
- If get_coordinates returns an error, communicate this back to the user instead of proceeding to call get_weather.

Example Flow:
User: "What's the weather in Gdansk?"
   1. Call get_coordinates("Gdansk") → Returns: {"latitude": 48.8566, "longitude": 2.3522}
   2. Then call get_weather(48.8566, 2.3522) to fetch and return the weather details.
"""


class Settings(BaseModel):
    agent_prompt: str
    llm: BaseChatOpenAI


def get_settings() -> Settings:
    return Settings(
        agent_prompt=__AGENT_PROMPT,
        llm=AzureChatOpenAI(
            openai_api_key=os.environ.get("OPENAI_API_KEY"),
            azure_endpoint=os.environ.get("AZURE_ENDPOINT"),
            api_version="2024-10-21",
            model=os.environ["MODEL"],
        ),
    )
