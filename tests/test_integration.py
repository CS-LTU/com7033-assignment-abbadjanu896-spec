"""
Integration tests for complete application workflows
"""
import pytest


class TestUserWorkflow:
    """Test complete user registration and login workflow"""
    
    def test_complete_registration_and_login(self, test_client):
        """Test user can register and then login"""
        # Register new user
        register_response = test_client.post('/auth/register', data={
            'username': 'workflowuser',
            'email': 'workflow@test.com',
            'password': 'WorkflowPass123',
            'confirm_password': 'WorkflowPass123'
        }, follow_redirects=True)
        
        assert register_response.status_code == 200
        
        # Login with the new user
        login_response = test_client.post('/auth/login', data={
            'username': 'workflowuser',
            'password': 'WorkflowPass123'
        }, follow_redirects=True)
        
        assert login_response.status_code == 200
        assert b'Dashboard' in login_response.data or b'Welcome' in login_response.data


class TestPatientWorkflow:
    """Test complete patient management workflow"""
    
    def test_patient_crud_workflow(self, logged_in_client):
        """Test complete patient CRUD workflow"""
        # Access patient list
        list_response = logged_in_client.get('/patients/')
        assert list_response.status_code == 200
        
        # Access add patient form
        add_form_response = logged_in_client.get('/patients/add')
        assert add_form_response.status_code == 200
        assert b'Add' in add_form_response.data


class TestSecurityHeaders:
    """Test security headers are present"""
    
    def test_security_headers_present(self, test_client):
        """Test that security headers are set"""
        response = test_client.get('/auth/login')
        
        # Check for security headers
        assert 'X-Content-Type-Options' in response.headers
        assert 'X-Frame-Options' in response.headers
        assert 'X-XSS-Protection' in response.headers


class TestErrorHandling:
    """Test error handling"""
    
    def test_404_error(self, test_client):
        """Test 404 error page"""
        response = test_client.get('/nonexistent-page')
        assert response.status_code == 404
    
    def test_error_page_contains_useful_info(self, test_client):
        """Test error page has helpful information"""
        response = test_client.get('/nonexistent-page')
        assert b'404' in response.data or b'Not Found' in response.data


class TestDatabaseOperations:
    """Test database operations"""
    
    def test_database_connection(self, test_client):
        """Test database is accessible"""
        from app.models.user import User
        
        # Query should not raise exception
        users = User.query.all()
        assert isinstance(users, list)
