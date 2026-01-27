# 📋 Deployment Checklist & Quick Reference

Comprehensive checklist and quick reference for deploying FastAPI + PostgreSQL.

---

## ✅ Pre-Deployment Checklist

### Local Testing
- [ ] `pip install -r requirements.txt` completes without errors
- [ ] `python main.py` starts without errors
- [ ] `curl http://localhost:8000/health` returns 200 status
- [ ] `http://localhost:8000/docs` loads Swagger UI
- [ ] All API endpoints work (tested with Postman/curl)
- [ ] Database connections work
- [ ] No console errors or warnings

### Code Preparation
- [ ] `.env` file created with local configuration
- [ ] `.gitignore` contains `.env`, `__pycache__`, `.venv`
- [ ] `requirements.txt` generated with `pip freeze > requirements.txt`
- [ ] All dependencies in `requirements.txt` (fastapi, uvicorn, psycopg2-binary, python-dotenv)
- [ ] Main file uses environment variables for configuration
- [ ] `Procfile` created with correct start command
- [ ] `.env.example` created (without real secrets)
- [ ] No hardcoded secrets in code
- [ ] Code formatted and commented

### GitHub Setup
- [ ] Repository created on GitHub
- [ ] All files committed (`git add .`)
- [ ] All files pushed to main branch (`git push origin main`)
- [ ] `.env` file NOT committed (check with `git log --name-status`)
- [ ] `requirements.txt` committed
- [ ] `.gitignore` file committed
- [ ] `README.md` with setup instructions

### Platform Account Setup
- [ ] Render account created (https://render.com)
- [ ] Or Railway account created (https://railway.app)
- [ ] GitHub account authorized with platform
- [ ] Email verified

### Deployment Configuration
- [ ] DatabaseURL obtained from PostgreSQL service
- [ ] SECRET_KEY generated (`python -c "import secrets; print(secrets.token_urlsafe(32))"`)
- [ ] Environment variables prepared (DATABASE_URL, SECRET_KEY, ENV)
- [ ] Build command correct: `pip install -r requirements.txt`
- [ ] Start command correct: `uvicorn main:app --host 0.0.0.0 --port $PORT`
- [ ] Python version selected (3.9+)
- [ ] Region selected (same as database)

### Post-Deployment Verification
- [ ] Service deployed successfully
- [ ] API URL obtained from platform
- [ ] Health endpoint returns 200: `curl https://api-url/health`
- [ ] Swagger docs load: `https://api-url/docs`
- [ ] API endpoints return data
- [ ] Logs show no errors
- [ ] React frontend updated with correct API URL

---

## 🚀 Step-by-Step Deployment (Render)

### Phase 1: Preparation (10 minutes)

```bash
# 1. Generate requirements.txt
pip freeze > requirements.txt

# 2. Create .env file locally
echo "DATABASE_URL=postgresql://..." > .env
echo "SECRET_KEY=your-key" >> .env
echo "ENV=development" >> .env

# 3. Add to .gitignore
echo ".env" >> .gitignore
echo "__pycache__/" >> .gitignore
echo ".venv/" >> .gitignore

# 4. Test locally
pip install -r requirements.txt
python main.py

# 5. Commit to GitHub
git add .
git commit -m "Prepare for deployment"
git push origin main
```

### Phase 2: Create Database (5 minutes)

On Render.com:

```
1. Dashboard → New + → PostgreSQL
2. Name: energy-db
3. Database: energy_db
4. User: postgres
5. Region: US East (or nearest)
6. Click "Create Database"
7. Wait 2-3 minutes
8. Copy Internal Database URL
```

**Result:** PostgreSQL service running with URL like:
```
postgresql://postgres:xxxxx@dpg-xxxxx.render.internal:5432/energy_db
```

### Phase 3: Deploy Web Service (10 minutes)

On Render.com:

```
1. Dashboard → New + → Web Service
2. Select your GitHub repository
3. Configure:
   - Name: energy-api
   - Environment: Python 3
   - Build: pip install -r requirements.txt
   - Start: uvicorn main:app --host 0.0.0.0 --port $PORT
   - Region: Same as database
   - Plan: Free
4. Click "Advanced" → Add Environment Variables:
   - DATABASE_URL: [paste from database service]
   - SECRET_KEY: [generated key]
   - ENV: production
5. Click "Create Web Service"
6. Wait 3-5 minutes for deployment
```

### Phase 4: Verify (5 minutes)

```bash
# Get your API URL from Render dashboard
# Example: https://energy-api-xxxxx.onrender.com

# Test health endpoint
curl https://energy-api-xxxxx.onrender.com/health

# Test API endpoint
curl https://energy-api-xxxxx.onrender.com/energy/readings

# View Swagger docs
# Open in browser: https://energy-api-xxxxx.onrender.com/docs
```

**Expected responses:**
- Health: `{"status": "healthy", "environment": "production"}`
- Energy readings: `[{...}, {...}, ...]`
- Docs: Interactive API documentation

---

## 🚂 Step-by-Step Deployment (Railway)

### Phase 1: Preparation (10 minutes)
[Same as Render Phase 1]

### Phase 2: Create Project (5 minutes)

On Railway.app:

```
1. Click "New Project"
2. Click "Add Services"
3. Select "PostgreSQL"
4. Wait for creation (2-3 minutes)
```

### Phase 3: Add Application (5 minutes)

```
1. Click "Add Services" → "GitHub Repo"
2. Select your FastAPI repository
3. Click "Deploy"
4. Railway auto-detects Python and builds
```

### Phase 4: Configure Environment (5 minutes)

```
1. Go to "Variables"
2. Add environment variables:
   - DATABASE_URL: [from PostgreSQL service]
   - SECRET_KEY: [generated key]
   - ENV: production
   - PORT: 8000
3. Click "Save"
```

To get DATABASE_URL:
```
1. Click "PostgreSQL" service
2. Click "Connect"
3. Copy connection string
```

### Phase 5: Verify (5 minutes)

```bash
# Get URL from Railway dashboard
# Example: https://project-xxxxx.railway.app

# Test endpoints (same as Render)
curl https://project-xxxxx.railway.app/health
curl https://project-xxxxx.railway.app/energy/readings
```

---

## 🔧 Common Configuration

### Build Command
```bash
# Both Render and Railway
pip install -r requirements.txt
```

### Start Command
```bash
# Both Render and Railway
uvicorn main:app --host 0.0.0.0 --port $PORT
```

### Environment Variables
```
DATABASE_URL=postgresql://user:password@host:5432/dbname
SECRET_KEY=generated-secret-key-string
ENV=production
PORT=8000
```

### Python Version
```
3.11 (recommended)
3.10, 3.9 also supported
```

---

## 🧪 Testing Endpoints

### Health Check
```bash
curl -X GET https://your-api/health
```

**Expected:** 200 status, JSON response

### Get Readings
```bash
curl -X GET https://your-api/energy/readings
```

**Expected:** 200 status, array of readings

### Get Forecast
```bash
curl -X POST https://your-api/prediction/train
curl -X GET https://your-api/prediction/next-7-days
```

**Expected:** Predictions as JSON

### Check Swagger
```
Open browser: https://your-api/docs
```

**Expected:** Interactive API documentation loads

---

## 🐛 Troubleshooting Quick Fixes

### "Application failed to start"
```bash
# Local test
python main.py

# Check logs on platform for specific error
# Common issues:
# - Missing import
# - Wrong main.py name
# - Missing dependency in requirements.txt
```

### "Database connection failed"
```bash
# Verify DATABASE_URL in environment variables
# Make sure internal URL used (if on same platform)
# Test connection locally with that URL first
```

### "502 Bad Gateway"
```bash
# Service crashed - check logs
# Not listening on PORT - verify start command
# Out of memory - check resource usage
```

### "Can't connect from React"
```javascript
// Check API URL
console.log("API URL:", process.env.REACT_APP_API_URL);

// Check CORS on backend
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
)
```

---

## 📊 Resource Usage

### Free Tier Limits

**Render Free:**
- 0.5 CPU
- 512 MB RAM
- PostgreSQL: 1 year free, then $8/month
- Auto-sleep after 15 min inactivity

**Railway Free:**
- $5 credit/month
- Can run small services
- PostgreSQL included
- No auto-sleep

### When to Upgrade

Upgrade if:
- Frequent requests (many users)
- Large database (>10GB)
- High CPU usage
- Need guaranteed uptime (no sleep)

---

## 🔐 Security Checklist

- [ ] `.env` in `.gitignore`
- [ ] No hardcoded secrets in code
- [ ] SECRET_KEY is strong (32+ characters)
- [ ] DATABASE_URL uses secure password
- [ ] HTTPS enabled (automatic on both platforms)
- [ ] CORS restricted to specific origins (not "*")
- [ ] Input validation on all endpoints
- [ ] Rate limiting (if needed)
- [ ] Logging enabled (no sensitive data logged)

---

## 📈 Monitoring

### Daily Checks
```bash
# Test health endpoint
curl https://your-api/health

# Check logs for errors
# Render: Dashboard → Logs
# Railway: Deployments → Logs

# Monitor response times
# Should be <500ms for most endpoints
```

### Weekly Tasks
- [ ] Check error logs
- [ ] Monitor CPU/memory usage
- [ ] Test all major endpoints
- [ ] Check database size

### Monthly Tasks
- [ ] Update dependencies
- [ ] Review security settings
- [ ] Analyze usage patterns
- [ ] Plan optimizations

---

## 🚀 Auto-Deployment Setup

Both platforms auto-deploy on GitHub push:

```bash
# After any changes:
git add .
git commit -m "Update API endpoints"
git push origin main

# Automatically:
# 1. Platform detects push
# 2. Pulls latest code
# 3. Runs build command
# 4. Runs start command
# 5. Deployment live in 2-3 minutes
```

No manual deployment needed!

---

## 📞 Support Resources

### Render
- Docs: https://render.com/docs
- FastAPI: https://render.com/docs/deploy-fastapi
- Status: https://status.render.com

### Railway
- Docs: https://docs.railway.app
- GitHub: https://github.com/railwayapp/railway
- Support: support@railway.app

### FastAPI
- Docs: https://fastapi.tiangolo.com/deployment/
- GitHub: https://github.com/tiangolo/fastapi

---

## 💡 Pro Tips

### Tip 1: Alias for Testing
```bash
# Create alias in ~/.bashrc or ~/.zshrc
alias test-api='curl -s https://your-api/health | jq'

# Then just use:
test-api
```

### Tip 2: Environment Variables Script
```bash
# Create deploy.sh
#!/bin/bash
export DATABASE_URL="postgresql://..."
export SECRET_KEY="generated-key"
export ENV="production"

uvicorn main:app --host 0.0.0.0 --port $PORT
```

### Tip 3: Backup Database
```bash
# Render PostgreSQL dashboard → Backups
# Railway PostgreSQL → Backups
# Automatic backups available
```

### Tip 4: Monitor with Logs
```bash
# Keep terminal open to watch logs
# Render: Dashboard → Logs (live view)
# Railway: Deployments → Logs (live view)
```

---

## 🎯 Success Indicators

When everything is working:

✅ Health endpoint returns 200 status  
✅ Swagger docs load at `/docs`  
✅ API endpoints return correct data  
✅ React dashboard connects successfully  
✅ No errors in logs  
✅ Response time <500ms  
✅ Database shows connected  

---

## 📋 After Deployment

### Update Frontend
```javascript
// dashboard/src/services/api.js
const baseURL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// dashboard/.env
REACT_APP_API_URL=https://your-deployed-api.onrender.com
```

### Deploy Frontend
```bash
# If using Netlify or Vercel
# They auto-deploy from GitHub push
# Just update .env and commit
```

### Monitor Live API
```bash
# Open browser
https://your-api/docs

# Should see:
# - All endpoints listed
# - Try out buttons
# - Real-time testing capability
```

---

## 🎉 You're Live!

Once deployed:
- Your backend runs 24/7 ☁️
- Database persists all data 💾
- React dashboard connects to live API 🎨
- Auto-deploys on code push 🚀
- Free SSL/HTTPS ✅

**Congratulations on going to production!** 🌍⚡

---

**Questions?** Check the Deployment Guide or platform-specific docs.
