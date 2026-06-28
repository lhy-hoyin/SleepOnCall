# ---- Stage 1: builder ----
FROM python:3.11 AS builder

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --user -r requirements.txt


# ---- Stage 2: final image ----
FROM python:3.11-slim

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /root/.local /root/.local

# Copy app code
COPY . .

# Ensure Python sees installed packages
ENV PATH=/root/.local/bin:$PATH

CMD ["python", "main.py"]