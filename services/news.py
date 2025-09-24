import aiohttp
import asyncio

from config import Config

API_KEY = Config.NEWS_API
BASE_URL = "https://newsapi.org/v2/everything"

async def get_news(sources=None, country=None, category=None, query=None, language=None):
    params = {
        "apiKey": API_KEY,
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
            data = await resp.json()
            return data.get("articles", [])

async def main():
    articles = await get_news(query="Ukraine")
    for article in articles:
        title = article["title"]
        description = article["description"]
        link = article["url"]

        print(f"title: {title}\ndescription: {description}\nurl: {link}\n\n")

if __name__ == "__main__":
    asyncio.run(main())
