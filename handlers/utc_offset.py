from datetime import datetime, timedelta, timezone

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from keyboards.timezones import get_timezone_kb
from states import UTC_Offset
from processors import database

router = Router()
timezones = [f"{i:+}" for i in range(-11, 12)]


@router.message(Command("set_utc_offset"))
async def cmd_set_utc_offset(message: Message, state: FSMContext):
    utc_time = datetime.now(timezone.utc).time()
    await message.answer(
        f"Current UTC time: {utc_time.isoformat(timespec='minutes')}. Please choose your timezone.",
        reply_markup=get_timezone_kb(),
    )
    await state.set_state(UTC_Offset.choosing_timezone)


@router.message(UTC_Offset.choosing_timezone, F.text.in_(timezones))
async def utc_offset_chosen(message: Message, state: FSMContext):
    if message.text and message.from_user:
        user_datetime = datetime.now(timezone.utc) + timedelta(hours=int(message.text))
        await message.answer(
            f"You have chosen timezone: {message.text}. "
            f"Your time: {user_datetime.time().isoformat(timespec='minutes')}",
            reply_markup=ReplyKeyboardRemove(),  # type: ignore
        )
        await database.set_user_timezone(
            user_id=message.from_user.id, timezone=int(message.text)
        )

        await state.clear()
