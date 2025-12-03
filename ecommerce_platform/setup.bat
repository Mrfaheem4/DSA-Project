@echo off
REM Setup script for TechStore E-commerce Platform

echo.
echo ============================================
echo TechStore - E-commerce Platform Setup
echo ============================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/
    exit /b 1
)

echo [1/3] Python found: 
python --version

echo.
echo [2/3] Installing Python dependencies...
cd backend
pip install -r requirements.txt
cd ..

echo.
echo [3/3] Setup complete!

echo.
echo ============================================
echo Next Steps:
echo ============================================
echo.
echo 1. Open Terminal 1 and run:
echo    cd backend
echo    python app.py
echo.
echo 2. Open Terminal 2 and run:
echo    cd frontend
echo    python -m http.server 8000
echo.
echo 3. Open your browser and visit:
echo    http://localhost:8000
echo.
echo ============================================
echo API will be available at: http://localhost:5000/api
echo ============================================
echo.
pause
