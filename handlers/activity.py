from datetime import date, datetime, timedelta
from typing import Match

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import BufferedInputFile, CallbackQuery, Message, ReplyKeyboardRemove

from filters.activity import isLapTimesMessage
from keyboards.calendar import CalendarCallbackFactory, get_calendar_kb
from keyboards.days import day_buttons, get_days_kb
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
        reply_markup=get_calendar_kb(),
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


@router.callback_query(
    AddingActivity.entering_date,
    CalendarCallbackFactory.filter(F.action == "change_month"),
)
async def callbacks_change_month(
    callback: CallbackQuery, callback_data: CalendarCallbackFactory
):
    month = callback_data.month
    year = callback_data.year
    if month == 12 and callback_data.change == 1:
        month = 1
        year += 1
    elif month == 1 and callback_data.change == -1:
        month = 12
        year -= 1
    else:
        month += callback_data.change
    await callback.message.edit_text(
        f"Choose date of activity or enter it manually in DD.MM.YYYY format.",
        reply_markup=get_calendar_kb(
            month=month,
            year=year,
        ),
    )
    await callback.answer()


@router.callback_query(
    AddingActivity.entering_date, CalendarCallbackFactory.filter(F.action == "ignore")
)
async def callbacks_ignore(
    callback: CallbackQuery, callback_data: CalendarCallbackFactory
):
    await callback.answer()


@router.callback_query(
    AddingActivity.entering_date,
    CalendarCallbackFactory.filter(F.action == "choose_day"),
)
async def callbacks_choose_day(
    callback: CallbackQuery, state: FSMContext, callback_data: CalendarCallbackFactory
):
    chosen_date = date(
        year=callback_data.year, month=callback_data.month, day=callback_data.day
    )
    await state.update_data(date=datetime.strftime(chosen_date, "%d.%m.%Y"))
    await callback.message.edit_text(
        text=f"Chosen {datetime.strftime(chosen_date, '%d %b %Y')}",
        reply_markup=None,
    )
    await callback.message.answer(
        f"Enter time in HH:MM format.",
        reply_markup=ReplyKeyboardRemove(),
    )
    await state.set_state(AddingActivity.entering_time)
    await callback.answer()


# @router.message(
#     AddingActivity.entering_date,
#     F.text.in_(list(day_buttons.keys())),
# )
# async def date_entered(message: Message, state: FSMContext):
#     current_date = datetime.now().date()
#     date = current_date + timedelta(days=day_buttons[message.text])
#     await state.update_data(date=datetime.strftime(date, "%d.%m.%Y"))
#     await message.answer(
#         f"Enter time in HH:MM format.",
#         reply_markup=ReplyKeyboardRemove(),
#     )
#     await state.set_state(AddingActivity.entering_time)


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
