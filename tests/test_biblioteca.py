from unittest.mock import patch

import pytest
from sqlmodel import Session, create_engine, SQLModel
from biblioteca.models.book import Book
from biblioteca.models.loan import Loan
from biblioteca.models.user import User
from biblioteca.repositories.repository import Repositories as repo
from biblioteca.controllers.controller import Controller as clr
from biblioteca.views.view import menu


# Configuración de la base de datos para pruebas
@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    with (Session(engine) as session):
        yield session


# Test para el modelo Book
def test_create_book(session):
    book = Book(isbn="1234567890", title="El Quijote", author="Miguel de Cervantes")
    session.add(book)
    session.commit()
    session.refresh(book)
    assert book.id is not None
    assert book.title == "El Quijote"
    assert book.author == "Miguel de Cervantes"

# Test para la relación entre Book y Loan
def test_book_loan_relationship(session):
    user = User(dni="12345678X", name="Juan Pérez", email="juan.perez@example.com")
    book = Book(isbn="1234567890", title="El Quijote", author="Miguel de Cervantes")
    session.add(user)
    session.add(book)
    loan = Loan(user=user, book=book)
    session.add(loan)
    session.commit()
    session.refresh(book)
    assert len(book.loans) == 1
    assert book.loans[0] == loan

# Test para el repositorio BookRepository
def test_book_repository():
    repository = repo("ejem1.db")
    book = Book(isbn="1234567890", title="El Quijote", author="Miguel de Cervantes")

    existing_book = repository.get_book(1)
    if not existing_book:
        repository.add_book(book)

    retrieved_book = repository.get_book(1)
    assert retrieved_book is not None
    assert retrieved_book.title == "El Quijote"

# Test para el controlador BookController
def test_book_controller():
    repository = repo("ejem2.db")
    controller = clr(repository)
    controller.add_book(
        isbn="1234567890",
        title="El Quijote",
        author="Miguel de Cervantes",
        genre="Novela",
        cover_uri="http://example.com/cover.jpg",
        synopsis="Una novela clásica de la literatura española."
    )
    retrieved_book = repository.get_book(id=1)
    assert retrieved_book is not None
    assert retrieved_book.title == "El Quijote"

# Test para crear un préstamo
def test_create_loan(session):
    user = User(dni="12345678X", name="Juan Pérez", email="juan.perez@example.com")
    book = Book(isbn="1234567890", title="El Quijote", author="Miguel de Cervantes")
    loan = Loan(user=user, book=book)
    session.add(user)
    session.add(book)
    session.add(loan)
    session.commit()
    session.refresh(loan)
    assert loan.user_id == user.id
    assert loan.book_id == book.id

# Test para la relación entre Loan y User
def test_loan_user_relationship(session):
    user = User(dni="12345678X", name="Juan Pérez", email="juan.perez@example.com")
    book = Book(isbn="1234567890", title="El Quijote", author="Miguel de Cervantes")
    loan = Loan(user=user, book=book)
    session.add(user)
    session.add(book)
    session.add(loan)
    session.commit()
    session.refresh(user)
    assert len(user.loans) == 1
    assert user.loans[0] == loan

# Test para la devolución de un libro
def test_return_book():
    repository = repo("ejem4.db")
    controller = clr(repository)
    user = User(dni="12345678X", name="Juan Pérez", email="juan.perez@example.com", phone="123456789", address="Calle Falsa 123")
    book = Book(isbn="1234567890", title="El Quijote", author="Miguel de Cervantes")
    try:
        controller.add_user(dni=user.dni, name=user.name, email=user.email, phone=user.phone, address=user.address)
        controller.add_book(isbn=book.isbn, title=book.title, author=book.author, genre="Novela", cover_uri="http://example.com/cover.jpg", synopsis="Una novela clásica de la literatura española.")
    except Exception as e:
        print(e)
    controller.lend_book(isbn=book.isbn, dni=user.dni)
    loans = repository.list_loans()
    assert loans
    controller.return_book(book.isbn)
    loans = repository.list_loans()
    assert not loans

# Test para crear un usuario
def test_create_user(session):
    repository = repo("ejem5.db")
    user = User(dni="12345678X", name="Juan Pérez", email="juan.perez@example.com", phone="123456789", address="Calle Falsa 123")
    try:
        repository.add_user(user)
    except Exception as e:
        print(e)
    user = repository.get_user(1)
    assert user.id is not None
    assert user.name == "Juan Pérez"
    assert user.email == "juan.perez@example.com"

# Test para actualizar la información de un usuario
def test_update_user(session):
    user = User(dni="12345678X", name="Juan Pérez", email="juan.perez@example.com", phone="123456789", address="Calle Falsa 123")
    session.add(user)
    session.commit()
    session.refresh(user)
    user.name = "Juan P. Pérez"
    session.commit()
    session.refresh(user)
    assert user.name == "Juan P. Pérez"

# Test para eliminar un usuario
def test_delete_user(session):
    user = User(dni="12345678X", name="Juan Pérez", email="juan.perez@example.com", phone="123456789", address="Calle Falsa 123")
    session.add(user)
    session.commit()
    session.refresh(user)
    session.delete(user)
    session.commit()
    deleted_user = session.get(User, user.id)
    assert deleted_user is None
