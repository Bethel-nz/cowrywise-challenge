import pytest
from frontend import create_app
from frontend.database import db, redis_client

@pytest.fixture(scope='session')
def app():
    """Create and configure a new app instance for each test."""
    app = create_app({
        'SQLALCHEMY_DATABASE_URI': 'postgresql://postgres:postgres@test-frontend-db:5432/test_frontend_db',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        'TESTING': True
    })
    
    # Create the database and tables
    with app.app_context():
        db.drop_all()  # Clean slate
        db.create_all()  # Create all tables
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture(scope='function')
def _db(app):
    """Provide the transactional fixtures with access to the database"""
    with app.app_context():
        db.session.begin_nested()
        yield db
        db.session.rollback()
        db.session.remove()

@pytest.fixture(scope='function')
def redis():
    return redis_client 