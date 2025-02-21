from flask_sqlalchemy import SQLAlchemy
import redis
import os
from sqlalchemy import text  # Import the text function

db = SQLAlchemy()

# Only create redis client if URL is provided
redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
redis_client = redis.Redis.from_url(redis_url) if redis_url else None

def init_db(app):
    # Configure MySQL connection
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
        'DATABASE_URL',
        'mysql://postgres:postgres@localhost:3306/frontend_db'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # MySQL-specific configuration
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_size': 10,  # Maximum number of connections in the pool
        'pool_timeout': 30,  # Timeout in seconds
        'pool_recycle': 1800,  # Recycle connections after 30 minutes
        'max_overflow': 2  # Allow 2 connections beyond pool_size
    }
    
    db.init_app(app)

def create_tables(app):
    with app.app_context():
        # Use text() to wrap the SQL commands
        db.session.execute(text('SET NAMES utf8mb4'))
        db.create_all()
        
        # Ensure proper encoding for MySQL
        db.session.execute(text('SET CHARACTER SET utf8mb4'))
        db.session.execute(text('SET character_set_connection=utf8mb4'))
        db.session.commit()