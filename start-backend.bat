@echo off
title Ritrotrade Backend Server (Port 8001)
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo [ERROR] Virtual environment not found in .venv!
    echo Please run setup first.
    pause
    exit /b 1
)

echo ===================================================
echo Starting Ritrotrade Backend on http://127.0.0.1:8001
echo Swagger API Docs available at http://127.0.0.1:8001/docs
echo ===================================================
call .venv\Scripts\activate.bat
python -m uvicorn main:app --app-dir service/server --port 8001
pause
