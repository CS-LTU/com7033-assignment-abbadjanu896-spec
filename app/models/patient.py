"""
Patient data management module for MongoDB operations
Implements CRUD operations for stroke prediction patient records
"""
from pymongo import MongoClient, ASCENDING
from pymongo.errors import PyMongoError, DuplicateKeyError
from bson.objectid import ObjectId
from datetime import datetime
import logging

# Configure logging
logger = logging.getLogger(__name__)


class PatientDatabase:
    """
    MongoDB database handler for patient records
    Implements secure CRUD operations with validation
    """
    
    def __init__(self, uri, db_name):
        """
        Initialize MongoDB connection
        
        Args:
            uri (str): MongoDB connection URI
            db_name (str): Database name
        """
        try:
            self.client = MongoClient(uri)
            self.db = self.client[db_name]
            self.collection = self.db['patients']
            self._create_indexes()
            logger.info("MongoDB connection established successfully")
        except PyMongoError as e:
            logger.error(f"Failed to connect to MongoDB: {str(e)}")
            raise
    
    def _create_indexes(self):
        """Create indexes for better query performance"""
        try:
            # Create index on patient_id for faster lookups
            self.collection.create_index([('patient_id', ASCENDING)], unique=True, sparse=True)
            logger.info("MongoDB indexes created successfully")
        except PyMongoError as e:
            logger.warning(f"Index creation warning: {str(e)}")
    
    def create_patient(self, patient_data):
        """
        Create a new patient record
        
        Args:
            patient_data (dict): Patient information
            
        Returns:
            str: Inserted document ID or None if failed
        """
        try:
            # Add timestamp
            patient_data['created_at'] = datetime.utcnow()
            patient_data['updated_at'] = datetime.utcnow()
            
            result = self.collection.insert_one(patient_data)
            logger.info(f"Patient record created with ID: {result.inserted_id}")
            return str(result.inserted_id)
        except DuplicateKeyError:
            logger.error("Patient ID already exists")
            return None
        except PyMongoError as e:
            logger.error(f"Error creating patient record: {str(e)}")
            return None
    
    def get_patient_by_id(self, patient_id):
        """
        Retrieve a patient record by MongoDB ObjectId
        
        Args:
            patient_id (str): MongoDB document ID
            
        Returns:
            dict: Patient record or None if not found
        """
        try:
            patient = self.collection.find_one({'_id': ObjectId(patient_id)})
            if patient:
                patient['_id'] = str(patient['_id'])
            return patient
        except Exception as e:
            logger.error(f"Error retrieving patient: {str(e)}")
            return None
    
    def get_all_patients(self, skip=0, limit=100):
        """
        Retrieve all patient records with pagination
        
        Args:
            skip (int): Number of records to skip
            limit (int): Maximum number of records to return
            
        Returns:
            list: List of patient records
        """
        try:
            patients = list(self.collection.find().skip(skip).limit(limit).sort('created_at', -1))
            for patient in patients:
                patient['_id'] = str(patient['_id'])
            return patients
        except PyMongoError as e:
            logger.error(f"Error retrieving patients: {str(e)}")
            return []
    
    def update_patient(self, patient_id, update_data):
        """
        Update an existing patient record
        
        Args:
            patient_id (str): MongoDB document ID
            update_data (dict): Fields to update
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Add update timestamp
            update_data['updated_at'] = datetime.utcnow()
            
            result = self.collection.update_one(
                {'_id': ObjectId(patient_id)},
                {'$set': update_data}
            )
            
            if result.modified_count > 0:
                logger.info(f"Patient record updated: {patient_id}")
                return True
            return False
        except PyMongoError as e:
            logger.error(f"Error updating patient: {str(e)}")
            return False
    
    def delete_patient(self, patient_id):
        """
        Delete a patient record
        
        Args:
            patient_id (str): MongoDB document ID
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            result = self.collection.delete_one({'_id': ObjectId(patient_id)})
            if result.deleted_count > 0:
                logger.info(f"Patient record deleted: {patient_id}")
                return True
            return False
        except PyMongoError as e:
            logger.error(f"Error deleting patient: {str(e)}")
            return False
    
    def search_patients(self, query):
        """
        Search patients by various fields
        
        Args:
            query (dict): Search criteria
            
        Returns:
            list: Matching patient records
        """
        try:
            patients = list(self.collection.find(query))
            for patient in patients:
                patient['_id'] = str(patient['_id'])
            return patients
        except PyMongoError as e:
            logger.error(f"Error searching patients: {str(e)}")
            return []
    
    def get_patient_count(self):
        """
        Get total number of patient records
        
        Returns:
            int: Total count of patients
        """
        try:
            return self.collection.count_documents({})
        except PyMongoError as e:
            logger.error(f"Error counting patients: {str(e)}")
            return 0
    
    def close(self):
        """Close MongoDB connection"""
        self.client.close()
        logger.info("MongoDB connection closed")
