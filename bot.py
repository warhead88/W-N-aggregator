import asyncio
import logging

from aiogram import Bot, Dispatcher

from config import Config
from db.db import init_db
from handlers import start, help, menu, news, weather, forecast
from services.scheduler import sched, check_and_send
from services import scheduler

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

async def main():
    await init_db()

    bot = Bot(token=Config.BOT_TOKEN)
    dp = Dispatcher()

    sched.add_job(
        check_and_send,
        "interval",
        minutes=0.5,
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
    dp.include_router(scheduler.router)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
