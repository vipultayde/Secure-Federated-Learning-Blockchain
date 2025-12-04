import torch
import torch.nn as nn
import torch.optim as optim
from copy import deepcopy

class FLClient:
    def __init__(self, client_id, data_loader, device='cpu'):
        self.client_id = client_id
        self.data_loader = data_loader
        self.device = device

    def train(self, model, epochs, lr, malicious=False):
        """
        Train local model on private data.
        """
        local_model = deepcopy(model)
        
        if malicious:
            # Return random weights
            for param in local_model.parameters():
                param.data = torch.randn_like(param.data)
            return {
                "weights": local_model.state_dict(),
                "loss": 10.0,
                "accuracy": 0.1,
                "samples": len(self.data_loader.dataset)
            }

        local_model.to(self.device)
        local_model.train()
        
        optimizer = optim.SGD(local_model.parameters(), lr=lr)
        criterion = nn.CrossEntropyLoss()
        
        epoch_loss = 0.0
        correct = 0
        total = 0
        
        for _ in range(epochs):
            for data, target in self.data_loader:
                data, target = data.to(self.device), target.to(self.device)
                optimizer.zero_grad()
                output = local_model(data)
                loss = criterion(output, target)
                loss.backward()
                optimizer.step()
                
                epoch_loss += loss.item() * data.size(0)
                pred = output.argmax(dim=1, keepdim=True)
                correct += pred.eq(target.view_as(pred)).sum().item()
                total += data.size(0)
                
        return {
            "weights": local_model.state_dict(),
            "loss": epoch_loss / total if total > 0 else 0.0,
            "accuracy": correct / total if total > 0 else 0.0,
            "samples": total
        }
