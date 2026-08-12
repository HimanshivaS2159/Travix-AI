#!/bin/bash

# Script to rebuild and restart the frontend service in Docker

echo "🔄 Stopping frontend container..."
docker-compose -f docker-compose.yml down frontend

echo "🗑️  Removing old frontend image..."
docker rmi travix-ai-frontend 2>/dev/null || true

echo "🔨 Building new frontend image..."
docker-compose -f docker-compose.yml build --no-cache frontend

echo "🚀 Starting frontend container..."
docker-compose -f docker-compose.yml up -d frontend

echo "✅ Frontend rebuild complete!"
echo "📱 Access the app at: http://localhost:3000"

echo ""
echo "📋 View logs with: docker-compose -f docker-compose.yml logs -f frontend"
