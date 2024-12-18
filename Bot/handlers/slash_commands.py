from aiogram import Router
from aiogram.types import Message
from aiogram.filters.command import Command


rt = Router()


@rt.message(Command('about'))
async def about(msg: Message):
    await msg.answer('ABOUT')
    await msg.delete()
