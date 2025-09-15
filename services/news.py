import aiohttp
import asyncio

from config import Config

API_KEY = Config.NEWS_API
BASE_URL = "https://newsapi.org/v2/top-headlines"

async def get_news(country="ru", category=None, query=None):
    params = {
        "apiKey": API_KEY,
        "country": country,
    }
    if category:
        params["category"] = category
    if query:
        params["q"] = query

    async with aiohttp.ClientSession() as session:
        async with session.get(BASE_URL, params=params) as resp:
            data = await resp.json()
            return data.get("articles", [])
