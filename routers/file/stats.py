import os
from os import path

from fastapi import APIRouter
from dotenv import load_dotenv

from utils import get_full_db

load_dotenv()
DB_PATH = os.environ["FILE_DB"]

file_stats_endpoint = APIRouter()


@file_stats_endpoint.get("/api/stats")
async def stats():
    """
    Stats on file uploaded
    """
    db_size = path.getsize(DB_PATH)
    return {
        "files_uploaded": len((await get_full_db())),
        "db": f"{round((db_size / 1000000), 2)}mb",
    }
