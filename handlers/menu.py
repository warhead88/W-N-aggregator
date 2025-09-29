from aiogram import Router, types, F
from aiogram.filters import Command

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from sqlalchemy import select, update

from db.db import get_async_session
from db.tables import User
from keyboards.inline import main_menu

router = Router()

class Weather(StatesGroup):
    waiting_for_text = State()

class News(StatesGroup):
    waiting_for_text = State()

class Count(StatesGroup):
    waiting_for_text = State()

@router.message(Command("menu"))
async def open_menu(message: types.Message):
    async with get_async_session() as session:
        result = await session.execute(
            select(User).where(User.id == message.from_user.id)
        )
        user = result.scalar_one_or_none()

        if not user.place:
            place = "Место не задано"
        else:
            place = user.place

        if not user.query:
            query = "Слова не заданы"
        else:
            query = user.query

        if not user.count:
            count = "Количество не задано"
        else:
            count = user.count

        await message.answer(f"""Это меню, где вы сможете увидеть и изменить свои параметры поиска, погоды и статус подписки.

Место, выбранное для ежедневной рассылки погоды: {place};

Ключевые слова для ежедневной подборки новостей: {query};

Количество новостей в ежедневной подборке: {count}.""", reply_markup=main_menu())

@router.message(Weather.waiting_for_text)
async def process_weather_place(message: types.Message, state: FSMContext):
    async with get_async_session() as session:
        place = message.text

        result = await session.execute(select(User).where(User.id == message.from_user.id))
        user = result.scalar_one_or_none()
        
        user.place = place
        
        await message.answer(f"Место: {place}; было успешно задано как ваше основное.")

    await state.clear()

@router.message(News.waiting_for_text)
async def process_news_query(message: types.Message, state: FSMContext):
    async with get_async_session() as session:
        query = message.text

        result = await session.execute(select(User).where(User.id == message.from_user.id))
        user = result.scalar_one_or_none()

        user.query = query

        await message.answer(f"Ключевые слова для поиска: {query}; были успешно заданы.")

    await state.clear()

@router.message(Count.waiting_for_text)
async def procces_news_count(message: types.Message, state: FSMContext):
    async with get_async_session() as session:
        try:
            count = int(message.text)
            if count > 10:
                await message.answer("Введите не более 10 новостей.")
                await state.clear()
                return
        except:
            await message.answer("Введите числовое значение.")
            await state.clear()
            return
        
        result = await session.execute(select(User).where(User.id == message.from_user.id))
        user = result.scalar_one_or_none()

        user.count = count

        await message.answer(f"Количество новостей в подборке: {count}; было успешно задано.")

    await state.clear()

@router.callback_query(F.data == "weather")
async def change_place(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(Weather.waiting_for_text)
    await callback.message.answer("Введите место для рассылки погоды (город или страну):")

@router.callback_query(F.data == "news")
async def change_query(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(News.waiting_for_text)
    await callback.message.answer("Введите ключевые слова для рассылки новостей:")

@router.callback_query(F.data == "cnt")
async def change_count(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(Count.waiting_for_text)
    await callback.message.answer("Введите количество новостей в подборке (до 10):")
