"""
Routes package initialization
"""
from .auth import auth_bp
from .patient import patient_bp
from .main import main_bp

__all__ = ['auth_bp', 'patient_bp', 'main_bp']
