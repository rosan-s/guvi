# 🚀 LIVE DEPLOYMENT OPTIONS

Choose ONE option below to deploy your app instantly:

---

## **OPTION 1: Railway (Easiest - Full Stack) ⭐ RECOMMENDED**

### Fastest deployment (2 minutes)

1. Go to https://railway.app/new
2. Click **"Deploy from GitHub"**
3. Select your GitHub account and authorize
4. Search & select: `rosan-s/guvi`
5. Click **"Deploy Now"**
6. **Wait 3-5 minutes** ✅ Your app is LIVE!

**Get your live URL:**
- Railway dashboard → Click your project → "Deployments"
- Copy the generated URL (e.g., `https://yourapp.railway.app`)

**Includes:**
- ✅ Backend API running
- ✅ PostgreSQL database
- ✅ Auto SSL/HTTPS
- ✅ Free tier: $5/month credits

---

## **OPTION 2: Vercel (Frontend) + Render (Backend)**

### For advanced setup

**Frontend (Vercel):**
1. https://vercel.com/new
2. Import: `rosan-s/guvi` → Root: `frontend`
3. Add env var: `VITE_API_BASE_URL` = your Render URL
4. Deploy ✅

**Backend (Render):**
1. https://render.com
2. New Web Service → `rosan-s/guvi`
3. Build: `pip install -r backend/requirements.txt`
4. Start: `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Deploy ✅

---

## **OPTION 3: Heroku (Simple)**

1. Go to https://heroku.com
2. Click **"New"** → **"Create new app"**
3. Name: `finhealth-app`
4. Go to **Deploy** tab
5. Connect GitHub → Select `rosan-s/guvi`
6. Click **"Deploy Branch"** ✅

---

## **OPTION 4: Replit (Fastest to Test)**

1. Go to https://replit.com
2. Click **"+ Create Repl"**
3. Select **"Import from GitHub"**
4. Paste: `https://github.com/rosan-s/guvi`
5. Click **"Import from GitHub"**
6. Click **"Run"** ✅
7. Get public URL in top-right

---

## **After Deployment:**

### Test your live app:
1. Open your live URL
2. Click **"Analyze Sample"** button
3. See financial analysis results instantly! 🎉

### Upload your PDF/CSV:
1. Use the sample at `data/sample.csv`
2. Make sure file has: `revenue`, `expenses` columns

### Update frontend API URL:
If using separate Vercel/Render, update environment variable with backend URL

---

## **Recommended: Railway (OPTION 1)**

Why Railway is best:
- ✅ Easiest one-click deploy
- ✅ Full-stack (frontend + backend)
- ✅ Auto database setup
- ✅ Free tier included
- ✅ Automatic HTTPS
- ✅ GitHub auto-sync

**Deploy now**: https://railway.app/new

---

## **Support**

| Issue | Solution |
|-------|----------|
| Build fails | Check Deployment Logs in dashboard |
| API not working | Verify `VITE_API_BASE_URL` env variable |
| File upload error | Use CSV with `revenue, expenses` columns |
| Database error | Railway auto-creates DB, just deploy |

**Your GitHub**: https://github.com/rosan-s/guvi
