from flask import Blueprint, request, jsonify
from models import Book, User, BorrowedBook
from database import db, redis_client
import json
from sqlalchemy.exc import SQLAlchemyError
import threading
from datetime import datetime

book_bp = Blueprint('admin_book_routes', __name__)
user_bp = Blueprint('admin_user_routes', __name__)


# Book routes
@book_bp.route('/admin/books', methods=['POST'])
def add_book():
    try:
        data = request.json
        book = Book(
            title=data['title'],
            publisher=data['publisher'],
            category=data['category'],
            is_available=True
        )
        
        db.session.add(book)
        db.session.commit()
        
        message = {
            'action': 'add',
            'book': {
                'id': book.id,
                'title': book.title,
                'publisher': book.publisher,
                'category': book.category,
                'is_available': book.is_available
            }
        }
        
        print(f"Admin: Publishing message to Redis: {message}")
        redis_client.publish('book_updates', json.dumps(message))
        print("Admin: Message published successfully")
        
        return jsonify({'message': 'Book added successfully', 'book_id': book.id}), 201
        
    except SQLAlchemyError as e:
        print(f"Admin: Database error: {str(e)}")
        db.session.rollback()
        return jsonify({'error': f'Database error: {str(e)}'}), 500
    except Exception as e:
        print(f"Admin: Unexpected error: {str(e)}")
        db.session.rollback()
        return jsonify({'error': f'Unexpected error: {str(e)}'}), 500
    

@book_bp.route('/admin/books/<int:book_id>', methods=['DELETE'])
def remove_book(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    
    redis_client.publish('book_updates', json.dumps({
        'action': 'delete',
        'book_id': book_id
    }))
    
    return jsonify({'message': 'Book removed successfully'}), 200


# User routes
@user_bp.route('/admin/users', methods=['GET'])
def list_users():
    users = User.query.all()
    return jsonify([{
        'id': user.id,
        'email': user.email,
        'firstname': user.firstname,
        'lastname': user.lastname
    } for user in users])

@book_bp.route('/admin/books/unavailable', methods=['GET'])
def list_unavailable_books():
    try:
        books = Book.query.filter_by(is_available=False).all()
        return jsonify([{
            'id': book.id,
            'title': book.title,
            'publisher': book.publisher,
            'category': book.category,
            'borrowed_date': book.borrowed_date.isoformat() if book.borrowed_date else None,
            'return_date': book.return_date.isoformat() if book.return_date else None
        } for book in books])
    except Exception as e:
        print(f"Admin: Error listing unavailable books: {str(e)}")
        return jsonify({'error': str(e)}), 500

@user_bp.route('/admin/users/borrowed', methods=['GET'])
def list_users_with_borrowed_books():
    try:
        users = User.query.join(BorrowedBook).all()
        
        return jsonify([{
            'id': user.id,
            'email': user.email,
            'firstname': user.firstname,
            'lastname': user.lastname,
            'borrowed_books': [{
                'book_id': borrowed.book_id,
                'title': Book.query.get(borrowed.book_id).title,
                'borrowed_date': borrowed.borrowed_date.isoformat(),
                'return_date': borrowed.return_date.isoformat()
            } for borrowed in user.borrowed_books]
        } for user in users])
    except Exception as e:
        print(f"Admin: Error listing users with borrowed books: {str(e)}")
        return jsonify({'error': str(e)}), 500

@book_bp.route('/admin/drop-data', methods=['POST'])
def drop_data():
    try:
        with db.session.begin():
            db.session.query(BorrowedBook).delete()
            db.session.query(User).delete()
            db.session.query(Book).delete()
            db.session.commit()
        return jsonify({'message': 'Admin database cleared'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500 