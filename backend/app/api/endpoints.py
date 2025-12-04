from fastapi import APIRouter, HTTPException
from app.core.schemas import InitRequest, RoundResponse, ChainResponse, BlockModel
from pydantic import BaseModel
from typing import List
from app.fl.model import HeartDiseaseNN
from app.fl.dataset import get_heart_disease_data, partition_data
from app.fl.client import FLClient
from app.fl.aggregator import Aggregator
from app.blockchain.web3_manager import Web3Manager
import torch
import copy
import hashlib

router = APIRouter()

# Global State
class ExperimentState:
    def __init__(self):
        self.num_clients = 0
        self.clients = []
        self.global_model = None
        self.web3 = None
        self.aggregator = Aggregator()
        self.test_loader = None
        self.round_id = 0
        self.initialized = False

state = ExperimentState()

# TODO: Replace with user provided credentials
GANACHE_URL = "http://127.0.0.1:8545"
# Default Ganache Account #0 Private Key (often deterministic, but user should provide)
PRIVATE_KEY = "0x4f3edf983ac636a65a842ce7c78d9aa706d3b113bce9c46f30d7d21715b23b1d" 

@router.post("/init")
def initialize_experiment(request: InitRequest):
    """
    Reset chain, re-partition data, initialize model.
    """
    global state
    state = ExperimentState() # Reset
    state.num_clients = request.num_clients
    
    # Load Data
    train_dataset, test_dataset = get_heart_disease_data()
    client_datasets = partition_data(train_dataset, request.num_clients)
    state.test_loader = torch.utils.data.DataLoader(test_dataset, batch_size=1000, shuffle=False)
    
    # Init Clients
    state.clients = []
    for i in range(request.num_clients):
        loader = torch.utils.data.DataLoader(client_datasets[i], batch_size=32, shuffle=True)
        state.clients.append(FLClient(i, loader))
        
    # Init Model
    state.global_model = HeartDiseaseNN()
    
    # Init Blockchain (Deploy Contract)
    try:
        if PRIVATE_KEY == "0x...":
             # We will try to proceed without a private key if the user hasn't set one, 
             # but Web3Manager might fail if it needs to sign transactions.
             # For Ganache, we can often use the unlocked accounts directly if we don't provide a key,
             # but our Web3Manager is written to use a key.
             # Let's assume the user will provide it.
             print("WARNING: No PRIVATE_KEY set. Blockchain operations may fail.")
             
        state.web3 = Web3Manager(GANACHE_URL, PRIVATE_KEY if PRIVATE_KEY != "0x..." else None)
        state.web3.deploy_contract()
    except Exception as e:
        print(f"Blockchain init failed: {e}")
        raise HTTPException(status_code=500, detail=f"Blockchain init failed: {str(e)}. Please check Ganache credentials.")
    
    state.initialized = True
    return {"status": "initialized", "genesis_block": "contract_deployed"}

class RoundRequest(BaseModel):
    malicious_indices: List[int] = []
    defense_enabled: bool = False

@router.post("/round", response_model=RoundResponse)
def run_round(request: RoundRequest = RoundRequest()):
    """
    Trigger one FL round.
    """
    if not state.initialized:
        raise HTTPException(status_code=400, detail="Experiment not initialized")
        
    state.round_id += 1
    
    # 1. Distribute global weights (simulated by passing model to clients)
    # 2. Local Training
    client_weights = []
    client_contributions = []
    
    for client in state.clients:
        # Train
        is_malicious = client.client_id in request.malicious_indices
        result = client.train(state.global_model, epochs=1, lr=0.01, malicious=is_malicious)
        
        # Defense: Evaluate client update on server validation set
        keep_update = True
        if request.defense_enabled:
            # Create temp model with client weights
            temp_model = copy.deepcopy(state.global_model)
            temp_model.load_state_dict(result['weights'])
            # Evaluate (using small subset of test loader for speed would be better, but full is fine for demo)
            val_metrics = state.aggregator.evaluate(temp_model, state.test_loader)
            if val_metrics['accuracy'] < 0.5: # Threshold
                keep_update = False
        
        if keep_update:
            client_weights.append({
                'weights': result['weights'],
                'samples': result['samples']
            })
            
        client_contributions.append({
            'client_id': client.client_id,
            'samples': result['samples'],
            'accuracy': result['accuracy'],
            'loss': result['loss'],
            'malicious': is_malicious,
            'accepted': keep_update
        })
        
    # 3. Aggregate
    if client_weights:
        new_weights = state.aggregator.aggregate(client_weights)
        state.global_model.load_state_dict(new_weights)
    else:
        # No updates accepted, keep old weights
        new_weights = state.global_model.state_dict()
    
    # 4. Evaluate
    metrics = state.aggregator.evaluate(state.global_model, state.test_loader)
    
    # 5. Record on Blockchain
    # Sort keys for deterministic hashing
    model_hash_input = str(new_weights.keys()) + str(sum([t.sum().item() for t in new_weights.values()]))
    model_hash = hashlib.sha256(model_hash_input.encode()).hexdigest()
    
    try:
        receipt = state.web3.add_round(model_hash, metrics['accuracy'], client_contributions)
        block_hash = receipt.transactionHash.hex()
    except Exception as e:
        print(f"Blockchain transaction failed: {e}")
        raise HTTPException(status_code=500, detail=f"Blockchain transaction failed: {str(e)}")

    return {
        "round_id": state.round_id,
        "global_accuracy": metrics['accuracy'],
        "block_hash": block_hash
    }

@router.get("/chain", response_model=ChainResponse)
def get_chain():
    """
    Get the full blockchain.
    """
    if not state.initialized:
        return {"blocks": []}
    
    try:
        chain_data = state.web3.get_chain()
        # Convert to BlockModel
        blocks = []
        for b in chain_data:
            blocks.append(BlockModel(**b))
        return {"blocks": blocks}
    except Exception as e:
        print(f"Failed to fetch chain: {e}")
        return {"blocks": []}

@router.get("/metrics")
def get_metrics():
    """
    Get training metrics (accuracy/loss over rounds).
    """
    if not state.initialized:
        return {"metrics": []}
        
    try:
        chain_data = state.web3.get_chain()
        metrics = []
        for b in chain_data:
            metrics.append({
                "round": b['index'],
                "accuracy": b['round_metrics']['accuracy'],
                "loss": 0.0 # We didn't store global loss in contract for simplicity, or we can add it
            })
        return {"metrics": metrics}
    except Exception as e:
        return {"metrics": []}
