# ─────────────────────────────────────────────────────────────────────────────
# Base image: Microsoft's official Playwright image for Python
# Includes Chromium + all required OS-level dependencies out of the box
# ─────────────────────────────────────────────────────────────────────────────
FROM mcr.microsoft.com/playwright/python:v1.44.0-jammy

# Set working directory inside container
WORKDIR /app

# Copy dependency manifest first (Docker layer caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Playwright browsers are already installed in the base image (Chromium).
# Run this only if you need a specific version or extra browsers:
# RUN playwright install chromium

# Copy the entire project
COPY . .

# Expose the port uvicorn will listen on
EXPOSE 8000

# Launch the API
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
