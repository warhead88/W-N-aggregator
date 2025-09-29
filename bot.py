import asyncio
import logging

from aiogram import Bot, Dispatcher

from config import Config
from db.db import init_db
from handlers import start, help, menu, news, weather, forecast

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

async def main():
    await init_db()

    bot = Bot(token=Config.BOT_TOKEN)
    dp = Dispatcher()

    dp.include_router(start.router)
    dp.include_router(help.router)
    dp.include_router(menu.router)
    dp.include_router(news.router)
    dp.include_router(weather.router)
    dp.include_router(forecast.router)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
