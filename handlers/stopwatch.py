from aiogram import F, Router
from aiogram.types import Message, ReplyKeyboardRemove

from processing import database
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
            total_distance = get_total_distance(lap_times)
            total_laps = get_laps_number(lap_times)
            total_time = get_total_time(lap_times)
            await database.add_user_data(
                user_id=message.from_user.id, timestamp=timestamp, lap_times=lap_times
            )
	        await message.answer(
	            f"Congratulations! You have run {total_laps} laps ({total_distance} km) in {total_time.seconds // 60} minutes and {total_time.seconds % 60} seconds.",
	            reply_markup=ReplyKeyboardRemove(remove_keyboard=True),
	        )
