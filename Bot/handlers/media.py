from aiogram import Router, F
from aiogram.types import Message

# from Bot.utils.functions import send_processed_img

rt = Router()


@rt.message(F.photo)
async def photo(msg: Message):
    # await send_processed_img(msg)
    await msg.answer_photo(msg.photo[-1].file_id)


@rt.message(F.video)
async def photo(msg: Message):
    await msg.answer_video(msg.video.file_id)
