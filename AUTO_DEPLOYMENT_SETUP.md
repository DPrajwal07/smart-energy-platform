# 🚀 Complete Auto-Deployment Setup Guide

**Goal:** Push to GitHub and auto-deploy to Render (backend) + Netlify (frontend)

**Timeline:** ~30 minutes total

---

## ⚡ QUICK START - DO THIS FIRST

### Step 1: Create Repository on GitHub (2 minutes)

**IMPORTANT:** You must create this repository first!

```
1. Open: https://github.com/new
2. Fill in:
   - Repository name: smart-energy-platform
   - Description: Smart Energy Platform - FastAPI backend with React dashboard
   - Visibility: Public
   - ⚠️ DO NOT check "Add a README"
   - ⚠️ DO NOT initialize with .gitignore
3. Click "Create repository"
```

✅ After creation, you'll see a page with setup instructions.

---

### Step 2: Push Code to GitHub (3 minutes)

**Copy and paste this entire command block:**

```bash
cd "/Users/prajwald/Documents/Smart Energy Platform " && \
git push -u origin main
```

**When prompted:**
```
Username: DPrajwal07
Password: [PASTE YOUR PERSONAL ACCESS TOKEN]
```

**Don't have a PAT? Create one quickly:**
```
1. Go to: https://github.com/settings/tokens
2. Click: "Generate new token" → "Generate new token (classic)"
3. Name: smart-energy-platform-token
4. Select: repo (all options under repo)
5. Click: "Generate token"
6. COPY the token (you won't see it again!)
7. Paste when git asks for password
```

**Expected output:**
```
Enumerating objects: 81, done.
...
 * [new branch]      main -> main
Branch 'main' set up to track remote branch 'main' from 'origin'.
```

✅ **Code is now on GitHub!**

---

## 🎯 DEPLOY BACKEND TO RENDER (with auto-deploy)

### Step 1: Connect Render to GitHub

```
1. Go to: https://render.com
2. Sign up with GitHub (or login)
3. Authorize Render to access your GitHub
4. You'll be on the Render dashboard
```

### Step 2: Create PostgreSQL Database

```
1. Click: "+ New +"
2. Select: "PostgreSQL"
3. Fill in:
   - Name: energy-db
   - Database: energy_db
   - User: postgres
   - Region: US East
4. Click: "Create Database"
5. Wait 2-3 minutes
6. Copy: "Internal Database URL"
   (Format: postgresql://postgres:xxxxx@dpg-xxxxx.render.internal:5432/energy_db)
7. SAVE THIS URL - you'll need it
```

### Step 3: Deploy Backend Service

```
1. Click: "+ New +"
2. Select: "Web Service"
3. Select: "Connect a repository"
4. Search: "smart-energy-platform"
5. Click: "Connect"
6. Fill in:
   - Name: energy-api
   - Environment: Python 3
   - Build Command: pip install -r requirements.txt
   - Start Command: uvicorn main:app --host 0.0.0.0 --port $PORT
   - Region: US East (same as database)
   - Plan: Free
7. Click: "Advanced"
   - Add Environment Variables:
     * DATABASE_URL: [paste your PostgreSQL URL from Step 2]
     * ENV: production
8. Click: "Create Web Service"
```

**Wait 3-5 minutes for deployment...**

### Step 4: Verify Backend Deployed

When you see a green status and URL like:
```
https://energy-api-xxxxx.onrender.com
```

Test it:
```bash
curl https://energy-api-xxxxx.onrender.com/health
# Should return: {"status":"healthy"}
```

✅ **Backend is live and auto-deploying!**

When you push to GitHub, Render automatically rebuilds and deploys.

---

## 🎨 DEPLOY FRONTEND TO NETLIFY (with auto-deploy)

### Step 1: Connect Netlify to GitHub

```
1. Go to: https://netlify.com
2. Sign up with GitHub (or login)
3. Authorize Netlify to access your GitHub
4. You'll be on the Netlify dashboard
```

### Step 2: Create React Environment Variable File

Before deploying, update the React environment variable in your GitHub repo:

```bash
# Add this to your repo
cd "/Users/prajwald/Documents/Smart Energy Platform /dashboard"

# Create .env file (this goes in dashboard folder, not root)
cat > .env << 'EOF'
REACT_APP_API_URL=https://energy-api-xxxxx.onrender.com
EOF

# Replace energy-api-xxxxx with your actual Render domain

# Commit and push
cd "/Users/prajwald/Documents/Smart Energy Platform "
git add dashboard/.env
git commit -m "Add React environment variables"
git push origin main
```

### Step 3: Deploy Frontend

```
1. On Netlify dashboard, click: "Add new site"
2. Select: "Import an existing project"
3. Choose: "GitHub"
4. Search: "smart-energy-platform"
5. Click: "Install and Authorize"
6. Select: "DPrajwal07/smart-energy-platform"
7. Configure:
   - Base directory: dashboard
   - Build command: npm run build
   - Publish directory: build
   - Click: "Show advanced"
   - Add variable:
     * Key: REACT_APP_API_URL
     * Value: https://energy-api-xxxxx.onrender.com
8. Click: "Deploy site"
```

**Wait 2-3 minutes...**

### Step 4: Verify Frontend Deployed

When you see a URL like:
```
https://your-site-xxxxx.netlify.app
```

Test it:
```
1. Open in browser
2. Dashboard should load
3. F12 to open console - no errors
4. Data should display from your API
```

✅ **Frontend is live and auto-deploying!**

---

## 🔄 AUTO-DEPLOYMENT IS NOW ACTIVE

### How It Works

**From now on:**

```bash
# Make changes to code
# Edit any file

# Push to GitHub
git add .
git commit -m "Update dashboard"
git push origin main

# Automatically:
# 1. Render detects push (2-3 min to redeploy backend)
# 2. Netlify detects push (1-2 min to redeploy frontend)
# 3. Changes are LIVE

# No manual deployment needed!
```

---

## 🔗 Update CORS (Final Step)

Update your backend to allow your frontend domain:

```python
# In main.py (at the top after FastAPI creation)
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "https://your-site-xxxxx.netlify.app",  # ← Replace with your actual Netlify URL
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Then push:
```bash
git add main.py
git commit -m "Update CORS for deployed frontend"
git push origin main
# Backend auto-redeploys in 2-3 minutes
```

---

## ✅ DEPLOYMENT CHECKLIST

- [ ] GitHub repository created at https://github.com/new
- [ ] Code pushed to GitHub: `git push -u origin main`
- [ ] Render connected to GitHub
- [ ] PostgreSQL database created on Render
- [ ] Backend web service deployed to Render
- [ ] Backend health check works: `curl https://energy-api-xxxxx.onrender.com/health`
- [ ] Netlify connected to GitHub
- [ ] React environment variable added (REACT_APP_API_URL)
- [ ] Frontend deployed to Netlify
- [ ] Frontend loads: `https://your-site-xxxxx.netlify.app`
- [ ] Dashboard displays data
- [ ] CORS updated in main.py
- [ ] Auto-deployment tested (make small change, push, verify auto-deploy)

---

## 🎯 YOUR PRODUCTION URLS

After deployment, you'll have:

```
Frontend Dashboard:
https://your-site-xxxxx.netlify.app

Backend API:
https://energy-api-xxxxx.onrender.com

API Docs:
https://energy-api-xxxxx.onrender.com/docs

API Health:
https://energy-api-xxxxx.onrender.com/health
```

---

## 🔐 Important Security Notes

### Never Commit `.env` with Real Secrets
```bash
# ✅ OK: .env.example (template, no real values)
cat .env.example
DATABASE_URL=postgresql://...

# ❌ NEVER: .env (with real secrets)
# This is in .gitignore - good!
```

### Use Environment Variables on Platforms
```
✅ Render: Set in Dashboard → Environment Variables
✅ Netlify: Set in Site Settings → Build & Deploy → Environment
❌ Never put secrets in code or .env files that are committed
```

---

## 🐛 Troubleshooting

### "Repository not found"
**Fix:**
1. Go to https://github.com/new
2. Create repository: smart-energy-platform
3. Then try: `git push -u origin main`

### "Authentication failed"
**Fix:**
1. Go to https://github.com/settings/tokens
2. Create Personal Access Token
3. Paste token when prompted (not your password)

### "Render can't find repository"
**Fix:**
1. Make sure code is pushed to GitHub
2. Disconnect Render app from GitHub: https://github.com/settings/installations
3. Reconnect Render and re-authorize

### "Frontend can't connect to API"
**Fix:**
1. Check REACT_APP_API_URL in Netlify environment variables
2. Check CORS in main.py includes your Netlify domain
3. F12 → Console for specific error message

### "502 Bad Gateway"
**Fix:**
1. Check Render logs for errors
2. Verify DATABASE_URL is set
3. Restart service: Render Dashboard → Manual Deploy

---

## 📊 Monitor Your Deployments

### Check Backend Status
```
1. Render Dashboard
2. Select energy-api service
3. View logs for errors
4. Check "Active" status is green
```

### Check Frontend Status
```
1. Netlify Dashboard
2. Select your site
3. View Deploy logs
4. Check "Published" status
```

### Test Endpoints
```bash
# Backend health
curl https://energy-api-xxxxx.onrender.com/health

# Frontend
Open https://your-site.netlify.app in browser
```

---

## 🚀 Next: Make Updates

### Local Development
```bash
cd "/Users/prajwald/Documents/Smart Energy Platform "

# Make changes to files
# Test locally

# Push to GitHub
git add .
git commit -m "Add new feature"
git push origin main

# Wait 2-3 minutes
# Changes are live!
```

### Add New API Endpoint
```python
# In main.py
@app.get("/new-endpoint")
def new_endpoint():
    return {"data": "value"}

# Push changes
git add main.py
git commit -m "Add new endpoint"
git push origin main
```

### Update Frontend
```bash
cd dashboard

# Make React changes
# Test with npm start

# Commit
git add .
git commit -m "Update dashboard"
git push origin main
```

---

## 🎉 SUCCESS STATE

When everything is working:

✅ Frontend loads instantly  
✅ Data displays from API  
✅ No console errors  
✅ Charts and tables work  
✅ Mobile view responsive  
✅ Auto-deploy works (push → live in 2-3 min)  
✅ 24/7 uptime  
✅ Free SSL/HTTPS  

---

## 📞 Quick Reference

| Task | Time | Status |
|------|------|--------|
| Create GitHub repo | 1 min | Before deployment |
| Push code | 2 min | Before deployment |
| Deploy backend | 10 min | In progress |
| Deploy database | 3 min | Auto with backend |
| Deploy frontend | 5 min | After backend |
| Setup auto-deploy | 5 min | Final step |
| **TOTAL** | **~30 min** | **🚀 LIVE** |

---

## 📚 Reference Documents

- [COMPLETE_DEPLOYMENT.md](COMPLETE_DEPLOYMENT.md) - Detailed version
- [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md) - Quick checklist
- [GITHUB_READY_TO_PUSH.md](GITHUB_READY_TO_PUSH.md) - GitHub setup only
- [REACT_DEPLOYMENT_GUIDE.md](REACT_DEPLOYMENT_GUIDE.md) - Frontend only

---

**Ready to go live? Follow the steps above! 🚀**

Questions? Check the troubleshooting section above.
