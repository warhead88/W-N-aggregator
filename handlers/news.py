from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from services import news

router = Router()

class Form(StatesGroup):
    waiting_for_q = State()
    waiting_for_count = State()

@router.message(Command("news"))
async def get_news(message: types.Message, state: FSMContext):
    await state.set_state(Form.waiting_for_q)
    await message.answer("Введите ключевые слова для поиска новостей:")

@router.message(Form.waiting_for_q)
async def process_query(message: types.Message, state: FSMContext):
    query = message.text
    await state.update_data(query=query)
    await state.set_state(Form.waiting_for_count)
    await message.answer("Введите количество новостей (макс 10):")

@router.message(Form.waiting_for_count)
async def process_count(message: types.Message, state: FSMContext):
    data = await state.get_data()
    query = data.get("query")
    try:
        count = int(message.text)
    except ValueError:
        count = 5  # если пользователь ввёл не число, пусть будет дефолт

    count = min(count, 10)

    articles = await news.get_news(query=query, country="ru")
    
    if not articles:
        await message.answer("Новости по заданной теме не найдены.")
        await state.clear()
        return

    text = ""
    for article in articles[:count]:
        title = article.get("title", "Без названия")
        description = article.get("description", "Нет описания")
        link = article.get("url", "#")

        text += f"<b>{title}</b>\n{description}\n<i>{link}</i>\n\n"

    await message.answer(text, parse_mode="HTML")
    await state.clear()
