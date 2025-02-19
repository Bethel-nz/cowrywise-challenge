import json
from models import Book, User
from database import db, redis_client
import threading
import time
from flask import current_app
from datetime import datetime

def handle_book_updates():
    try:
        pubsub = redis_client.pubsub()
        pubsub.subscribe('book_updates')
        
        # Test Redis connection
        try:
            redis_client.ping()
        except Exception as e:
            print(f"Frontend: Redis connection test failed: {e}")
        
        for message in pubsub.listen():
            if message['type'] == 'message':
                try:
                    data = json.loads(message['data'])
                    
                    if data['action'] == 'add':
                        book_data = data['book']
                        
                        with current_app.app_context():
                            new_book = Book(
                                id=book_data['id'],
                                title=book_data['title'],
                                publisher=book_data['publisher'],
                                category=book_data['category'],
                                is_available=book_data['is_available']
                            )
                            db.session.add(new_book)
                            db.session.commit()
                            print(Book.query.all(), User.query.all())
                    
                    elif data['action'] == 'delete':
                        book_id = data['book_id']
                        print(f"Frontend: Deleting book {book_id}")
                        
                        with current_app.app_context():
                            book = Book.query.get(book_id)
                            if book:
                                db.session.delete(book)
                                db.session.commit()
                                print(f"Frontend: Successfully deleted book {book_id}")
                    
                    elif data['action'] == 'borrow':
                        book_data = data['book']
                        print(f"Frontend: Updating book borrow status: {book_data}")
                        
                        with current_app.app_context():
                            book = Book.query.get(book_data['id'])
                            if book:
                                book.is_available = book_data['is_available']
                                book.borrowed_date = datetime.fromisoformat(book_data['borrowed_date'])
                                book.return_date = datetime.fromisoformat(book_data['return_date'])
                                db.session.commit()
                                print(f"Frontend: Updated book {book.id} borrow status")
                                
                except json.JSONDecodeError as e:
                    print(f"Frontend: JSON decode error: {e}")
                except Exception as e:
                    print(f"Frontend: Error processing message: {e}")
                    
    except Exception as e:
        print(f"Frontend: Subscriber error: {e}")
        # Wait a bit before reconnecting
        time.sleep(5)
        handle_book_updates()

def start_subscriber(app):
    def run_subscriber():
        with app.app_context():
            handle_book_updates()
            
    thread = threading.Thread(target=run_subscriber, daemon=True)
    thread.start()
    return thread 