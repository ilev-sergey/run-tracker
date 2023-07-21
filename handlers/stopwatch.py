from aiogram import F, Router
from aiogram.types import BufferedInputFile, Message, ReplyKeyboardRemove

from processing import database
from processing.analytics import (
    get_laps_number,
    get_plot_buffer,
    get_total_distance,
    get_total_time,
)
from processing.stopwatch_parser import get_lap_times, get_start_time

router = Router()


@router.message(F.text)
async def stopwatch_message(message: Message):
    if message.text and message.from_user:  # TODO: use filter
        try:
            start_time = get_start_time(message.text)
            lap_times = get_lap_times(message.text)
        except:
            await message.answer("Incorrect data format. Please try again")
        else:
            plot_buffer = await get_plot_buffer(lap_times)
            total_distance = get_total_distance(lap_times)
            total_laps = get_laps_number(lap_times)
            total_time = get_total_time(lap_times)
            await database.add_user_data(
                user_id=message.from_user.id, start_time=start_time, lap_times=lap_times
            )
            await message.answer_photo(
                BufferedInputFile(
                    plot_buffer.read(),
                    filename="Run_tracker_plot.png",
                ),
                caption=f"Congratulations! You have run {total_laps} laps ({total_distance} km) in {total_time.seconds // 60} minutes and {total_time.seconds % 60} seconds.",
                reply_markup=ReplyKeyboardRemove(remove_keyboard=True),
            )
