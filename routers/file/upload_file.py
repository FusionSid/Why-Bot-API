from fastapi import APIRouter, UploadFile, Request
from slowapi import Limiter
from slowapi.util import get_remote_address

import utils

limiter = Limiter(key_func=get_remote_address)

tags_metadata = [
    {
        "name": "Upload file",
    }
]

upload_file_endpoint = APIRouter(tags=tags_metadata)


@upload_file_endpoint.post("/api/upload")
@limiter.limit("42/minute")
async def post_upload(
    request: Request, file: UploadFile, file_type: str, file_code: str = None
):
    if len(file_code) > 10:
        file_code = None
        
    if file_type.lower() not in ["png", "txt", "jpeg", "gif", "mp4", "mp3"]:
        return {
            "error": "Must include file type, Options: png, txt, jpeg, gif, mp4, mp3]"
        }

    file = await file.read()
    if len(file) > 15000000:
        return {"error": "File to large, Max size 15mb"}

    code = await utils.insert_file(bytes(file), file_type, file_code)
    return {
        "code": code,
        "url": f"https://whyapi.fusionsid.xyz/api/file?code={code}",
    }
