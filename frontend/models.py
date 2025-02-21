from flask_sqlalchemy import SQLAlchemy
from database import db
from datetime import datetime

class Book(db.Model):
    __tablename__ = 'book'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(120), nullable=False)
    publisher = db.Column(db.String(80), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    is_available = db.Column(db.Boolean, default=True)
    borrowed_date = db.Column(db.DateTime, nullable=True)
    return_date = db.Column(db.DateTime, nullable=True)
    borrowed_records = db.relationship('BorrowedBook', backref='book', lazy=True)

    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4'
    }

class User(db.Model):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    firstname = db.Column(db.String(80), nullable=False)
    lastname = db.Column(db.String(80), nullable=False)
    borrowed_books = db.relationship('BorrowedBook', backref='user', lazy=True)

    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4'
    }

class BorrowedBook(db.Model):
    __tablename__ = 'borrowed_book'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id', ondelete='CASCADE'), nullable=False)
    borrowed_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    return_date = db.Column(db.DateTime, nullable=False)

    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4'
    } 