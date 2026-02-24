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

        if user is None:
            await message.answer("Сначала напишите /start для регистрации.")
            return

        import html
        place = html.escape(user.place) if user.place else "Место не задано"
        query = html.escape(user.query) if user.query else "Слова не заданы"
        count = user.count if user.count else "Количество не задано"
        is_subscribed = "Активна" if user.is_subscribed else "Неактивна"
        timezone = html.escape(user.timezone) if user.timezone else "Часовой пояс не задан."

        await message.answer(f"""<b>Настройки</b>

Место, выбранное для ежедневной рассылки погоды: <b>{place}</b>

Ключевые слова для ежедневной подборки новостей: <b>{query}</b>

Количество новостей в ежедневной подборке: <b>{count}</b>

Часовой пояс: <b>{timezone}</b>

Статус подписки: <b>{is_subscribed}</b>""", reply_markup=main_menu(), parse_mode="HTML")

@router.message(Weather.waiting_for_text)
async def process_weather_place(message: types.Message, state: FSMContext):
    async with get_async_session() as session:
        place = message.text

        result = await session.execute(select(User).where(User.id == message.from_user.id))
        user = result.scalar_one_or_none()
        if user:
            user.place = place
            await message.answer(f"Место: {place}; было успешно задано как ваше основное.")

    await state.clear()

@router.message(News.waiting_for_text)
async def process_news_query(message: types.Message, state: FSMContext):
    async with get_async_session() as session:
        query = message.text

        result = await session.execute(select(User).where(User.id == message.from_user.id))
        user = result.scalar_one_or_none()
        if user:
            user.query = query
            await message.answer(f"Ключевые слова для поиска: {query}; были успешно заданы.")

    await state.clear()

@router.message(Count.waiting_for_text)
async def process_news_count(message: types.Message, state: FSMContext):
    async with get_async_session() as session:
        try:
            count = int(message.text)
            if count <= 0 or count > 10:
                await message.answer("Введите число от 1 до 10.")
                await state.clear()
                return
        except Exception:
            await message.answer("Введите числовое значение.")
            await state.clear()
            return

        result = await session.execute(select(User).where(User.id == message.from_user.id))
        user = result.scalar_one_or_none()
        if user:
            user.count = count
            await message.answer(f"Количество новостей в подборке: {count}; было успешно задано.")

    await state.clear()

@router.message(Timezone.waiting_for_text)
async def process_timezone(message: types.Message, state: FSMContext):
    timezone = message.text

    if validate_timezone(timezone):
        async with get_async_session() as session:
            result = await session.execute(
                select(User).where(User.id == message.from_user.id)
            )
            user = result.scalar_one_or_none()
            if user:
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
        if not user:
            await callback.answer("Пользователь не найден. Введите /start!", show_alert=True)
            return

        if not user.is_subscribed:
            if user.timezone is None:
                await callback.message.answer("Вам нужно указать свой часовой пояс, чтобы подписаться.")
            else:
                user.is_subscribed = True
                await callback.message.answer("Вы успешно подписались на ежедневную рассылку!")
        else:
            user.is_subscribed = False
            await callback.message.answer("Вы успешно отписались от ежедневной рассылки!")
    await callback.answer()
