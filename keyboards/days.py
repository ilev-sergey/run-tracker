from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

day_buttons = {"Day before yesterday": -2, "yesterday": -1, "today": 0}


def get_days_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    for text in day_buttons.keys():
        kb.add(KeyboardButton(text=text))
    return kb.as_markup(resize_keyboard=True)
