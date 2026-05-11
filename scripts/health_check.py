import time
import requests
from prometheus_client import start_http_server, Gauge

# Metrics
UPTIME = Gauge('service_up', '1 if service is up, 0 otherwise', ['service'])
LATENCY = Gauge('service_latency_seconds', 'Time taken for health check', ['service'])

def check_health():
    while True:
        start_time = time.time()
        try:
            # Check the app service
            response = requests.get("http://app:5000/health", timeout=5)
            latency = time.time() - start_time
            
            if response.status_code == 200:
                UPTIME.labels(service='app').set(1)
            else:
                UPTIME.labels(service='app').set(0)
            
            LATENCY.labels(service='app').set(latency)
        except Exception:
            UPTIME.labels(service='app').set(0)
            LATENCY.labels(service='app').set(0)
        
        time.sleep(15) # Check every 15s

if __name__ == '__main__':
    # Start Prometheus metrics server for this script
    start_http_server(8000)
    print("Health check script started on port 8000")
    check_health()
