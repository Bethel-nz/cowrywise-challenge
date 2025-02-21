from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
from models import Book, User, BorrowedBook
from database import db, redis_client
from sqlalchemy.exc import SQLAlchemyError
import json

book_bp = Blueprint('book_routes', __name__)
user_bp = Blueprint('user_routes', __name__)
borrow_bp = Blueprint('borrow_routes', __name__)

# Book routes
@book_bp.route('/books', methods=['GET'])
def list_books():
    try:
        publisher = request.args.get('publisher')
        category = request.args.get('category')
        
        query = Book.query.filter_by(is_available=True)
        
        if publisher:
            query = query.filter_by(publisher=publisher)
        if category:
            query = query.filter_by(category=category)
            
        books = query.all()
        return jsonify([{
            'id': book.id,
            'title': book.title,
            'publisher': book.publisher,
            'category': book.category
        } for book in books])
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@book_bp.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = Book.query.get_or_404(book_id)
    return jsonify({
        'id': book.id,
        'title': book.title,
        'publisher': book.publisher,
        'category': book.category,
        'is_available': book.is_available
    })

@book_bp.route('/books/all', methods=['GET'])
def list_all_books():
    try:
        books = Book.query.all()
        return jsonify([{
            'id': book.id,
            'title': book.title,
            'publisher': book.publisher,
            'category': book.category,
            'is_available': book.is_available
        } for book in books])
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# User routes
@user_bp.route('/users', methods=['POST'])
def enroll_user():
    data = request.json
    user = User(
        email=data['email'],
        firstname=data['firstname'],
        lastname=data['lastname']
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User enrolled successfully', 'user_id': user.id}), 201

# Borrow routes
@borrow_bp.route('/books/<int:book_id>/borrow', methods=['POST'])
def borrow_book(book_id):
    try:
        data = request.json
        days = data.get('days', 14)  # Default to 14 days
		
        book = Book.query.filter_by(id=book_id).first()
        if not book:
            return jsonify({'error': 'Book not found'}), 404
        
        if not book.is_available:
            return jsonify({'error': 'Book is not available', 
                          'available_from': book.return_date.isoformat() if book.return_date else None}), 400
            
        user = User.query.filter_by(id=data['user_id']).first()
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        now = datetime.now()
        return_date = now + timedelta(days)
        
        book.is_available = False
        book.borrowed_date = now
        book.return_date = return_date
        
        borrowed_book = BorrowedBook(
            user_id=user.id,
            book_id=book.id,
            borrowed_date=now,
            return_date=return_date
        )
        
        db.session.add(borrowed_book)
        db.session.commit()
        
        # Create borrow update message
        message = {
            'action': 'borrow',
            'book': {
                'id': book.id,
                'is_available': False,
                'borrowed_date': now.isoformat(),
                'return_date': return_date.isoformat()
            },
            'user': {
                'id': user.id,
                'email': user.email,
                'firstname': user.firstname,
                'lastname': user.lastname
            }
        }
        
        # Publish to both channels
        redis_client.publish('book_updates', json.dumps(message))  # For frontend sync
        redis_client.publish('borrow_updates', json.dumps(message))  # For admin sync
        
        return jsonify({
            'message': 'Book borrowed successfully',
            'borrowed_date': now.isoformat(),
            'return_date': return_date.isoformat()
        }), 200
        
    except Exception as e:
        print(f"Error borrowing book: {str(e)}")
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    