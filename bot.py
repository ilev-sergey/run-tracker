import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config_reader import config
from filters.chat_type import ChatTypeFilter
from handlers import activity, control, stats, stopwatch, utc_offset


async def main():
    logging.basicConfig(level=logging.INFO)

    bot = Bot(token=config.bot_token.get_secret_value())

    dp = Dispatcher(storage=MemoryStorage())
    dp.message.filter(ChatTypeFilter(chat_type=["private", "group", "supergroup"]))
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
