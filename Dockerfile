FROM python:3.10-slim

# -------------------------
# System dependencies
# -------------------------
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    curl \
    gnupg \
    ca-certificates \
    chromium \
    chromium-driver \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

# -------------------------
# Environment
# -------------------------
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app
ENV HEADLESS=true
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER_PATH=/usr/bin/chromedriver

# -------------------------
# Workdir
# -------------------------
WORKDIR /app

# -------------------------
# Python deps
# -------------------------
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# -------------------------
# Node deps (HTML report)
# -------------------------
RUN npm install cucumber-html-reporter

# -------------------------
# Project files
# -------------------------
COPY docker .

# -------------------------
# Default command
# -------------------------
CMD bash docker-run.sh
