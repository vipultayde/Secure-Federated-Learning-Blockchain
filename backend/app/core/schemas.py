from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class InitRequest(BaseModel):
    num_clients: int = 5
    local_epochs: int = 1
    learning_rate: float = 0.01

class BlockModel(BaseModel):
    index: int
    timestamp: float
    previous_hash: str
    model_hash: str
    round_metrics: Dict[str, float]
    client_contributions: List[Dict[str, Any]]
    hash: str

class ChainResponse(BaseModel):
    blocks: List[BlockModel]

class RoundResponse(BaseModel):
    round_id: int
    global_accuracy: float
    block_hash: str
