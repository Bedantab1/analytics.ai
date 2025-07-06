======= DevOps AI Agent – Anomaly detection =======
This project is an AI-powered multi-tool DevOps Agent designed to:

1. Continuously monitor infrastructure metrics (CPU usage)

2. Detect sustained CPU spikes

3. Retrieve relevant logs and analyze them using an LLM (Ollama)

4. Automatically remediate by restarting containers

5. Verify system stability after remediation

6. Notify the team via Slack notifications

 -------Features-------
CPU Spike Detection

Uses Prometheus Node Exporter metrics

Configurable thresholds (default: 40% CPU sustained for 10 seconds)

Log Retrieval and Analysis

Collects logs from /var/log/syslog

Filters for ERROR and WARNING entries

Sends logs to Ollama LLM (tinyllama) for root cause analysis

Automated Remediation

If LLM identifies known issues (e.g., memory leak, infinite loop), restarts the specified Docker container (test_container)

Verifies CPU usage after remediation to confirm system stability

Notifications

Sends structured Slack-style notifications to console (simulated Slack webhook)

------- Requirements -------
Python 3.8+

Docker

Prometheus

Node Exporter

Ollama LLM server running locally (http://localhost:11434)

Python dependencies:

pip install prometheus-api-client

------- Setup Instructions -------
1️. Launch Prometheus & Node Exporter

Example Docker run:

docker run -d -p 9090:9090 prom/prometheus

docker run -d --net="host" quay.io/prometheus/node-exporter

2️. Start Ollama

ollama serve

Ensure Ollama is accessible at http://localhost:11434

3️. Start Test Container

docker run -d --name test_container ubuntu:22.04 tail -f /dev/null

4️. Install Python Dependencies

pip install prometheus-api-client

------- How It Works -------
Monitoring Loop

Queries Prometheus every 15 seconds for CPU usage

If CPU exceeds threshold for the specified duration, triggers analysis

Log Analysis

Fetches last 20 lines from /var/log/syslog

Sends to Ollama LLM with a prompt to analyze root cause

Remediation Logic

If the LLM mentions known terms (memory leak, infinite loop), restarts the Docker container

Waits 30 seconds and re-queries CPU usage

Notification

Prints structured notification to console (simulating Slack)

Includes analysis and remediation details

------- Agent Personality Prompt -------
You are an AI DevOps assistant. Given these logs, identify likely causes of high CPU usage and suggest potential remediation steps.

------- Simulating a CPU Spike  -------
Run this in another terminal:

yes > /dev/null

Or use stress if available:

stress --cpu 2

======= Known Limitations / Tradeoffs ========
CPU Metric Source:

This implementation uses Prometheus Node Exporter.

In early testing, we also used psutil for local-only metrics.

Note: For production, Prometheus is preferred.

Email Notifications:

Not implemented. Slack simulation is done via console print.

Bonus Features:

Memory, disk, and network monitoring are planned for future extensions.

======= Test Scenarios =======
1. CPU Spike detection

2. LLM log analysis with synthetic "memory leak" messages

3. Container restart

4. CPU re-verification post-remediation

5. Notification output

======= Running the Agent =======
Launch:

python3 agent.py

======= Author =======
Bedanta Bhandar Kayastha

Bedantab1@gmail.com

https://www.linkedin.com/in/bedanta-bhandar-k-ba39251b2/
