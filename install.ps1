# Complete Installation Script for Windows PowerShell
# Stroke Prediction System Setup

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Stroke Prediction System - Installation" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Check Python installation
Write-Host "Step 1: Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version
    Write-Host "✓ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Python not found. Please install Python 3.8 or higher." -ForegroundColor Red
    exit 1
}

# Step 2: Create virtual environment
Write-Host ""
Write-Host "Step 2: Creating virtual environment..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "Virtual environment already exists, skipping..." -ForegroundColor Yellow
} else {
    python -m venv venv
    Write-Host "✓ Virtual environment created" -ForegroundColor Green
}

# Step 3: Activate virtual environment
Write-Host ""
Write-Host "Step 3: Activating virtual environment..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1
Write-Host "✓ Virtual environment activated" -ForegroundColor Green

# Step 4: Upgrade pip
Write-Host ""
Write-Host "Step 4: Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip
Write-Host "✓ Pip upgraded" -ForegroundColor Green

# Step 5: Install dependencies
Write-Host ""
Write-Host "Step 5: Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt
Write-Host "✓ Dependencies installed" -ForegroundColor Green

# Step 6: Check MongoDB
Write-Host ""
Write-Host "Step 6: Checking MongoDB..." -ForegroundColor Yellow
try {
    $mongoService = Get-Service -Name MongoDB -ErrorAction Stop
    if ($mongoService.Status -eq "Running") {
        Write-Host "✓ MongoDB is running" -ForegroundColor Green
    } else {
        Write-Host "! MongoDB service exists but is not running" -ForegroundColor Yellow
        Write-Host "  Starting MongoDB..." -ForegroundColor Yellow
        Start-Service -Name MongoDB
        Write-Host "✓ MongoDB started" -ForegroundColor Green
    }
} catch {
    Write-Host "! MongoDB service not found" -ForegroundColor Yellow
    Write-Host "  Please ensure MongoDB is installed and running" -ForegroundColor Yellow
    Write-Host "  Download from: https://www.mongodb.com/try/download/community" -ForegroundColor Cyan
}

# Step 7: Verify .env file
Write-Host ""
Write-Host "Step 7: Checking environment configuration..." -ForegroundColor Yellow
if (Test-Path ".env") {
    Write-Host "✓ .env file exists" -ForegroundColor Green
} else {
    Write-Host "! .env file not found, copying from .env.example..." -ForegroundColor Yellow
    Copy-Item .env.example .env
    Write-Host "✓ .env file created" -ForegroundColor Green
    Write-Host "  Please review .env and update SECRET_KEY for production" -ForegroundColor Yellow
}

# Step 8: Run tests
Write-Host ""
Write-Host "Step 8: Running tests..." -ForegroundColor Yellow
Write-Host "NOTE: Tests may fail if MongoDB is not running properly" -ForegroundColor Cyan
$testChoice = Read-Host "Do you want to run tests now? (y/n)"
if ($testChoice -eq "y" -or $testChoice -eq "Y") {
    pytest -v
}

# Installation complete
Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "Installation Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Cyan
Write-Host "1. Ensure MongoDB is running" -ForegroundColor White
Write-Host "2. Run the application: python run.py" -ForegroundColor White
Write-Host "3. Open browser: http://127.0.0.1:5000" -ForegroundColor White
Write-Host "4. Register a new account" -ForegroundColor White
Write-Host "5. Start managing patient data!" -ForegroundColor White
Write-Host ""
Write-Host "For detailed instructions, see:" -ForegroundColor Cyan
Write-Host "- README.md (comprehensive guide)" -ForegroundColor White
Write-Host "- QUICKSTART.md (quick start guide)" -ForegroundColor White
Write-Host ""

# Ask if user wants to start the application
$runChoice = Read-Host "Do you want to start the application now? (y/n)"
if ($runChoice -eq "y" -or $runChoice -eq "Y") {
    Write-Host ""
    Write-Host "Starting application..." -ForegroundColor Green
    Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
    Write-Host ""
    python run.py
}
