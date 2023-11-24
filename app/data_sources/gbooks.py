from aiohttp import ClientSession
import asyncio
from typing import List
from datetime import datetime

from .models import Book, BookQuery 

API_URI = "https://www.googleapis.com/books/v1"


async def search_volumes(session: ClientSession, query: BookQuery) -> dict:
    query_list = []
    if query.author:
        query_list.append("inauthor:" + query.author)
    if query.title:
        query_list.append("intitle:" + query.title)
    if not len(query_list):
        raise ValueError("Not enough data to perform search")
    query_str = "+".join(query_list) 

    params = {"q": query_str}
    async with session.get(API_URI + "/volumes", params=params) as resp:
        data = await resp.json()
    items = data.get("items", [])
    vols = [it["volumeInfo"] for it in items]
    return vols


async def get_books(query: BookQuery) -> List[Book]:
    async with ClientSession() as session:
        results = await search_volumes(session, query)

    books = []
    for res in results:
        published = res.get("publishedDate")
        if published and len(published) != 4:
            try:
                published = datetime.fromisoformat(published).year
            except ValueError:
                raise RuntimeError(
                    f"Failed to get year from date '{published}'"
                )
        book = Book(
            source="FantLab",
            title=res["title"],
            authors=res["authors"],
            description=res.get("description"),
            published_year=published,
            poster=res.get("thumbnail")
        )
        books.append(book)
    return books


if __name__ == "__main__":
    query = BookQuery(
        author="Сандерсон"
    )
    books = asyncio.run(get_books(query))
    for book in books:
        print(book)
