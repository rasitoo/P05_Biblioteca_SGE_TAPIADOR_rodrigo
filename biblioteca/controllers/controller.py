from datetime import date

from biblioteca.models.user import User
from biblioteca.models.book import Book
from biblioteca.models.loan import Loan
from biblioteca.repositories.repository import Repositories

class Controller:
    def __init__(self, db: Repositories):
        self.repo = db

    def add_user(self, dni: str, name: str, email: str, phone: str, address: str):
        if not dni:
            raise ValueError("El DNI no puede estar vacío")
        user = User(dni=dni, name=name, email=email, phone=phone, address=address)
        self.repo.add_user(user)

    def remove_user(self, dni: str):
        if not dni:
            raise ValueError("El DNI no puede estar vacío")
        self.repo.remove_user(dni)

    def add_book(self, isbn: str, title: str, author: str, genre: str, cover_uri: str, synopsis: str, copies: int):
        if not isbn:
            raise ValueError("El ISBN no puede estar vacío")
        if copies == "":
            copies = None
        else:
            try:
                copies = int(copies)
            except ValueError:
                raise ValueError("Las copias deben ser un número")
        book = Book(isbn=isbn, title=title, author=author, genre=genre, cover_uri=cover_uri, synopsis=synopsis, copies=copies)
        self.repo.add_book(book)

    def remove_book(self, isbn: str):
        if not isbn:
            raise ValueError("El ISBN no puede estar vacío")
        self.repo.remove_book(isbn)

    def lend_book(self, isbn: str, dni: str):
        if not isbn:
            raise ValueError("El ISBN no puede estar vacío")
        if not dni:
            raise ValueError("El DNI no puede estar vacío")
        user = self.repo.get_user_by_dni(dni)
        book = self.repo.get_book_by_isbn(isbn)
        loan = Loan(book=book, user=user, loan_date=date.today())
        self.repo.lend_book(loan)

    def return_book(self, isbn: str):
        if not isbn:
            raise ValueError("El ISBN no puede estar vacío")
        book = self.repo.get_book_by_isbn(isbn)
        if not book:
            raise ValueError("El libro no existe")
        self.repo.return_book(book.id)

    def list_books(self):
        books = self.repo.list_books()
        loans = self.repo.list_loans()
        loan_dict = {loan.book_id: loan for loan in loans}
        result = []
        for book in books:
            result.append(f"ID:{book.id} ISBN:{book.isbn} Título:{book.title} Autor:{book.author} Género:{book.genre} Portada:{book.cover_uri} Sinopsis:{book.synopsis} Copias:{book.copies} ")
            loan_info = loan_dict.get(book.id)
            if loan_info:
                user = self.repo.get_user_by_id(loan_info.user_id)
                result.append(f"\tPrestado a: (Usuario:{user.id} DNI:{user.dni} Nombre:{user.name} Email:{user.email} tlf:{user.phone} dirección:{user.address}) ")
            else:
                result.append("\tDisponible")
        return result

    def list_users(self):
        users = self.repo.list_users()
        loans = self.repo.list_loans()
        loan_dict = {loan.user_id: loan for loan in loans}
        result = []
        for user in users:
            result.append(f"Usuario:{user.id} DNI:{user.dni} Nombre:{user.name} Email:{user.email} tlf:{user.phone} dirección:{user.address} ")
            loan_info = loan_dict.get(user.id)
            if loan_info:
                book = self.repo.get_book_by_id(loan_info.book_id)
                result.append(f"\tPrestado: {book.title} (ISBN: {book.isbn}, ID: {book.id})")
            else:
                result.append(f"\tSin préstamos")
        return result

    def list_loans(self):
        result = []
        for loan in self.repo.list_loans():
            result.append(f"Libro: (ID:{loan.book_id}) prestado a: (Usuario:{loan.user_id})")
        return result