# Quick Start Guide - Stroke Prediction System

## 🚀 Quick Setup (5 Minutes)

### Step 1: Prepare Environment

```powershell
# Navigate to project directory
cd c:\Users\dell\Desktop\Dataset

# Create and activate virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### Step 2: Install Dependencies

```powershell
pip install -r requirements.txt
```

### Step 3: Start MongoDB

```powershell
# Start MongoDB service (if installed locally)
net start MongoDB

# Or if using MongoDB installed without service:
# Navigate to MongoDB bin directory and run: mongod
```

### Step 4: Run the Application

```powershell
python run.py
```

### Step 5: Access the Application

Open your browser and go to: **http://127.0.0.1:5000**

---

## 📝 First Steps After Launch

### 1. Create Your Account

- Click "Register" in the navigation bar
- Fill in the form:
  - Username: `admin` (or your choice)
  - Email: `admin@hospital.com`
  - Password: `SecurePass123` (must have uppercase, lowercase, digit)
  - Confirm Password: `SecurePass123`
- Click "Register"

### 2. Login

- Use your username and password to login
- You'll be redirected to the dashboard

### 3. Add Your First Patient

- Click "Add Patient" in the navigation
- Fill in all required fields (example below)
- Click "Submit"

#### Example Patient Data:

```
Patient ID: 1001
Gender: Male
Age: 45
Hypertension: No
Heart Disease: No
Ever Married: Yes
Work Type: Private
Residence Type: Urban
Average Glucose Level: 110.5
BMI: 25.3
Smoking Status: never smoked
Stroke: No
```

---

## 🧪 Quick Test

### Test the Application is Working:

```powershell
# In a new terminal, with venv activated
pytest -v
```

---

## ⚠️ Common Issues

### Issue: MongoDB Not Running

**Error:** `ServerSelectionTimeoutError`
**Fix:** Start MongoDB service

```powershell
net start MongoDB
```

### Issue: Port 5000 Already in Use

**Fix:** Change port in `run.py` from 5000 to 5001

### Issue: Module Not Found

**Fix:** Ensure virtual environment is activated

```powershell
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

---

## 🎯 What to Show Your Instructor

### 1. Security Features Implemented

- ✅ Password hashing (check database - no plain text passwords)
- ✅ CSRF protection (view page source - look for csrf_token)
- ✅ Input validation (try submitting empty forms)
- ✅ Session management (logout and try accessing /dashboard)
- ✅ Secure headers (check browser dev tools - Network tab)

### 2. CRUD Operations

- ✅ Create: Add a patient
- ✅ Read: View patient list and details
- ✅ Update: Edit a patient record
- ✅ Delete: Remove a patient (with confirmation)

### 3. Database Integration

- ✅ SQLite: User authentication (check `users.db` file)
- ✅ MongoDB: Patient records (check MongoDB Compass or shell)

### 4. Testing

```powershell
pytest -v --cov=app tests/
```

### 5. Code Quality

- Professional structure
- Comprehensive comments
- Security best practices
- Error handling

---

## 📊 Verify Databases

### SQLite:

```powershell
# View users database
python -c "from app.models.user import User; from app import create_app, db; app = create_app(); app.app_context().push(); print(User.query.all())"
```

### MongoDB:

```powershell
# Open MongoDB shell
mongosh

# Switch to database
use stroke_prediction

# Count patients
db.patients.countDocuments()

# View patients
db.patients.find().pretty()
```

---

## 🎓 Features Checklist for Assessment

- [x] Flask web application
- [x] SQLite for authentication
- [x] MongoDB for patient data
- [x] User registration/login/logout
- [x] Password hashing
- [x] CSRF protection
- [x] Input validation (WTForms)
- [x] CRUD operations
- [x] Bootstrap UI
- [x] Security headers
- [x] Logging system
- [x] Unit tests
- [x] Professional documentation
- [x] Secure session handling
- [x] XSS prevention
- [x] SQL injection prevention
- [x] Error pages (403, 404, 500)

---

## 💡 Tips for Demonstration

1. **Start with Registration**: Show the password requirements
2. **Show Failed Login**: Demonstrate invalid credentials handling
3. **Add Patient**: Show form validation (try submitting with missing fields)
4. **View Patients**: Demonstrate pagination if you have many records
5. **Edit Patient**: Show that Patient ID cannot be changed
6. **Delete Confirmation**: Show the safety measure before deletion
7. **Security**: Open browser dev tools and show security headers
8. **Tests**: Run pytest and show all tests passing

---

**Ready to go!** Your application is now set up and ready for assessment. Good luck! 🎉
