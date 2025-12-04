# How to Run the Secure Federated Learning Project Manually

Follow these steps to run the project on your local machine without the AI agent.

## 1. Prerequisites

*   **Python 3.8+**: Ensure Python is installed.
*   **Node.js & npm**: Ensure Node.js is installed.
*   **Ganache**: Download and install [Ganache](https://trufflesuite.com/ganache/) for a local Ethereum blockchain.

## 2. Start Ganache

1.  Open **Ganache**.
2.  Click **"Quickstart"** to create a temporary workspace.
3.  Note the **RPC Server** URL (usually `http://127.0.0.1:7545`).
4.  Copy the **Private Key** of the first account (Account 0). Click the "Key" icon on the right side of the account row to reveal it.

## 3. Backend Setup (Python)

1.  Open a terminal and navigate to the `backend` directory:
    ```bash
    cd backend
    ```

2.  Create and activate a virtual environment (optional but recommended):
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # Mac/Linux
    source venv/bin/activate
    ```

3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Blockchain Credentials**:
    *   Open `backend/app/api/endpoints.py` in a text editor.
    *   Find the `PRIVATE_KEY` variable (around line 26).
    *   Replace `"0x..."` with the Private Key you copied from Ganache.
    ```python
    PRIVATE_KEY = "YOUR_COPIED_PRIVATE_KEY"
    ```

5.  Run the Backend Server:
    ```bash
    uvicorn main:app --reload
    ```
    The backend will start at `http://127.0.0.1:8000`.

## 4. Frontend Setup (React)

1.  Open a **new** terminal window and navigate to the `frontend_react` directory:
    ```bash
    cd frontend_react
    ```

2.  Install dependencies:
    ```bash
    npm install
    ```

3.  Start the Frontend:
    ```bash
    npm start
    ```
    The application will open in your browser at `http://localhost:3000`.

## 5. Using the Application

1.  Go to `http://localhost:3000` in your browser.
2.  Click **"Initialize Experiment"**. This will:
    *   Download the Heart Disease dataset.
    *   Deploy the Smart Contract to your Ganache blockchain.
3.  Use the **"Run Training Round"** button to start the Federated Learning process.
4.  Watch the **Training Accuracy** chart update and new blocks appear in the **Blockchain Ledger**.
