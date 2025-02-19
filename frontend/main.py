from flask import Flask
from database import init_db, create_tables
from routes import book_bp, user_bp, borrow_bp
from redis_subscriber import start_subscriber

def create_app():
    app = Flask(__name__)
    app.config['DEBUG'] = True
    
    init_db(app)
    
    # Test Redis connection
    from database import redis_client
    try:
        redis_client.ping()
        # Subscribe test
        pubsub = redis_client.pubsub()
        pubsub.subscribe('book_updates')
    except Exception as e:
        print(f"Frontend service: Redis connection failed: {e}")
    
    app.register_blueprint(book_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(borrow_bp)
    
    with app.app_context():
        create_tables(app)
        start_subscriber(app)
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=8181, debug=True) 
