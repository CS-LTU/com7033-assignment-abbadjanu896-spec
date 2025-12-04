"""
Patient management routes module
Handles CRUD operations for patient records with security
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app.utils.validators import PatientForm
from app.utils.validators import UpdatePatientForm
from app.utils.security import log_security_event, sanitize_input
from app import mongo_db
import logging

# Configure logging
logger = logging.getLogger(__name__)

# Create Blueprint
patient_bp = Blueprint('patient', __name__, url_prefix='/patients')


@patient_bp.route('/')
@login_required
def list_patients():
    """
    Display list of all patients
    Implements pagination for better performance
    """
    try:
        # Get pagination parameters
        page = request.args.get('page', 1, type=int)
        per_page = 20
        skip = (page - 1) * per_page
        
        # Retrieve patients from MongoDB
        patients = mongo_db.get_all_patients(skip=skip, limit=per_page)
        total_count = mongo_db.get_patient_count()
        total_pages = (total_count + per_page - 1) // per_page
        
        return render_template(
            'patients/list.html',
            patients=patients,
            page=page,
            total_pages=total_pages,
            total_count=total_count,
            title='Patient List'
        )
    except Exception as e:
        logger.error(f"Error listing patients: {str(e)}")
        flash('An error occurred while retrieving patient records.', 'danger')
        return redirect(url_for('main.dashboard'))


@patient_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_patient():
    """
    Add new patient record
    Validates input and prevents duplicate patient IDs
    """
    form = PatientForm()
    
    if form.validate_on_submit():
        try:
            # Prepare patient data
            patient_data = {
                'patient_id': int(form.patient_id.data),
                'gender': sanitize_input(form.gender.data),
                'age': float(form.age.data),
                'hypertension': int(form.hypertension.data),
                'heart_disease': int(form.heart_disease.data),
                'ever_married': sanitize_input(form.ever_married.data),
                'work_type': sanitize_input(form.work_type.data),
                'residence_type': sanitize_input(form.residence_type.data),
                'avg_glucose_level': float(form.avg_glucose_level.data),
                'bmi': float(form.bmi.data) if form.bmi.data else None,
                'smoking_status': sanitize_input(form.smoking_status.data),
                'stroke': int(form.stroke.data),
                'created_by': current_user.id
            }
            
            # Check if patient ID already exists
            existing = mongo_db.search_patients({'patient_id': patient_data['patient_id']})
            if existing:
                flash(f"Patient ID {patient_data['patient_id']} already exists.", 'warning')
                return render_template('patients/add.html', form=form, title='Add Patient')
            
            # Insert patient record
            patient_id = mongo_db.create_patient(patient_data)
            
            if patient_id:
                log_security_event('PATIENT_CREATED', user_id=current_user.id, 
                                 details=f"Patient ID: {patient_data['patient_id']}")
                flash('Patient record added successfully!', 'success')
                logger.info(f"Patient added by user {current_user.username}: ID {patient_data['patient_id']}")
                return redirect(url_for('patient.list_patients'))
            else:
                flash('Failed to add patient record. Please try again.', 'danger')
                
        except ValueError as e:
            flash('Invalid input data. Please check your entries.', 'danger')
            logger.error(f"Validation error in add_patient: {str(e)}")
        except Exception as e:
            logger.error(f"Error adding patient: {str(e)}")
            flash('An error occurred while adding the patient record.', 'danger')
    
    return render_template('patients/add.html', form=form, title='Add Patient')


@patient_bp.route('/view/<patient_id>')
@login_required
def view_patient(patient_id):
    """
    View detailed patient information
    """
    try:
        patient = mongo_db.get_patient_by_id(patient_id)
        
        if not patient:
            flash('Patient record not found.', 'warning')
            return redirect(url_for('patient.list_patients'))
        
        return render_template('patients/view.html', patient=patient, title='View Patient')
        
    except Exception as e:
        logger.error(f"Error viewing patient: {str(e)}")
        flash('An error occurred while retrieving patient details.', 'danger')
        return redirect(url_for('patient.list_patients'))


@patient_bp.route('/edit/<patient_id>', methods=['GET', 'POST'])
@login_required
def edit_patient(patient_id):
    """
    Edit existing patient record
    Patient ID cannot be changed for data integrity
    """
    try:
        patient = mongo_db.get_patient_by_id(patient_id)
        
        if not patient:
            flash('Patient record not found.', 'warning')
            return redirect(url_for('patient.list_patients'))
        
        form = UpdatePatientForm()
        
        if form.validate_on_submit():
            # Prepare update data
            update_data = {
                'gender': sanitize_input(form.gender.data),
                'age': float(form.age.data),
                'hypertension': int(form.hypertension.data),
                'heart_disease': int(form.heart_disease.data),
                'ever_married': sanitize_input(form.ever_married.data),
                'work_type': sanitize_input(form.work_type.data),
                'residence_type': sanitize_input(form.residence_type.data),
                'avg_glucose_level': float(form.avg_glucose_level.data),
                'bmi': float(form.bmi.data) if form.bmi.data else None,
                'smoking_status': sanitize_input(form.smoking_status.data),
                'stroke': int(form.stroke.data),
                'updated_by': current_user.id
            }
            
            # Update patient record
            success = mongo_db.update_patient(patient_id, update_data)
            
            if success:
                log_security_event('PATIENT_UPDATED', user_id=current_user.id, 
                                 details=f"Patient MongoDB ID: {patient_id}")
                flash('Patient record updated successfully!', 'success')
                logger.info(f"Patient updated by user {current_user.username}: ID {patient_id}")
                return redirect(url_for('patient.view_patient', patient_id=patient_id))
            else:
                flash('Failed to update patient record. Please try again.', 'danger')
        
        # Pre-populate form with existing data
        elif request.method == 'GET':
            form.gender.data = patient.get('gender')
            form.age.data = patient.get('age')
            form.hypertension.data = str(patient.get('hypertension'))
            form.heart_disease.data = str(patient.get('heart_disease'))
            form.ever_married.data = patient.get('ever_married')
            form.work_type.data = patient.get('work_type')
            form.residence_type.data = patient.get('residence_type')
            form.avg_glucose_level.data = patient.get('avg_glucose_level')
            form.bmi.data = patient.get('bmi')
            form.smoking_status.data = patient.get('smoking_status')
            form.stroke.data = str(patient.get('stroke'))
        
        return render_template('patients/edit.html', form=form, patient=patient, title='Edit Patient')
        
    except Exception as e:
        logger.error(f"Error editing patient: {str(e)}")
        flash('An error occurred while editing patient record.', 'danger')
        return redirect(url_for('patient.list_patients'))


@patient_bp.route('/delete/<patient_id>', methods=['GET', 'POST'])
@login_required
def delete_patient(patient_id):
    """
    Delete patient record with confirmation
    """
    try:
        patient = mongo_db.get_patient_by_id(patient_id)
        
        if not patient:
            flash('Patient record not found.', 'warning')
            return redirect(url_for('patient.list_patients'))
        
        if request.method == 'POST':
            # Perform deletion
            success = mongo_db.delete_patient(patient_id)
            
            if success:
                log_security_event('PATIENT_DELETED', user_id=current_user.id, 
                                 details=f"Patient MongoDB ID: {patient_id}")
                flash('Patient record deleted successfully.', 'success')
                logger.info(f"Patient deleted by user {current_user.username}: ID {patient_id}")
                return redirect(url_for('patient.list_patients'))
            else:
                flash('Failed to delete patient record. Please try again.', 'danger')
        
        return render_template('patients/delete.html', patient=patient, title='Delete Patient')
        
    except Exception as e:
        logger.error(f"Error deleting patient: {str(e)}")
        flash('An error occurred while deleting patient record.', 'danger')
        return redirect(url_for('patient.list_patients'))


@patient_bp.route('/search')
@login_required
def search_patients():
    """
    Search patients by various criteria
    """
    try:
        query = {}
        search_term = request.args.get('q', '').strip()
        
        if search_term:
            # Build search query
            if search_term.isdigit():
                query['patient_id'] = int(search_term)
            else:
                # Search by gender, work_type, etc.
                query = {
                    '$or': [
                        {'gender': {'$regex': search_term, '$options': 'i'}},
                        {'work_type': {'$regex': search_term, '$options': 'i'}},
                        {'smoking_status': {'$regex': search_term, '$options': 'i'}}
                    ]
                }
        
        patients = mongo_db.search_patients(query) if query else []
        
        return render_template(
            'patients/search.html',
            patients=patients,
            search_term=search_term,
            title='Search Patients'
        )
        
    except Exception as e:
        logger.error(f"Error searching patients: {str(e)}")
        flash('An error occurred during search.', 'danger')
        return redirect(url_for('patient.list_patients'))
