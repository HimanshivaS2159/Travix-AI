@echo off
echo.
echo ================================================
echo   Travix AI - Frontend Rebuild Script (DEV)
echo ================================================
echo.

echo [1/5] Stopping frontend container...
docker-compose -f docker-compose.dev.yml down frontend

echo.
echo [2/5] Removing old frontend image...
docker rmi travix-ai-frontend 2>nul

echo.
echo [3/5] Building new frontend image (this may take a few minutes)...
docker-compose -f docker-compose.dev.yml build --no-cache frontend

echo.
echo [4/5] Starting frontend container...
docker-compose -f docker-compose.dev.yml up -d frontend

echo.
echo [5/5] Waiting for container to be ready...
timeout /t 5 /nobreak >nul

echo.
echo ================================================
echo   Frontend rebuild complete!
echo ================================================
echo.
echo   Access the app at: http://localhost:3000
echo   Vite dev server running on port 5173 (mapped to 3000)
echo.
echo   View logs: docker-compose -f docker-compose.dev.yml logs -f frontend
echo.

pause
