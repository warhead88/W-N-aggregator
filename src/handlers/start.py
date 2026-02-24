from aiogram import Router, types
from aiogram.filters import Command

from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession

from db.tables import User

router = Router()

@router.message(Command("start"))
async def start(message: types.Message, session: AsyncSession):
    result = await session.execute(select(User).filter_by(id=message.from_user.id))
    user = result.scalar_one_or_none()

    if not user:
        user = User(id=message.from_user.id)
        session.add(user)
        # Note: the middleware commits automatically
        await message.answer("Привет! Это бот-агрегатор новостей и погоды. Здесь ты можешь получать последнюю информацию. Напиши /help для дополнительной информации.")
    else:
        await message.answer("Для получения инструкций введи команду /help.")
