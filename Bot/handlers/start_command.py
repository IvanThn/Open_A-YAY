from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart

rt = Router()


@rt.message(CommandStart())
async def start_message(msg: Message):
    await msg.answer('Hello, world!')
    await msg.delete()
