from aiohttp import ClientSession
import asyncio
from typing import List

from app.models import Book, BookQuery

API_URI = "https://api.fantlab.ru"
MAIN_URI = "https://fantlab.ru"
IGNORE = ("cycle", "review", "other")
MAX_WORKS = 10


async def search_works(session: ClientSession, query: BookQuery) -> dict:
    query_list = [val for val in query.model_dump().values() if val]
    query_str = "+".join(query_list)
    params = {"q": query_str, "page": 1, "onlymatches": 0}

    async with session.get(API_URI + "/search-works", params=params) as resp:
        data = await resp.json()
    works = data["matches"]
    work_ids = [
        str(work["work_id"]) for work in works
        if work["name_eng"] not in IGNORE
    ][:MAX_WORKS]
    return work_ids


async def get_works(session: ClientSession, work_id: str) -> dict:
    async with session.get(API_URI + "/work/" + work_id) as resp:
        data = await resp.json()
    return data


async def fantlab_search(query: BookQuery) -> List[Book]:
    async with ClientSession() as session:
        work_ids = await search_works(session, query)
        tasks = [get_works(session, work_id) for work_id in work_ids]
        results = await asyncio.gather(*tasks)

    books = []
    for res in results:
        poster = res.get("image")
        poster = None if poster is None else MAIN_URI + poster
        book = Book(
            source="FantLab",
            title=res["work_name"],
            authors=[au["name"] for au in res["authors"]],
            description=res.get("work_description"),
            poster=poster,
            published=res.get("work_year"),
        )
        books.append(book)
    return books
