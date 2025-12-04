import json
import os
from web3 import Web3
from solcx import compile_standard, install_solc

class Web3Manager:
    def __init__(self, rpc_url="http://127.0.0.1:7545", private_key=None):
        self.w3 = Web3(Web3.HTTPProvider(rpc_url))
        self.private_key = private_key
        self.account = self.w3.eth.account.from_key(private_key) if private_key else None
        self.contract = None
        self.chain_id = 1337 # Default Ganache

        if not self.w3.is_connected():
            raise Exception("Failed to connect to Ganache")
        
        # Install specific solc version
        try:
            install_solc('0.8.0')
        except Exception as e:
            print(f"Solc install warning: {e}")

    def deploy_contract(self):
        with open("contracts/FLRegistry.sol", "r") as file:
            fl_registry_file = file.read()

        compiled_sol = compile_standard(
            {
                "language": "Solidity",
                "sources": {"FLRegistry.sol": {"content": fl_registry_file}},
                "settings": {
                    "outputSelection": {
                        "*": {
                            "*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]
                        }
                    }
                },
            },
            solc_version="0.8.0",
        )

        bytecode = compiled_sol["contracts"]["FLRegistry.sol"]["FLRegistry"]["evm"]["bytecode"]["object"]
        abi = compiled_sol["contracts"]["FLRegistry.sol"]["FLRegistry"]["abi"]

        # Deploy
        FLRegistry = self.w3.eth.contract(abi=abi, bytecode=bytecode)
        
        nonce = self.w3.eth.get_transaction_count(self.account.address)
        transaction = FLRegistry.constructor().build_transaction({
            "chainId": self.chain_id,
            "gasPrice": self.w3.eth.gas_price,
            "from": self.account.address,
            "nonce": nonce,
        })
        
        signed_txn = self.w3.eth.account.sign_transaction(transaction, private_key=self.private_key)
        tx_hash = self.w3.eth.send_raw_transaction(signed_txn.raw_transaction)
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        
        self.contract = self.w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
        return tx_receipt.contractAddress

    def add_round(self, model_hash, global_accuracy, contributions):
        """
        contributions: List of dicts matching the struct
        """
        nonce = self.w3.eth.get_transaction_count(self.account.address)
        
        # Scale float metrics to int (x 10000)
        scaled_acc = int(global_accuracy * 10000)
        
        formatted_contributions = []
        for c in contributions:
            formatted_contributions.append((
                c['client_id'],
                c['samples'],
                int(c['accuracy'] * 10000),
                int(c['loss'] * 10000),
                c['malicious'],
                c.get('accepted', True)
            ))

        transaction = self.contract.functions.addRound(
            model_hash,
            scaled_acc,
            formatted_contributions
        ).build_transaction({
            "chainId": self.chain_id,
            "gasPrice": self.w3.eth.gas_price,
            "from": self.account.address,
            "nonce": nonce,
        })
        
        signed_txn = self.w3.eth.account.sign_transaction(transaction, private_key=self.private_key)
        tx_hash = self.w3.eth.send_raw_transaction(signed_txn.raw_transaction)
        return self.w3.eth.wait_for_transaction_receipt(tx_hash)

    def get_chain(self):
        length = self.contract.functions.getChainLength().call()
        chain_data = []
        for i in range(length):
            data = self.contract.functions.getRound(i).call()
            # Unpack
            round_id, model_hash, global_acc, timestamp, contribs = data
            
            # Format contributions back to list of dicts
            formatted_contribs = []
            for c in contribs:
                formatted_contribs.append({
                    "client_id": c[0],
                    "samples": c[1],
                    "accuracy": c[2] / 10000.0,
                    "loss": c[3] / 10000.0,
                    "malicious": c[4],
                    "accepted": c[5]
                })

            chain_data.append({
                "index": round_id,
                "model_hash": model_hash,
                "round_metrics": {"accuracy": global_acc / 10000.0},
                "timestamp": timestamp,
                "client_contributions": formatted_contribs,
                "hash": f"block_{round_id}", # Placeholder as we don't hash the block on-chain in this simple contract
                "previous_hash": "0x0" if round_id == 0 else f"block_{round_id-1}"
            })
        return chain_data
