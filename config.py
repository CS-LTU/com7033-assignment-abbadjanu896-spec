"""
Configuration module for Flask application
Implements secure configuration with environment variables
"""
import os
from datetime import timedelta
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Base configuration class with security-focused settings"""
    
    # Flask Core Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(32)
    
    # SQLite Database Configuration (for user authentication)
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') or 'sqlite:///users.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # MongoDB Configuration (for patient records)
    MONGODB_URI = os.environ.get('MONGODB_URI') or 'mongodb://localhost:27017/'
    MONGODB_DB_NAME = os.environ.get('MONGODB_DB_NAME') or 'stroke_prediction'
    
    # Security Configuration
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = 3600  # 1 hour
    
    # Session Configuration
    SESSION_COOKIE_SECURE = os.environ.get('SESSION_COOKIE_SECURE', 'False').lower() == 'true'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)
    
    # Password Hashing Configuration
    BCRYPT_LOG_ROUNDS = 12
    
    # Logging Configuration
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')


class DevelopmentConfig(Config):
    """Development environment configuration"""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Production environment configuration with enhanced security"""
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = True  # Require HTTPS in production


class TestingConfig(Config):
    """Testing environment configuration"""
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
    MONGODB_DB_NAME = 'stroke_prediction_test'


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
