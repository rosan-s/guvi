# 🚀 NETLIFY DEPLOYMENT GUIDE

## **Option A: Netlify (Frontend Only) + Render (Backend)**

This is the **RECOMMENDED** setup - works perfectly and stays FREE!

---

## **Step 1: Deploy Backend to Render (5 min)**

1. Go to https://render.com
2. Click **"New Web Service"**
3. Select: `rosan-s/guvi`
4. Set:
   - **Name**: `finhealth-backend`
   - **Build Command**: `pip install -r backend/requirements.txt`
   - **Start Command**: `python -m uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT`
5. **Environment Variables**:
   - `API_KEY` = `dev-key`
   - `CORS_ORIGINS` = `*`
6. Click **"Create Web Service"**
7. **Wait for GREEN status** ✅
8. **Copy your Render URL** (e.g., `https://finhealth-backend.onrender.com`)

---

## **Step 2: Deploy Frontend to Netlify (3 min)**

1. Go to https://netlify.com
2. Click **"Add new site"** → **"Import an existing project"**
3. Select **GitHub** → Authorize Netlify
4. Search for: `guvi`
5. Select: `rosan-s/guvi`

### **Netlify Settings**:
- **Build Command**: (leave empty - uses netlify.toml)
- **Publish Directory**: `frontend/dist`
- **Root Directory**: `/`

### **Environment Variables** (click "Show advanced"):
- Key: `VITE_API_BASE_URL`
- Value: Paste your **Render URL** from Step 1

### **Deploy**:
1. Click **"Deploy site"**
2. **Wait 2-3 minutes** for build ✅
3. Get your live URL! 🎉

---

## **Step 3: Test Your Live App**

1. Open your **Netlify URL** in browser
2. Click **"Analyze Sample"** button
3. See results from your live backend! 🚀

---

## **Your Live URLs:**
- **Frontend (Netlify)**: `https://your-app.netlify.app`
- **Backend (Render)**: `https://finhealth-backend.onrender.com`

---

## **Why This Setup?**

✅ **Netlify for Frontend**:
- Free hosting for static sites
- Automatic deployments from GitHub
- Built-in CI/CD
- Global CDN
- Deploy logs built-in

✅ **Render for Backend**:
- Free Python hosting
- PostgreSQL support
- Easy API deployment
- Great for microservices

---

## **Auto-Sync with GitHub**

After first deployment:
- Push to GitHub
- Both Netlify and Render auto-redeploy! 🔄

---

## **Troubleshooting**

| Issue | Solution |
|-------|----------|
| "Analysis failed" | Check Netlify env vars has correct Render URL |
| Build fails | Check build logs in Netlify dashboard |
| CORS error | Render should have `CORS_ORIGINS=*` |
| API not responding | Make sure Render backend is GREEN ✅ |

---

## **QUICK SUMMARY**

| Platform | What | Status |
|----------|------|--------|
| GitHub | Code repo | ✅ Ready |
| Render | Backend API | Deploy now |
| Netlify | Frontend App | Deploy now |

**Deploy now**: 
- Backend: https://render.com
- Frontend: https://netlify.com

Your app will be live in 10 minutes! 🚀
