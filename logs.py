from ollama import Client
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeout

client = Client(host="http://localhost:11434", timeout=120)
executor = ThreadPoolExecutor(max_workers=1)

def filter_logs(logs):
    """
    Keep only lines containing ERROR or WARNING.
    """
    filtered = []
    for line in logs.splitlines():
        if "ERROR" in line or "WARNING" in line:
            filtered.append(line)
    return "\n".join(filtered) if filtered else logs

def analyze_logs(logs):
    cleaned_logs = filter_logs(logs)

    prompt = f"""
You are an AI DevOps assistant. Given these logs, identify likely causes of high CPU usage and suggest potential remediation steps.

Logs:
{cleaned_logs}
"""

    print("Sending logs to Ollama...")

    def call_ollama():
        response = client.chat(
            model="tinyllama",
            messages=[
                {"role": "system", "content": "You are a reliable DevOps assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return response

    future = executor.submit(call_ollama)
    try:
        response = future.result(timeout=120)  # 20 seconds timeout

        print("=== RAW RESPONSE ===")
        print(response)

        if "message" in response and "content" in response["message"]:
            content = response["message"]["content"].strip()
            print("=== MESSAGE CONTENT ===")
            print(content)
            return content
        else:
            print("⚠️ Unexpected response format")
            return "No valid response from Ollama."

    except FuturesTimeout:
        print("❌ Ollama timed out.")
        return "Ollama took too long to respond."

    except Exception as e:
        print("❌ Error during Ollama call:", e)
        return "Error analyzing logs."
