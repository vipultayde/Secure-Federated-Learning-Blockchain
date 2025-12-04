# How to Run the Project from Console

Follow these steps exactly. You will need **3 separate terminal windows**.

## Terminal 1: Blockchain (Ganache)
Run this command to start the local blockchain on port 8545.
```bash
npx ganache --port 8545 --wallet.deterministic
```
*Keep this terminal open. Do not close it.*

## Terminal 2: Backend (Python API)
Open a new terminal and navigate to the `backend` folder.
```bash
cd backend
```
Install dependencies (only need to do this once):
```bash
pip install -r requirements.txt
```
Start the backend server:
```bash
uvicorn main:app --reload
```
*You should see "Uvicorn running on http://127.0.0.1:8000". Keep this terminal open.*

## Terminal 3: Frontend (React UI)
Open a new terminal and navigate to the `frontend_react` folder.
```bash
cd frontend_react
```
Install dependencies (only need to do this once):
```bash
npm install
```
Start the frontend:
```bash
npm start
```
*This will open your browser at http://localhost:3000.*

## Final Step: Use the App
1. Go to **http://localhost:3000**.
2. Click **"Initialize Experiment"**.
3. Click **"Run Training Round"**.
