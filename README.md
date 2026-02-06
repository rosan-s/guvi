# Financial Health Assessment Tool

## Overview
A full-stack platform for SMEs to assess financial health, creditworthiness, risks, and recommendations. Supports CSV/XLSX/PDF uploads, industry benchmarking, multilingual UI (English/Hindi), and mock banking integrations.

## Tech Stack
- Frontend: React + Vite
- Backend: FastAPI + pandas
- Database: SQLite (dev) / PostgreSQL (prod)

## Setup

### 1) Database (choose one)
- SQLite (dev):
  - Copy `backend/.env.example` to `backend/.env`
  - Set `DATABASE_URL=sqlite:///./finhealth.db`
- PostgreSQL (prod):
  - Use Docker Compose: `docker compose up -d`
  - Set `DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/finhealth`

### 2) Backend
- Create virtual environment and install requirements:
  - `pip install -r backend/requirements.txt`
- Run API:
  - `uvicorn backend.app.main:app --reload`

### 3) Frontend
- Install dependencies:
  - `npm install` (in frontend)
- Run dev server:
  - `npm run dev` (in frontend)

## API
- Default API key: `dev-key` (set in `backend/.env`)
- Endpoints:
  - `POST /analyze` (file upload)
  - `POST /analyze-json` (JSON payload)
  - `GET /integrations/bank-a`
  - `GET /integrations/bank-b`

## Render Deployment (Blueprint)
1. Push this repo to GitHub.
2. In Render, create a new Blueprint and select this repo.
3. Render uses render.yaml to provision:
  - finhealth-api (FastAPI web service)
  - finhealth-frontend (static site)
  - finhealth-db (PostgreSQL)
4. Update these in render.yaml (or Render dashboard):
  - `CORS_ORIGINS` to your frontend URL
  - `VITE_API_BASE_URL` to your backend URL

## Security Notes
- Use HTTPS/TLS in production for all traffic in transit.
- Encrypt database storage and backups.
- Rotate API keys and restrict CORS in production.

## Data Format
Include columns like:
- revenue, expenses, cash_in, cash_out, ar, ap, inventory, debt, tax
