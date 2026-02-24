from aiogram.utils.keyboard import InlineKeyboardBuilder

def main_menu():
    kb = InlineKeyboardBuilder()
    kb.button(text="Изменить место", callback_data="weather")
    kb.button(text="Изменить слова", callback_data="news")
    kb.button(text="Изменить количество", callback_data="cnt")
    kb.button(text="Изменить часовой пояс", callback_data="timezone")
    kb.button(text="Изменить статус подписки", callback_data="sub")
    kb.adjust(2, 2, 1)
    return kb.as_markup()
