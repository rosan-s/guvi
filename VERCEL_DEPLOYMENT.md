# Deployment Guide - Vercel + Render

## Step 1: Deploy Backend to Render (Free Tier)

1. Go to https://render.com
2. Click **"New +"** → **"Web Service"**
3. Click **"Deploy existing repository"** or paste: `https://github.com/rosan-s/guvi.git`
4. Configure settings:
   - **Name**: `finhealth-api`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r backend/requirements.txt`
   - **Start Command**: `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Region**: Choose closest to you

5. **Environment Variables** (add these):
   ```
   API_KEY=dev-key
   CORS_ORIGINS=*
   DATABASE_URL=sqlite:///finance.db
   ```

6. Click **"Create Web Service"**
7. Wait 2-3 minutes for deployment
8. **Copy your URL** (e.g., `https://finhealth-api.onrender.com`)

---

## Step 2: Deploy Frontend to Vercel

1. Go to https://vercel.com
2. Click **"Add New..."** → **"Project"**
3. Click **"Import Git Repository"**
4. Paste: `https://github.com/rosan-s/guvi.git`
5. Configure:
   - **Framework Preset**: `Vite`
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
   - **Install Command**: `npm install`

6. **Environment Variables**:
   - Key: `VITE_API_BASE_URL`
   - Value: `https://finhealth-api.onrender.com` (from Step 1)

7. Click **"Deploy"**
8. Wait 2-3 minutes
9. Get your live URL! 🚀

---

## Testing

After deployment, your app will be at: `https://your-project.vercel.app`

### Quick Test:
1. Click **"Analyze Sample"** button - should work instantly
2. The sample data will be analyzed by your Render backend
3. View all the financial metrics and AI insights

### To Upload Files:
- Your CSV/Excel must have columns: `revenue`, `expenses`
- Use the sample file at `data/sample.csv` for reference

---

## If Deploy Fails

**Render Backend Issues:**
```bash
# Check logs in Render dashboard → Web Service → Logs
# Common fixes:
- Python version must be 3.8+
- All dependencies in requirements.txt must be compatible
```

**Vercel Frontend Issues:**
```bash
# Check logs in Vercel dashboard → Deployments → Logs
# Common fixes:
- Root Directory: `frontend`
- Environment variable: `VITE_API_BASE_URL`
- Build succeeds locally: `cd frontend && npm run build`
```

---

## Troubleshooting

### "Analysis failed" on Vercel:
1. Check browser console (F12) for error message
2. Verify `VITE_API_BASE_URL` is set in Vercel environment
3. Check that Render backend is running (green status)

### CORS errors:
1. Render: Set `CORS_ORIGINS=*`
2. Vercel: Should work automatically

### Build fails on Render:
1. Check if all packages in `requirements.txt` are compatible
2. Try: `pip install --upgrade -r requirements.txt` locally first

---

## Live App Structure

```
Frontend (Vercel)
    ↓ API calls
Backend (Render)
    ↓ database queries
SQLite (Render)
```

Your app is now production-ready! 🎉
