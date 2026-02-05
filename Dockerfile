FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "policy_kg_pipeline.api_server:app", "--host", "0.0.0.0", "--port", "8000"]
