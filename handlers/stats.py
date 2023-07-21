from datetime import datetime, timedelta

from aiogram import Router
from aiogram.enums.parse_mode import ParseMode
from aiogram.filters import Command
from aiogram.types import Message

from processing import database

router = Router()


@router.message(Command("stats"))
async def cmd_stats(message: Message):
    def get_answer(data):
        if data:
            time = datetime.strptime(data["avg_time"], "%H:%M:%S.%f")
            delta = timedelta(
                hours=time.hour,
                minutes=time.minute,
                seconds=time.second,
                milliseconds=time.microsecond / 1000,
            )
            return (
                f"\n- average distance: {round(data['avg_distance'], 1)} km"
                + f"\n- average lap time: {str(delta)[2:-3]}"
            )
        return "no data for this period"

    if message.from_user:
        weekly_avg = await database.avg_for_period(
            user_id=message.from_user.id, period_in_days=7
        )
        monthly_avg = await database.avg_for_period(
            user_id=message.from_user.id, period_in_days=30
        )
        all_time_avg = await database.avg_for_period(user_id=message.from_user.id)
        await message.answer(
            f"Your running stats:\n"
            + f"*For past week:* {get_answer(weekly_avg)}\n"
            + f"*For past month:* {get_answer(monthly_avg)}\n"
            + f"*For all time:* {get_answer(all_time_avg)}\n",
            parse_mode=ParseMode.MARKDOWN,
        )
