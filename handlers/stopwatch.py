from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from datetime import timedelta
from processing.parsing import *

router = Router()


@router.message(F.text)
async def stopwatch_message(message: Message):
    if message.text:
        timestamp = get_timestamp(message.text)
        lap_times = get_lap_times(message.text)
        sum_time = timedelta()
        for lap_time in lap_times:
            sum_time += lap_time
        await message.answer(
            f"Congratulations! You have run {len(lap_times)} laps in {sum_time.seconds // 60} minutes and {sum_time.seconds % 60} seconds",
            reply_markup=ReplyKeyboardRemove(),
        )
