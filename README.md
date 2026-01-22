# Blockchain-Based Dual-Key Encryption & Secure Key Management System

## 📌 Project Overview
This project is an enterprise-grade backend security system designed to protect sensitive data using a **Dual-Key Encryption Model** combined with a **Blockchain-Based Immutable Audit Ledger**. It eliminates single points of failure by requiring two independent keys for decryption and ensures all access events are permanently logged.

It is future-proofed against next-generation threats by integrating **Post-Quantum Cryptography (Kyber-1024)**.

## 🚀 Key Features
### 🔐 Advanced Security
- **Dual-Key Encryption**: Requires both a System Key (Key-A) and a User Key (Key-B) to decrypt data.
- **Post-Quantum Cryptography**: Uses **Kyber-1024** (NIST-approved) to protect keys against quantum computer attacks.
- **AES-256**: Military-grade standard for data encryption.

### 📜 Immutable Audit Trail
- **Blockchain Ledger**: Every action (Encrypt, Decrypt, Failure) is recorded in a tamper-proof SHA-256 linked list.
- **MySQL Storage**: The blockchain is persisted in a relational database for reliability.

### 📂 File Security
- **File Encryption**: Securely upload, encrypt, and download files (PDFs, Images, Docs).
- **Secure Transfer**: Files are encrypted in transit and at rest.

### 📊 Visual Analytics
- **Security Dashboard**: Real-time graphs showing system activity (Encryption vs Decryption).
- **Anomaly Detection**: Alerts for suspicious activities like excessive decryption failures.

### 👥 Role-Based Access Control (RBAC)
- **ADMIN**: Full access (Encrypt, Decrypt, Audit, Monitor).
- **SERVICE**: Encryption only (cannot decrypt).
- **AUDITOR**: Read-only access to the blockchain ledger.

---

## 🛠️ Tech Stack
- **Backend**: Python, FastAPI, SQLAlchemy, PyMySQL.
- **Frontend**: React.js, Vite, Recharts (for graphs).
- **Database**: MySQL.
- **Cryptography**: `pycryptodome` (AES), `pqc` (Kyber).
- **Blockchain**: Custom Python implementation with SHA-256 hashing.

---

## 📥 Installation & Setup

### Option 1: One-Click Setup (Recommended)
1.  Clone the repository.
2.  Double-click **`setup_project.bat`**.
    *   This script will automatically install all Python and Node.js dependencies for you.

### Option 2: Manual Setup
**Backend:**
```bash
cd backend
pip install -r requirements.txt
```

**Frontend:**
```bash
cd frontend
npm install
```

### Database Setup
1.  Ensure you have MySQL installed and running.
2.  Create a database named `dualkey_db`.
3.  (Optional) You can import the schema from `database/Database.sql`.

---

## ▶️ Running the Application

Simply double-click **`run_app.bat`** to start both the Backend and Frontend servers automatically.

Or run them manually:
*   **Backend**: `uvicorn app.main:app --reload` (Port 8000)
*   **Frontend**: `npm run dev` (Port 5173)

---

## 📖 Usage Guide

### 1. Login
Access the UI at `http://localhost:5173`.
*   **Admin**: `admin` / `password`
*   **Service**: `service` / `password`
*   **Auditor**: `auditor` / `password`

### 2. Encrypting Data (Text or File)
1.  Go to **Encrypt Data**.
2.  Choose **Text** or **File** tab.
3.  Enter data/upload file.
4.  Provide a **User Key** (Password) and **Key ID**.
5.  **Save the Output**: You need the `Kyber Ciphertext` to decrypt later!

### 3. Decrypting Data
1.  Go to **Decrypt Data**.
2.  Paste the `Encrypted Data` (or upload `.enc` file).
3.  Paste the `Kyber Ciphertext`.
4.  Enter the **Same User Key**.
5.  Click Decrypt.

### 4. Monitoring
*   **Audit Ledger**: View the raw blockchain logs.
*   **Security Alerts**: View visual graphs of system usage and alerts.

---

## 📂 Project Structure
```
├── backend/                # FastAPI Backend
│   ├── app/
│   │   ├── auth/           # JWT & RBAC
│   │   ├── blockchain/     # Ledger Logic
│   │   ├── encryption/     # Dual-Key & Kyber Engine
│   │   ├── monitoring/     # Analytics & Alerts
│   │   └── main.py         # Entry Point
│   └── database/           # Database Config
│
├── frontend/               # React Frontend
│   ├── src/
│   │   ├── components/     # UI Components (Dashboard, Charts, etc.)
│   │   └── api.js          # Axios Config
│
├── database/               # SQL Schema
├── interview.txt           # Project Explanation Guide
├── run_app.bat             # Start App Script
├── setup_project.bat       # Install Dependencies Script
└── README.md               # This file
```
