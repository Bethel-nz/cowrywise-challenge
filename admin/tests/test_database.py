import pytest
from admin.models import Book, User, BorrowedBook
from admin.database import db, init_db
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
#         existing_tables = inspector.get_table_names()
        
#         assert 'book' in existing_tables
#         assert 'user' in existing_tables
#         assert 'borrowed_book' in existing_tables

# @pytest.mark.skip("Database initialization test needs fixing")
# def test_database_initialization(app, _db):
#     book = Book(
#         title='Test Book',
#         publisher='Test Publisher',
#         category='Test Category',
#         is_available=True
#     )
#     _db.session.add(book)
#     _db.session.commit()
    
#     queried_book = Book.query.filter_by(title='Test Book').first()
#     assert queried_book is not None
#     assert queried_book.publisher == 'Test Publisher'

# @pytest.mark.skip("Borrowed book relationships test needs fixing")
# def test_borrowed_book_relationships(app):
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
#             lastname='User',
#             is_admin=False
#         )
#         db.session.add_all([book, user])
#         db.session.commit()
        
#         # Create borrowed book record
#         now = datetime.utcnow()
#         borrowed_book = BorrowedBook(
#             user_id=user.id,
#             book_id=book.id,
#             borrowed_date=now,
#             return_date=now + timedelta(days=14)
#         )
#         book.is_available = False
#         book.borrowed_date = now
#         book.return_date = now + timedelta(days=14)
        
#         db.session.add(borrowed_book)
#         db.session.commit()
        
#         # Test relationships
#         assert len(user.borrowed_books) == 1
#         assert len(book.borrowed_records) == 1
#         assert user.borrowed_books[0].book_id == book.id
#         assert book.borrowed_records[0].user_id == user.id

