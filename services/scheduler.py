import datetime
from zoneinfo import ZoneInfo
import asyncio

from sqlalchemy import select
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from aiogram import Router, Bot

from db.db import get_async_session
from db.tables import User

from services.news import get_news

router = Router()

sched = AsyncIOScheduler()

async def check_and_send(bot: Bot):
    async with get_async_session() as session:
        now_utc = datetime.datetime.now(datetime.timezone.utc)

        result = await session.execute(
            select(User).where(User.is_subscribed == True)
        )
        users = result.scalars().all()

        for user in users:
            if not user.is_subscribed:
                continue

            try:
                tz = ZoneInfo(user.timezone)

            except Exception:
                continue

            user_time = now_utc.astimezone(tz)
            
            if datetime.time(14, 0) <= user_time.time() <= datetime.time(15, 5):
                query = user.query
                place = user.place
                count = user.count

                articles = await get_news(query=query, country="ru")

                if not articles:
                    await bot.send_message(user.id, "Новости по заданной теме не найдены.")
                else:
                    text = ""
                    for article in articles[:count]:
                        title = article.get("title", "Без названия")
                        description = article.get("description", "Нет описания")
                        link = article.get("url", "#")

                        text += f"<b>{title}</b>\n{description}\n<i>{link}</i>\n\n"

                await bot.send_message(user.id, text, parse_mode="HTML")
