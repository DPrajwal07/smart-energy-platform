# 🚀 Deploy React Frontend & Connect to FastAPI Backend

Complete beginner-friendly guide to deploy your React dashboard and connect it to your live FastAPI backend.

---

## 📋 Prerequisites

Before starting, you need:

- ✅ React dashboard code (in `/dashboard` folder)
- ✅ Deployed FastAPI backend (from DEPLOYMENT_GUIDE.md)
- ✅ FastAPI API URL (example: `https://energy-api-xxxxx.onrender.com`)
- ✅ GitHub account (free)
- ✅ Hosting account (Netlify or Vercel - free)

**Have these ready:**
- Your deployed API URL (you got this from Render/Railway)
- Your GitHub repository link
- Access to your React project files

---

## 🔍 What You'll Learn

By the end of this guide, you'll know how to:

1. ✅ Update React to use your deployed API URL
2. ✅ Create environment variables for React
3. ✅ Deploy React to Netlify or Vercel
4. ✅ Test the full frontend-backend connection
5. ✅ Troubleshoot connection issues
6. ✅ Update your frontend when API changes

---

## 📝 Step 1: Prepare Your React Dashboard

### 1.1 Locate Your Dashboard

Your React dashboard files are in:
```
Smart Energy Platform/
└── dashboard/          ← This folder
    ├── src/
    ├── package.json
    ├── .env            ← You may need to create this
    └── .env.example    ← Reference file
```

### 1.2 Update API Configuration

**Option A: Using Environment Variables (Recommended)**

Create `.env` file in your `dashboard/` folder:

```bash
# dashboard/.env
REACT_APP_API_URL=https://your-deployed-api.onrender.com
```

Replace `your-deployed-api.onrender.com` with your actual API URL.

**Example if using Render:**
```
REACT_APP_API_URL=https://energy-api-xyz123.onrender.com
```

**Example if using Railway:**
```
REACT_APP_API_URL=https://energy-api-abc456.railway.app
```

### 1.3 Update API Service File

Find and open your API service file:
```
dashboard/src/services/api.js
```

Make sure it uses the environment variable:

```javascript
// dashboard/src/services/api.js
const baseURL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// Rest of your API code...
```

If this doesn't exist, create it:

```javascript
// dashboard/src/services/api.js
import axios from 'axios';

const baseURL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export const energyAPI = axios.create({
  baseURL: baseURL,
  timeout: 10000,
});

// Example endpoints
export const getEnergyReadings = () => 
  energyAPI.get('/energy/readings');

export const getPredictions = () => 
  energyAPI.get('/prediction/next-7-days');

export const getHealth = () => 
  energyAPI.get('/health');
```

### 1.4 Update Components to Use Service

In your React components, import and use the API service:

```javascript
import { getEnergyReadings } from '../services/api';

function DashboardComponent() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    getEnergyReadings()
      .then(res => setData(res.data))
      .catch(err => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;
  return <div>{/* Display data */}</div>;
}
```

### 1.5 Test Locally

**Test with your deployed API:**

```bash
# In dashboard folder
cd dashboard

# Install dependencies (if needed)
npm install

# Start React development server
npm start

# Open browser at http://localhost:3000
```

**Verify the connection:**
- Dashboard loads without errors
- Charts/data appear
- Check console (F12) for no errors
- Try refreshing the page

**If you see errors:**
- Check console (F12 → Console tab)
- Verify REACT_APP_API_URL is correct
- Make sure FastAPI is running on deployed platform
- Check that FastAPI allows CORS (see section below)

---

## 🔓 Step 2: Enable CORS on FastAPI Backend

Your React frontend is on a different domain than your API, so you need CORS enabled.

### 2.1 Update Your FastAPI Code

Open your main FastAPI file (usually `main.py` in the backend):

```python
# main.py (Backend)
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

# Allow frontend to access API
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Local React dev server
        "http://localhost:5173",  # Vite dev server
        "https://*.netlify.app",  # All Netlify deployments
        "https://*.vercel.app",   # All Vercel deployments
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "healthy"}

# Rest of your endpoints...
```

**Or more secure (specific domain):**

```python
# Specific domain only
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://your-dashboard.netlify.app",  # Your exact domain
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 2.2 Commit and Push

```bash
# In your backend folder
git add main.py
git commit -m "Enable CORS for frontend"
git push origin main
```

**Wait 2-3 minutes** for auto-deployment on Render/Railway.

### 2.3 Verify CORS Works

```bash
# Test CORS from command line
curl -H "Origin: http://localhost:3000" \
     -H "Access-Control-Request-Method: GET" \
     https://your-api-url/health

# Should see CORS headers in response
```

---

## 🌐 Step 3: Deploy React to Netlify

### Option 1: Netlify (Recommended for Beginners)

**Advantages:**
- Easiest to use
- Free tier is generous
- Auto-deploys on GitHub push
- Free SSL/HTTPS
- Free functions for serverless

#### 3.1 Prepare Your Code

```bash
cd dashboard

# Make sure everything is committed
git add .
git commit -m "Prepare React for deployment"
git push origin main
```

#### 3.2 Create Netlify Account

1. Go to https://netlify.com
2. Click "Sign up"
3. Choose "GitHub"
4. Authorize Netlify to access your GitHub
5. Click "Install" (if prompted)

#### 3.3 Deploy from GitHub

1. On Netlify dashboard, click "New site from Git"
2. Click "GitHub"
3. Select your repository
4. Configure build settings:

```
Build command: npm run build
Publish directory: build
```

5. Click "Advanced" → "New variable":
   - Key: `REACT_APP_API_URL`
   - Value: `https://your-api-url.onrender.com`

6. Click "Deploy site"

**Wait 2-3 minutes for deployment.**

#### 3.4 Get Your URL

After deployment, Netlify gives you a URL:
```
https://your-site-xxxxx.netlify.app
```

**Test it:**
- Open the URL in browser
- Verify dashboard loads
- Check that data appears
- Verify no console errors (F12)

#### 3.5 Custom Domain (Optional)

In Netlify dashboard:
1. Go to "Site settings"
2. Click "Domain management"
3. Add custom domain (need to own the domain)
4. Update DNS settings with your registrar

---

## 🚀 Step 4: Deploy React to Vercel (Alternative)

**Advantages:**
- Even faster deployment
- Great Next.js support
- Edge functions included
- Very beginner-friendly

#### 4.1 Create Vercel Account

1. Go to https://vercel.com
2. Click "Sign up"
3. Choose "GitHub"
4. Authorize and install Vercel

#### 4.2 Deploy

1. On Vercel dashboard, click "Add New..." → "Project"
2. Select your repository
3. Configure:
   - Framework: React
   - Build command: `npm run build`
   - Output directory: `build`
4. Click "Environment Variables"
   - Add: `REACT_APP_API_URL` = `https://your-api-url.onrender.com`
5. Click "Deploy"

**Wait 1-2 minutes.**

#### 4.3 Get Your URL

Vercel gives you:
```
https://your-site.vercel.app
```

---

## 🔗 Step 5: Connect Frontend to Backend

### 5.1 Update Environment Variable

Once you have your React URL deployed, update your FastAPI CORS:

```python
# main.py (Backend)
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://your-site.netlify.app",  # Or vercel.app
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Then:
```bash
git add main.py
git commit -m "Update CORS for deployed frontend"
git push origin main
```

Wait for auto-deployment (2-3 minutes).

### 5.2 Verify Full Stack Connection

```bash
# Test health endpoint
curl https://your-api-url/health

# Test CORS headers
curl -H "Origin: https://your-site.netlify.app" \
     https://your-api-url/health
```

**In your deployed dashboard browser:**
- Open DevTools (F12)
- Go to Network tab
- Refresh page
- Look for API calls
- Verify they return 200 status
- Check data appears on dashboard

---

## 🧪 Step 6: Test the Full System

### Test Checklist

- [ ] Dashboard loads on deployed URL
- [ ] Charts display without errors
- [ ] API calls in Network tab show 200 status
- [ ] No CORS errors in console
- [ ] Data refreshes when you click refresh
- [ ] No "Cannot connect to API" errors
- [ ] All pages/components load
- [ ] Responsive design works on mobile

### Manual Testing

**Test 1: Load Dashboard**
```
1. Open https://your-site.netlify.app
2. Should see dashboard load
3. F12 → Console should be clean (no errors)
```

**Test 2: Check Data**
```
1. Charts should show data
2. Tables should be populated
3. Statistics should display
4. All visuals should render
```

**Test 3: Network Requests**
```
1. F12 → Network tab
2. Refresh page
3. Look for API calls
4. Status should be 200 or 201
5. No 403, 404, or 500 errors
```

**Test 4: CORS**
```
No errors like:
"Access to XMLHttpRequest blocked by CORS policy"
"The value of the 'Access-Control-Allow-Origin' header is '*'"
```

**Test 5: Mobile**
```
1. Open on phone/tablet
2. Dashboard should be responsive
3. Touch interactions work
4. No layout breaks
```

---

## 🐛 Troubleshooting

### Issue 1: "Cannot Connect to API"

**Symptoms:**
- Dashboard shows error message
- Console shows "Failed to fetch"
- Network tab shows failed API calls

**Solutions:**
```javascript
// 1. Check environment variable
console.log("API URL:", process.env.REACT_APP_API_URL);

// 2. Verify FastAPI is running
curl https://your-api-url/health

// 3. Check CORS is enabled
// See if response headers include Access-Control-Allow-Origin

// 4. Verify full URL
// Should be: https://api-domain.com (not http://, not /api)
```

**Fix:**
1. Verify API URL in environment variables
2. Ensure FastAPI backend is deployed and running
3. Check CORS headers match your frontend domain
4. Restart your deployment (Netlify/Vercel redeploy)

### Issue 2: CORS Errors

**Symptom:**
```
Access to XMLHttpRequest blocked by CORS policy
```

**Cause:**
- FastAPI CORS not configured
- CORS configured for wrong domain

**Fix:**
```python
# main.py - Update CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Temporary: allow all
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Then after testing, restrict it:
```python
allow_origins=[
    "http://localhost:3000",
    "https://your-site.netlify.app",
]
```

### Issue 3: Blank Dashboard / No Data

**Check:**
1. Browser console (F12) for errors
2. Network tab for failed API calls
3. FastAPI logs for errors
4. Database connection on backend

**Test:**
```bash
# Test API directly
curl https://your-api-url/energy/readings

# Should return JSON array with data
```

### Issue 4: Environment Variable Not Working

**Symptoms:**
- React using localhost instead of deployed API
- REACT_APP_API_URL is undefined

**Solutions:**

**For Netlify:**
1. Site settings → Build & Deploy → Environment
2. Add variable: `REACT_APP_API_URL`
3. Trigger redeploy

**For Vercel:**
1. Project settings → Environment Variables
2. Add variable: `REACT_APP_API_URL`
3. Trigger redeploy

**Important:** Variable name must start with `REACT_APP_`

### Issue 5: Build Fails

**Symptom:**
```
Build failed - npm run build error
```

**Common causes:**
- Missing dependencies in package.json
- Import errors
- TypeScript errors

**Fix:**
```bash
# Test build locally
npm install
npm run build

# Fix any errors shown
# Then push to GitHub
git push origin main
```

Check deployment logs on Netlify/Vercel for specific error.

---

## 🔄 Step 7: Auto-Deploy Updates

### When You Update React Code

```bash
# Make changes
# Edit files, test locally

# Commit and push
git add .
git commit -m "Update dashboard styling"
git push origin main

# Netlify/Vercel automatically:
# 1. Detect push
# 2. Build new version
# 3. Deploy live (2-3 minutes)
```

**No manual deployment needed!**

### When You Update FastAPI Backend

```bash
# Same process
git add .
git commit -m "Add new API endpoint"
git push origin main

# Render/Railway automatically:
# 1. Detect push
# 2. Install dependencies
# 3. Restart service (2-3 minutes)
```

### When API URL Changes

If you change your API domain:

**Option 1: Netlify**
1. Go to Site settings → Environment variables
2. Update `REACT_APP_API_URL`
3. Trigger redeploy

**Option 2: Vercel**
1. Go to Settings → Environment Variables
2. Update `REACT_APP_API_URL`
3. Trigger redeploy

---

## 📊 Monitoring Your Deployment

### Daily Checks

```bash
# Test health endpoint
curl https://your-api-url/health

# Should respond with 200 status and healthy status
```

### Weekly Checks

- [ ] Dashboard loads without errors
- [ ] Data displays correctly
- [ ] API responds within 1 second
- [ ] Check deployment logs for errors
- [ ] Verify auto-deploy worked after code push

### Monthly Tasks

- [ ] Update dependencies
- [ ] Review analytics
- [ ] Check for console errors
- [ ] Monitor API response times
- [ ] Plan optimizations

---

## 🎯 Common Patterns

### Pattern 1: Using API Service

**Best Practice:**
```javascript
// dashboard/src/services/api.js
import axios from 'axios';

const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL,
});

export const getReadings = () => api.get('/energy/readings');
export const getPredictions = () => api.get('/prediction/next-7-days');
```

**In Components:**
```javascript
import { getReadings } from '../services/api';

useEffect(() => {
  getReadings().then(res => setData(res.data));
}, []);
```

### Pattern 2: Error Handling

```javascript
const [error, setError] = useState(null);

useEffect(() => {
  getReadings()
    .then(res => setData(res.data))
    .catch(err => {
      console.error("API Error:", err);
      setError(err.message || "Failed to load data");
    });
}, []);

return error ? <ErrorMessage msg={error} /> : <Dashboard data={data} />;
```

### Pattern 3: Loading States

```javascript
const [loading, setLoading] = useState(true);

useEffect(() => {
  setLoading(true);
  getReadings()
    .then(res => setData(res.data))
    .finally(() => setLoading(false));
}, []);

return loading ? <Spinner /> : <Dashboard data={data} />;
```

---

## 🔐 Security Best Practices

### Do's ✅

- ✅ Use environment variables for API URL
- ✅ Never commit `.env` file
- ✅ Use HTTPS (automatic on Netlify/Vercel)
- ✅ Validate user input
- ✅ Keep dependencies updated
- ✅ Use `.env.example` as template

### Don'ts ❌

- ❌ Don't hardcode API URL
- ❌ Don't put secrets in code
- ❌ Don't use `allow_origins=["*"]` in production
- ❌ Don't log sensitive data
- ❌ Don't expose environment variables in JS

### Example Secure Setup

```javascript
// ✅ Good
const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL,
});

// ❌ Bad
const api = axios.create({
  baseURL: 'https://my-api.onrender.com',
});
```

---

## 📋 Quick Reference

### Deploy React to Netlify

```
1. Push to GitHub
2. Connect to Netlify
3. Add REACT_APP_API_URL environment variable
4. Click Deploy
5. Wait 2-3 minutes
6. Get URL like: https://site.netlify.app
```

### Deploy React to Vercel

```
1. Push to GitHub
2. Connect to Vercel
3. Add REACT_APP_API_URL environment variable
4. Click Deploy
5. Wait 1-2 minutes
6. Get URL like: https://site.vercel.app
```

### Connect to FastAPI

```
1. Update REACT_APP_API_URL to deployed API
2. Enable CORS in FastAPI main.py
3. Push backend code
4. Wait 2-3 minutes for auto-deploy
5. Test with curl and browser
```

### Test Connection

```bash
# API health
curl https://your-api/health

# Dashboard
Open https://your-site.netlify.app

# Check console (F12)
Should see no errors
```

---

## 🚀 You Did It!

When everything is working:

✅ React dashboard deployed to Netlify/Vercel  
✅ FastAPI backend deployed to Render/Railway  
✅ Frontend connects to backend successfully  
✅ Data displays in real-time  
✅ Auto-deploy works on code push  
✅ No console errors  
✅ HTTPS everywhere  

**Your Smart Energy Platform is live in production!** 🎉⚡

---

## 📚 Next Steps

1. **Monitor Performance**
   - Set up analytics
   - Monitor API response times
   - Track errors

2. **Add Features**
   - User authentication
   - Real-time updates (WebSockets)
   - Export data to CSV
   - Mobile app

3. **Scale Up**
   - Upgrade to paid plans if needed
   - Add CDN for static files
   - Optimize database queries
   - Implement caching

4. **Security**
   - Add rate limiting
   - Implement authentication
   - Regular dependency updates
   - Security headers

---

## 🆘 Need Help?

**Check these first:**
1. [Netlify Docs](https://docs.netlify.com)
2. [Vercel Docs](https://vercel.com/docs)
3. [React Docs](https://react.dev)
4. [Axios Docs](https://axios-http.com)

**Common issues:**
- CORS errors → Enable CORS in FastAPI
- 404 errors → Check API URL is correct
- Blank dashboard → Check console for errors
- Build fails → Run `npm install && npm run build` locally

**Got stuck?** Check the error message carefully, search the docs, or ask for help!

---

**Congratulations! Your platform is now live! 🎉**
