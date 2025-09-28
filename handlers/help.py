from aiogram import Router, types
from aiogram.filters import Command

router = Router()

@router.message(Command("help"))
async def show_help(message: types.Message):
    await message.answer("""Команды для бота:
1. /news - поиск новостей; нужно следовать инструкциям после написания команды;
2. /weather <место> - узнать погоду в конкретном месте;
3. /forecast <место> - узнать прогноз на 3 дня в конкретном месте.""")
