import pytest
from admin.models import Book, User, BorrowedBook
from datetime import datetime, timedelta

def test_book_model(app):
    book = Book(
        title="Test Book",
        publisher="Test Publisher",
        category="Test Category",
        is_available=True
    )
    assert book.title == "Test Book"
    assert book.publisher == "Test Publisher"
    assert book.category == "Test Category"
    assert book.is_available == True

def test_user_model():
    user = User(
        email="test@example.com",
        firstname="Test",
        lastname="User"
    )
    assert user.email == "test@example.com"
    assert user.firstname == "Test"
    assert user.lastname == "User"

def test_borrowed_book_model():
    now = datetime.utcnow()
    borrowed_book = BorrowedBook(
        user_id=1,
        book_id=1,
        borrowed_date=now,
        return_date=now + timedelta(days=7)
    )
    assert borrowed_book.user_id == 1
    assert borrowed_book.book_id == 1
    assert borrowed_book.borrowed_date == now 