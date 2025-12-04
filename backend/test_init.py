import requests
import json

try:
    print("Sending request to http://127.0.0.1:8000/api/init")
    response = requests.post(
        "http://127.0.0.1:8000/api/init",
        json={"num_clients": 5}
    )
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
