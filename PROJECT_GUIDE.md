# Secure Federated Learning with Blockchain - Project Guide

This project demonstrates a secure, decentralized approach to machine learning using **Federated Learning (FL)** and **Blockchain**.

## 1. Project Overview

### What is Federated Learning?
Traditionally, to train an AI model (like predicting heart disease), all hospitals would send their patient data to a central server. This is a huge privacy risk.
**Federated Learning** solves this:
1.  The Server sends the global model to the hospitals (Clients).
2.  Hospitals train the model on their *private* data locally.
3.  Hospitals send only the *updates* (mathematical weights) back to the server.
4.  The Server averages these updates to improve the global model.
**Result**: The model learns from everyone's data, but the data never leaves the hospital.

### Why Blockchain?
In standard FL, the central server is a single point of failure. It could lie about the results or be hacked.
**Blockchain** adds a layer of trust:
1.  Every training round is recorded on an immutable ledger.
2.  We store the **Model Hash** (digital fingerprint) and performance metrics on-chain.
3.  This creates an audit trail that proves the model's history and integrity.

## 2. Technical Architecture

*   **Frontend**: React (TypeScript) + Tailwind CSS.
    *   *Role*: Dashboard to control the experiment and visualize the blockchain ledger.
*   **Backend**: Python (FastAPI).
    *   *Role*: Orchestrates the FL process, manages the Neural Network, and talks to the Blockchain.
*   **ML Engine**: PyTorch.
    *   *Model*: A Neural Network (`HeartDiseaseNN`) trained on the UCI Heart Disease dataset.
*   **Blockchain**: Ganache (Local Ethereum) + Solidity Smart Contract.
    *   *Contract*: `FLRegistry.sol` stores the history of training rounds.

## 3. How to Run the Project

### Prerequisites
1.  **Ganache**: Installed and running (Quickstart workspace).
2.  **Node.js**: Installed.
3.  **Python**: Installed.

### Step 1: Start Ganache
You have two options:

**Option A: Using CLI (Recommended)**
Run this command to start a blockchain on port 8545 with the correct keys:
```bash
npx ganache --port 8545 --wallet.deterministic
```

**Option B: Using GUI**
1.  Open Ganache.
2.  Go to **Settings** -> **Server**.
3.  Change **Port Number** to `8545`.
4.  Restart Ganache.
5.  Copy the Private Key of Account 0.
6.  Update `backend/app/api/endpoints.py` with your key if it differs from the default.

### Step 2: Configure Backend
1.  Open `backend/app/api/endpoints.py`.
2.  Paste your Private Key into the `PRIVATE_KEY` variable:
    ```python
    PRIVATE_KEY = "YOUR_COPIED_PRIVATE_KEY"
    ```

### Step 3: Start Backend Server
Open a terminal:
```bash
cd backend
# Install dependencies (if needed)
pip install -r requirements.txt
# Run server
uvicorn main:app --reload
```
*Server runs at http://127.0.0.1:8000*

### Step 4: Start Frontend
Open a **new** terminal:
```bash
cd frontend_react
# Install dependencies (if needed)
npm install
# Run frontend
npm start
```
*App opens at http://localhost:3000*

## 4. Using the Application

1.  **Initialize**: Go to the web app and click **"Initialize Experiment"**.
    *   *What happens*: The backend downloads the data, creates 5 simulated clients, and deploys the Smart Contract to your Ganache blockchain.
2.  **Run Round**: Click **"Run Training Round"**.
    *   *What happens*: The server coordinates a training round. Clients train locally. The server aggregates the results and saves the proof (Block) to the Blockchain.
3.  **Verify**:
    *   Watch the **Accuracy Chart** go up.
    *   See new **Blocks** appear in the Ledger below.
    *   Check **Ganache**: You will see new transactions and blocks being mined!
