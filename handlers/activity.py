from datetime import datetime
from typing import Match

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import BufferedInputFile, Message, ReplyKeyboardRemove

from keyboards.confirmation import get_yes_no_kb
from keyboards.days import get_days_kb
from parsers.activity import get_lap_times
from processors import database
from states import AddingActivity

router = Router()


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
    await state.update_data(date=date.string)
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
    await state.update_data(time=time.string)
    await message.answer(
        f"Enter your lap times in MM:SS or MM:SS.SSS format.",
    )
    await state.set_state(AddingActivity.entering_lap_times)


@router.message(
    AddingActivity.entering_lap_times,
    F.text.regexp(r"(\S*(\d{2}:\d{2}|\d{2}:\d{2}.\d{2, 3}))+"),
)
async def lap_times_entered(
    message: Message, state: FSMContext
):  # TODO: fix code repetition (stopwatch)
    if message.text and message.from_user:
        lap_times = get_lap_times(text=message.text)
        plot_buffer = await get_plot_buffer(lap_times)
        total_distance = get_total_distance(lap_times)
        total_laps = get_laps_number(lap_times)
        total_time = get_total_time(lap_times)
        await state.update_data(lap_times=lap_times)
        await message.answer_photo(
            BufferedInputFile(
                plot_buffer.read(),
                filename="Run_tracker_plot.png",
            ),
            caption=f"Congratulations! You have run {total_laps} laps ({total_distance:.1f} km) in {total_time.seconds // 60} minutes and {total_time.seconds % 60} seconds. Is that correct?",
            reply_markup=get_yes_no_kb(),
        )
        await state.set_state(Activity.confirming_result)


@router.message(Activity.confirming_result, F.text == "Yes")
async def result_confirmed(message: Message, state: FSMContext):
    if message.text and message.from_user:
        user_data = await state.get_data()

        await database.add_user_data(
            user_id=message.from_user.id,
            start_time=datetime.strptime(
                user_data["date"] + " " + user_data["time"], "%d.%m.%Y %H:%M"
            ),
            lap_times=user_data["lap_times"],
        )
        await message.answer(
            f"The activity has been added!",
            reply_markup=ReplyKeyboardRemove(remove_keyboard=True),
        )
        await state.clear()


@router.message(Activity.confirming_result)
async def result_unconfirmed(message: Message, state: FSMContext):
    await message.answer(
        f"The result hasn't been confirmed.\nRe-enter lap times "
        f"or use /add_activity to start from scratch, or /cancel to cancel adding an activity",
        reply_markup=ReplyKeyboardRemove(remove_keyboard=True),
    )
    await state.set_state(Activity.entering_lap_times)
