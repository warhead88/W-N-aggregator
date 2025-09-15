import asyncio
import logging

from aiogram import Bot, Dispatcher

from config import Config

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

async def main():
    bot = Bot(token=Config.BOT_TOKEN)
    dp = Dispatcher()

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
