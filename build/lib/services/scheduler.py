import datetime
from zoneinfo import ZoneInfo
import asyncio

from sqlalchemy import select
from apscheduler.schedulers.asyncio import AsyncIOScheduler

import logging
import html

from aiogram import Bot

from db.db import get_async_session
from db.tables import User

from services.news import get_news
from services.weather import get_weather

logger = logging.getLogger(__name__)

sched = AsyncIOScheduler()

# Simple in-memory cache to prevent spam
daily_cache = {}

async def check_and_send(bot: Bot):
    async with get_async_session() as session:
        now_utc = datetime.datetime.now(datetime.timezone.utc)
        today_str = now_utc.strftime("%Y-%m-%d")

        result = await session.execute(
            select(User).where(User.is_subscribed.is_(True))
        )
        users = result.scalars().all()

        for user in users:
            try:
                tz = ZoneInfo(user.timezone)
            except Exception:
                continue

            user_time = now_utc.astimezone(tz)
            
            # Key for cache
            cache_key = f"{user.id}_{today_str}"

            if datetime.time(14, 0) <= user_time.time() <= datetime.time(15, 5):
                if daily_cache.get(cache_key):
                    continue  # Already sent today
                
                query = user.query
                count = user.count or 5
                place = user.place

                # Mark as sent
                daily_cache[cache_key] = True
                
                text_parts = ["<b>🌟 Ваш ежедневный дайджест:</b>\n"]

                if place:
                    safe_place = html.escape(place)
                    try:
                        weather_data = await get_weather(place)
                        name = html.escape(weather_data.get("name", place))
                        weather_desc = html.escape(weather_data.get("weather", [{}])[0].get("description", "Нет данных"))
                        temp = weather_data.get("main", {}).get("temp", "N/A")
                        text_parts.append(f"<b>Погода в {name}</b>: {weather_desc}, 🌡 {temp} °C\n")
                    except Exception as e:
                        logger.error(f"Error fetching weather for user {user.id} ({place}): {e}")
                        text_parts.append(f"<b>Погода в {safe_place}</b>: Недоступна в данный момент.\n")
                
                text_parts.append("\n<b>📰 Новости:</b>\n")

                try:
                    articles = await get_news(query=query, country="ru")
                except Exception as e:
                    articles = []
                    logger.error(f"Error fetching news for user {user.id}: {e}")

                if not articles:
                    text_parts.append("Новости по вашей теме сегодня не найдены.")
                else:
                    for article in articles[:count]:
                        title = html.escape(article.get("title", "Без названия"))
                        description = html.escape(article.get("description", "Нет описания"))
                        link = article.get("url", "#")
                        text_parts.append(f"<b>{title}</b>\n{description}\n<i>{link}</i>\n\n")

                await bot.send_message(user.id, "".join(text_parts), parse_mode="HTML")

            # Cleanup old cache keys periodically (basic approach)
            if len(daily_cache) > 1000:
                daily_cache.clear()
