from datetime import datetime, timedelta

from aiogram import Router
from aiogram.types import Message

from filters.stopwatch import isStopwatchMessage
from handlers.activity import _send_activity_info
from processors import database

router = Router()


@router.message(isStopwatchMessage())
async def stopwatch_message(
    message: Message, start_time: datetime, lap_times: list[timedelta]
):
    await database.add_user_data(
        user_id=message.from_user.id,
        start_time=start_time,
        lap_times=lap_times,
    )
    await _send_activity_info(message, lap_times)
