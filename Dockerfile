FROM python:3.11-slim

WORKDIR /app

# Copy everything
COPY . .

# Install backend dependencies
RUN pip install --no-cache-dir -r backend/requirements.txt

# Expose port
EXPOSE 8000

# Set working directory to backend
WORKDIR /app/backend

# Start backend
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
