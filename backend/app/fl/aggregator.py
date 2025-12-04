import torch
import torch.nn as nn
from copy import deepcopy

class Aggregator:
    def aggregate(self, client_weights_list):
        """
        FedAvg implementation.
        Expects list of dicts: {'weights': state_dict, 'samples': num_samples}
        """
        total_samples = sum(c['samples'] for c in client_weights_list)
        if total_samples == 0:
            return None
            
        # Initialize with first client's weights * weight_fraction
        first_client = client_weights_list[0]
        w_avg = deepcopy(first_client['weights'])
        
        for key in w_avg.keys():
            w_avg[key] = w_avg[key] * (first_client['samples'] / total_samples)
            
        # Add rest
        for i in range(1, len(client_weights_list)):
            client = client_weights_list[i]
            for key in w_avg.keys():
                w_avg[key] += client['weights'][key] * (client['samples'] / total_samples)
                
        return w_avg

    def evaluate(self, model, test_loader, device='cpu'):
        """
        Evaluate global model.
        """
        model.to(device)
        model.eval()
        test_loss = 0
        correct = 0
        criterion = nn.CrossEntropyLoss(reduction='sum')
        
        with torch.no_grad():
            for data, target in test_loader:
                data, target = data.to(device), target.to(device)
                output = model(data)
                test_loss += criterion(output, target).item()
                pred = output.argmax(dim=1, keepdim=True)
                correct += pred.eq(target.view_as(pred)).sum().item()
                
        test_loss /= len(test_loader.dataset)
        accuracy = correct / len(test_loader.dataset)
        
        return {"accuracy": accuracy, "loss": test_loss}
