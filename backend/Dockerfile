# Use official lightweight Python image
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Copy dependency definition
COPY pyproject.toml .

# Install FastAPI and Uvicorn
RUN pip install --no-cache-dir "fastapi[standard]>=0.142.2"

# Copy application source code
COPY main.py .

# Expose FastAPI default port
EXPOSE 8000

# Run FastAPI app with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
