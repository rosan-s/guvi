# AI-Powered Financial Health Assessment Tool

## 🎯 Overview
A cutting-edge, full-stack platform leveraging **machine learning** to deliver comprehensive financial analysis for SMEs. Combines traditional financial metrics with AI predictions, anomaly detection, risk scoring, and scenario analysis.

**For:** Career Carnival Hackathon 2026 - AI Engineer Track

## ✨ AI-Driven Features

✅ **3-Month Forecasting** - Predict revenue & expense trends using ML
✅ **Anomaly Detection** - Identify fraud/errors automatically  
✅ **Credit Risk Scoring** - Calculate default probability with ML  
✅ **Scenario Analysis** - Pessimistic/Base/Optimistic planning  
✅ **Smart Recommendations** - AI-powered, contextual advice  
✅ **Industry Benchmarking** - 6 industry benchmarks with gap analysis

[See Full Feature List →](FEATURES.md)

## 🏗️ Tech Stack
- **Frontend:** React 18 + Vite + TailwindCSS-inspired
- **Backend:** FastAPI + AsyncIO (high performance)
- **Database:** SQLite (dev) / PostgreSQL (prod)
- **ML:** scikit-learn, pandas, numpy, scipy
- **Deployment:** Docker + Render

## 🚀 Quick Start

### 1. Backend Setup
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### 3. Access Application
Visit `http://localhost:5173`

## 📊 How It Works

1. **Upload** → CSV/XLSX/PDF file with financial data
2. **Analyze** → FastAPI processes with ML models
3. **Insights** → Get metrics, forecasts, risks, recommendations
4. **Act** → Use insights for better financial decisions

### Sample Data Format
```csv
revenue,expenses,cash_in,cash_out,ar,ap,inventory,debt,tax
120000,90000,115000,88000,25000,18000,12000,15000,8000
```

## 🔗 API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/health` | GET | Health check |
| `/analyze` | POST | File upload analysis |
| `/analyze-json` | POST | JSON payload analysis |
| `/integrations/bank-a` | GET | Bank A integration |
| `/integrations/bank-b` | GET | Bank B integration |

**Headers:** `X-API-Key: dev-key` (development)

## 📋 Configuration

### Environment Variables
```bash
# backend/.env
DATABASE_URL=sqlite:///./finhealth.db
API_KEY=dev-key
CORS_ORIGINS=["http://localhost:5173"]
```

### Database Options
- **SQLite** (default, dev): File-based, zero setup
- **PostgreSQL** (prod): Use `docker compose up -d`

## 🐳 Docker Deployment

```bash
# Spin up PostgreSQL
docker compose up -d

# Backend will auto-connect
uvicorn backend.app.main:app --reload
```

## 📈 Key Metrics Provided

| Metric | Formula | Purpose |
|--------|---------|---------|
| **Risk Score** | Composite (0-100) | Overall financial health |
| **Net Margin** | (Revenue - Expenses) / Revenue | Profitability |
| **Current Ratio** | Current Assets / Current Liabilities | Liquidity |
| **DSO Days** | (AR / Revenue) × 365 | Receivables efficiency |
| **DSCR** | Net Cashflow / Debt | Debt service capability |
| **Default Probability** | ML-based prediction | Credit risk |

## 🎓 Innovation Highlights

1. **ML Pipeline Integration** - 5 different algorithms working together
2. **Real-time Predictions** - Sub-second inference on financial data
3. **Practical Use Cases** - Solves real SME challenges
4. **Production-Grade** - Error handling, security, monitoring
5. **User-Centric Design** - Multilingual, intuitive UI
6. **Scalable Architecture** - AsyncIO, connection pooling, optimized queries

## 🔐 Security

- ✅ API key authentication
- ✅ CORS protection
- ✅ Input validation (CSV/XLSX/PDF parsing)
- ✅ SQL injection prevention (SQLAlchemy ORM)
- ✅ TLS/HTTPS ready for production

## 📱 Browser Support

- Chrome, Firefox, Safari, Edge (latest versions)
- Mobile responsive design

## 🚢 Production Deployment

### Option 1: Render (Recommended)
1. Push repo to GitHub
2. Connect to Render Blueprint
3. Auto-deploys with PostgreSQL

### Option 2: Traditional
1. Set `DATABASE_URL` to PostgreSQL connection string
2. Run: `uvicorn app.main:app --host 0.0.0.0 --port 8000`
3. Serve frontend from CDN or nginx

## 📞 Support & Documentation

- **Features Deep Dive:** See [FEATURES.md](FEATURES.md)
- **API Docs:** `http://localhost:8000/docs` (Swagger)
- **Backend:** `backend/` directory
- **Frontend:** `frontend/` directory

## 📄 License

This project is provided as-is for the hackathon.

---

**Built for Career Carnival Hackathon 2026** 🚀

