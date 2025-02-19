import json
from models import Book, User, BorrowedBook
from database import db, redis_client
import threading
import time
from flask import current_app
from datetime import datetime

def handle_book_updates():
    try:
        pubsub = redis_client.pubsub()
        pubsub.subscribe('borrow_updates')  # Listen for borrow updates
        
        for message in pubsub.listen():
            if message['type'] == 'message':
                try:
                    data = json.loads(message['data'])
                    
                    if data['action'] == 'borrow':
                        user_data = data['user']
                        book_data = data['book']
                        
                        with current_app.app_context():
                            print(f"Admin: Processing borrow update: {data}")
                            
                            # First, ensure user exists
                            user = User.query.get(user_data['id'])
                            if not user:
                                user = User(
                                    id=user_data['id'],
                                    email=user_data['email'],
                                    firstname=user_data['firstname'],
                                    lastname=user_data['lastname']
                                )
                                db.session.add(user)
                                db.session.commit()  # Commit user first
                                print(f"Admin: Created user {user.id}")
                            
                            # Then update book status
                            book = Book.query.get(book_data['id'])
                            if book:
                                book.is_available = book_data['is_available']
                                book.borrowed_date = datetime.fromisoformat(book_data['borrowed_date'])
                                book.return_date = datetime.fromisoformat(book_data['return_date'])
                                db.session.commit()  # Commit book updates
                                print(f"Admin: Updated book {book.id}")
                                
                                # Finally create borrowed book record
                                borrowed_book = BorrowedBook(
                                    user_id=user_data['id'],
                                    book_id=book_data['id'],
                                    borrowed_date=datetime.fromisoformat(book_data['borrowed_date']),
                                    return_date=datetime.fromisoformat(book_data['return_date'])
                                )
                                db.session.add(borrowed_book)
                                db.session.commit()  # Commit borrowed book
                                print(f"Admin: Created borrowed book record for book {book.id} and user {user.id}")
                                
                except json.JSONDecodeError as e:
                    print(f"Admin: JSON decode error: {e}")
                except Exception as e:
                    print(f"Admin: Error processing message: {e}")
                    db.session.rollback()  # Rollback on error
                    
    except Exception as e:
        print(f"Admin: Subscriber error: {e}")
        time.sleep(5)
        handle_book_updates()

def start_subscriber(app):
    def run_subscriber():
        with app.app_context():
            handle_book_updates()
            
    thread = threading.Thread(target=run_subscriber, daemon=True)
    thread.start()
    return thread 