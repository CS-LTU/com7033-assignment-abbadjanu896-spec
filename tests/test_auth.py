"""
Unit tests for authentication functionality
Tests user registration, login, logout, and password security
"""
import pytest
from app.models.user import User
from app import db


class TestUserModel:
    """Test User model functionality"""
    
    def test_password_hashing(self, test_client):
        """Test password hashing and verification"""
        user = User(username='hashtest', email='hash@test.com')
        user.set_password('SecurePassword123')
        
        # Password should be hashed, not stored in plain text
        assert user.password_hash != 'SecurePassword123'
        
        # Correct password should verify
        assert user.check_password('SecurePassword123') == True
        
        # Incorrect password should fail
        assert user.check_password('WrongPassword') == False
    
    def test_user_creation(self, test_client):
        """Test creating a new user"""
        user = User(username='newuser', email='new@test.com')
        user.set_password('TestPass123')
        
        db.session.add(user)
        db.session.commit()
        
        # Verify user was created
        retrieved_user = User.query.filter_by(username='newuser').first()
        assert retrieved_user is not None
        assert retrieved_user.email == 'new@test.com'
    
    def test_unique_username(self, test_client, init_database):
        """Test that usernames must be unique"""
        # Try to create user with existing username
        user = User(username='testuser', email='different@test.com')
        user.set_password('TestPass123')
        
        db.session.add(user)
        
        # Should raise integrity error
        with pytest.raises(Exception):
            db.session.commit()
        
        db.session.rollback()


class TestRegistration:
    """Test user registration functionality"""
    
    def test_registration_page_loads(self, test_client):
        """Test registration page is accessible"""
        response = test_client.get('/auth/register')
        assert response.status_code == 200
        assert b'Register' in response.data
    
    def test_valid_registration(self, test_client):
        """Test successful user registration"""
        response = test_client.post('/auth/register', data={
            'username': 'validuser',
            'email': 'valid@test.com',
            'password': 'ValidPass123',
            'confirm_password': 'ValidPass123'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        assert b'Registration successful' in response.data or b'Login' in response.data
        
        # Verify user was created in database
        user = User.query.filter_by(username='validuser').first()
        assert user is not None
    
    def test_registration_weak_password(self, test_client):
        """Test registration with weak password fails"""
        response = test_client.post('/auth/register', data={
            'username': 'weakpass',
            'email': 'weak@test.com',
            'password': 'weak',
            'confirm_password': 'weak'
        }, follow_redirects=True)
        
        # Should fail validation
        assert b'Password must be' in response.data or b'at least 8 characters' in response.data
    
    def test_registration_password_mismatch(self, test_client):
        """Test registration with mismatched passwords"""
        response = test_client.post('/auth/register', data={
            'username': 'mismatch',
            'email': 'mismatch@test.com',
            'password': 'ValidPass123',
            'confirm_password': 'DifferentPass123'
        }, follow_redirects=True)
        
        assert b'Passwords must match' in response.data
    
    def test_registration_duplicate_username(self, test_client, init_database):
        """Test registration with duplicate username fails"""
        response = test_client.post('/auth/register', data={
            'username': 'testuser',
            'email': 'duplicate@test.com',
            'password': 'ValidPass123',
            'confirm_password': 'ValidPass123'
        }, follow_redirects=True)
        
        assert b'already taken' in response.data or b'already registered' in response.data


class TestLogin:
    """Test user login functionality"""
    
    def test_login_page_loads(self, test_client):
        """Test login page is accessible"""
        response = test_client.get('/auth/login')
        assert response.status_code == 200
        assert b'Login' in response.data
    
    def test_valid_login(self, test_client, init_database):
        """Test successful login"""
        response = test_client.post('/auth/login', data={
            'username': 'testuser',
            'password': 'TestPassword123'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        assert b'Welcome' in response.data or b'Dashboard' in response.data
    
    def test_invalid_username(self, test_client):
        """Test login with invalid username"""
        response = test_client.post('/auth/login', data={
            'username': 'nonexistent',
            'password': 'TestPassword123'
        }, follow_redirects=True)
        
        assert b'Invalid username or password' in response.data
    
    def test_invalid_password(self, test_client, init_database):
        """Test login with invalid password"""
        response = test_client.post('/auth/login', data={
            'username': 'testuser',
            'password': 'WrongPassword123'
        }, follow_redirects=True)
        
        assert b'Invalid username or password' in response.data
    
    def test_csrf_protection(self, test_client):
        """Test that CSRF protection is enabled"""
        response = test_client.get('/auth/login')
        assert b'csrf_token' in response.data


class TestLogout:
    """Test user logout functionality"""
    
    def test_logout(self, logged_in_client):
        """Test successful logout"""
        response = logged_in_client.get('/auth/logout', follow_redirects=True)
        
        assert response.status_code == 200
        assert b'logged out' in response.data or b'Login' in response.data


class TestAuthorizationProtection:
    """Test that routes are protected"""
    
    def test_dashboard_requires_login(self, test_client):
        """Test that dashboard requires authentication"""
        response = test_client.get('/dashboard', follow_redirects=True)
        
        # Should redirect to login
        assert b'Login' in response.data or b'log in' in response.data
    
    def test_patients_requires_login(self, test_client):
        """Test that patient routes require authentication"""
        response = test_client.get('/patients/', follow_redirects=True)
        
        # Should redirect to login
        assert b'Login' in response.data or b'log in' in response.data
