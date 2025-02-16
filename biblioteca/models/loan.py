#Información de como hacer un many-to-many con campos extra en sqlmodel sacada de https://sqlmodel.tiangolo.com/tutorial/many-to-many/link-with-extra-fields/
from typing import Optional

from sqlmodel import Field, SQLModel, Relationship
from datetime import date



class Loan(SQLModel, table=True):
    user_id: int | None = Field(default=None, foreign_key="user.id", primary_key=True)
    book_id: int | None = Field(default=None, foreign_key="book.id", primary_key=True)
    loan_date: Optional[date] = date.today()
    return_date: date | None = None

    book: "Book" = Relationship(back_populates="loans") #Aunque avise de hacer el import mejor no hacerlo porque se producen imports en bucle
    user: "User" = Relationship(back_populates="loans")