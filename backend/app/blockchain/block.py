import hashlib
import json
import time

class Block:
    def __init__(self, index, previous_hash, model_hash, round_metrics, client_contributions):
        self.index = index
        self.timestamp = time.time()
        self.previous_hash = previous_hash
        self.model_hash = model_hash
        self.round_metrics = round_metrics
        self.client_contributions = client_contributions
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "previous_hash": self.previous_hash,
            "model_hash": self.model_hash,
            "round_metrics": self.round_metrics,
            "client_contributions": self.client_contributions
        }, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()
