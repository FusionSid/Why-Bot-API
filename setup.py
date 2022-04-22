import asyncio

import aiosqlite

db1 = input("ENTER DB PATH FOR WHY BOT: ")
db2 = input("ENTER DB PATH FOR FILE HOST: ")

with open(".env", 'w') as f:
    f.write("WHY_BOT_DB = {}".format(db1))
    f.write("\n")
    f.write("FILE_DB = {}".format(db2))

async def main():
    async with aiosqlite.connect(db2) as db:
        await db.execute("""CREATE TABLE Files (
            file_id INTEGER PRIMARY KEY AUTOINCREMENT,
            time_added INTEGER,
            file_code TEXT,
            file_type TEXT,
            file_data BLOB
            )""")

asyncio.run(main())