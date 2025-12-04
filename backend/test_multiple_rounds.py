import requests
import json
import time

BASE_URL = "http://127.0.0.1:8000/api"

def run_multiple_rounds():
    try:
        # 1. Init
        print("Initializing...")
        requests.post(f"{BASE_URL}/init", json={"num_clients": 5})
        
        # 2. Run 3 Rounds
        for i in range(3):
            print(f"Running Round {i+1}...")
            response = requests.post(f"{BASE_URL}/round", json={"malicious_indices": [], "defense_enabled": False})
            if response.status_code != 200:
                print(f"Round {i+1} Failed: {response.text}")
                break
            print(f"Round {i+1} Success. Block Hash: {response.json().get('block_hash')}")
            time.sleep(1) # Brief pause
            
        # 3. Get Chain
        print("Fetching Chain...")
        chain_res = requests.get(f"{BASE_URL}/chain")
        blocks = chain_res.json().get('blocks', [])
        print(f"Total Blocks: {len(blocks)}")
        for b in blocks:
            print(f"Block Index: {b['index']}, Hash: {b['hash']}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    run_multiple_rounds()
