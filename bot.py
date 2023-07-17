import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config_reader import config


async def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=config.bot_token.get_secret_value())

    dp = Dispatcher(storage=MemoryStorage())

    # await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    asyncio.run(main())
