import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import torch
from torch.utils.data import TensorDataset, random_split

def get_heart_disease_data():
    # Load Heart Disease dataset (Cleveland)
    url = "https://archive.ics.uci.edu/ml/machine-learning-databases/heart-disease/processed.cleveland.data"
    column_names = [
        "age", "sex", "cp", "trestbps", "chol", "fbs", "restecg", 
        "thalach", "exang", "oldpeak", "slope", "ca", "thal", "target"
    ]
    
    # '?' indicates missing values
    df = pd.read_csv(url, names=column_names, na_values="?")
    
    # Drop rows with missing values (only a few in this dataset)
    df = df.dropna()
    
    X = df.drop("target", axis=1).values
    y = df["target"].values
    
    # Convert target to binary: 0 = no disease, 1-4 = disease
    y = np.where(y > 0, 1, 0)

    # Normalize features
    scaler = StandardScaler()
    X = scaler.fit_transform(X)

    # Convert to Tensor
    X_tensor = torch.tensor(X, dtype=torch.float32)
    y_tensor = torch.tensor(y, dtype=torch.long)

    # Split
    X_train, X_test, y_train, y_test = train_test_split(X_tensor, y_tensor, test_size=0.2, random_state=42)

    train_dataset = TensorDataset(X_train, y_train)
    test_dataset = TensorDataset(X_test, y_test)

    return train_dataset, test_dataset

def partition_data(dataset, num_clients):
    """
    Split dataset into `num_clients` IID subsets.
    """
    total_size = len(dataset)
    split_size = total_size // num_clients
    lengths = [split_size] * num_clients
    # Handle remainder
    lengths[-1] += total_size - sum(lengths)
    
    return random_split(dataset, lengths)
