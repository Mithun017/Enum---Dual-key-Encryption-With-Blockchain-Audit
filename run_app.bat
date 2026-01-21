@echo off
echo Starting Blockchain-Based Dual-Key Encryption System...

echo Starting Backend Server...
start "Backend Server" cmd /k "cd backend && uvicorn app.main:app --reload"

echo Starting Frontend Server...
start "Frontend Server" cmd /k "cd frontend && npm run dev"

echo System is starting up...
echo Backend: http://127.0.0.1:8000
echo Frontend: http://localhost:5173

timeout /t 2 >nul
start http://localhost:5173
