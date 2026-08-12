# 🐳 Travix AI - Docker Setup Guide

## 🚀 Quick Start

### For Production Build (with Nginx)

```bash
# Windows
rebuild-frontend.bat

# Linux/Mac
bash rebuild-frontend.sh
```

Then visit: **http://localhost:3000**

### For Development Build (with hot reload)

```bash
# Windows
rebuild-frontend-dev.bat

# Linux/Mac
bash rebuild-frontend-dev.sh
```

Then visit: **http://localhost:3000**

---

## 🔧 Manual Commands

### Production Build

```bash
# Stop and remove containers
docker-compose -f docker-compose.yml down

# Build with no cache
docker-compose -f docker-compose.yml build --no-cache frontend

# Start all services
docker-compose -f docker-compose.yml up -d

# View logs
docker-compose -f docker-compose.yml logs -f frontend
```

### Development Build

```bash
# Stop and remove containers
docker-compose -f docker-compose.dev.yml down

# Build with no cache
docker-compose -f docker-compose.dev.yml build --no-cache frontend

# Start all services
docker-compose -f docker-compose.dev.yml up -d

# View logs
docker-compose -f docker-compose.dev.yml logs -f frontend
```

---

## 📋 Architecture

### Production Setup
- **Dockerfile**: Multi-stage build (Node.js → Nginx)
- **Port**: 3000 (Nginx serving on port 80 internally)
- **Features**:
  - Optimized production build
  - Gzip compression
  - Client-side routing support via Nginx
  - Static asset caching
  - Security headers

### Development Setup
- **Dockerfile.dev**: Node.js with Vite dev server
- **Port**: 3000 (mapped from 5173)
- **Features**:
  - Hot module replacement (HMR)
  - Live reload on file changes
  - Volume mounting for instant updates
  - Source maps for debugging

---

## 🗂️ Key Files

### Nginx Configuration (`nginx.conf`)
- Handles client-side routing (React Router)
- Redirects all routes to `index.html`
- Caches static assets
- Security headers

### Docker Compose Files
- `docker-compose.yml` - Production configuration
- `docker-compose.dev.yml` - Development configuration

---

## 🛠️ Troubleshooting

### Issue: 404 errors on routes
**Solution**: This is fixed! The Nginx config now redirects all routes to `index.html`.

### Issue: Changes not reflecting in dev mode
```bash
# Rebuild the dev container
docker-compose -f docker-compose.dev.yml down
docker-compose -f docker-compose.dev.yml build --no-cache frontend
docker-compose -f docker-compose.dev.yml up -d
```

### Issue: Can't access the app
1. Check if container is running:
   ```bash
   docker ps
   ```

2. Check logs for errors:
   ```bash
   docker-compose -f docker-compose.yml logs frontend
   ```

3. Check if port 3000 is available:
   ```bash
   netstat -ano | findstr :3000
   ```

### Issue: Build fails
1. Clear Docker cache:
   ```bash
   docker system prune -a
   ```

2. Remove node_modules and rebuild:
   ```bash
   cd apps/frontend
   rm -rf node_modules package-lock.json
   npm install
   ```

---

## 📱 Application Routes

- **`/`** - Login Page (default)
- **`/dashboard`** - Main Dashboard (after login)
- **`/home`** - Home Page

---

## 🎨 Features

✅ Beautiful animated login page with world map  
✅ AI-powered travel dashboard  
✅ Client-side routing (React Router)  
✅ Dark/Light theme support  
✅ Responsive design  
✅ Docker containerized  
✅ Hot reload in development  
✅ Optimized production build  

---

## 📦 Tech Stack

- **Frontend**: React 19, TypeScript, Vite
- **Styling**: Tailwind CSS v4
- **Routing**: React Router v7
- **Animation**: Framer Motion
- **Icons**: Lucide React
- **Containerization**: Docker, Nginx (production)

---

## 🔐 Environment Variables

No environment variables required for frontend at the moment.
Backend connection will be configured when API integration is added.

---

## 📝 Notes

- The login page automatically navigates to `/dashboard` on sign-in
- In production, implement real authentication
- Google OAuth button is ready for integration
- All forms have proper validation
