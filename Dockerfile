FROM python:3.10-slim

# -------------------------
# System dependencies
# -------------------------
RUN apt-get update && apt-get install -y \
    wget unzip curl gnupg ca-certificates \
    chromium chromium-driver \
    nodejs npm \
    && rm -rf /var/lib/apt/lists/*

# -------------------------
# Environment
# -------------------------
ENV PYTHONUNBUFFERED=1 \
    HEADLESS=true \
    CHROME_BIN=/usr/bin/chromium \
    CHROMEDRIVER_PATH=/usr/bin/chromedriver \
    PYTHONPATH=/app:/quality-platform

WORKDIR /app

# -------------------------
# Python deps
# -------------------------
COPY requirements.txt .
RUN pip install --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

# -------------------------
# Source code
# -------------------------
COPY quality-platform /quality-platform
COPY . .

# -------------------------
# Runner script
# -------------------------
CMD ["python", "run_and_report.py"]





