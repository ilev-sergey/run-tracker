import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, F
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv

from handlers import activity, control, stats, stopwatch, utc_offset


async def main():
    logging.basicConfig(level=logging.INFO)

    load_dotenv()
    bot = Bot(token=os.environ["TOKEN"])

    dp = Dispatcher(storage=MemoryStorage())
    dp.message.filter(
        F.chat.type.in_({"private", "group", "supergroup"}),
        F.from_user,
        F.text,
    )
    dp.include_routers(
        control.router,
        utc_offset.router,
        stats.router,
        activity.router,
        stopwatch.router,
    )

    # await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    asyncio.run(main())
