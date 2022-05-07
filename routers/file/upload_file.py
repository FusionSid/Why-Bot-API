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
@limiter.limit("15/minute")
async def post_upload(
    request: Request, file: UploadFile, file_type: str, file_code: str = None
):
    """
    Lets you upload a file
    Max size 50mb

    Supported file types: png, txt, jpeg, jpg, gif, mp4, mp3, json, bmp, html, css, csv, plain, ttf, sh, pdf, otf, svg, zip
    """
    if file_code is not None and len(file_code) > 10:
        file_code = None
    
    ftypes = ["png", "txt", "jpeg", "jpg", "gif", "mp4", "mp3", "json", "bmp", "html", "css", "csv", "plain", "ttf", "sh", "pdf", "otf", "svg", "zip"]
    if file_type.lower() not in ftypes:
        return {
            "error": "Must include valid file type",
            "options": ", ".join(ftypes)
        }

    file = await file.read()
    if len(file) > 50000000:
        return {"error": "File to large, Max size 50mb"}

    code = await utils.insert_file(bytes(file), file_type, file_code)
    return {
        "code": code,
        "url": f"https://whyapi.fusionsid.xyz/api/file?code={code}",
    }
