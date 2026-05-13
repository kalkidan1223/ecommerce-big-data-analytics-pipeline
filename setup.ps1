# Data Pipeline Setup Script for Windows
# Run this script from PowerShell to set up the development environment

$ErrorActionPreference = "Stop"

Write-Host "======================================"
Write-Host "Data Pipeline Setup Script"
Write-Host "======================================"

# Check Python installation
Write-Host "`nChecking Python installation..."
try {
    $pythonVersion = python --version 2>&1
    Write-Host "Found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "Python not found! Please install Python 3.9 or higher." -ForegroundColor Red
    exit 1
}

# Create virtual environment
Write-Host "`nCreating virtual environment..."
if (Test-Path "venv") {
    Write-Host "Virtual environment already exists."
} else {
    python -m venv venv
    Write-Host "Virtual environment created." -ForegroundColor Green
}

# Activate virtual environment
Write-Host "`nActivating virtual environment..."
& ".\venv\Scripts\Activate.ps1"
Write-Host "Virtual environment activated." -ForegroundColor Green

# Upgrade pip
Write-Host "`nUpgrading pip..."
python -m pip install --upgrade pip
Write-Host "pip upgraded." -ForegroundColor Green

# Install requirements
Write-Host "`nInstalling Python dependencies..."
pip install -r requirements.txt
Write-Host "Dependencies installed." -ForegroundColor Green

# Create .env file from template
Write-Host "`nSetting up configuration..."
if (Test-Path ".env") {
    Write-Host ".env file already exists."
} else {
    if (Test-Path ".env.example") {
        Copy-Item ".env.example" ".env"
        Write-Host ".env file created from template." -ForegroundColor Green
        Write-Host "⚠️  Please update .env with your configuration!" -ForegroundColor Yellow
    }
}

# Create necessary directories
Write-Host "`nCreating directory structure..."
$dirs = @(
    "data\raw",
    "data\processed",
    "airflow\logs",
    "airflow\plugins",
    "dbt\analytics\models\staging",
    "dbt\analytics\models\marts\core",
    "dbt\analytics\tests",
    "logs"
)

foreach ($dir in $dirs) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        Write-Host "Created: $dir" -ForegroundColor Green
    }
}

# Initialize Airflow
Write-Host "`nInitializing Airflow..."
$env:AIRFLOW_HOME = ".\airflow"
airflow db init

# Create Airflow user
Write-Host "`nCreating Airflow user..."
airflow users create `
    --username admin `
    --firstname Admin `
    --lastname User `
    --role Admin `
    --email admin@datapipeline.com `
    --password admin | Out-Null
Write-Host "Airflow user 'admin' created (password: admin)" -ForegroundColor Green

Write-Host "`n======================================"
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "======================================"
Write-Host "`nNext steps:"
Write-Host "1. Update .env file with your configuration"
Write-Host "2. Verify data files exist in data/raw/"
Write-Host "3. Run the pipeline: python -m src.pipeline"
Write-Host "4. Or start Airflow:"
Write-Host "   - Scheduler: airflow scheduler"
Write-Host "   - Webserver: airflow webserver --port 8080"
Write-Host "`nFor more information, see README.md"
