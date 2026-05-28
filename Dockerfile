# ── Samakan versi image dengan versi playwright di requirements.txt ────────────
FROM mcr.microsoft.com/playwright/python:v1.60.0-jammy

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Install Chromium yang sesuai versi playwright yang ter-install
RUN python -m playwright install chromium --with-deps

COPY . .

EXPOSE 8000

CMD ["python", "main.py"]