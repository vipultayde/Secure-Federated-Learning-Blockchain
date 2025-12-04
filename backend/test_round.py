import requests
import json
import time

BASE_URL = "http://127.0.0.1:8000/api"

def run_test():
    try:
        # 1. Init (just in case, though it should be initialized)
        # print("Initializing...")
        # requests.post(f"{BASE_URL}/init", json={"num_clients": 5})
        
        # 2. Run Round
        print("Running Round...")
        start_time = time.time()
        response = requests.post(f"{BASE_URL}/round", json={"malicious_indices": [], "defense_enabled": False})
        print(f"Round Status: {response.status_code}")
        print(f"Round Response: {response.text}")
        print(f"Time taken: {time.time() - start_time:.2f}s")
        
        if response.status_code == 200:
            # 3. Get Chain
            print("Fetching Chain...")
            chain_res = requests.get(f"{BASE_URL}/chain")
            print(f"Chain: {json.dumps(chain_res.json(), indent=2)}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    run_test()
