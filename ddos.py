import threading
import requests

# Define the function to send the request
def send_request(router_ip):
    try:
        response = requests.get(f"http://{router_ip}", timeout=2)
        print("Status Code:", response.status_code)
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")

# Replace with your router IP
router_ip = "192.168.0.1"

# Create multiple threads
threads = []
for _ in range(5000):  # Number of instances
    thread = threading.Thread(target=send_request, args=(router_ip,))
    threads.append(thread)
    thread.start()

# Wait for all threads to complete
for thread in threads:
    thread.join()

