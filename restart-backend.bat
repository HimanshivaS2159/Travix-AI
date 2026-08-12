@echo off
echo.
echo ================================================
echo   Travix AI - Backend Restart Script
echo ================================================
echo.

echo [1/2] Restarting backend container with new environment...
docker-compose restart backend

echo.
echo [2/2] Waiting for backend to be ready...
timeout /t 3 /nobreak >nul

echo.
echo ================================================
echo   Backend restarted!
echo ================================================
echo.
echo   Health check: http://localhost:8000/health
echo   View logs: docker-compose logs -f backend
echo.

pause
