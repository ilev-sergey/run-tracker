from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_days_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    days = ["Day before yesterday", "yesterday", "today"]
    for text in days:
        kb.add(KeyboardButton(text=text))
    return kb.as_markup(resize_keyboard=True)
