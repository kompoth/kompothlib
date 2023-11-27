from aiohttp import ClientSession
from typing import List
from datetime import datetime
import logging
from pydantic import ValidationError

from app.models import Book, BookQuery
from app.utils import extract_year

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


async def gbooks_search(query: BookQuery) -> List[Book]:
    async with ClientSession() as session:
        results = await search_volumes(session, query)

    books = []
    for res in results:
        published = res.get("publishedDate")
        if published:
            published = extract_year(published)
        try:
            book = Book(
                source="Google Books",
                title=res["title"],
                authors=res["authors"],
                description=res.get("description"),
                published=published,
                poster=res.get("imageLinks", {}).get("thumbnail"),
            )
            books.append(book)
        except (KeyError, ValidationError) as err:
            logging.warning(
                f"Failed to handle '{res.get('title')}': " + str(err)
            )
    return books
