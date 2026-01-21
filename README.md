# Blockchain-Based Dual-Key Encryption & Secure Key Management System

## 📌 Project Overview
This project is an enterprise-grade backend security system designed to protect sensitive data using a **Dual-Key Encryption Model** combined with a **Blockchain-Based Immutable Audit Ledger**. It eliminates single points of failure by requiring two independent keys for decryption and ensures all access events are permanently logged.

## 🚀 Features
- **Dual-Key Encryption**: Requires both a System Key (Key-A) and a User Key (Key-B) to decrypt data (AES-256).
- **Blockchain Audit Ledger**: Tamper-proof log of all encryption and decryption events using SHA-256 hashing.
- **Role-Based Access Control (RBAC)**:
  - **ADMIN**: Full access (Encrypt, Decrypt, Audit, Monitor).
  - **SERVICE**: Encryption only (cannot decrypt).
  - **AUDITOR**: Read-only access to the blockchain ledger.
- **Real-time Monitoring**: Detects anomalies like excessive decryption failures.
- **Modern Frontend**: React-based dashboard for easy interaction.

## 🛠️ Tech Stack
- **Backend**: Python, FastAPI, Cryptography (Fernet/AES), Jose (JWT).
- **Frontend**: React.js, Vite, Axios, Vanilla CSS.
- **Database**: MySQL (Relational Database).
- **Encryption**: Hybrid Post-Quantum (Kyber-1024 + AES-256).


## ⚙️ Prerequisites
- **Python** (3.8 or higher)
- **Node.js** (14 or higher) & **npm**

---

## 📥 Installation & Setup

### 1. Backend Setup
Navigate to the project root and install Python dependencies:

```bash
cd backend
pip install -r requirements.txt
```

### 2. Frontend Setup
Navigate to the frontend directory and install Node dependencies:

```bash
cd frontend
npm install
```

---

## ▶️ Running the Application

You need to run the Backend and Frontend in separate terminals.

### Terminal 1: Start Backend
```bash
# From the 'backend' directory
uvicorn app.main:app --reload
```
*Server running at: `http://127.0.0.1:8000`*

### Terminal 2: Start Frontend
```bash
# From the 'frontend' directory
npm run dev
```
*UI running at: `http://localhost:5173`*

### Alternative: One-Click Start (Windows)
Simply double-click the `run_app.bat` file in the root directory to start both servers automatically.

---

## 📖 Usage Guide

### 1. Login
Access the frontend at `http://localhost:5173`. Use the following credentials:

| Role | Username | Password | Capabilities |
|------|----------|----------|--------------|
| **Admin** | `admin` | `password` | Encrypt, Decrypt, View Ledger, View Alerts |
| **Service** | `service` | `password` | Encrypt Only |
| **Auditor** | `auditor` | `password` | View Ledger Only |

### 2. Encrypting Data
1. Login as **Admin** or **Service**.
2. Go to **Encrypt Data**.
3. Enter your sensitive text.
4. Provide a **User Key** (e.g., `my-secret-pass`) and a **Key ID** (e.g., `doc-1`).
5. Click **Encrypt**.
6. **IMPORTANT**: Copy BOTH the `Encrypted Data` and the `Kyber Ciphertext`. You will need both to decrypt.

### 3. Decrypting Data
1. Login as **Admin**.
2. Go to **Decrypt Data**.
3. Paste the `Encrypted Data`.
4. Paste the `Kyber Ciphertext`.
4. Enter the **SAME** User Key and Key ID used during encryption.
5. Click **Decrypt** to reveal the original text.

### 4. Auditing
1. Login as **Admin** or **Auditor**.
2. Go to **Audit Ledger**.
3. View the immutable chain of blocks recording every action.

---

## 🧪 Running Tests
To run the backend integration tests:

```bash
# From the root directory
$env:PYTHONPATH="backend"
pytest backend/tests/test_main.py
```

---

## 📂 Project Structure
```
├── backend/                # Backend (FastAPI)
│   ├── app/
│   │   ├── auth/           # JWT Authentication
│   │   ├── blockchain/     # Ledger Logic
│   │   ├── encryption/     # Dual-Key Engine
│   │   ├── key_management/ # Key Storage
│   │   ├── monitoring/     # Anomaly Detection
│   │   └── main.py         # App Entry Point
│   ├── database/           # Local storage for Ledger & Keys
│   └── tests/              # Integration Tests
│
├── frontend/               # Frontend (React)
│   ├── src/
│   │   ├── components/     # React Components
│   │   └── api.js          # API Configuration
│   └── package.json
│
└── README.md               # This file
```
