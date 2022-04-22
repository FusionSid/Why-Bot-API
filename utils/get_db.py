import os
from dotenv import load_dotenv

import aiosqlite

load_dotenv()
DB_PATH = os.environ["FILE_DB"]


async def get_file(code):
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute("SELECT * FROM Files WHERE file_code=?", (code, ))
        data = await cur.fetchall()
    try:
        return data[0]
    except IndexError:
        return False


async def get_full_db():
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute("SELECT * FROM Files")
        data = await cur.fetchall()
    return data