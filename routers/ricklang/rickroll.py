from fastapi import APIRouter
from pydantic import BaseModel

from .runner import run_code


class Code(BaseModel):
    code : str
    language : str


rickroll_lang = APIRouter()


@rickroll_lang.post("/api/ricklang")
async def run_the_code(code : Code):
    output = await run_code(code.code, code.language, await_task=True)
    return {"output":output}