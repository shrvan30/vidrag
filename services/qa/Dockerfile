FROM python:3.10-slim

WORKDIR /app

# 🔥 Install system deps (important for stability)
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

COPY . .

# 🔥 Better startup
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8004"]