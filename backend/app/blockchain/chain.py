from .block import Block

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, "0", "genesis_model", {}, [])

    def add_block(self, block):
        if block.previous_hash != self.chain[-1].hash:
            return False
        if block.index != self.chain[-1].index + 1:
            return False
        self.chain.append(block)
        return True

    def is_valid(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i-1]
            
            if current.hash != current.calculate_hash():
                return False
            if current.previous_hash != previous.hash:
                return False
        return True
