from monitor import monitor_loop, get_cpu_usage
from logs import analyze_logs  # uses Ollama
from remediation import restart_container
from notify import send_slack_notification

import subprocess
import time

# You can change this container name if needed
TARGET_CONTAINER = "myapp"

def fetch_logs():
    logs = subprocess.check_output(["tail", "-n", "5", "/var/log/syslog"]).decode()
    return logs

def main():
    while True:
        print("Monitoring...")
        if monitor_loop():
            logs = fetch_logs()
            print("Fetched logs:\n", logs)
            analysis = analyze_logs(logs)
            print("Analysis:", analysis)

            if "infinite loop" in analysis.lower() or "memory leak" in analysis.lower():
                restart_container(TARGET_CONTAINER)

                # Wait to let the system stabilize
                time.sleep(15)
                post_cpu = get_cpu_usage()

                if post_cpu < 40:
                    remediation_msg = (
                        f"✅ Remediation succeeded. CPU usage normalized to {post_cpu:.2f}%."
                    )
                else:
                    remediation_msg = (
                        f"⚠️ Remediation applied, but CPU usage still high ({post_cpu:.2f}%)."
                    )

                msg = f"""
🚨 CPU Spike Detected!
Analysis:
{analysis}

Action: Container '{TARGET_CONTAINER}' restarted.
{remediation_msg}
"""
                send_slack_notification(msg)
            else:
                send_slack_notification(
                    f"🚨 CPU spike detected but no clear remediation identified.\nAnalysis:\n{analysis}"
                )

if __name__ == "__main__":
    main()
