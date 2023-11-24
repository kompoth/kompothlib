from pydantic import BaseModel, HttpUrl, field_validator
from typing import List, Annotated


class BookQuery(BaseModel):
    title: str | None = None
    author: str | None = None


class Book(BaseModel):
    source: str
    title: str
    authors: List[str] | str
    published_year: str | int | None = None
    poster: HttpUrl | None = None
    description: str | None = None
    
    @field_validator("published_year")
    def check_year(cls, year):
        if year is None:
            return None
        if not isinstance(year, str):
            year = str(year)
        assert len(year) == 4
        return year


if __name__ == "__main__":
    book = Book(
        source="manual",
        title="Сплав закона",
        authors="Брэндон Сандерсон",
        published_year="2017",
        description="test",
        poster="https://fantlab.ru/images/editions/orig/190247?r=1492536245"
    )
