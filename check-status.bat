@echo off
echo.
echo ================================================
echo   Travix AI - Status Check
echo ================================================
echo.

echo [Docker Containers]
echo -------------------
docker ps --filter "name=travix" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

echo.
echo [Frontend Container Logs (last 20 lines)]
echo -------------------------------------------
docker logs travix-ai-frontend-1 --tail 20 2>nul || docker logs travix_ai_frontend_1 --tail 20 2>nul || echo Frontend container not found

echo.
echo [Network Check]
echo ---------------
echo Checking if port 3000 is listening...
netstat -ano | findstr :3000

echo.
echo [Quick Commands]
echo ----------------
echo View live logs:     docker-compose logs -f frontend
echo Restart frontend:   docker-compose restart frontend
echo Rebuild frontend:   rebuild-frontend.bat
echo.

pause
