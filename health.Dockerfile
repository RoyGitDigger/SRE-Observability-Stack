FROM python:3.9-slim
WORKDIR /app
RUN pip install requests prometheus_client
COPY scripts/health_check.py .
CMD ["python", "health_check.py"]
