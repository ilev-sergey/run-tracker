from aiogram import Router
from aiogram.enums.parse_mode import ParseMode
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message):
    with open("welcome.md", "r") as file:
        answer = file.read()
    await message.answer(
        answer, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True
    )


@router.message(Command("cancel"))
async def cmd_cancel(message: Message):
    await message.answer(
        "Action canceled",
        reply_markup=ReplyKeyboardRemove(),
    )
