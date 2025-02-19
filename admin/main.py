from flask import Flask
from database import init_db, create_tables
from routes import book_bp, user_bp
from redis_subscriber import start_subscriber
import json

def create_app():
    app = Flask(__name__)
    app.config['DEBUG'] = True
    
    init_db(app)
    
    # Test Redis connection
    from database import redis_client
    try:
        redis_client.ping()
        
    except Exception as e:
        print(f"Admin service: Redis connection failed: {e}")
    
    app.register_blueprint(book_bp)
    app.register_blueprint(user_bp)
    
    with app.app_context():
        create_tables(app)
        start_subscriber(app)  # Start the Redis subscriber

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=8080, debug=True)
