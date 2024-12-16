import asyncio
import datetime
import os

from aiogram import Bot, Dispatcher
from aiogram.client.bot import DefaultBotProperties
from dotenv import load_dotenv

from handlers import start_command


async def main():
    load_dotenv()
    #  session = AiohttpSession(proxy=os.getenv('PROXY'))
    bot = Bot(token=os.getenv('TOKEN'), default=DefaultBotProperties(parse_mode='HTML'))
    dp = Dispatcher()
    dp.include_routers(start_command.rt)
    print(f'Bot online at {datetime.datetime.now()}')
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f'Bot offline at {datetime.datetime.now()}')
