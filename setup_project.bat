@echo off
echo ==========================================
echo      Dual-Key Encryption Project Setup
echo ==========================================
echo.

echo [1/3] Installing Backend Dependencies...
cd backend
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Failed to install backend dependencies.
    pause
    exit /b %errorlevel%
)
cd ..
echo Backend dependencies installed.
echo.

echo [2/3] Installing Frontend Dependencies...
cd frontend
call npm install
if %errorlevel% neq 0 (
    echo Failed to install frontend dependencies.
    pause
    exit /b %errorlevel%
)
cd ..
echo Frontend dependencies installed.
echo.

echo [3/3] Setup Complete!
echo.
echo You can now run the application using 'run_app.bat'
echo.
pause
