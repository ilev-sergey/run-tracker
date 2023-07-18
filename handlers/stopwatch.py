from aiogram import F, Router
from aiogram.types import Message, ReplyKeyboardRemove
from datetime import timedelta
from processing.stopwatch_parser import get_lap_times, get_timestamp

router = Router()


@router.message(F.text)
async def stopwatch_message(message: Message):
    if message.text and message.from_user:  # TODO: use filter
        try:
            timestamp = get_timestamp(message.text)
            lap_times = get_lap_times(message.text)
        except:
            await message.answer("Incorrect data format. Please try again")
        else:
	        sum_time = timedelta()
	        for lap_time in lap_times:
	            sum_time += lap_time
	        await message.answer(
	            f"Congratulations! You have run {len(lap_times)} laps in {sum_time.seconds // 60} minutes and {sum_time.seconds % 60} seconds",
	            reply_markup=ReplyKeyboardRemove(remove_keyboard=True),
	        )
