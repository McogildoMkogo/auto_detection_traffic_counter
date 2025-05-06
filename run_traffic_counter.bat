@echo off
echo Traffic Counter Setup
echo ====================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed!
    echo Please install Python 3.8 or later from https://www.python.org/downloads/
    pause
    exit /b
)

REM Create and activate virtual environment
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

echo Activating virtual environment...
call venv\Scripts\activate

REM Install requirements
echo Installing required packages...
pip install -r requirements.txt

REM Run the app
echo Starting Traffic Counter...
streamlit run app.py --server.address 0.0.0.0

pause 