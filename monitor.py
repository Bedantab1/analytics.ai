from prometheus_api_client import PrometheusConnect
from datetime import datetime, timedelta
import time

prom = PrometheusConnect(url="http://localhost:9090", disable_ssl=True)

THRESHOLD = 80.0
DURATION_SECONDS = 120 # 2 min window

def get_cpu_usage():
    result = prom.custom_query('100 - (avg by (instance)(rate(node_cpu_seconds_total{mode="idle"}[1m])) * 100)')
    if result:
        return float(result[0]['value'][1])
    return 0.0

def monitor_loop():
    spike_start = None

    while True:
        cpu = get_cpu_usage()
        print(f"CPU Usage: {cpu:.2f}%")

        if cpu > THRESHOLD:
            if not spike_start:
                spike_start = datetime.utcnow()
            elif (datetime.utcnow() - spike_start).seconds >= DURATION_SECONDS:
                print("CPU Spike Detected!")
                return True
        else:
            spike_start = None

        time.sleep(15)

if __name__ == "__main__":
    monitor_loop()
