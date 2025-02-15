from datetime import date

from sqlmodel import Session, select
from biblioteca.models.user import User
from biblioteca.models.book import Book
from biblioteca.models.loan import Loan
from biblioteca.database import Database

class Repositories:
    def __init__(self, db_name: str):
        self.db = Database(db_name)
        self.db.init_db()

    def add_user(self, user: User):
        with Session(self.db.engine) as session:
            session.add(user)
            session.commit()

    def remove_user(self, dni: str):
        with Session(self.db.engine) as session:
            user = session.exec(select(User).where(User.dni == dni)).one()
            session.delete(user)
            session.commit()

    def update_user(self, user: User):
        with Session(self.db.engine) as session:
            existing_user = session.exec(select(User).where(User.id == user.id)).one()
            existing_user.dni = user.dni
            existing_user.name = user.name
            existing_user.email = user.email
            existing_user.phone = user.phone
            existing_user.address = user.address
            session.add(existing_user)
            session.commit()

    def add_book(self, book: Book):
        with Session(self.db.engine) as session:
            session.add(book)
            session.commit()

    def remove_book(self, isbn: str):
        with Session(self.db.engine) as session:
            book = session.exec(select(Book).where(Book.isbn == isbn)).one()
            session.delete(book)
            session.commit()

    def lend_book(self, loan: Loan):
        with Session(self.db.engine) as session:
            session.add(loan)
            session.commit()


    def return_book(self, id: int):
        with Session(self.db.engine) as session:
            loan = session.exec(select(Loan).where(Loan.book_id == id, Loan.return_date == None)).one()
            session.delete(loan)
            session.commit()

    def update_book(self, book: Book):
        with Session(self.db.engine) as session:
            existing_book = session.exec(select(Book).where(Book.id == book.id)).one()
            existing_book.title = book.title
            existing_book.author = book.author
            existing_book.genre = book.genre
            existing_book.cover_uri = book.cover_uri
            existing_book.synopsis = book.synopsis
            existing_book.copies = book.copies
            session.add(existing_book)
            session.commit()
    def list_books(self):
        with Session(self.db.engine) as session:
            return session.exec(select(Book)).all()

    def list_users(self):
        with Session(self.db.engine) as session:
            return session.exec(select(User)).all()

    def list_loans(self):
        with Session(self.db.engine) as session:
            return session.exec(select(Loan)).all()

    def get_user_by_id(self, user_id: str):
        with Session(self.db.engine) as session:
            return session.exec(select(User).where(User.id == user_id)).one()

    def get_book_by_id(self, book_id: str):
        with Session(self.db.engine) as session:
            return session.exec(select(Book).where(Book.id == book_id)).one()

    def get_user_by_dni(self, dni: str):
        with Session(self.db.engine) as session:
            return session.exec(select(User).where(User.dni == dni)).one()

    def get_book_by_isbn(self, isbn: str):
        with Session(self.db.engine) as session:
            return session.exec(select(Book).where(Book.isbn == isbn)).one()