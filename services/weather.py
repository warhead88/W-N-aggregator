import aiohttp
import asyncio

from config import Config

API_KEY = Config.WEATHER_API
WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "http://api.openweathermap.org/data/2.5/forecast"

async def get_weather(city):
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric",
        "lang": "ru"
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(WEATHER_URL, params=params) as resp:
            data = await resp.json()
            return data

async def get_forecast(city):
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric",
        "lang": "ru"
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(FORECAST_URL, params=params) as resp:
            data = await resp.json()
            return data
