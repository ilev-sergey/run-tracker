import calendar
from datetime import datetime
from typing import Optional

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


class CalendarCallbackFactory(CallbackData, prefix="calendar"):
    action: str
    year: Optional[int] = None
    month: Optional[int] = None
    day: Optional[int] = None
    change: Optional[int] = None


def get_calendar_kb(month: Optional[int] = None, year: Optional[int] = None):
    current_date = datetime.now().date()
    if not year:
        year = current_date.year
    if not month:
        month = current_date.month

    keyboard = InlineKeyboardBuilder()

    # Month and year
    info_button = InlineKeyboardButton(
        text=calendar.month_name[month] + " " + str(year),
        callback_data=CalendarCallbackFactory(action="ignore").pack(),
    )
    keyboard.row(info_button)

    # Weekdays
    weekdays = [
        InlineKeyboardButton(
            text=day, callback_data=CalendarCallbackFactory(action="ignore").pack()
        )
        for day in ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]
    ]
    keyboard.row(*weekdays)

    # Days
    matrix = calendar.monthcalendar(year, month)
    for week in matrix:
        days = []
        for day in week:
            if day == 0:
                days.append(
                    InlineKeyboardButton(
                        text=" ",
                        callback_data=CalendarCallbackFactory(action="ignore").pack(),
                    )
                )
            else:
                days.append(
                    InlineKeyboardButton(
                        text=str(day),
                        callback_data=CalendarCallbackFactory(
                            action="choose_day", year=year, month=month, day=day
                        ).pack(),
                    )
                )
        keyboard.row(*days)

    # Control Buttons
    control_buttons = []
    control_buttons.append(
        InlineKeyboardButton(
            text="<",
            callback_data=CalendarCallbackFactory(
                action="change_month", month=month, year=year, change=-1
            ).pack(),
        )
    )
    control_buttons.append(
        InlineKeyboardButton(
            text=" ", callback_data=CalendarCallbackFactory(action="ignore").pack()
        )
    )
    control_buttons.append(
        InlineKeyboardButton(
            text=">",
            callback_data=CalendarCallbackFactory(
                action="change_month", month=month, year=year, change=1
            ).pack(),
        )
    )
    keyboard.row(*control_buttons)

    return keyboard.as_markup()
