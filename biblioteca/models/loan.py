#Información de como hacer un many-to-many con campos extra en sqlmodel sacada de https://sqlmodel.tiangolo.com/tutorial/many-to-many/link-with-extra-fields/

from sqlmodel import Field, SQLModel, Relationship
from datetime import date

from biblioteca.models.book import Book
from biblioteca.models.user import User


class Loan(SQLModel, table=True):
    user_id: int | None = Field(default=None, foreign_key="user.id", primary_key=True)
    book_id: int | None = Field(default=None, foreign_key="book.id", primary_key=True)
    loan_date: date | None = date.today()
    return_date: date | None = None

    book: Book = Relationship(back_populates="loans")
    user: User = Relationship(back_populates="loans")