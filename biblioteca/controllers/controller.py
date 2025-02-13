from biblioteca.models.user import User
from biblioteca.models.book import Book
from biblioteca.models.loan import Loan
from biblioteca.database import Database
from datetime import date

class Controller:
    def __init__(self, db_name):
        self.db = Database(db_name)

    def add_user(self, dni, name, email, number, address):
        user = User(dni=dni, name=name, email=email, number=number, address=address)
        self.db.execute("INSERT INTO users (dni, name, email, number, address) VALUES (?, ?, ?, ?, ?)",
                        (user.dni, user.name, user.email, user.number, user.address))

    def remove_user(self, dni):
        self.db.execute("DELETE FROM users WHERE dni = ?", (dni,))

    def add_book(self, isbn, title, author, genre, cover_uri, synopsis, copies):
        book = Book(isbn=isbn, title=title, author=author, genre=genre, cover_uri=cover_uri, synopsis=synopsis, copies=copies)
        self.db.execute("INSERT INTO books (isbn, title, author, genre, cover_uri, synopsis, copies) VALUES (?, ?, ?, ?, ?, ?, ?)",
                        (book.isbn, book.title, book.author, book.genre, book.cover_uri, book.synopsis, book.copies))

    def remove_book(self, isbn):
        self.db.execute("DELETE FROM books WHERE isbn = ?", (isbn,))

    def lend_book(self, isbn, dni):
        user = self.db.execute("SELECT * FROM users WHERE dni = ?", (dni,)).fetchone()
        book = self.db.execute("SELECT * FROM books WHERE isbn = ?", (isbn,)).fetchone()
        loan = Loan(user=user, book=book, loan_date=date.today())
        self.db.execute("INSERT INTO loans (user_id, book_id, loan_date) VALUES (?, ?, ?)",
                        (user['id'], book['id'], loan.loan_date))

    def return_book(self, isbn):
        self.db.execute("UPDATE loans SET return_date = ? WHERE book_id = ? AND return_date IS NULL",
                        (date.today(), isbn))

    def list_books(self):
        self.db.execute("SELECT * FROM books")
        return self.db.fetchall()

    def list_users(self):
        self.db.execute("SELECT * FROM users")
        return self.db.fetchall()