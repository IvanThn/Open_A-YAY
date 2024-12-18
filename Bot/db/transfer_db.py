from Bot.db.requests import transfer_db
import codecs
import asyncio


async def transfer():
    f = codecs.open('D:/PyProjects/Open_A-YAY/Bot/db/tr_sg.txt', 'r', "utf_8_sig")
    for line in f.read().split('||'):
        l = line.split('|')
        if l is None:
            continue
        id = l[0].strip()
        name = l[1].strip()
        about = l[2].strip()
        await transfer_db(id, name, about)
    f.close()
