# Multi-stage Dockerfile for Voynich Morphemic Decryption
# Stage 1: Build stage
FROM python:3.11-slim as builder

LABEL maintainer="Mateusz Piesiak <mateuszpiesiak1990@gmail.com>"
LABEL description="Voynich Manuscript Morphemic Analysis API"

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Set working directory
WORKDIR /build

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt requirements-dev.txt ./

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Stage 2: Runtime stage
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    APP_HOME=/app \
    APP_USER=voynich

# Create app user
RUN groupadd -r ${APP_USER} && \
    useradd -r -g ${APP_USER} -d ${APP_HOME} -s /sbin/nologin ${APP_USER}

# Set working directory
WORKDIR ${APP_HOME}

# Copy Python dependencies from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code
COPY --chown=${APP_USER}:${APP_USER} src/ ${APP_HOME}/src/
COPY --chown=${APP_USER}:${APP_USER} pyproject.toml setup.py setup.cfg README.md VERSION ./

# Install application
RUN pip install -e .

# Create necessary directories
RUN mkdir -p ${APP_HOME}/{data,output,logs} && \
    chown -R ${APP_USER}:${APP_USER} ${APP_HOME}

# Switch to app user
USER ${APP_USER}

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/api/v1/health')" || exit 1

# Run FastAPI application
CMD ["uvicorn", "voynich_decryption.api.app:app", "--host", "0.0.0.0", "--port", "8000"]
