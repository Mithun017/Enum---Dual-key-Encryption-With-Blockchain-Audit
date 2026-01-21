from fastapi.testclient import TestClient
from app.main import app
import pytest

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "System Operational"}

def test_full_flow():
    # 1. Login as ADMIN
    login_response = client.post(
        "/auth/login",
        json={"username": "admin", "role": "ADMIN"},
        params={"password": "password"} # Assuming password is in body or params based on implementation
    )
    # Wait, my implementation expects body for both user and password?
    # Let's check app/auth/routes.py:
    # async def user_login(user: User = Body(...), password: str = Body(...)):
    # So it expects a JSON body with 'user' object and 'password' string?
    # No, Body(...) means it expects them as top level keys if not embedded?
    # Actually, if I use Body(...), it expects:
    # {
    #   "user": { "username": "...", "role": "..." },
    #   "password": "..."
    # }
    
    payload = {
        "user": {"username": "admin", "role": "ADMIN"},
        "password": "password"
    }
    login_response = client.post("/auth/login", json=payload)
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Encrypt Data
    encrypt_payload = {
        "data": "Sensitive Secret Data",
        "user_key": "user-secret-key-123",
        "key_id": "system-key-001"
    }
    encrypt_response = client.post("/encryption/encrypt", json=encrypt_payload, headers=headers)
    assert encrypt_response.status_code == 200
    encrypted_data = encrypt_response.json()["encrypted_data"]
    kyber_ciphertext = encrypt_response.json()["kyber_ciphertext"]
    assert encrypted_data != "Sensitive Secret Data"

    # 3. Decrypt Data
    decrypt_payload = {
        "encrypted_data": encrypted_data,
        "kyber_ciphertext": kyber_ciphertext,
        "user_key": "user-secret-key-123",
        "key_id": "system-key-001"
    }
    decrypt_response = client.post("/encryption/decrypt", json=decrypt_payload, headers=headers)
    if decrypt_response.status_code != 200:
        print(f"Decryption failed: {decrypt_response.text}")
    assert decrypt_response.status_code == 200
    assert decrypt_response.json()["data"] == "Sensitive Secret Data"

    # 4. Verify Blockchain Audit
    # Login as AUDITOR
    audit_login_payload = {
        "user": {"username": "auditor", "role": "AUDITOR"},
        "password": "password"
    }
    audit_login_response = client.post("/auth/login", json=audit_login_payload)
    audit_token = audit_login_response.json()["access_token"]
    audit_headers = {"Authorization": f"Bearer {audit_token}"}

    ledger_response = client.get("/audit/ledger", headers=audit_headers)
    assert ledger_response.status_code == 200
    chain = ledger_response.json()["chain"]
    
    # Should have at least Genesis, Encryption, Decryption
    # Should have at least Genesis, Encryption, Decryption
    assert len(chain) >= 3
    assert chain[-2]["event_type"] == "ENCRYPTION_KYBER"
    assert chain[-1]["event_type"] == "DECRYPTION_KYBER"

def test_access_denied():
    # Service user trying to decrypt
    payload = {
        "user": {"username": "service", "role": "SERVICE"},
        "password": "password"
    }
    login_response = client.post("/auth/login", json=payload)
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    decrypt_payload = {
        "encrypted_data": "some-data",
        "kyber_ciphertext": "some-ciphertext",
        "user_key": "key",
        "key_id": "id"
    }
    response = client.post("/encryption/decrypt", json=decrypt_payload, headers=headers)
    assert response.status_code == 403
