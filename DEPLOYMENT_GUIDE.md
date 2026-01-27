# 🚀 Deploy FastAPI + PostgreSQL on Render or Railway

Complete beginner's guide to deploying your Smart Energy Platform backend to the cloud.

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Prepare Your App](#prepare-your-app)
3. [Deploy on Render](#deploy-on-render) ⭐ Recommended
4. [Deploy on Railway](#deploy-on-railway) (Alternative)
5. [Verify Deployment](#verify-deployment)
6. [Troubleshooting](#troubleshooting)
7. [Monitor & Update](#monitor--update)

---

## 📦 Prerequisites

Before you start, make sure you have:

### 1. GitHub Account
- Go to https://github.com
- Sign up (free)
- Create new repository for your project

### 2. Code on GitHub
Your FastAPI project uploaded to GitHub with:
- ✅ `main.py` (FastAPI app)
- ✅ `requirements.txt` (dependencies)
- ✅ `.gitignore` file
- ✅ `README.md`

### 3. Verify requirements.txt
```bash
pip freeze > requirements.txt
```

**Should include:**
- fastapi
- uvicorn
- sqlalchemy
- psycopg2-binary (PostgreSQL driver)
- python-dotenv

**Example requirements.txt:**
```
fastapi==0.104.1
uvicorn==0.24.0
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
python-dotenv==1.0.0
scikit-learn==1.3.2
pandas==2.1.1
```

### 4. Environment Variables File (.env)
Create `.env` file in your project root:
```
DATABASE_URL=postgresql://user:password@localhost:5432/energy_db
SECRET_KEY=your-secret-key-here
ENV=development
```

**Important:** Add to `.gitignore`
```
.env
*.pyc
__pycache__/
.venv/
venv/
```

### 5. Port Configuration
Your FastAPI should use environment variable for port:
```python
import os
from fastapi import FastAPI
from contextlib import asynccontextmanager

app = FastAPI()

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))  # Use PORT env var
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)
```

---

## 🔧 Prepare Your App

### Step 1: Create requirements.txt
```bash
cd /path/to/your/project
pip freeze > requirements.txt
```

### Step 2: Create Procfile (optional but recommended)
Create file named `Procfile` in project root:
```
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```

### Step 3: Test Locally
```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
python main.py

# Test at http://localhost:8000
```

### Step 4: Create .env.example
For security, create example file without real values:
```
DATABASE_URL=postgresql://user:password@host:5432/dbname
SECRET_KEY=your-secret-key-here
ENV=production
```

Add to `.gitignore`:
```
.env
.env.local
*.db
__pycache__
```

### Step 5: Update main.py
Ensure your app reads from environment variables:
```python
import os
from dotenv import load_dotenv

load_dotenv()  # Load .env file

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://user:password@localhost:5432/energy_db"
)

SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
ENV = os.getenv("ENV", "development")

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "environment": ENV,
        "database": "connected" if check_db() else "disconnected"
    }
```

### Step 6: Push to GitHub
```bash
git add .
git commit -m "Prepare for deployment"
git push origin main
```

---

## 🌐 Deploy on Render ⭐ Recommended

### Why Render?
✅ Free tier available  
✅ PostgreSQL built-in  
✅ Easy GitHub integration  
✅ Auto-deploy on push  
✅ Good documentation  

### Step 1: Sign Up on Render
1. Go to https://render.com
2. Click "Sign Up"
3. Choose "Sign up with GitHub"
4. Authorize Render to access GitHub
5. Create account

### Step 2: Create PostgreSQL Database

1. **Dashboard → New +** → **PostgreSQL**
2. **Fill in details:**
   - Name: `energy-db` (or your choice)
   - Database: `energy_db`
   - User: `postgres`
   - Region: Pick closest to you (e.g., US East, EU West)
3. **Click "Create Database"**
4. **Wait 2-3 minutes** for creation
5. **Copy the Internal Database URL** (you'll need this)

**Look for something like:**
```
postgresql://postgres:xxxxxx@dpg-xxxxx.render.internal:5432/energy_db
```

### Step 3: Create Web Service

1. **Dashboard → New +** → **Web Service**
2. **Connect Repository:**
   - Click "Connect a repository"
   - Select your FastAPI project
   - Click "Connect"
3. **Configure Service:**

   | Setting | Value |
   |---------|-------|
   | Name | `energy-api` (or your choice) |
   | Environment | `Python 3` |
   | Build Command | `pip install -r requirements.txt` |
   | Start Command | `uvicorn main:app --host 0.0.0.0 --port $PORT` |
   | Region | Same as database |
   | Plan | `Free` |

4. **Add Environment Variables:**
   - Click "Advanced"
   - Click "Add Environment Variable"
   - Add each variable:

   ```
   Key: DATABASE_URL
   Value: [Paste from Step 2 above]
   
   Key: SECRET_KEY
   Value: your-secure-random-string
   
   Key: ENV
   Value: production
   ```

   **To generate SECRET_KEY:**
   ```bash
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

5. **Click "Create Web Service"**
6. **Wait for deployment** (takes 3-5 minutes)

### Step 4: Get Your API URL

Once deployed:
1. Go to your service dashboard
2. Look for "URL" at top
3. Should be something like: `https://energy-api-xxxxx.onrender.com`

**Test it:**
```bash
curl https://energy-api-xxxxx.onrender.com/health
```

Should return:
```json
{"status": "healthy", "environment": "production"}
```

---

## 🚂 Deploy on Railway (Alternative)

### Why Railway?
✅ PostgreSQL included  
✅ Easy GitHub integration  
✅ Generous free tier  
✅ Good developer experience  

### Step 1: Sign Up on Railway
1. Go to https://railway.app
2. Click "Get Started"
3. Sign in with GitHub
4. Authorize Railway

### Step 2: Create New Project

1. **Click "New Project"**
2. **Add PostgreSQL:**
   - Click "Add Services"
   - Select "PostgreSQL"
   - Wait for creation (2-3 minutes)

3. **Add Python Application:**
   - Click "Add Services"
   - Select "GitHub Repo"
   - Select your FastAPI repository
   - Click "Deploy"

### Step 3: Configure Environment

1. **Click "Variables"**
2. **Add these variables:**

   ```
   DATABASE_URL: [Copy from PostgreSQL service]
   SECRET_KEY: your-secret-string
   ENV: production
   PORT: 8000
   ```

3. **Get DATABASE_URL:**
   - Go to "PostgreSQL" service
   - Click "Connect"
   - Copy connection string
   - Looks like: `postgresql://postgres:xxxxx@containers-us-west-xxxxx.railway.internal:5432/railway`

### Step 4: Configure Deployment

1. **Railway automatically detects Python**
2. **Click "Settings"**
3. **Verify:**
   - **Root Directory:** `.` (current directory)
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`

### Step 5: Deploy

1. **Click "Deploy"**
2. **Wait for build & deployment** (3-5 minutes)
3. **Get your URL:**
   - Go to "Deployments"
   - Copy the domain (something like `railway-xxxxx.railway.app`)

**Test it:**
```bash
curl https://railway-xxxxx.railway.app/health
```

---

## ✅ Verify Deployment

### Test API Endpoints

After deployment, test your endpoints:

**1. Health Check**
```bash
curl https://your-api-url/health
```

Expected response:
```json
{"status": "healthy", "environment": "production", "database": "connected"}
```

**2. Get Energy Readings**
```bash
curl https://your-api-url/energy/readings
```

**3. Check Docs**
Visit: `https://your-api-url/docs`

Should see Swagger UI with all endpoints listed.

### Check Logs

**On Render:**
1. Go to your service
2. Click "Logs" tab
3. Look for errors or issues

**On Railway:**
1. Go to "Deployments"
2. Click latest deployment
3. View logs in terminal

### Common Successful Indicators

✅ Health check returns 200 status  
✅ Swagger docs load at `/docs`  
✅ Data endpoints return JSON  
✅ Database shows "connected"  

---

## 🔌 Connect Frontend to Deployed API

Once backend is deployed, update your React dashboard.

### In React Component (EnergyDataFetcher.js)

**Before (local):**
```javascript
const response = await fetch('http://127.0.0.1:8000/energy/readings');
```

**After (deployed):**
```javascript
const response = await fetch('https://your-api-url.onrender.com/energy/readings');
```

### Better: Use Environment Variables

Create `.env` in `dashboard` folder:
```
REACT_APP_API_URL=https://your-api-url.onrender.com
```

In `api.js`:
```javascript
const baseURL = process.env.REACT_APP_API_URL || 'http://127.0.0.1:8000';

const api = axios.create({
  baseURL: baseURL,
});
```

This way you can switch between local and deployed easily!

---

## 🐛 Troubleshooting

### Problem: "Application failed to start"

**Causes & Solutions:**

1. **Missing main.py**
   - Check file exists at root
   - Verify name is exactly `main.py`

2. **Missing dependencies**
   - Run `pip freeze > requirements.txt`
   - Check `fastapi`, `uvicorn` are listed

3. **Port not set correctly**
   - Use `$PORT` environment variable
   - Don't hardcode port (except 8000 for local)

4. **Import errors**
   - Check all imports are available
   - Run locally first: `python main.py`

**Solution:**
```bash
# Locally, test everything works
pip install -r requirements.txt
python main.py

# Then push to GitHub
git add .
git commit -m "Fix deployment issues"
git push
```

### Problem: "Database connection failed"

**Check DATABASE_URL:**
```python
# Add to main.py temporarily
import os
print("DATABASE_URL:", os.getenv("DATABASE_URL"))
```

Then check logs on Render/Railway.

**Solution:**
1. Go to PostgreSQL service
2. Get correct connection string
3. Copy exactly (no extra spaces)
4. Update in environment variables
5. Restart deployment

### Problem: "502 Bad Gateway"

**Causes:**
- Service crashed
- Not listening on correct port
- Database not connected

**Solutions:**
1. Check logs for errors
2. Verify PORT environment variable set
3. Test locally first
4. Check database connection string

### Problem: "React can't connect to API"

**Causes:**
- Wrong API URL in React
- CORS not enabled on backend

**Solutions:**

1. **Check API URL:**
   ```javascript
   console.log("API URL:", baseURL);
   ```

2. **Add CORS to FastAPI:**
   ```python
   from fastapi.middleware.cors import CORSMiddleware

   app.add_middleware(
       CORSMiddleware,
       allow_origins=["https://your-frontend-url.com"],
       allow_credentials=True,
       allow_methods=["*"],
       allow_headers=["*"],
   )
   ```

3. **Or allow all (not recommended for production):**
   ```python
   allow_origins=["*"]
   ```

---

## 📊 Monitor & Update

### View Logs

**Render:**
1. Service Dashboard
2. Click "Logs"
3. Search for errors

**Railway:**
1. Go to "Deployments"
2. Click deployment
3. View live logs

### Update Your App

**1. Make changes locally:**
```bash
git add .
git commit -m "Add new feature"
```

**2. Push to GitHub:**
```bash
git push origin main
```

**3. Auto-deploy:**
- Render/Railway watches GitHub
- Automatically redeploys when you push
- Takes 2-3 minutes

### Restart Service

**Render:**
1. Service Dashboard
2. Click "Manual Deploy"
3. Select "Deploy latest commit"

**Railway:**
1. Go to "Deployments"
2. Click "Redeploy"

### Check Database

**Render PostgreSQL:**
1. Database Dashboard
2. Click "Connect"
3. Use connection string to connect with tools:
   ```bash
   psql postgresql://user:pass@host:5432/dbname
   ```

**Railway PostgreSQL:**
1. PostgreSQL service
2. Click "Connect"
3. Copy connection string

---

## 🔐 Security Best Practices

### 1. Never Commit Secrets
```bash
# .gitignore should have:
.env
.env.local
secrets/
*.key
```

### 2. Use Strong SECRET_KEY
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 3. Validate Environment
```python
import os

required_vars = ["DATABASE_URL", "SECRET_KEY"]
for var in required_vars:
    if not os.getenv(var):
        raise ValueError(f"Missing environment variable: {var}")
```

### 4. Use HTTPS Only
Both Render and Railway provide HTTPS automatically.

### 5. Restrict CORS Origins
```python
allow_origins=[
    "https://your-frontend.netlify.app",
    "https://your-domain.com"
]
```

Not:
```python
allow_origins=["*"]  # Too permissive!
```

---

## 📈 Performance Tips

### 1. Optimize Database Queries
```python
# Bad: N+1 queries
for reading in readings:
    user = session.query(User).filter_by(id=reading.user_id).first()

# Good: Join query
readings = session.query(Reading).join(User).all()
```

### 2. Add Caching
```python
from functools import lru_cache

@lru_cache(maxsize=100)
def get_forecast():
    # Only recalculate every 30 minutes
    return model.predict()
```

### 3. Use Connection Pooling
```python
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20,
)
```

---

## 📚 Deployment Checklist

Before deploying, verify:

- [ ] `requirements.txt` created and contains all dependencies
- [ ] `.env` file created locally and in `.gitignore`
- [ ] `main.py` reads environment variables
- [ ] Code tested locally and works
- [ ] All files pushed to GitHub
- [ ] PostgreSQL service created on platform
- [ ] Environment variables set correctly
- [ ] Start command configured
- [ ] Logs checked - no errors
- [ ] Health endpoint returns 200
- [ ] Swagger docs load at `/docs`
- [ ] Frontend updated with correct API URL
- [ ] CORS configured if needed

---

## 🎯 Quick Comparison

| Feature | Render | Railway |
|---------|--------|---------|
| **Free Tier** | Yes | Yes |
| **PostgreSQL** | ✅ Included | ✅ Included |
| **GitHub Integration** | ✅ Automatic | ✅ Automatic |
| **Pricing** | Simple | Simple |
| **Ease of Use** | Very Easy | Very Easy |
| **Cold Starts** | Possible on free | Rare |
| **Support** | Good | Good |
| **Recommended** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |

**Recommendation:** Start with Render (slightly easier setup, clearer documentation).

---

## 🚀 Next Steps After Deployment

### 1. Monitor Performance
- Check logs daily
- Watch error rates
- Monitor response times

### 2. Keep Dependencies Updated
```bash
pip list --outdated
pip install --upgrade package-name
```

### 3. Add More Features
- ML model improvements
- More API endpoints
- Database optimizations

### 4. Scale If Needed
- Upgrade to paid tier if free doesn't suffice
- Add caching layer
- Optimize database

### 5. Set Up Monitoring
- Add application monitoring
- Set up alerts
- Track metrics

---

## 📞 Need Help?

### Render Documentation
- https://render.com/docs
- https://render.com/docs/deploy-fastapi

### Railway Documentation
- https://docs.railway.app
- https://docs.railway.app/getting-started

### FastAPI Documentation
- https://fastapi.tiangolo.com/deployment/

### Common Issues
- Render Support: support@render.com
- Railway Support: support@railway.app

---

## 🎉 Success!

Once your API is deployed:

✅ Backend runs 24/7 on cloud  
✅ Database persists data  
✅ React dashboard connects to live API  
✅ Auto-deploys on GitHub push  
✅ Free SSL/HTTPS certificate  

**Your Smart Energy Platform is now live!** 🌍⚡

---

## 📋 Quick Reference

### API URL Format
```
https://service-name-xxxxx.onrender.com
https://service-name-xxxxx.railway.app
```

### Database Connection
```
postgresql://user:password@host:port/dbname
```

### Environment Variables
```
DATABASE_URL=postgresql://...
SECRET_KEY=your-secret
ENV=production
PORT=8000
```

### Test Endpoints
```bash
# Health check
curl https://your-api/health

# Docs
https://your-api/docs

# API endpoint
curl https://your-api/energy/readings
```

---

**Congratulations on deploying to production!** 🚀

For detailed help, refer to the Render or Railway documentation linked above.
