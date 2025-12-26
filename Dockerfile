# Multi-stage Dockerfile for full-stack deployment
# Serves FastAPI backend + Next.js frontend (static export) from one container

# Stage 1: Build Next.js frontend (static export)
FROM node:18-alpine AS frontend-builder

WORKDIR /app/frontend

# Copy package files
COPY frontend/package*.json ./

# Install dependencies
RUN npm ci

# Copy frontend source
COPY frontend/ ./

# Build Next.js app (static export - creates simple HTML/CSS/JS)
ENV NEXT_TELEMETRY_DISABLED=1
ENV NODE_OPTIONS=--max_old_space_size=4096
RUN npm run build

# Stage 2: Python backend with frontend
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY . .

# Copy built Next.js static files (from 'out' directory)
COPY --from=frontend-builder /app/frontend/out ./frontend/out

# Create non-root user (must be before chmod so permissions are set correctly)
RUN useradd -m -u 1000 appuser

# Make start.py executable
RUN chmod +x start.py && chown appuser:appuser start.py

# Switch to non-root user
USER appuser

# Expose port (Render/other platforms will set PORT env var)
EXPOSE 8000

# Health check for Render
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:${PORT:-8000}/api/health || exit 1

# Start backend (serves frontend static files)
# Platform provides PORT environment variable, default to 8000 if not set
CMD ["python", "start.py"]
