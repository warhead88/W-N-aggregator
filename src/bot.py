import asyncio
import logging

from aiogram import Bot, Dispatcher

from config import Config
from db.db import SessionLocal
from handlers import start, help, menu, news, weather, forecast
from services.scheduler import sched, check_and_send
from middlewares.db import DbSessionMiddleware

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

async def main():
    bot = Bot(token=Config.BOT_TOKEN)
    dp = Dispatcher()
    dp.update.middleware(DbSessionMiddleware(session_pool=SessionLocal))

    sched.add_job(
        check_and_send,
        "interval",
        minutes=5,
        id = "daily_news_check",
        args=[bot]
    )

    sched.start()

    dp.include_router(start.router)
    dp.include_router(help.router)
    dp.include_router(menu.router)
    dp.include_router(news.router)
    dp.include_router(weather.router)
    dp.include_router(forecast.router)

    try:
        await dp.start_polling(bot)
    finally:
        sched.shutdown(wait=False)
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
