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
        if any(user.dni == dni for user in self.repo.list_users()):
            raise ValueError("El DNI ya existe")
        if not name:
            name = None
        if not email:
            email = None
        if not phone:
            phone = None
        if not address:
            address = None
        user = User(dni=dni, name=name, email=email, phone=phone, address=address)
        self.repo.add_user(user)

    def remove_user(self, dni: str):
        if not dni:
            raise ValueError("El DNI no puede estar vacío")
        for user in self.repo.list_users():
            if user.dni == dni:
                self.repo.remove_user(user.id)
                break
        else:
            raise Exception("No existe ningún usuario con ese dni")


    def add_book(self, isbn: str, title: str, author: str, genre: str, cover_uri: str, synopsis: str):
        if not isbn:
            raise ValueError("El ISBN no puede estar vacío")
        if not title:
            title = None
        if not author:
            author = None
        if not genre:
            genre = None
        if not cover_uri:
            cover_uri = None
        if not synopsis:
            synopsis = None
        try:
            for book in self.repo.list_books():
                if book.isbn == isbn:
                    book.copies += 1
                    self.repo.update_book(book)
                    break
            else:
                raise Exception("No existe ningún libro con ese isbn")
        except Exception as e:
            book = Book(isbn=isbn, title=title, author=author, genre=genre, cover_uri=cover_uri, synopsis=synopsis, copies=1)
            self.repo.add_book(book)

    def remove_book(self, id: int):
        if not id:
            raise ValueError("El id no puede estar vacío")
        self.repo.remove_book(id)

    def lend_book(self, isbn: str, dni: str):
        if not isbn:
            raise ValueError("El ISBN no puede estar vacío")
        if not dni:
            raise ValueError("El DNI no puede estar vacío")

        for user in self.repo.list_users():
            if user.dni == dni:
                user_loan = user
                break
        else:
            raise Exception("No existe ningún usuario con ese dni")

        for book in self.repo.list_books():
            if book.isbn == isbn:
                book_loan = book
                break
        else:
            raise Exception("No existe ningún libro con ese isbn")

        loan = Loan(book=book_loan, user=user_loan, loan_date=date.today())
        self.repo.lend_book(loan)

    def return_book(self, isbn: str):
        if not isbn:
            raise ValueError("El ISBN no puede estar vacío")
        for book in self.repo.list_books():
            if book.isbn == isbn:
                self.repo.return_book(book.id)
                break
        else:
            raise Exception("No existe ningún libro con ese isbn")

    def list_books(self):
        books = self.repo.list_books()
        loans = self.repo.list_loans()
        loan_dict = {loan.book_id: loan for loan in loans}
        result = []
        for book in books:
            result.append(f"ID:{book.id} ISBN:{book.isbn} Título:{book.title} Autor:{book.author} Género:{book.genre} Portada:{book.cover_uri} Sinopsis:{book.synopsis} Copias:{book.copies} ")
            loan_info = loan_dict.get(book.id)
            if loan_info:
                user = self.repo.get_user(loan_info.user_id)
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
                book = self.repo.get_book(loan_info.book_id)
                result.append(f"\tPrestado: {book.title} (ISBN: {book.isbn}, ID: {book.id})")
            else:
                result.append(f"\tSin préstamos")
        return result

    def list_loans(self):
        result = []
        for loan in self.repo.list_loans():
            result.append(f"Libro: (ID:{loan.book_id}) prestado a: (Usuario:{loan.user_id})")
        return result