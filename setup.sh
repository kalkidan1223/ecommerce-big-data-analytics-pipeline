#!/bin/bash
# Data Pipeline Setup Script for Unix/Linux/macOS
# Run this script to set up the development environment

set -e

echo "======================================"
echo "Data Pipeline Setup Script"
echo "======================================"

# Check Python installation
echo ""
echo "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "Python 3 not found! Please install Python 3.9 or higher."
    exit 1
fi
python_version=$(python3 --version)
echo "Found: $python_version"

# Create virtual environment
echo ""
echo "Creating virtual environment..."
if [ -d "venv" ]; then
    echo "Virtual environment already exists."
else
    python3 -m venv venv
    echo "Virtual environment created."
fi

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source venv/bin/activate
echo "Virtual environment activated."

# Upgrade pip
echo ""
echo "Upgrading pip..."
python -m pip install --upgrade pip
echo "pip upgraded."

# Install requirements
echo ""
echo "Installing Python dependencies..."
pip install -r requirements.txt
echo "Dependencies installed."

# Create .env file from template
echo ""
echo "Setting up configuration..."
if [ -f ".env" ]; then
    echo ".env file already exists."
else
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo ".env file created from template."
        echo "⚠️  Please update .env with your configuration!"
    fi
fi

# Create necessary directories
echo ""
echo "Creating directory structure..."
mkdir -p data/raw data/processed
mkdir -p airflow/logs airflow/plugins
mkdir -p dbt/analytics/models/{staging,marts/core} dbt/analytics/tests
mkdir -p logs

echo "Directories created."

# Initialize Airflow
echo ""
echo "Initializing Airflow..."
export AIRFLOW_HOME=./airflow
airflow db init

# Create Airflow user
echo ""
echo "Creating Airflow user..."
airflow users create \
    --username admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@datapipeline.com \
    --password admin || true
echo "Airflow user 'admin' created (password: admin)"

echo ""
echo "======================================"
echo "Setup Complete!"
echo "======================================"
echo ""
echo "Next steps:"
echo "1. Update .env file with your configuration"
echo "2. Verify data files exist in data/raw/"
echo "3. Run the pipeline: python -m src.pipeline"
echo "4. Or start Airflow:"
echo "   - Scheduler: airflow scheduler"
echo "   - Webserver: airflow webserver --port 8080"
echo ""
echo "For more information, see README.md"
