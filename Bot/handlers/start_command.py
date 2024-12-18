from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart

from Bot.db.requests import insert_user

rt = Router()


@rt.message(CommandStart())
async def start_message(msg: Message):
    await insert_user(msg.from_user.id, msg.from_user.first_name)
    await msg.answer(
        f'👋Привет, {msg.from_user.first_name}! Это бот для распознавания дорожных знаков \n\n🤖Этот бот создан '
        f'специально для того, чтобы помогать водителям и пешеходам лучше ориентироваться в дорожной инфраструктуре. '
        f'Просто отправьте ему фотографию или видео с дорожными знаками, и он выделит все найденные знаки '
        f'прямо на изображении, а также предоставит их подробное описание. \n\nНаш бот станет вашим '
        f'надежным помощником на дороге, помогая избежать недоразумений и повышая безопасность движения. '
        f'Попробуйте прямо сейчас – просто пришлите фото или видео с дорожными знаками!'
    )
    await msg.delete()
