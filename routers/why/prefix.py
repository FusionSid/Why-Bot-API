import os

import aiosqlite
from fastapi import APIRouter
from dotenv import load_dotenv

why_bot_endpoint = APIRouter(tags=[{"name":"Get guild prefix"}])

load_dotenv()

WHY_DB = os.environ["WHY_BOT_DB"]

@why_bot_endpoint.get("/api/get-prefix")
async def get_prefix(guild_id:int):
    async with aiosqlite.connect(WHY_DB) as db:
        cur = await db.execute("SELECT * FROM Prefix WHERE guild_id=?", (guild_id,))
        prefix = await cur.fetchall()

        if len(prefix) == 0:
            prefix = "?"
            await db.execute("INSERT INTO Prefix (guild_id, prefix) VALUES (?, ?)", (guild_id, prefix))
            await db.commit()
        else:
            prefix = prefix[0][1]
    
    return {
        "prefix": prefix
    }