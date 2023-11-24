from fastapi import FastAPI
from typing import List
import asyncio

from app.models import BookQuery, Book
from app.data_sources.fantlab import fantlab_get_books
from app.data_sources.gbooks import gbooks_get_books

app = FastAPI()


@app.post("/bookquery")
async def index(query: BookQuery) -> List[Book]:
    tasks = [fantlab_get_books(query), gbooks_get_books(query)]
    results = await asyncio.gather(*tasks)
    results = [item for task in results for item in task]
    return results
