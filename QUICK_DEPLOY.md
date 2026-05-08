# Quick Start for Deployment

## 🚀 30-Second Deployment Overview

1. **Fork/Clone to GitHub** → Push code to your GitHub repository
2. **Create Render Account** → Sign up at [render.com](https://render.com)
3. **Deploy Database** → Create PostgreSQL database on Render
4. **Deploy Backend** → Deploy web service with PostgreSQL URL
5. **Deploy Frontend** → Deploy static site
6. **Connect** → Update CORS on backend to include frontend URL

**Total Time:** 5-10 minutes ⏱️

---

## 📋 Deployment Checklist

### Prerequisites
- [ ] Code pushed to GitHub
- [ ] GitHub account connected to Render
- [ ] Render account created

### Step 1: Database (1 minute)
```bash
# In Render Dashboard:
1. Click New → PostgreSQL
2. Name: task_manager_db
3. Copy the Internal Database URL
```

### Step 2: Backend (3 minutes)
```bash
# In Render Dashboard:
1. Click New → Web Service
2. Select GitHub repository
3. Build Command: pip install -r backend/requirements.txt
4. Start Command: gunicorn -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000 backend.app.main:app
5. Add Environment Variables:
   - DATABASE_URL=[copied from database]
   - SECRET_KEY=[generate: python -c "import secrets; print(secrets.token_urlsafe(32))"]
   - DEBUG=False
   - CORS_ORIGINS=http://localhost:5173
```

### Step 3: Frontend (2 minutes)
```bash
# In Render Dashboard:
1. Click New → Static Site
2. Select GitHub repository
3. Build Command: cd frontend && npm install && npm run build
4. Publish Directory: frontend/dist
```

### Step 4: Connect (1 minute)
```bash
# Update Backend CORS:
1. Go to backend service
2. Environment → CORS_ORIGINS
3. Set to: https://task-management-ui.onrender.com
4. Save (auto-redeploy)
```

---

## 🔍 Verify Deployment

```bash
# Test Backend Health
curl https://your-backend-url.onrender.com/health

# Test API Docs
https://your-backend-url.onrender.com/api/docs

# Test Frontend
https://your-frontend-url.onrender.com
```

---

## 🛠️ Common Tasks

### Change Backend URL in Frontend
```env
# frontend/.env or Render environment variables
VITE_API_URL=https://your-new-backend-url.onrender.com
```

### Update CORS Origins
```bash
# Backend environment variables on Render
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

### View Backend Logs
```bash
# In Render Dashboard → Backend Service → Logs
# Check for errors and deployment status
```

### Restart Backend Service
```bash
# In Render Dashboard → Backend Service
# Click "Manual Deploy" → "Deploy Latest Commit"
```

### Check Database Connection
```bash
# In Render Dashboard → PostgreSQL Database
# View connection details and test connection
```

---

## 🔐 Security Settings

Required for Production:
- ✅ `DEBUG=False`
- ✅ `SECRET_KEY` - Secure random value (32+ chars)
- ✅ `CORS_ORIGINS` - Only your domain
- ✅ Database URL - Strong password
- ✅ HTTPS enabled (automatic on Render)

---

## 📞 Troubleshooting

### Backend won't start
```
1. Check build logs in Render dashboard
2. Verify DATABASE_URL format
3. Ensure SECRET_KEY is set
4. Check if port 8000 is exposed
```

### Frontend shows blank page
```
1. Check console for errors (F12)
2. Verify VITE_API_URL is correct
3. Check backend CORS includes frontend URL
4. Clear browser cache (Ctrl+Shift+Del)
```

### Can't connect to database
```
1. Verify DATABASE_URL in environment
2. Check PostgreSQL database is running
3. Verify database name exists
4. Check firewall settings
```

### CORS errors in browser
```
1. Add frontend URL to backend CORS_ORIGINS
2. Redeploy backend
3. Wait 30 seconds for changes
4. Clear browser cache
```

---

## 📚 Reference

| Component | Technology | Status |
|-----------|-----------|--------|
| Backend API | FastAPI + Uvicorn | ✅ Ready |
| Database | PostgreSQL | ✅ Ready |
| Frontend | React + Vite | ✅ Ready |
| Hosting | Render | ✅ Configured |
| Auth | JWT + Bcrypt | ✅ Ready |
| Documentation | Swagger + ReDoc | ✅ Ready |

---

## 🎯 Next Steps

1. **Custom Domain** (Optional)
   - Purchase domain
   - Add to Render in service settings
   - Update CORS_ORIGINS

2. **Monitoring** (Recommended)
   - Set up uptime monitoring
   - Enable error alerts
   - Track API response times

3. **Scaling** (When needed)
   - Upgrade Render plan
   - Add caching (Redis)
   - Optimize database queries

---

## 📖 Detailed Guides

- [Full Deployment Guide](DEPLOYMENT.md)
- [Production Checklist](PRODUCTION_CHECKLIST.md)
- [Scalability Notes](SCALABILITY.md)
- [Main README](README.md)

---

**Ready to Deploy?** Follow the checklist above and you'll be live in minutes! 🚀
