"""
Application entry point
Runs the Flask application
"""
from app import create_app
import os

# Create Flask application instance
app = create_app(os.getenv('FLASK_ENV', 'development'))

if __name__ == '__main__':
    # Run development server
    app.run(
        host='127.0.0.1',
        port=5000,
        debug=True
    )
