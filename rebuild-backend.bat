@echo off
echo.
echo ================================================
echo   Travix AI - Backend Rebuild Script
echo ================================================
echo.

echo [1/4] Stopping backend container...
docker-compose down backend

echo.
echo [2/4] Removing old backend image...
docker rmi travix-ai-backend 2>nul

echo.
echo [3/4] Building new backend image (this may take a few minutes)...
docker-compose build --no-cache backend

echo.
echo [4/4] Starting backend container...
docker-compose up -d backend

echo.
echo ================================================
echo   Backend rebuild complete!
echo ================================================
echo.
echo   Access the backend at: http://localhost:8000
echo   Health check: http://localhost:8000/health
echo.
echo   View logs: docker-compose logs -f backend
echo.

pause
