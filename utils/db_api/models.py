from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel, Field


class Article(SQLModel, table=True):
    pk: Optional[int] = Field(default=None, primary_key=True)
    id: int
    url: str
    title: str
    date: datetime
    author: str
    event: Optional[str]
    place: str
    fragment: Optional[str]
