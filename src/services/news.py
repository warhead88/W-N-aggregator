import aiohttp

from config import Config

API_KEY = Config.NEWS_API
BASE_URL = "https://gnews.io/api/v4/top-headlines"

async def get_news(sources=None, country=None, category=None, query=None, language=None):
    params = {
        "apikey": API_KEY,
    }
    if sources:
        params["sources"] = sources
    if country:
        params["country"] = country
    if category:
        params["category"] = category
    if language:
        params["language"] = language
    if query:
        params["q"] = query

    async with aiohttp.ClientSession() as session:
        async with session.get(BASE_URL, params=params) as resp:
            resp.raise_for_status()
            data = await resp.json()
            return data.get("articles", [])


