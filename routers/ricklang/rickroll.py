from fastapi import APIRouter, Request
from pydantic import BaseModel
from slowapi import Limiter
from slowapi.util import get_remote_address

from .runner import run_code

limiter = Limiter(key_func=get_remote_address)

class Code(BaseModel):
    code : str
    language : str


rickroll_lang = APIRouter()


@rickroll_lang.post("/api/ricklang")
@limiter.limit("10/minute")
async def run_the_code(request:Request, code : Code):
    output = await run_code(code.code, code.language, await_task=True)
    return {"output":output}