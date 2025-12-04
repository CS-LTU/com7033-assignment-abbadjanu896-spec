"""
Form validation module using Flask-WTF and WTForms
Implements secure input validation and CSRF protection
"""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, FloatField, IntegerField
from wtforms.validators import (
    DataRequired, Email, EqualTo, Length, ValidationError,
    NumberRange, Optional, Regexp
)
from app.models.user import User


class RegistrationForm(FlaskForm):
    """
    User registration form with validation
    Implements input sanitization and validation rules
    """
    username = StringField(
        'Username',
        validators=[
            DataRequired(message='Username is required'),
            Length(min=3, max=80, message='Username must be between 3 and 80 characters'),
            Regexp('^[A-Za-z0-9_]+$', message='Username must contain only letters, numbers, and underscores')
        ],
        render_kw={'placeholder': 'Enter username', 'class': 'form-control'}
    )
    
    email = StringField(
        'Email',
        validators=[
            DataRequired(message='Email is required'),
            Email(message='Invalid email address'),
            Length(max=120, message='Email must be less than 120 characters')
        ],
        render_kw={'placeholder': 'Enter email', 'class': 'form-control'}
    )
    
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(message='Password is required'),
            Length(min=8, max=128, message='Password must be between 8 and 128 characters'),
            Regexp(
                r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)',
                message='Password must contain at least one uppercase letter, one lowercase letter, and one digit'
            )
        ],
        render_kw={'placeholder': 'Enter password', 'class': 'form-control'}
    )
    
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[
            DataRequired(message='Please confirm your password'),
            EqualTo('password', message='Passwords must match')
        ],
        render_kw={'placeholder': 'Confirm password', 'class': 'form-control'}
    )
    
    submit = SubmitField('Register', render_kw={'class': 'btn btn-primary btn-block'})
    
    def validate_username(self, username):
        """Check if username already exists"""
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already taken. Please choose a different one.')
    
    def validate_email(self, email):
        """Check if email already exists"""
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered. Please use a different one.')


class LoginForm(FlaskForm):
    """
    User login form with validation
    """
    username = StringField(
        'Username',
        validators=[
            DataRequired(message='Username is required'),
            Length(min=3, max=80, message='Invalid username')
        ],
        render_kw={'placeholder': 'Enter username', 'class': 'form-control'}
    )
    
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(message='Password is required')
        ],
        render_kw={'placeholder': 'Enter password', 'class': 'form-control'}
    )
    
    submit = SubmitField('Login', render_kw={'class': 'btn btn-primary btn-block'})


class PatientForm(FlaskForm):
    """
    Patient data form with comprehensive validation
    Based on Stroke Prediction Dataset schema
    """
    # Patient identification
    patient_id = IntegerField(
        'Patient ID',
        validators=[
            DataRequired(message='Patient ID is required'),
            NumberRange(min=1, max=999999, message='Invalid Patient ID')
        ],
        render_kw={'placeholder': 'Enter patient ID', 'class': 'form-control'}
    )
    
    # Demographics
    gender = SelectField(
        'Gender',
        choices=[('', 'Select Gender'), ('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')],
        validators=[DataRequired(message='Gender is required')],
        render_kw={'class': 'form-control'}
    )
    
    age = FloatField(
        'Age',
        validators=[
            DataRequired(message='Age is required'),
            NumberRange(min=0, max=120, message='Age must be between 0 and 120')
        ],
        render_kw={'placeholder': 'Enter age', 'class': 'form-control'}
    )
    
    # Medical history
    hypertension = SelectField(
        'Hypertension',
        choices=[('', 'Select'), ('0', 'No'), ('1', 'Yes')],
        validators=[DataRequired(message='Hypertension status is required')],
        render_kw={'class': 'form-control'}
    )
    
    heart_disease = SelectField(
        'Heart Disease',
        choices=[('', 'Select'), ('0', 'No'), ('1', 'Yes')],
        validators=[DataRequired(message='Heart disease status is required')],
        render_kw={'class': 'form-control'}
    )
    
    ever_married = SelectField(
        'Ever Married',
        choices=[('', 'Select'), ('Yes', 'Yes'), ('No', 'No')],
        validators=[DataRequired(message='Marital status is required')],
        render_kw={'class': 'form-control'}
    )
    
    # Lifestyle and occupation
    work_type = SelectField(
        'Work Type',
        choices=[
            ('', 'Select Work Type'),
            ('Private', 'Private'),
            ('Self-employed', 'Self-employed'),
            ('Govt_job', 'Government Job'),
            ('children', 'Children'),
            ('Never_worked', 'Never Worked')
        ],
        validators=[DataRequired(message='Work type is required')],
        render_kw={'class': 'form-control'}
    )
    
    residence_type = SelectField(
        'Residence Type',
        choices=[('', 'Select'), ('Urban', 'Urban'), ('Rural', 'Rural')],
        validators=[DataRequired(message='Residence type is required')],
        render_kw={'class': 'form-control'}
    )
    
    # Health metrics
    avg_glucose_level = FloatField(
        'Average Glucose Level',
        validators=[
            DataRequired(message='Average glucose level is required'),
            NumberRange(min=0, max=500, message='Glucose level must be between 0 and 500')
        ],
        render_kw={'placeholder': 'Enter glucose level (mg/dL)', 'class': 'form-control'}
    )
    
    bmi = FloatField(
        'BMI',
        validators=[
            Optional(),
            NumberRange(min=10, max=100, message='BMI must be between 10 and 100')
        ],
        render_kw={'placeholder': 'Enter BMI (optional)', 'class': 'form-control'}
    )
    
    smoking_status = SelectField(
        'Smoking Status',
        choices=[
            ('', 'Select Smoking Status'),
            ('formerly smoked', 'Formerly Smoked'),
            ('never smoked', 'Never Smoked'),
            ('smokes', 'Smokes'),
            ('Unknown', 'Unknown')
        ],
        validators=[DataRequired(message='Smoking status is required')],
        render_kw={'class': 'form-control'}
    )
    
    # Outcome
    stroke = SelectField(
        'Stroke',
        choices=[('', 'Select'), ('0', 'No'), ('1', 'Yes')],
        validators=[DataRequired(message='Stroke status is required')],
        render_kw={'class': 'form-control'}
    )
    
    submit = SubmitField('Submit', render_kw={'class': 'btn btn-success'})


class UpdatePatientForm(FlaskForm):
    """
    Patient update form (without patient_id as it's not editable)
    """
    # Demographics
    gender = SelectField(
        'Gender',
        choices=[('', 'Select Gender'), ('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')],
        validators=[DataRequired(message='Gender is required')],
        render_kw={'class': 'form-control'}
    )
    
    age = FloatField(
        'Age',
        validators=[
            DataRequired(message='Age is required'),
            NumberRange(min=0, max=120, message='Age must be between 0 and 120')
        ],
        render_kw={'placeholder': 'Enter age', 'class': 'form-control'}
    )
    
    # Medical history
    hypertension = SelectField(
        'Hypertension',
        choices=[('', 'Select'), ('0', 'No'), ('1', 'Yes')],
        validators=[DataRequired(message='Hypertension status is required')],
        render_kw={'class': 'form-control'}
    )
    
    heart_disease = SelectField(
        'Heart Disease',
        choices=[('', 'Select'), ('0', 'No'), ('1', 'Yes')],
        validators=[DataRequired(message='Heart disease status is required')],
        render_kw={'class': 'form-control'}
    )
    
    ever_married = SelectField(
        'Ever Married',
        choices=[('', 'Select'), ('Yes', 'Yes'), ('No', 'No')],
        validators=[DataRequired(message='Marital status is required')],
        render_kw={'class': 'form-control'}
    )
    
    # Lifestyle and occupation
    work_type = SelectField(
        'Work Type',
        choices=[
            ('', 'Select Work Type'),
            ('Private', 'Private'),
            ('Self-employed', 'Self-employed'),
            ('Govt_job', 'Government Job'),
            ('children', 'Children'),
            ('Never_worked', 'Never Worked')
        ],
        validators=[DataRequired(message='Work type is required')],
        render_kw={'class': 'form-control'}
    )
    
    residence_type = SelectField(
        'Residence Type',
        choices=[('', 'Select'), ('Urban', 'Urban'), ('Rural', 'Rural')],
        validators=[DataRequired(message='Residence type is required')],
        render_kw={'class': 'form-control'}
    )
    
    # Health metrics
    avg_glucose_level = FloatField(
        'Average Glucose Level',
        validators=[
            DataRequired(message='Average glucose level is required'),
            NumberRange(min=0, max=500, message='Glucose level must be between 0 and 500')
        ],
        render_kw={'placeholder': 'Enter glucose level (mg/dL)', 'class': 'form-control'}
    )
    
    bmi = FloatField(
        'BMI',
        validators=[
            Optional(),
            NumberRange(min=10, max=100, message='BMI must be between 10 and 100')
        ],
        render_kw={'placeholder': 'Enter BMI (optional)', 'class': 'form-control'}
    )
    
    smoking_status = SelectField(
        'Smoking Status',
        choices=[
            ('', 'Select Smoking Status'),
            ('formerly smoked', 'Formerly Smoked'),
            ('never smoked', 'Never Smoked'),
            ('smokes', 'Smokes'),
            ('Unknown', 'Unknown')
        ],
        validators=[DataRequired(message='Smoking status is required')],
        render_kw={'class': 'form-control'}
    )
    
    # Outcome
    stroke = SelectField(
        'Stroke',
        choices=[('', 'Select'), ('0', 'No'), ('1', 'Yes')],
        validators=[DataRequired(message='Stroke status is required')],
        render_kw={'class': 'form-control'}
    )
    
    submit = SubmitField('Update', render_kw={'class': 'btn btn-primary'})
