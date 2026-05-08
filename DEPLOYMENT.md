# Deployment Guide - Render

This guide walks you through deploying the Task Management Application on Render (backend + PostgreSQL database + static frontend).

## Prerequisites

- Render account ([render.com](https://render.com)) - free tier available
- GitHub repository with your code
- Basic understanding of environment variables

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Render Platform                      │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌──────────────────┐     ┌──────────────────────────┐ │
│  │  Static Site     │     │   Web Service (FastAPI) │ │
│  │  (React Frontend)│     │   (Python Backend)      │ │
│  │  Port: 443       │────▶│   Port: 8000            │ │
│  └──────────────────┘     └──────────────────────────┘ │
│                                    ▲                    │
│                                    │                    │
│                           ┌────────▼─────────┐         │
│                           │  PostgreSQL DB   │         │
│                           │  (Internal)      │         │
│                           └──────────────────┘         │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## Quick Deploy (5-10 minutes)

### Option 1: Using render.yaml (Recommended)

This repository includes a `render.yaml` file for easy deployment.

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Ready for production deployment"
   git push origin main
   ```

2. **Create Render Account & Connect GitHub**
   - Go to [render.com](https://render.com)
   - Sign up (free tier available)
   - Connect your GitHub account

3. **Deploy with render.yaml**
   - From Render Dashboard, click **New** → **Blueprint**
   - Select your GitHub repository
   - Render will auto-detect `render.yaml` and configure everything
   - Review the configuration and click **Create New Service**
   - Wait for deployment (5-10 minutes)

4. **Update Environment Variables**
   - Go to backend service settings
   - Update `SECRET_KEY` with a secure value (use Render-generated value)
   - Verify `DATABASE_URL` is populated from database
   - Set `CORS_ORIGINS` to your frontend URL

### Option 2: Manual Deployment (Step-by-Step)

#### Step 1: Create PostgreSQL Database

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click **New +** → **PostgreSQL**
3. Configure:
   - **Name**: `task_manager_db`
   - **Database**: `task_manager`
   - **Region**: Select your region (e.g., Oregon)
   - **PostgreSQL Version**: 15 or latest
4. Click **Create**
5. **Important**: Copy the **Internal Database URL** from the connection string
   - Format: `postgresql://username:password@hostname:5432/task_manager`
   - Save this for backend configuration

#### Step 2: Deploy Backend API

1. Click **New +** → **Web Service**
2. Connect your GitHub repository
3. Configure Web Service:
   - **Name**: `task-management-api`
   - **Environment**: Python 3
   - **Build Command**: 
     ```bash
     pip install -r backend/requirements.txt
     ```
   - **Start Command**: 
     ```bash
     gunicorn -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000 backend.app.main:app
     ```
   - **Region**: Same as database (e.g., Oregon)
   - **Plan**: Free (paid plan available for production)

4. Add Environment Variables (in Settings → Environment):
   ```
   DATABASE_URL           = postgresql://user:password@hostname/task_manager
   SECRET_KEY            = [Generate: python -c "import secrets; print(secrets.token_urlsafe(32))"]
   DEBUG                 = False
   ENVIRONMENT           = production
   CORS_ORIGINS          = http://localhost:5173  (will update after frontend deploy)
   ACCESS_TOKEN_EXPIRE_MINUTES = 30
   REFRESH_TOKEN_EXPIRE_DAYS = 7
   ```

5. Click **Create Web Service**
6. Wait for deployment (~5 minutes)
7. Note your backend URL: `https://task-management-api.onrender.com`

#### Step 3: Deploy Frontend

1. Click **New +** → **Static Site**
2. Connect your GitHub repository
3. Configure Static Site:
   - **Name**: `task-management-ui`
   - **Build Command**: 
     ```bash
     cd frontend && npm install && npm run build
     ```
   - **Publish Directory**: `frontend/dist`
4. Click **Create Static Site**
5. Wait for deployment (~3 minutes)
6. Note your frontend URL: `https://task-management-ui.onrender.com`

#### Step 4: Update Backend CORS

1. Go to backend web service
2. Go to **Environment** in Settings
3. Update `CORS_ORIGINS`:
   ```
   https://task-management-ui.onrender.com,https://www.task-management-ui.onrender.com
   ```
4. Click **Save** (automatic redeployment)

#### Step 5: Verify Frontend .env

Create `frontend/.env.production`:
```env
VITE_API_URL=https://task-management-api.onrender.com
```

Or set as Render environment variable:
- Go to frontend static site settings
- Add environment variable: `VITE_API_URL=https://task-management-api.onrender.com`
- Redeploy

## Testing Your Deployment

1. **Test Frontend**
   - Visit `https://task-management-ui.onrender.com`
   - Should see login page

2. **Test Backend Health Check**
   - Visit `https://task-management-api.onrender.com/health`
   - Should return: `{"status":"healthy","app":"Task Management API","version":"1.0.0"}`

3. **Test API Documentation**
   - Visit `https://task-management-api.onrender.com/api/docs`
   - Should see Swagger UI

4. **Test Full Workflow**
   - Register new user in frontend
   - Create a task
   - Verify data persists

## Troubleshooting

### Backend Deployment Issues

**Build Failed: Module not found**
```
Solution: Ensure requirements.txt is in backend/ directory
Check: build command includes full path if needed
```

**Build Failed: Connection string error**
```
Solution: Verify DATABASE_URL environment variable is set
Format: postgresql://user:password@host:port/database
```

**Build Failed: Gunicorn not found**
```
Solution: Add gunicorn==21.2.0 to requirements.txt
Rebuild the service from dashboard
```

**Service crashes on startup**
```
Solution: Check logs in Render dashboard
Verify SECRET_KEY is at least 32 characters
Ensure database is ready and accessible
```

### Frontend Deployment Issues

**Static site not building**
```
Solution: Verify build command: cd frontend && npm install && npm run build
Check: package.json exists in frontend/
Ensure: npm scripts include "build"
```

**Frontend can't connect to backend**
```
Solution: Verify VITE_API_URL points to backend URL
Check: Backend CORS includes frontend URL
Clear: Browser cache (Ctrl+Shift+Del)
Hard refresh: Ctrl+Shift+R
```

**404 error on page refresh**
```
Solution: This is normal for SPA routes
Add: Render's auto-redirect for single-page apps
Configure in static site settings if needed
```

### Database Issues

**Connection refused**
```
Solution: Verify database is running in Render dashboard
Check: DATABASE_URL environment variable is correct
Ensure: PostgreSQL service is in same region
```

**Database not found**
```
Solution: Create database manually in PostgreSQL
Command in psql: CREATE DATABASE task_manager;
```

### CORS Errors

**"No 'Access-Control-Allow-Origin' header"**
```
Solution: Add frontend URL to backend CORS_ORIGINS
Format: https://your-frontend-domain.com
Redeploy backend
```

## Monitoring & Logs

### View Logs
1. Go to your service in Render dashboard
2. Click **Logs** tab
3. Search for errors or issues
4. Check recent activity

### Health Checks
- Backend health: `GET /health`
- Render automatically monitors services
- Get alerts if service crashes

## Database Backups

Render PostgreSQL provides:
- **Free tier**: 7-day automatic backups
- **Paid tier**: 30-day automatic backups

To backup manually:
```bash
pg_dump -U username -h hostname -d task_manager > backup.sql
```

## Scaling Considerations

### Free Tier Limits
- 750 hours/month compute (enough for 1 service always running)
- 0.5 GB RAM per service
- Automatic sleep after 15 minutes of inactivity
- 1 GB storage for static sites

### Upgrade to Paid
- Always-on services
- More RAM and CPU
- Custom domains
- Email support

## Custom Domain Setup

1. **Purchase Domain** from registrar (GoDaddy, Namecheap, etc.)
2. **In Render Dashboard**:
   - Go to service settings
   - Add **Custom Domain**
   - Follow DNS configuration instructions
3. **Update Frontend .env**:
   ```env
   VITE_API_URL=https://api.yourdomain.com
   ```
4. **Update Backend CORS**:
   ```
   CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
   ```

## Security Checklist

- ✅ `SECRET_KEY` is secure (32+ chars, random)
- ✅ `DEBUG=False` in production
- ✅ `DATABASE_URL` uses strong password
- ✅ `CORS_ORIGINS` only includes your domains
- ✅ Use HTTPS (automatic on Render)
- ✅ Regularly update dependencies
- ✅ Monitor logs for errors
- ✅ Keep database backed up

## Cost Estimate

**Free Tier** (perfect for learning):
- 1 free web service
- 1 free PostgreSQL database
- 1 free static site
- **Total**: $0/month (includes 750 compute hours)

**Production Tier** (recommended):
- Web Service (Standard): ~$7/month
- PostgreSQL (Standard): ~$30/month
- Static Site: Free
- **Total**: ~$37/month

## Next Steps

1. Set up custom domain (optional)
2. Configure automated backups
3. Set up monitoring and alerts
4. Plan database scaling strategy
5. Consider CDN for static assets (optional)

## Getting Help

- [Render Documentation](https://render.com/docs)
- [PostgreSQL Docs](https://www.postgresql.org/docs/)
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [React Vite Docs](https://vitejs.dev/)

---

**Happy Deployment!** 🚀

For issues or questions, check the troubleshooting section or contact Render support.
