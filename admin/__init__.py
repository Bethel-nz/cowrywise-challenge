from flask import Flask
from database import db, init_db, redis_client

def create_app(test_config=None):
    app = Flask(__name__)
    
    if test_config is None:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@db:5432/admin_db'
    else:
        app.config.update(test_config)
    
    init_db(app)
    
    from routes import book_bp, user_bp
    app.register_blueprint(book_bp)
    app.register_blueprint(user_bp)
    
    return app

__all__ = [
    'create_app',
    'db',
    "redis_client",
    "init_db"
]
