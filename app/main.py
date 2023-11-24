from fastapi import FastAPI, Request
from pydantic import BaseModel

from app.models import BookQuery
from app.data_sources.gbooks import get_books

app = FastAPI()


@app.post("/bookquery")
async def index(query: BookQuery):
    return await get_books(query)
