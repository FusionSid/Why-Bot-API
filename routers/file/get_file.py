from io import BytesIO

from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse
from slowapi import Limiter
from slowapi.util import get_remote_address

import utils

limiter = Limiter(key_func=get_remote_address)

tags_metadata = [
    {
        "name": "Get file from db",
    }
]

get_file_endpoint = APIRouter(tags=tags_metadata)


@get_file_endpoint.get("/api/file")
@limiter.limit("42/minute")
async def getfile(request: Request, code: str):
    db_data = await utils.get_file(code)

    if db_data == False or len(db_data) == 0:
        return {"error": "File not found"}

    file = BytesIO(db_data[4])
    file.seek(0)

    file_type = db_data[3].lower()

    if file_type == "png":
        return StreamingResponse(file, media_type="image/png")
    if file_type == "jpeg":
        return StreamingResponse(file, media_type="image/jpg")
    if file_type == "txt":
        return StreamingResponse(file, media_type="image/plain")
    if file_type == "mp4":
        return StreamingResponse(file, media_type="video/mp4")
    if file_type == "gif":
        return StreamingResponse(file, media_type="image/gif")
    if file_type == "mp3":
        return StreamingResponse(file, media_type="audio/mpeg")

    else:
        return {"error": "Incorrect file type"}
