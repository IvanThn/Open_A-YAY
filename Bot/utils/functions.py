import io
import os
import cv2
import numpy as np

from ultralytics import YOLO
from aiogram.types import Message, FSInputFile

from Bot.db.requests import select_signs


async def img_process(msg: Message) -> dict[str, list]:
    bot = msg.bot
    file_id = msg.photo[-1].file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path
    bytes_io = io.BytesIO()
    await bot.download_file(file_path, bytes_io)
    bytes_io.seek(0)
    img_arr = np.frombuffer(bytes_io.read(), dtype=np.uint8)
    img = cv2.imdecode(img_arr, cv2.IMREAD_COLOR)
    model = YOLO('D:\\PyProjects\\Open_A-YAY\\best.pt')
    results = model.predict(
        source=img,
        #  show=True,
        save=True,
        show_labels=True,
        show_conf=True,
        name="res",
        conf=0.25,
        agnostic_nms=True,
    )
    data = {'paths': [], 'id': []}
    for res in results:
        data['paths'].append(f'{res.save_dir}\\{res.path}')
        for i in res.boxes.cls:
            data['id'].append(model.names[int(i.item())].replace('_', '.'))
    return data


async def send_processed_img(msg: Message) -> None:
    data = await img_process(msg)
    paths = data['paths']
    signs_id = data['id']
    for path in paths:
        signs = await select_signs(signs_id)
        text = ''
        for sign in signs:
            text += f'- ({sign.id}) {sign.name}\n'
        await msg.answer_photo(FSInputFile(path), caption=text)
        os.remove(path)
        os.rmdir(path[:path.rfind('\\')])
