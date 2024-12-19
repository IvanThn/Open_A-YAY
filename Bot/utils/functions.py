import io
import os
import cv2
import numpy as np
import requests

from moviepy import VideoFileClip
from ultralytics import YOLO
from aiogram.types import Message, FSInputFile

from Bot.db.requests import select_signs


TOKEN = os.getenv('TOKEN')


async def processing(files: list[str] | str, files_type: str = 'photo') -> dict[str, list | str]:
    model = YOLO('D:\\PyProjects\\Open_A-YAY\\YOLOv8epoch20.pt')
    results = model.predict(
        source=files,
        #  show=True,
        save=True,
        show_labels=True,
        show_conf=True,
        name="res",
        conf=0.25,
        agnostic_nms=True,
        # stream=True,
    )
    if files_type == 'photo':
        dir_path = f'results[0].save_dir\\{results[0].path}'
    else:
        dir_path = f'D:\\PyProjects\\Open_A-YAY\\runs\\detect\\res\\{files[files.rfind('/')+1:files.rfind('.')]}.avi'
        os.remove(results[0].path)
    data = {'id': [], 'path': dir_path}
    for res in results:
        for t in res.boxes.cls:
            data[f'id'].append(model.names[int(t.item())].replace('_', '.'))
    print(set(data['id']), data['path'])
    return data


async def img_process(msg: Message) -> dict[str, list | str]:
    bot = msg.bot
    file_id = msg.photo[-1].file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path
    bytes_io = io.BytesIO()
    await bot.download_file(file_path, bytes_io)
    bytes_io.seek(0)
    img_arr = np.frombuffer(bytes_io.read(), dtype=np.uint8)
    img = cv2.imdecode(img_arr, cv2.IMREAD_COLOR)
    data = await processing(img)
    return data


async def send_processed_video(msg: Message) -> None:
    file_id = [msg.document.file_id if msg.document else msg.video.file_id][0]
    file_path = requests.get(
        f'https://api.telegram.org/bot{TOKEN}/getFile?file_id={file_id}'
    ).json()['result']['file_path']
    file = f'https://api.telegram.org/file/bot{TOKEN}/{file_path}'
    data = await processing(file, 'video')
    path = data['path']
    try:
        signs_id = data['id']
        avi_video = VideoFileClip(path)
        avi_video.write_videofile(path[:path.rfind('.')] + '.mp4')
        os.remove(path)
        path = path[:path.rfind('.')] + '.mp4'
        signs = await select_signs(signs_id)
        text = ''
        for sign in signs:
            text += f'- ({sign.id}) {sign.name}\n'
        await msg.answer_video(FSInputFile(path), caption=text)
        os.remove(path)
        os.rmdir(path[:path.rfind('\\')])
    except Exception as e:
        print(e)
        os.remove(path)
        os.rmdir(path[:path.rfind('\\')])


async def send_processed_img(msg: Message) -> None:
    data = await img_process(msg)
    path = data['path']
    signs_id = data['id']
    signs = await select_signs(signs_id)
    text = ''
    for sign in signs:
        text += f'- ({sign.id}) {sign.name}\n'
    await msg.answer_photo(FSInputFile(path), caption=text)
    os.remove(path)
    os.rmdir(path[:path.rfind('\\')])
