import aiohttp

from config import Config

API_KEY = Config.WEATHER_API
BASE_URL = "https://api.openweathermap.org/data/2.5"

async def _fetch_weather_data(endpoint: str, city: str):
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric",
        "lang": "ru"
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{BASE_URL}/{endpoint}", params=params) as resp:
            resp.raise_for_status()
            return await resp.json()

async def get_weather(city: str):
    return await _fetch_weather_data("weather", city)

async def get_forecast(city: str):
    return await _fetch_weather_data("forecast", city)
