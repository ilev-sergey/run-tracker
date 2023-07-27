from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_timezone_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    for i in range(-11, 12):
        kb.add(KeyboardButton(text=f"{i:+}"))
    kb.adjust(8)
    return kb.as_markup(resize_keyboard=True)
