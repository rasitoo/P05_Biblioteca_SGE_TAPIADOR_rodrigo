from typing import Optional
from sqlmodel import Field, SQLModel, Relationship
from biblioteca.models.loan import Loan

class Book(SQLModel, table=True):
    id : Optional[int] = Field(default=None, primary_key=True)
    isbn: str = Field(unique=True)
    title: Optional[str] = "Unknown"
    author: Optional[str] = "Unknown"
    genre: Optional[str] = "Unknown"
    cover_uri: Optional[str] = "Unknown"
    synopsis: Optional[str] = "Unknown"
    copies: Optional[int] = 0
    loans: list[Loan] = Relationship(back_populates="book")