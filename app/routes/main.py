"""
Main routes module
Handles main application pages like home and dashboard
"""
from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user

# Create Blueprint
main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """
    Home page
    Redirects to dashboard if logged in, otherwise shows welcome page
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return redirect(url_for('auth.login'))


@main_bp.route('/dashboard')
@login_required
def dashboard():
    """
    Main dashboard page
    Shows overview and quick actions
    """
    return render_template('dashboard.html', title='Dashboard')


@main_bp.route('/about')
def about():
    """
    About page with application information
    """
    return render_template('about.html', title='About')
