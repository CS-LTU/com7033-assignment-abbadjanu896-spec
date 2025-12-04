"""
Authentication routes module
Handles user registration, login, and logout with security measures
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models.user import User
from app.utils.validators import LoginForm, RegistrationForm
from app.utils.security import log_security_event
import logging

# Configure logging
logger = logging.getLogger(__name__)

# Create Blueprint
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    Handle user registration
    Implements secure password hashing and input validation
    """
    # Redirect if already logged in
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form = RegistrationForm()
    
    if form.validate_on_submit():
        try:
            # Create new user with hashed password
            user = User(
                username=form.username.data.strip(),
                email=form.email.data.strip().lower()
            )
            user.set_password(form.password.data)
            
            # Save to database
            db.session.add(user)
            db.session.commit()
            
            # Log security event
            log_security_event('USER_REGISTRATION', user_id=user.id, details=f"Username: {user.username}")
            
            flash('Registration successful! Please log in.', 'success')
            logger.info(f"New user registered: {user.username}")
            
            return redirect(url_for('auth.login'))
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Registration error: {str(e)}")
            flash('An error occurred during registration. Please try again.', 'danger')
    
    return render_template('auth/register.html', form=form, title='Register')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handle user login
    Implements secure authentication with session management
    """
    # Redirect if already logged in
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form = LoginForm()
    
    if form.validate_on_submit():
        # Find user by username
        user = User.query.filter_by(username=form.username.data.strip()).first()
        
        # Verify credentials
        if user and user.check_password(form.password.data):
            if not user.is_active:
                log_security_event('LOGIN_ATTEMPT_INACTIVE', user_id=user.id)
                flash('Your account has been deactivated. Please contact support.', 'warning')
                return redirect(url_for('auth.login'))
            
            # Log user in
            login_user(user)
            user.update_last_login()
            
            # Log security event
            log_security_event('USER_LOGIN', user_id=user.id, details=f"Username: {user.username}")
            logger.info(f"User logged in: {user.username}")
            
            flash(f'Welcome back, {user.username}!', 'success')
            
            # Redirect to next page or dashboard
            next_page = request.args.get('next')
            if next_page and next_page.startswith('/'):
                return redirect(next_page)
            return redirect(url_for('main.dashboard'))
        else:
            # Log failed login attempt
            log_security_event('LOGIN_FAILED', details=f"Username: {form.username.data}")
            flash('Invalid username or password. Please try again.', 'danger')
    
    return render_template('auth/login.html', form=form, title='Login')


@auth_bp.route('/logout')
@login_required
def logout():
    """
    Handle user logout
    Clears session and logs out user securely
    """
    username = current_user.username
    user_id = current_user.id
    
    # Log security event
    log_security_event('USER_LOGOUT', user_id=user_id, details=f"Username: {username}")
    logger.info(f"User logged out: {username}")
    
    logout_user()
    flash('You have been logged out successfully.', 'info')
    
    return redirect(url_for('auth.login'))
