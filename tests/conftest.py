"""
Pytest configuration and fixtures
"""
import pytest
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models.user import User


@pytest.fixture(scope='module')
def test_client():
    """
    Create a test client for the Flask application
    """
    # Set testing environment
    os.environ['FLASK_ENV'] = 'testing'
    
    # Create Flask app in testing mode
    flask_app = create_app('testing')
    
    # Create a test client
    with flask_app.test_client() as testing_client:
        # Establish application context
        with flask_app.app_context():
            # Create database tables
            db.create_all()
            
            yield testing_client
            
            # Clean up database
            db.session.remove()
            db.drop_all()


@pytest.fixture(scope='module')
def init_database(test_client):
    """
    Initialize database with test data
    """
    # Create test user
    user = User(username='testuser', email='test@example.com')
    user.set_password('TestPassword123')
    
    db.session.add(user)
    db.session.commit()
    
    yield
    
    # Cleanup
    db.session.remove()


@pytest.fixture(scope='function')
def logged_in_client(test_client, init_database):
    """
    Create a logged-in test client
    """
    # Log in the test user
    test_client.post('/auth/login', data={
        'username': 'testuser',
        'password': 'TestPassword123'
    }, follow_redirects=True)
    
    yield test_client
    
    # Log out
    test_client.get('/auth/logout', follow_redirects=True)
