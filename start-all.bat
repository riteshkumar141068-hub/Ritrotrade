@echo off
title Ritrotrade Launcher
cd /d "%~dp0"

echo ===================================================
echo Launching Ritrotrade Backend & Frontend
echo Backend:  http://127.0.0.1:8001 (Docs: /docs)
echo Frontend: http://localhost:3001
echo ===================================================

start "Ritrotrade Backend" cmd /c "start-backend.bat"
timeout /t 3 /nobreak >nul
start "Ritrotrade Frontend" cmd /c "start-frontend.bat"
timeout /t 2 /nobreak >nul
start http://localhost:3001

echo Both services launched in separate windows!
