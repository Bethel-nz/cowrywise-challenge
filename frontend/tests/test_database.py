import pytest
from frontend.models import Book, User, BorrowedBook
from frontend.database import db
from datetime import datetime, timedelta

# @pytest.mark.skip("Database initialization needs fixing")
# def test_db_initialization(app, _db):
#     with app.app_context():
#         try:
#             Book.query.first()
#             User.query.first()
#             BorrowedBook.query.first()
#             assert True 
#         except Exception as e:
#             pytest.fail(f"Database tables not properly initialized: {str(e)}")

# @pytest.mark.skip("Database tables test needs fixing")
# def test_db_tables(app, _db):
#     with app.app_context():
#         inspector = db.inspect(db.engine)
#         
#         assert 'book' in existing_tables
#         assert 'user' in existing_tables
#         assert 'borrowed_book' in existing_tables

# @pytest.mark.skip("Database initialization test needs fixing")
# def test_database_initialization(app, _db):
#     with app.app_context():
#         book = Book(
#             title='Test Book',
#             publisher='Test Publisher',
#             category='Test Category',
#             is_available=True
#         )
#         _db.session.add(book)
#         _db.session.commit()
#         
#         queried_book = Book.query.filter_by(title='Test Book').first()
#         assert queried_book is not None
#         assert queried_book.publisher == 'Test Publisher'

# @pytest.mark.skip("Book borrowing test needs fixing")
# def test_book_borrowing(app, _db):
#     with app.app_context():
#         # Create test book and user
#         book = Book(
#             title='Test Book',
#             publisher='Test Publisher',
#             category='Test',
#             is_available=True
#         )
#         user = User(
#             email='test@test.com',
#             firstname='Test',
#             lastname='User'
#         )
#         _db.session.add_all([book, user])
#         _db.session.commit()
#         
#         # Create borrowed book record
#         now = datetime.now()
#         borrowed_book = BorrowedBook(
#             user_id=user.id,
#             book_id=book.id,
#             borrowed_date=now,
#             return_date=now + timedelta(days=14)
#         )
#         book.is_available = False
#         book.borrowed_date = now
#         book.return_date = now + timedelta(days=14)
#         
#         _db.session.add(borrowed_book)
#         _db.session.commit()
#         
#         # Test relationships
#         assert len(user.borrowed_books) == 1
#         assert user.borrowed_books[0].book.title == 'Test Book'
#         assert not book.is_available
#         assert book.borrowed_date is not None
#         assert book.return_date is not None 