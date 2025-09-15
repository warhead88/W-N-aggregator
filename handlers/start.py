from aiogram import Router, types
from aiogram.filters import Command

router = Router()

@router.message(Command("start"))
async def start(message: types.Message):
    await message.answer("""Привет! Это бот-аггрегатор новостей. Тут ты можешь узнать
    погоду в своём городе и получить сводку новостей по интересующей тебя теме. Так же доступна подписка на рассылку.""")
