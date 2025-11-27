FROM python:3.11-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ ./src/

# Copy essential data files (CSV only, no large telemetry files)
# Barber - files at root level
COPY barber/*.CSV ./barber/
COPY barber/*.csv ./barber/

# Indianapolis - files at root level
COPY indianapolis/*.CSV ./indianapolis/
COPY indianapolis/*.csv ./indianapolis/

# RAG dataset
COPY rag_dataset/ ./rag_dataset/

# Expose port 8080 (required by Cloud Run)
EXPOSE 8080

# Run FastAPI with uvicorn
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8080"]
