import pytest
from frontend.models import Book, User, BorrowedBook
from frontend.database import db
from datetime import datetime, timedelta

@pytest.fixture
def app():
    from frontend import create_app
    app = create_app()
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    with app.app_context():
        db.create_all()
    yield app
    
    with app.app_context():
        db.session.remove()
        db.drop_all()

def test_db_initialization(app):
    with app.app_context():
        assert Book.query.first() is None
        assert User.query.first() is None
        assert BorrowedBook.query.first() is None

def test_db_tables(app):
    with app.app_context():
        # Test we can create and query records
        book = Book(
            title='Test Book',
            publisher='Test Publisher',
            category='Test Category',
            is_available=True
        )
        db.session.add(book)
        db.session.commit()
        
        assert Book.query.count() == 1
        assert Book.query.first().title == 'Test Book'

def test_database_initialization(app):
    with app.app_context():
        book = Book(
            title='Test Book',
            publisher='Test Publisher',
            category='Test Category',
            is_available=True
        )
        db.session.add(book)
        db.session.commit()
        
        queried_book = Book.query.filter_by(title='Test Book').first()
        assert queried_book is not None
        assert queried_book.publisher == 'Test Publisher'

def test_book_borrowing(app):
    with app.app_context():
        # Create test book and user
        book = Book(
            title='Test Book',
            publisher='Test Publisher',
            category='Test',
            is_available=True
        )
        user = User(
            email='test@test.com',
            firstname='Test',
            lastname='User'
        )
        db.session.add_all([book, user])
        db.session.commit()
        
        # Create borrowed book record
        now = datetime.utcnow()
        borrowed_book = BorrowedBook(
            user_id=user.id,
            book_id=book.id,
            borrowed_date=now,
            return_date=now + timedelta(days=14)
        )
        book.is_available = False
        book.borrowed_date = now
        book.return_date = now + timedelta(days=14)
        
        db.session.add(borrowed_book)
        db.session.commit()
        
        # Test relationships
        assert len(user.borrowed_books) == 1
        assert user.borrowed_books[0].book.title == 'Test Book'
        assert not book.is_available
        assert book.borrowed_date is not None
        assert book.return_date is not None
        
        # Test cascade delete
        db.session.delete(user)
        db.session.commit()
        assert BorrowedBook.query.count() == 0 