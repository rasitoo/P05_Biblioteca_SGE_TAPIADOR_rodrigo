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
            try:
                session.add(user)
                session.commit()
            except Exception as e:
                session.rollback()
                raise e

    def remove_user(self, id: int):
        with Session(self.db.engine) as session:
            try:
                user = session.exec(select(User).where(User.id == id)).one_or_none()
                if user:
                    session.delete(user)
                    session.commit()
            except Exception as e:
                session.rollback()
                raise e

    def update_user(self, user: User):
        with Session(self.db.engine) as session:
            try:
                existing_user = session.exec(select(User).where(User.id == user.id)).one_or_none()
                if existing_user:
                    existing_user.dni = user.dni
                    existing_user.name = user.name
                    existing_user.email = user.email
                    existing_user.phone = user.phone
                    existing_user.address = user.address
                    session.add(existing_user)
                    session.commit()
            except Exception as e:
                session.rollback()
                raise e

    def add_book(self, book: Book):
        with Session(self.db.engine) as session:
            try:
                session.add(book)
                session.commit()
            except Exception as e:
                session.rollback()
                raise e

    def remove_book(self, id: int):
        with Session(self.db.engine) as session:
            try:
                book = session.exec(select(Book).where(Book.id == id)).one_or_none()
                if book:
                    session.delete(book)
                    session.commit()
            except Exception as e:
                session.rollback()
                raise e

    def lend_book(self, loan: Loan):
        with Session(self.db.engine) as session:
            try:
                session.add(loan)
                session.commit()
            except Exception as e:
                session.rollback()
                raise e

    def return_book(self, id: int):
        with Session(self.db.engine) as session:
            try:
                loan = session.exec(select(Loan).where(Loan.book_id == id, Loan.return_date == None)).one_or_none()
                if loan:
                    session.delete(loan)
                    session.commit()
            except Exception as e:
                session.rollback()
                raise e

    def update_book(self, book: Book):
        with Session(self.db.engine) as session:
            try:
                existing_book = session.exec(select(Book).where(Book.id == book.id)).one_or_none()
                if existing_book:
                    existing_book.title = book.title
                    existing_book.author = book.author
                    existing_book.genre = book.genre
                    existing_book.cover_uri = book.cover_uri
                    existing_book.synopsis = book.synopsis
                    existing_book.copies = book.copies
                    session.add(existing_book)
                    session.commit()
            except Exception as e:
                session.rollback()
                raise e

    def list_books(self):
        with Session(self.db.engine) as session:
            try:
                return session.exec(select(Book)).all()
            except Exception as e:
                session.rollback()
                raise e

    def list_users(self):
        with Session(self.db.engine) as session:
            try:
                return session.exec(select(User)).all()
            except Exception as e:
                session.rollback()
                raise e


    def get_user(self, id: int):
        with Session(self.db.engine) as session:
            try:
                user = session.exec(select(User).where(User.id == id)).one_or_none()
                return user
            except Exception as e:
                session.rollback()
                raise e

    def get_book(self, id: int):
        with Session(self.db.engine) as session:
            try:
                book = session.exec(select(Book).where(Book.id == id)).one_or_none()
                return book
            except Exception as e:
                session.rollback()
                raise e

    def list_loans(self):
        with Session(self.db.engine) as session:
            try:
                return session.exec(select(Loan)).all()
            except Exception as e:
                session.rollback()
                raise e