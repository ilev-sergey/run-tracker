from typing import Match

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from keyboards.confirmation import get_yes_no_kb
from keyboards.days import get_days_kb
from states import Activity

router = Router()


@router.message(Command("add_activity"))
async def cmd_add_activity(message: Message, state: FSMContext):
    await message.answer(
        f"Choose date of activity or enter it manually in DD.MM format.",
        reply_markup=get_days_kb(),
    )
    await state.set_state(Activity.entering_date)


@router.message(
    Activity.entering_date,
    F.text.regexp(r"(0[1-9]|[12][0-9]|3[01])[./](0[1-9]|1[012])").as_("date"),
)
async def date_entered(message: Message, state: FSMContext, date: Match[str]):
    await state.update_data(date=date)
    await message.answer(
        f"Enter time in HH:MM format.",
        reply_markup=ReplyKeyboardRemove(),
    )

    await state.set_state(Activity.entering_time)


@router.message(
    Activity.entering_time,
    F.text.regexp(r"(0[0-9]|1[0-9]|2[0-3])[:.][0-5][0-9]").as_("time"),
)
async def time_entered(message: Message, state: FSMContext, time: Match[str]):
    await state.update_data(time=time)
    await message.answer(
        f"Enter your lap times in MM:SS or MM:SS.SSS format.",
    )
    await state.set_state(Activity.entering_lap_times)


@router.message(
    Activity.entering_lap_times,
    F.text.regexp(r"(\S*(\d{2}:\d{2}|\d{2}:\d{2}.\d{2, 3}))+"),
)
async def lap_times_entered(message: Message, state: FSMContext):
    await message.answer(
        f"Great! It seems that you ran {1} laps in {1} time. Is that correct?",
        reply_markup=get_yes_no_kb(),
    )
    await state.set_state(Activity.confirming_result)


@router.message(Activity.confirming_result, F.text == "Yes")
async def result_confirmed(message: Message, state: FSMContext):
    await message.answer(
        f"The activity has been added!",
        reply_markup=ReplyKeyboardRemove(),
    )
    await state.clear()


@router.message(Activity.confirming_result)
async def result_unconfirmed(message: Message, state: FSMContext):
    await message.answer(
        f"The result hasn't been confirmed.\nRe-enter lap times "
        f"or use /add_activity to start from scratch, or /cancel to cancel adding an activity",
        reply_markup=ReplyKeyboardRemove(),
    )
    await state.set_state(Activity.entering_lap_times)
