from io import BytesIO

from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse
from slowapi import Limiter
from slowapi.util import get_remote_address

import utils

limiter = Limiter(key_func=get_remote_address)

tags_metadata = [
    {
        "name": "Get a file",
    }
]

get_file_endpoint = APIRouter(tags=tags_metadata)


@get_file_endpoint.get("/api/file")
@limiter.limit("42/minute")
async def getfile(request: Request, code: str):
    """
    Get a file with the code
    """
    db_data = await utils.get_file(code)

    if db_data == False or len(db_data) == 0:
        return {"error": "File not found"}

    file = BytesIO(db_data[4])
    file.seek(0)

    file_type = db_data[3].lower()

    mtypes = {
        "png": "image/png",
        "txt": "text/plain",
        "jpeg": "image/jpeg",
        "jpg": "image/jpg",
        "gif": "image/gif",
        "mp4": "video/mp4",
        "mp3": "audio/mpeg",
        "json": "application/json",
        "bmp": "image/bmp",
        "csv": "text/csv",
        "plain": "text/plain",
        "ttf": "font/ttf",
        "pdf": "application/pdf",
        "otf": "font/otf",
        "svg": "image/svg+xml",
        "zip": "application/zip"
    }

    if file_type in mtypes:
        return StreamingResponse(file, media_type=mtypes[file_type])

    else:
        return {"error": "Incorrect file type"}