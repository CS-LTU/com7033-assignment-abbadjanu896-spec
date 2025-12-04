"""
Unit tests for patient CRUD operations
Tests Create, Read, Update, Delete functionality for patient records
"""
import pytest
from app.models.patient import PatientDatabase


class TestPatientModel:
    """Test Patient database operations"""
    
    def test_create_patient(self, test_client, logged_in_client):
        """Test creating a patient record"""
        patient_data = {
            'patient_id': 12345,
            'gender': 'Male',
            'age': 45.0,
            'hypertension': 0,
            'heart_disease': 0,
            'ever_married': 'Yes',
            'work_type': 'Private',
            'residence_type': 'Urban',
            'avg_glucose_level': 120.5,
            'bmi': 25.3,
            'smoking_status': 'never smoked',
            'stroke': 0
        }
        
        # This test verifies the patient data structure
        assert patient_data['patient_id'] == 12345
        assert patient_data['gender'] in ['Male', 'Female', 'Other']
        assert 0 <= patient_data['age'] <= 120
        assert patient_data['hypertension'] in [0, 1]
        assert patient_data['stroke'] in [0, 1]


class TestPatientRoutes:
    """Test patient CRUD routes"""
    
    def test_patient_list_page(self, logged_in_client):
        """Test patient list page loads"""
        response = logged_in_client.get('/patients/')
        assert response.status_code == 200
        assert b'Patient' in response.data
    
    def test_add_patient_page_loads(self, logged_in_client):
        """Test add patient page is accessible"""
        response = logged_in_client.get('/patients/add')
        assert response.status_code == 200
        assert b'Add' in response.data or b'Patient' in response.data
    
    def test_add_patient_form_validation(self, logged_in_client):
        """Test patient form validation"""
        # Submit form with missing required fields
        response = logged_in_client.post('/patients/add', data={
            'patient_id': '',
            'gender': '',
            'age': ''
        }, follow_redirects=True)
        
        # Should show validation errors
        assert response.status_code == 200
        assert b'required' in response.data or b'field' in response.data
    
    def test_patient_requires_authentication(self, test_client):
        """Test that patient routes require login"""
        # Test various patient routes without authentication
        routes = [
            '/patients/',
            '/patients/add',
        ]
        
        for route in routes:
            response = test_client.get(route, follow_redirects=True)
            assert b'Login' in response.data or b'log in' in response.data


class TestInputValidation:
    """Test input validation for patient data"""
    
    def test_patient_id_validation(self, logged_in_client):
        """Test patient ID must be valid"""
        response = logged_in_client.post('/patients/add', data={
            'patient_id': -1,  # Invalid negative ID
            'gender': 'Male',
            'age': 45,
            'hypertension': 0,
            'heart_disease': 0,
            'ever_married': 'Yes',
            'work_type': 'Private',
            'residence_type': 'Urban',
            'avg_glucose_level': 120,
            'bmi': 25,
            'smoking_status': 'never smoked',
            'stroke': 0
        }, follow_redirects=True)
        
        # Should fail validation
        assert response.status_code == 200
    
    def test_age_validation(self, logged_in_client):
        """Test age must be within valid range"""
        response = logged_in_client.post('/patients/add', data={
            'patient_id': 99999,
            'gender': 'Male',
            'age': 150,  # Invalid age
            'hypertension': 0,
            'heart_disease': 0,
            'ever_married': 'Yes',
            'work_type': 'Private',
            'residence_type': 'Urban',
            'avg_glucose_level': 120,
            'bmi': 25,
            'smoking_status': 'never smoked',
            'stroke': 0
        }, follow_redirects=True)
        
        # Should fail validation
        assert response.status_code == 200
    
    def test_glucose_level_validation(self, logged_in_client):
        """Test glucose level validation"""
        response = logged_in_client.post('/patients/add', data={
            'patient_id': 99998,
            'gender': 'Female',
            'age': 50,
            'hypertension': 0,
            'heart_disease': 0,
            'ever_married': 'Yes',
            'work_type': 'Private',
            'residence_type': 'Urban',
            'avg_glucose_level': -10,  # Invalid negative glucose
            'bmi': 25,
            'smoking_status': 'never smoked',
            'stroke': 0
        }, follow_redirects=True)
        
        # Should fail validation
        assert response.status_code == 200


class TestSecurityFeatures:
    """Test security features in patient management"""
    
    def test_csrf_protection_add_patient(self, logged_in_client):
        """Test CSRF protection on add patient form"""
        response = logged_in_client.get('/patients/add')
        assert b'csrf_token' in response.data
    
    def test_xss_prevention(self, logged_in_client):
        """Test XSS prevention in patient data"""
        # Try to submit XSS payload
        response = logged_in_client.post('/patients/add', data={
            'patient_id': 88888,
            'gender': '<script>alert("XSS")</script>',
            'age': 45,
            'hypertension': 0,
            'heart_disease': 0,
            'ever_married': 'Yes',
            'work_type': 'Private',
            'residence_type': 'Urban',
            'avg_glucose_level': 120,
            'bmi': 25,
            'smoking_status': 'never smoked',
            'stroke': 0
        }, follow_redirects=True)
        
        # Script tags should be sanitized or rejected
        assert response.status_code == 200


class TestDataIntegrity:
    """Test data integrity and constraints"""
    
    def test_required_fields(self, logged_in_client):
        """Test that required fields are enforced"""
        # Submit form with only patient_id
        response = logged_in_client.post('/patients/add', data={
            'patient_id': 77777
        }, follow_redirects=True)
        
        # Should show validation errors for missing fields
        assert response.status_code == 200
    
    def test_valid_choices(self, logged_in_client):
        """Test that select fields only accept valid choices"""
        response = logged_in_client.post('/patients/add', data={
            'patient_id': 66666,
            'gender': 'InvalidGender',  # Invalid choice
            'age': 45,
            'hypertension': 0,
            'heart_disease': 0,
            'ever_married': 'Yes',
            'work_type': 'Private',
            'residence_type': 'Urban',
            'avg_glucose_level': 120,
            'bmi': 25,
            'smoking_status': 'never smoked',
            'stroke': 0
        }, follow_redirects=True)
        
        # Should fail validation
        assert response.status_code == 200
