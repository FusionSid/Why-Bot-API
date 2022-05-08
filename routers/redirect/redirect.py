import os

from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from dotenv import load_dotenv

from slowapi import Limiter
from slowapi.util import get_remote_address

import utils

load_dotenv()
DB_PATH = os.environ["FILE_DB"]


limiter = Limiter(key_func=get_remote_address)

tags_metadata = [
    {
        "name": "Create a redirect link",
    }
]

redirect = APIRouter()

@redirect.post("/api/redirect")
@limiter.limit("10/minute")
async def post_redirect(request: Request, url:str, file_code: str = None):
    """
    Lets you enter a url and gives you the redirect url.
    Make sure the url you give has the http:// or https:// part in it
    """
    code = await utils.insert_file_red(url, file_code)
    return {
        "code": code,
        "url": f"https://whyapi.fusionsid.xyz/r/{code}",
    }


@redirect.get("/r/{code:str}")
@limiter.limit("42/minute")
async def red(request: Request, code: str):
    """
    Redirect to url using code
    """
    db_data = await utils.get_redirect(code)

    if db_data == False or len(db_data) == 0:
        return {"error": "File not found"}

    if "http://" in db_data[1] or "https://" in db_data[1]:
        pass
    else:
        db_data = list(db_data)
        db_data[1] = f"http://{db_data[1]}"

    return RedirectResponse(str(db_data[1]))