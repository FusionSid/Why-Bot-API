import os
import time
import asyncio

from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

import uvicorn 
import aiosqlite
from dotenv import load_dotenv

import utils
import routers 

load_dotenv()
DB_PATH = os.environ["FILE_DB"]

description = """
This API is for me to use Why-Bot
This api is mainly for me to use for the why bot dashboard

This also contains the file host api
You can upload files and use a code to get them later

Supported file types: png, txt, jpeg, gif, mp4, mp3

Contact: Discord: FusionSid#3645
"""

app = FastAPI(
    title="Why Bot API",
    description=description,
    license_info={
        "name": "MIT LICENCE",
        "url": "https://opensource.org/licenses/MIT",
    },
)

app.state.limiter = Limiter(key_func=get_remote_address)
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


@app.get("/")
async def home():
    return RedirectResponse("/docs")


async def loop_cleanup():
    # Deletes all files that have been in the db for more than 24h
    delete_interval = 86_400 # seconds

    # Checks every 6 hours
    check_every = 21_600 # seconds

    while True:
        time_right_now = int(time.time())
        data = await utils.get_full_db()
        for file in data:
            time_added = file[1]
            if (time_right_now - time_added) > delete_interval:
                async with aiosqlite.connect(DB_PATH) as db:
                    await db.execute("DELETE FROM Files WHERE file_id=? and file_code=?", (file[0], file[2],))
                    await db.commit()
                    await db.execute("VACUUM")

        await asyncio.sleep(check_every)


app.include_router(routers.why_bot_endpoint)
app.include_router(routers.get_file_endpoint)
app.include_router(routers.upload_file_endpoint)
app.include_router(routers.file_stats_endpoint)


@app.on_event("startup")
async def startup():
    loop = asyncio.get_event_loop()
    loop.create_task(loop_cleanup())

if __name__ == "__main__":
    uvicorn.run(app, reload=False, host="0.0.0.0", port=443, ssl_keyfile="./key.pem", ssl_certfile="./cert.pem")
