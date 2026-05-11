import time
import random
import json
import logging
import os
from flask import Flask, request, Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST, Counter, Gauge, Histogram

# --- CONFIG ---
LOG_FILE = "app/logs/app.log"
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

# --- LOGGING SETUP (Human-style structured logs) ---
class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
        }
        if hasattr(record, "extra_info"):
            log_record.update(record.extra_info)
        return json.dumps(log_record)

logger = logging.getLogger("app")
logger.setLevel(logging.INFO)
fh = logging.FileHandler(LOG_FILE)
fh.setFormatter(JsonFormatter())
logger.addHandler(fh)

# --- METRICS SETUP ---
# We use standard prometheus_client metrics
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP Requests', ['method', 'endpoint', 'http_status'])
REQUEST_LATENCY = Histogram('http_request_duration_seconds', 'HTTP request latency', ['endpoint'])
MEMORY_USAGE = Gauge('app_memory_usage_bytes', 'Simulated memory usage')

app = Flask(__name__)

@app.before_request
def start_timer():
    request.start_time = time.time()

@app.after_request
def log_request(response):
    # Track metrics
    latency = time.time() - request.start_time
    REQUEST_COUNT.labels(method=request.method, endpoint=request.path, http_status=response.status_code).inc()
    REQUEST_LATENCY.labels(endpoint=request.path).observe(latency)
    
    # Log to file for Loki
    logger.info(f"{request.method} {request.path} {response.status_code}", extra={"extra_info": {
        "ip": request.remote_addr,
        "latency": latency,
        "status": response.status_code
    }})
    return response

@app.route('/')
def hello():
    return "Observability Stack is Running."

@app.route('/login', methods=['POST'])
def login():
    data = request.json or {}
    username = data.get('username', 'unknown')
    # Simulate a brute force/fail scenario
    if username == "admin" and random.random() < 0.7:
        logger.warning(f"Failed login attempt for user: {username}", extra={"extra_info": {"ip": request.remote_addr, "event": "auth_failure"}})
        return {"status": "unauthorized"}, 401
    
    logger.info(f"Successful login: {username}", extra={"extra_info": {"event": "auth_success"}})
    return {"status": "success"}, 200

@app.route('/metrics')
def metrics():
    # Update some dynamic gauges
    MEMORY_USAGE.set(random.randint(500, 1000) * 1024 * 1024) # Simulated 500MB - 1GB
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

@app.route('/health')
def health():
    return {"status": "up", "timestamp": time.time()}

if __name__ == '__main__':
    # Running on 5000 as per user request
    app.run(host='0.0.0.0', port=5000)
