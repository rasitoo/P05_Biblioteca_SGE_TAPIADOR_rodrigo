from typing import Optional
from sqlmodel import Field, SQLModel, Relationship
from biblioteca.models.loan import Loan

class User(SQLModel, table=True):
    id : Optional[int] = Field(default=None, primary_key=True)
    dni: str
    name: Optional[str] = "Unknown"
    email: Optional[str] = "Unknown"
    number: Optional[str] = "Unknown"
    address: Optional[str] = "Unknown"
    loans: list[Loan] = Relationship(back_populates="user")