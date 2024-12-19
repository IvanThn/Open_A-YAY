from aiogram import Router, F
from aiogram.types import Message

from Bot.utils.functions import send_processed_img, send_processed_video

rt = Router()


@rt.message(F.photo)
async def photo(msg: Message):
    await send_processed_img(msg)


@rt.message(F.content_type.in_({'video', 'document'}))
async def photo(msg: Message):
    temp_msg = await msg.answer('Выполняется обработка...')
    try:
        await send_processed_video(msg)
        await temp_msg.delete()
    except Exception as e:
        print(e)
        await temp_msg.delete()
        await msg.answer('Что-то пошло не так...')
