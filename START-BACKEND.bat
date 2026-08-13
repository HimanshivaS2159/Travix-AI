@echo off
echo Starting Travix-AI Backend Server...
echo.
cd apps\backend
python -m uvicorn app.main:app --reload --port 8000 --host 0.0.0.0
pause
