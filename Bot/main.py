import asyncio
import datetime
import os

from aiogram import Bot, Dispatcher
from aiogram.client.bot import DefaultBotProperties
from dotenv import load_dotenv

from db.ORM import async_main
from db.transfer_db import transfer
from handlers import start_command, media, slash_commands


async def main():
    load_dotenv()
    await async_main()
    #  await transfer()
    bot = Bot(token=os.getenv('TOKEN'), default=DefaultBotProperties(parse_mode='HTML'))
    dp = Dispatcher()
    dp.include_routers(start_command.rt, media.rt, slash_commands.rt)
    print(f'Bot online at {datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")}')
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f'Bot offline at {datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")}')
