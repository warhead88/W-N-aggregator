from aiogram import Router, types
from aiogram.filters import Command

router = Router()

@router.message(Command("start"))
async def start(message: types.Message):
    await message.answer("""Привет! Это бот-аггрегатор новостей и погоды. Здесь ты можешь получать последнюю информацию. Напиши /help для дополнительной информации.""")
