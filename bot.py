import asyncio
import logging

from aiogram import Bot, Dispatcher

from config import Config
from handlers import start, news, weather, forecast, get_sticker

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

async def main():
    bot = Bot(token=Config.BOT_TOKEN)
    dp = Dispatcher()

    dp.include_router(start.router)
    dp.include_router(news.router)
    dp.include_router(weather.router)
    dp.include_router(forecast.router)
    dp.include_router(get_sticker.router)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
