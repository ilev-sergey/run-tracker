from datetime import datetime, timedelta
from typing import Match

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import BufferedInputFile, Message, ReplyKeyboardRemove

from filters.activity import isLapTimesMessage
from keyboards.days import get_days_kb
from processors import database
from processors.activity import Activity
from states import AddingActivity

router = Router()


async def _send_activity_info(message: Message, lap_times: list[timedelta]):
    activity = Activity(lap_times)
    plot_buffer = await activity.plot_buffer()
    await message.answer_photo(
        BufferedInputFile(
            plot_buffer.read(),
            filename="Run_tracker_plot.png",
        ),
        caption=f"Congratulations! You have run {activity.laps_number} laps ({activity.distance.km:.1f} km) "
        f"in {activity.time.seconds // 60} minutes and {activity.time.seconds % 60} seconds.",
        reply_markup=ReplyKeyboardRemove(),
    )


@router.message(Command("add_activity"))
async def cmd_add_activity(message: Message, state: FSMContext):
    await message.answer(
        f"Choose date of activity or enter it manually in DD.MM.YYYY format.",
        reply_markup=get_days_kb(),
    )
    await state.set_state(AddingActivity.entering_date)


@router.message(
    AddingActivity.entering_date,
    F.text.regexp(r"(0[1-9]|[12][0-9]|3[01]).(0[1-9]|1[012]).(19|20)[0-9]{2}").as_(
        "date"
    ),
)
async def date_entered(message: Message, state: FSMContext, date: Match[str]):
    await state.update_data(date=date.group())
    await message.answer(
        f"Enter time in HH:MM format.",
        reply_markup=ReplyKeyboardRemove(),
    )
    await state.set_state(AddingActivity.entering_time)


@router.message(
    AddingActivity.entering_time,
    F.text.regexp(r"(0[0-9]|1[0-9]|2[0-3])[:.][0-5][0-9]").as_("time"),
)
async def time_entered(message: Message, state: FSMContext, time: Match[str]):
    await state.update_data(time=time.group())
    await message.answer(
        f"Enter your lap times in MM:SS or MM:SS.SSS format.",
    )
    await state.set_state(AddingActivity.entering_lap_times)


@router.message(
    AddingActivity.entering_lap_times,
    isLapTimesMessage(),
)
async def lap_times_entered(
    message: Message, state: FSMContext, lap_times: list[timedelta]
):
    user_data = await state.get_data()
    await database.add_user_data(
        user_id=message.from_user.id,
        start_time=datetime.strptime(
            user_data["date"] + " " + user_data["time"], "%d.%m.%Y %H:%M"
        ),
        lap_times=lap_times,
    )
    await _send_activity_info(message, lap_times)
    await state.clear()
