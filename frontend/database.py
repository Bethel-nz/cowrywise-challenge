from flask_sqlalchemy import SQLAlchemy
import redis
import os

db = SQLAlchemy()

# Only create redis client if URL is provided
redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
redis_client = redis.Redis.from_url(redis_url) if redis_url else None

def init_db(app):
    # Use localhost:5433 when running locally
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://postgres:frontend_db@localhost:5433/frontend_db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app) 

def create_tables(app):
    with app.app_context():
        db.create_all()