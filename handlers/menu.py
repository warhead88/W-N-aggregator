from zoneinfo import ZoneInfo

from aiogram import Router, types, F
from aiogram.filters import Command

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from sqlalchemy import select

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

class Timezone(StatesGroup):
    waiting_for_text = State()

def validate_timezone(tz_str: str) -> bool:
    try:
        _ = ZoneInfo(tz_str)
        return True
    except Exception:
        return False

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
        
        if user.is_subscribed == True:
            is_subscribed = "Активна"
        else:
            is_subscribed = "Неактивна"

        if not user.timezone:
            timezone = "Часовой пояс не задан."
        else:
            timezone = user.timezone

        await message.answer(f"""Это меню, где вы сможете увидеть и изменить свои параметры поиска, погоды и статус подписки.

Место, выбранное для ежедневной рассылки погоды: {place};

Ключевые слова для ежедневной подборки новостей: {query};

Количество новостей в ежедневной подборке: {count};

Часовой пояс: {timezone};

Статус подписки: {is_subscribed}.""", reply_markup=main_menu())

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
async def process_news_count(message: types.Message, state: FSMContext):
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

@router.message(Timezone.waiting_for_text)
async def process_timezone(message: types.Message, state: FSMContext):
    timezone = message.text

    if validate_timezone(timezone) == True:
        async with get_async_session() as session:
            result = await session.execute(
                select(User).where(User.id == message.from_user.id)
            )
            user = result.scalar_one_or_none()
    
            user.timezone = timezone
    
            await message.answer(f"Вы успешно установили свой часовой пояс: {timezone}!")
    else:
        await message.answer("Введён неверный часовой пояс.")

    await state.clear()

@router.callback_query(F.data == "weather")
async def change_place(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(Weather.waiting_for_text)
    await callback.message.answer("Введите место для рассылки погоды (город или страну):")
    await callback.answer()

@router.callback_query(F.data == "news")
async def change_query(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(News.waiting_for_text)
    await callback.message.answer("Введите ключевые слова для рассылки новостей:")
    await callback.answer()

@router.callback_query(F.data == "cnt")
async def change_count(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(Count.waiting_for_text)
    await callback.message.answer("Введите количество новостей в подборке (до 10):")
    await callback.answer()

@router.callback_query(F.data == "timezone")
async def change_timezone(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(Timezone.waiting_for_text)
    await callback.message.answer("Введите свой часовой пояс в формате 'Europe/Moscow' (IASA-формат):")
    await callback.answer()


@router.callback_query(F.data == "sub")
async def change_sub(callback: types.CallbackQuery, state: FSMContext):
    async with get_async_session() as session:
        result = await session.execute(select(User).where(User.id == callback.from_user.id))
        user = result.scalar_one_or_none()

        if user.is_subscribed != True:
            user.is_subscribed = True

            if user.timezone == None:
                await callback.message.answer("Вам нужно указать свой часовой пояс, чтобы подписаться.")    
            else:
                await callback.message.answer("Вы успешно подписались не ежедневную рассылку!")

        else:
            user.is_subscribed = False
            await callback.message.answer("Вы успешно отписались от ежедневной рассылки!")
    await callback.answer()
