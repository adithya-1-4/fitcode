@echo off
echo FitCode Application Setup

REM Check if virtual environment exists, if not create it
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate

REM Install requirements
echo Installing requirements...
pip install -r requirements.txt

REM Initialize database if it doesn't exist
if not exist project.db (
    echo Initializing database...
    python init_db.py
)

REM Run application
echo Starting FitCode application...
python application.py 