from fastapi import FastAPI
from typing import List
import asyncio

from app.models import BookQuery, Book
from app.data_sources import fantlab_search, gbooks_search

app = FastAPI()


@app.post("/bookquery")
async def index(query: BookQuery) -> List[Book]:
    tasks = [fantlab_search(query), gbooks_search(query)]
    results = await asyncio.gather(*tasks)
    results = [item for task in results for item in task]
    return results
