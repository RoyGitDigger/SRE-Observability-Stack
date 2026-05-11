FROM python:3.9-slim
WORKDIR /app
RUN pip install flask prometheus_client
COPY app/main.py .
CMD ["python", "main.py"]
