import subprocess
import time

def restart_container(container_name):
    subprocess.run(["docker", "restart", container_name], check=True)

def verify_stability():
    time.sleep(30)
    from monitor import get_cpu_usage
    cpu = get_cpu_usage()
    return cpu < 80
