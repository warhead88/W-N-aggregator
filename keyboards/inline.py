from aiogram.utils.keyboard import InlineKeyboardBuilder

def main_menu():
    kb = InlineKeyboardBuilder()
    kb.button(text="Изменить место", callback_data="weather")
    kb.button(text="Изменить слова", callback_data="news")
    kb.button(text="Изменить количество", callback_data="cnt")
    kb.adjust(1)
    return kb.as_markup()
