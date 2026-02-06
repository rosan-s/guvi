# Deployment Guide

This guide covers deploying the AI-Powered Financial Health Assessment Tool to production.

## Table of Contents
1. [Local Development](#local-development)
2. [Docker Deployment](#docker-deployment)
3. [Render.com Deployment](#rendercom-deployment)
4. [Traditional VPS](#traditional-vps)
5. [Environment Configuration](#environment-configuration)

---

## Local Development

### Quick Start (5 minutes)

#### Prerequisites
- Python 3.10+
- Node.js 18+

#### Step 1: Clone Repository
```bash
git clone <repo-url>
cd "financial tool"
```

#### Step 2: Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env if needed (default SQLite is fine for dev)

# Run server
uvicorn app.main:app --reload
```

Backend should be running at `http://localhost:8000`

#### Step 3: Frontend Setup
```bash
cd ../frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend should be running at `http://localhost:5173`

#### Step 4: Test Application
1. Open browser to `http://localhost:5173`
2. Click "Analyze Sample" button
3. View financial metrics and AI predictions

#### Troubleshooting
```bash
# If backend won't start:
pip install --upgrade -r requirements.txt
# Or clear pycache:
find . -type d -name __pycache__ -exec rm -r {} +

# If frontend won't start:
npm cache clean --force
rm -rf node_modules
npm install
```

---

## Docker Deployment

### Using Docker Compose

#### Prerequisites
- Docker
- Docker Compose

#### Step 1: Configure Environment
```bash
# Copy environment template
cp backend/.env.example backend/.env

# Update for production (optional)
# nano backend/.env
```

#### Step 2: Start Services
```bash
# Start all services in background
docker compose up -d

# View logs
docker compose logs -f

# Services will be available at:
# Backend API:  http://localhost:8000
# Frontend:     http://localhost:3000
# PostgreSQL:   localhost:5432
```

#### Step 3: Initialize Database
```bash
# Database initializes automatically on first run
# To reset database:
docker compose down -v
docker compose up -d
```

#### Useful Commands
```bash
# Stop services
docker compose stop

# Restart services
docker compose restart

# View service status
docker compose ps

# Remove all containers (caution!)
docker compose down

# Remove all data (caution!)
docker compose down -v

# View service logs
docker compose logs backend
docker compose logs frontend
```

#### Production Adjustments
For production use, update `docker-compose.yml`:

```yaml
services:
  backend:
    environment:
      - DATABASE_URL=postgresql+psycopg2://postgres:postgres@db:5432/finhealth
      - CORS_ORIGINS=https://yourdomain.com
      - API_KEY=${PRODUCTION_API_KEY}  # Use strong key!
```

---

## Render.com Deployment

### One-Click Deployment

Render.com uses `render.yaml` for infrastructure-as-code deployment.

#### Prerequisites
- GitHub account
- Render account (free tier available)

#### Step 1: Push to GitHub
```bash
# Initialize git (if not done)
git init
git add .
git commit -m "Initial commit"

# Create new repo on GitHub
# Then:
git remote add origin https://github.com/yourusername/financial-health-tool.git
git push -u origin main
```

#### Step 2: Connect to Render
1. Go to [render.com/dashboard](https://dashboard.render.com)
2. Click "New +" → "Blueprint"
3. Select GitHub repo
4. Name your service
5. Click "Create Blueprint"

#### Step 3: Configure Environment (in Render Dashboard)
1. Go to Blueprint → Environment
2. Set variables:
   ```
   DATABASE_URL=postgresql://...  (auto-provided by Render)
   API_KEY=your-production-key
   CORS_ORIGINS=https://yourdomain.onrender.com
   ```
3. Deploy!

#### Step 4: Verify Deployment
```bash
# Check backend health
curl https://your-backend.onrender.com/health

# Check frontend
Open https://your-frontend.onrender.com in browser
```

#### What Render.yml Provides
- ✅ Backend FastAPI service
- ✅ Frontend static hosting
- ✅ PostgreSQL database
- ✅ Auto SSL/HTTPS
- ✅ Auto-scaling
- ✅ Github auto-deploy (on push)

#### Pricing (Render.com)
- Backend: $7/month (free tier available)
- Frontend: Free
- PostgreSQL: $15/month (free tier available)
- **Total: ~$22/month** (or free on trial)

---

## Traditional VPS

### Self-Hosted Deployment

#### Prerequisites
- Ubuntu 20.04+ or similar Linux
- Nginx or Apache
- Supervisor or systemd

#### Step 1: Server Setup
```bash
# SSH into server
ssh root@your-server-ip

# Update system
apt update && apt upgrade -y

# Install Python and Node
apt install -y python3.10 python3-venv nodejs npm

# Install system dependencies
apt install -y postgresql postgresql-contrib

# Install Nginx
apt install -y nginx
```

#### Step 2: PostgreSQL Setup
```bash
# Start PostgreSQL
systemctl start postgresql

# Create database and user
sudo -u postgres psql << EOF
CREATE DATABASE finhealth;
CREATE USER finhealth_user WITH PASSWORD 'strong-password-here';
ALTER ROLE finhealth_user SET client_encoding TO 'utf8';
ALTER ROLE finhealth_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE finhealth_user SET default_transaction_deferrable TO on;
ALTER ROLE finhealth_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE finhealth TO finhealth_user;
EOF
```

#### Step 3: Backend Deployment
```bash
# Clone repository
cd /opt
git clone <repo-url> financial-health-tool
cd financial-health-tool/backend

# Create virtual environment
python3.10 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cat > .env << EOF
DATABASE_URL=postgresql+psycopg2://finhealth_user:strong-password-here@localhost:5432/finhealth
API_KEY=$(openssl rand -hex 16)
CORS_ORIGINS=https://yourdomain.com
EOF

# Test run
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

#### Step 4: Create Systemd Service for Backend
```bash
# Create service file
sudo tee /etc/systemd/system/finhealth-backend.service > /dev/null << EOF
[Unit]
Description=Financial Health Assessment Tool Backend
After=network.target

[Service]
Type=notify
User=www-data
Group=www-data
WorkingDirectory=/opt/financial-health-tool/backend
Environment="PATH=/opt/financial-health-tool/backend/venv/bin"
ExecStart=/opt/financial-health-tool/backend/venv/bin/gunicorn \
    -w 4 \
    -k uvicorn.workers.UvicornWorker \
    --bind 127.0.0.1:8000 \
    app.main:app
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable finhealth-backend
sudo systemctl start finhealth-backend
sudo systemctl status finhealth-backend
```

#### Step 5: Frontend Deployment
```bash
cd /opt/financial-health-tool/frontend

# Install and build
npm install
npm run build

# Copy to web root
sudo cp -r dist/* /var/www/html/
```

#### Step 6: Nginx Configuration
```bash
# Create Nginx config
sudo tee /etc/nginx/sites-available/finhealth > /dev/null << 'EOF'
upstream finhealth_backend {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name yourdomain.com;

    # Redirect to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com;

    # SSL certificates (use Let's Encrypt)
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    # Frontend
    root /var/www/html;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    # API proxy
    location /api/ {
        proxy_pass http://finhealth_backend/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
EOF

# Enable site
sudo ln -s /etc/nginx/sites-available/finhealth /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

#### Step 7: SSL Certificate (Let's Encrypt)
```bash
# Install certbot
apt install -y certbot python3-certbot-nginx

# Get certificate
certbot certonly --nginx -d yourdomain.com
```

#### Step 8: Monitoring and Logs
```bash
# Backend logs
journalctl -u finhealth-backend -f

# Nginx logs
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log

# Backend health check
curl https://yourdomain.com/api/health
```

---

## Environment Configuration

### Development (.env)
```bash
DATABASE_URL=sqlite:///./finhealth.db
API_KEY=dev-key
CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
LOG_LEVEL=DEBUG
```

### Production (.env)
```bash
DATABASE_URL=postgresql+psycopg2://user:password@db-host:5432/finhealth
API_KEY=<strong-random-key-32-chars>
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
LOG_LEVEL=INFO
```

### Environment Variables Reference
| Variable | Purpose | Example |
|----------|---------|---------|
| `DATABASE_URL` | Database connection | `sqlite:///./finhealth.db` |
| `API_KEY` | API authentication | `abc123def456...` |
| `CORS_ORIGINS` | Allowed origins | `https://domain.com` |
| `LOG_LEVEL` | Logging verbosity | `DEBUG\|INFO\|WARNING` |

---

## Performance Tuning

### Backend Optimization
```python
# uvicorn with multiple workers
uvicorn app.main:app \
    --host 0.0.0.0 \
    --port 8000 \
    --workers 4 \
    --loop uvloop \
    --http h11
```

### Database Optimization
```sql
-- Add indexes for common queries
CREATE INDEX idx_companies_industry ON companies(industry);
CREATE INDEX idx_records_company_period ON financial_records(company_id, period);
```

### Frontend Optimization
```bash
# Build with minification
npm run build  # Creates optimized dist/

# Serve with compression
npm install -g serve
serve -s dist -c -l 3000
```

---

## Backup & Recovery

### Database Backup
```bash
# PostgreSQL backup
pg_dump -U finhealth_user finhealth > finhealth_backup.sql

# Restore from backup
psql -U finhealth_user finhealth < finhealth_backup.sql
```

### Automated Backups
```bash
# Add to crontab (daily at 2 AM)
0 2 * * * pg_dump -U finhealth_user finhealth | gzip > /backups/finhealth_$(date +\%Y\%m\%d).sql.gz
```

---

## Monitoring & Alerts

### Health Check Endpoint
```bash
# All services should return 200
curl https://yourdomain.com/api/health
```

### Uptime Monitoring (UptimeRobot.com)
- Monitor: `https://yourdomain.com/api/health`
- Interval: 5 minutes
- Alert: Email on downtime

### Log Aggregation (Optional)
```bash
# Send logs to external service
# e.g., Datadog, ELK, Loggly
```

---

## Troubleshooting

### Backend Issues
```bash
# Check if port is in use
lsof -i :8000

# Verify database connection
psql -U finhealth_user finhealth -c "SELECT 1"

# Check logs
journalctl -u finhealth-backend -n 100
```

### Frontend Issues
```bash
# Clear build cache
rm -rf dist/
npm run build

# Check Nginx config
sudo nginx -t

# View Nginx logs
sudo tail -f /var/log/nginx/error.log
```

### General
```bash
# Restart all services
systemctl restart finhealth-backend
systemctl restart nginx

# Clear application cache
# For SQLite: rm finhealth.db
# For PostgreSQL: psql ... -c "DROP DATABASE finhealth;"
```

---

## Summary

| Method | Difficulty | Time | Cost | Best For |
|--------|-----------|------|------|----------|
| Local Dev | ⭐ | 5 min | Free | Development |
| Docker | ⭐⭐ | 10 min | Free | Testing |
| Render | ⭐ | 10 min | $0-22/mo | Quick launch |
| VPS | ⭐⭐⭐⭐ | 1 hour | $5-20/mo | Full control |

**Recommended for hackathon:** Render (one-click, free trial available)

---

**Questions?** Check the [README.md](README.md) and [FEATURES.md](FEATURES.md)
