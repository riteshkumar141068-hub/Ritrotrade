@echo off
title Ritrotrade Frontend (Port 3001)
cd /d "%~dp0service\frontend"

if not exist "node_modules" (
    echo [ERROR] node_modules not found! Running npm install...
    call npm install
)

echo ===================================================
echo Starting Ritrotrade Frontend on http://localhost:3001
echo API calls proxied to Backend on port 8001
echo ===================================================
npm run dev
pause
