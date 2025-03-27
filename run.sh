#!/bin/bash

# Check if virtual environment exists, if not create it
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install requirements
echo "Installing requirements..."
pip install -r requirements.txt

# Initialize database if it doesn't exist
if [ ! -f "project.db" ]; then
    echo "Initializing database..."
    python init_db.py
fi

# Run application
echo "Starting FitCode application..."
python application.py 