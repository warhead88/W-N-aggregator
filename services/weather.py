import aiohttp
import asyncio

from config import Config

API_KEY = Config.WEATHER_API
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

async def get_weather(city="Chicago"):
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric",
        "lang": "ru"
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(BASE_URL, params=params) as resp:
            data = await resp.json()
            return data
