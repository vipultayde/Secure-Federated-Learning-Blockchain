# Secure Federated Learning with Blockchain

A decentralized machine learning system that combines **Federated Learning (FL)** with **Blockchain** technology to enable secure, privacy-preserving, and auditable AI model training.

![Project Status](https://img.shields.io/badge/status-active-success)
![License](https://img.shields.io/badge/license-MIT-blue)

## 🚀 Project Overview

Traditional machine learning requires collecting data on a central server, which raises significant privacy concerns, especially in healthcare and finance. **Federated Learning** solves this by training models locally on client devices and only sharing model updates.

However, standard FL systems rely on a central aggregator that could be a single point of failure or manipulation. This project integrates **Blockchain** to create an immutable ledger of all training rounds, ensuring transparency, traceability, and trust.

### Key Features
*   **Privacy-First**: Raw data never leaves the client (simulated hospitals).
*   **Immutable Audit Trail**: Every training round, model hash, and performance metric is recorded on the Ethereum blockchain.
*   **Decentralized Trust**: Smart contracts verify and log the training process.
*   **Healthcare Use Case**: Demonstrates Heart Disease prediction using a Neural Network.
*   **Interactive Dashboard**: A React-based UI to visualize the training progress and blockchain ledger in real-time.

---

## 🛠 Tech Stack

### Frontend
*   **React (TypeScript)**: For a robust and type-safe user interface.
*   **Tailwind CSS**: For modern, responsive styling.
*   **Recharts**: For real-time visualization of model accuracy.

### Backend
*   **Python (FastAPI)**: High-performance API for orchestration.
*   **PyTorch**: Deep learning framework for the Neural Network.
*   **Web3.py**: Python library for interacting with the Ethereum blockchain.
*   **Scikit-Learn**: For data preprocessing and splitting.

### Blockchain
*   **Ganache**: Local Ethereum blockchain for development.
*   **Solidity**: Smart contract language for the `FLRegistry`.

---

## 🏗 Architecture

1.  **Initialization**: The system deploys the `FLRegistry` smart contract and prepares the dataset.
2.  **Distribution**: The global model is sent to selected clients.
3.  **Local Training**: Clients train the model on their private data (FedAvg algorithm).
4.  **Aggregation**: The server aggregates client updates to create a new global model.
5.  **Consensus & Logging**: The new model's hash and metrics are mined into a block on the blockchain.

---

## 🏁 Getting Started

### Prerequisites
*   **Node.js** (v14+)
*   **Python** (v3.8+)
*   **Ganache** (CLI or GUI)

### Installation & Run Guide

#### 1. Start the Blockchain
Open a terminal and start a local Ganache instance on port 8545.
```bash
npx ganache --port 8545 --wallet.deterministic
```

#### 2. Start the Backend
Open a new terminal.
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```
*The API will run at `http://127.0.0.1:8000`*

#### 3. Start the Frontend
Open a new terminal.
```bash
cd frontend_react
npm install
npm start
```
*The app will open at `http://localhost:3000`*

---

## 🧪 Usage

1.  **Initialize Experiment**: Click the button on the dashboard to deploy the contract and prepare the clients.
2.  **Run Training Round**: Click to trigger a Federated Learning round.
    *   Watch the **Accuracy Chart** update.
    *   See a new **Block** appear in the ledger below.
3.  **Simulate Attacks**: Toggle "Malicious Client" to see how the system behaves (optional defense mechanisms can be enabled).

---

## 📂 Project Structure

```
├── backend/
│   ├── app/
│   │   ├── api/            # API Endpoints
│   │   ├── blockchain/     # Web3 & Smart Contract Logic
│   │   ├── fl/             # ML Model, Client, & Aggregator
│   │   └── core/           # Config & Schemas
│   ├── contracts/          # Solidity Smart Contracts
│   └── main.py             # Entry Point
├── frontend_react/
│   ├── src/
│   │   ├── components/     # UI Components (Charts, Cards)
│   │   ├── pages/          # Main Dashboard
│   │   └── api/            # API Client
└── README.md
```

## 📜 License
This project is licensed under the MIT License.
