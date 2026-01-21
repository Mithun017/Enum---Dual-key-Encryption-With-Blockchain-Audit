from fastapi import APIRouter, Depends, HTTPException, Body, UploadFile, File, Form, Response
import base64
from pydantic import BaseModel
from app.encryption.core import DualKeyEncryption
from app.key_management.manager import KeyManager
from app.rbac.dependencies import RoleChecker, UserRole, get_current_user_id
from app.blockchain.chain import Blockchain

router = APIRouter()
encryption_engine = DualKeyEncryption()
key_manager = KeyManager()
blockchain = Blockchain()

# RBAC: Only ADMIN and SERVICE can encrypt
allow_encrypt = RoleChecker([UserRole.ADMIN, UserRole.SERVICE])
# RBAC: Only ADMIN can decrypt (SERVICE encrypts only, AUDITOR views logs)
allow_decrypt = RoleChecker([UserRole.ADMIN])

class EncryptionRequest(BaseModel):
    data: str
    user_key: str # Key-B (Password/Passphrase)
    key_id: str # Identifier for Key-A (System Kyber Key)

class DecryptionRequest(BaseModel):
    encrypted_data: str
    kyber_ciphertext: str # NEW: Required for Kyber Decapsulation
    user_key: str # Key-B
    key_id: str # Identifier for Key-A

@router.post("/encrypt", dependencies=[Depends(allow_encrypt)])
async def encrypt_data(request: EncryptionRequest, user_id: str = Depends(get_current_user_id)):
    # 1. Retrieve System Key (Public Key only needed for encryption)
    pk, _ = key_manager.get_or_create_system_keypair(request.key_id)
    
    # 2. Encrypt
    try:
        result = encryption_engine.encrypt_data(
            request.data, 
            pk, 
            request.user_key
        )
        
        # 3. Log to Blockchain
        blockchain.add_block(
            event_type="ENCRYPTION_KYBER",
            key_id=request.key_id,
            user_id=user_id,
            data_reference=f"hash-{hash(result['encrypted_data'])}"
        )
        
        # Return both the encrypted data AND the Kyber ciphertext (encapsulated key)
        return {
            "encrypted_data": result["encrypted_data"],
            "kyber_ciphertext": result["kyber_ciphertext"],
            "key_id": request.key_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/decrypt", dependencies=[Depends(allow_decrypt)])
async def decrypt_data(request: DecryptionRequest, user_id: str = Depends(get_current_user_id)):
    # 1. Retrieve System Key (Private Key needed for decryption)
    _, sk = key_manager.get_or_create_system_keypair(request.key_id)
    
    # 2. Decrypt
    try:
        decrypted = encryption_engine.decrypt_data(
            request.encrypted_data,
            request.kyber_ciphertext,
            sk, 
            request.user_key
        )
        
        # 3. Log to Blockchain
        blockchain.add_block(
            event_type="DECRYPTION_KYBER",
            key_id=request.key_id,
            user_id=user_id,
            data_reference=f"hash-{hash(request.encrypted_data)}"
        )
        
        return {"data": decrypted}
    except Exception as e:
        # Log failed attempt?
        blockchain.add_block(
            event_type="DECRYPTION_FAILED",
            key_id=request.key_id,
            user_id=user_id,
            data_reference="N/A"
        )
        raise HTTPException(status_code=400, detail=f"Decryption failed. Invalid keys or data. {str(e)}")
@router.post("/encrypt-file", dependencies=[Depends(allow_encrypt)])
async def encrypt_file(
    file: UploadFile = File(...),
    user_key: str = Form(...),
    key_id: str = Form(...),
    user_id: str = Depends(get_current_user_id)
):
    # 1. Retrieve System Key
    pk, _ = key_manager.get_or_create_system_keypair(key_id)
    
    # 2. Read File
    file_bytes = await file.read()
    
    # 3. Encrypt
    try:
        result = encryption_engine.encrypt_file(
            file_bytes, 
            pk, 
            user_key
        )
        
        # 4. Log to Blockchain
        blockchain.add_block(
            event_type="FILE_ENCRYPTION",
            key_id=key_id,
            user_id=user_id,
            data_reference=f"file-hash-{hash(file.filename)}"
        )
        
        # Return as JSON with base64 encoded file (for simplicity in this MVP)
        # In a real app, we might stream this back.
        return {
            "encrypted_file": base64.b64encode(result["encrypted_file"]).decode('utf-8'),
            "kyber_ciphertext": result["kyber_ciphertext"],
            "filename": f"{file.filename}.enc"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/decrypt-file", dependencies=[Depends(allow_decrypt)])
async def decrypt_file(
    file: UploadFile = File(...),
    kyber_ciphertext: str = Form(...),
    user_key: str = Form(...),
    key_id: str = Form(...),
    user_id: str = Depends(get_current_user_id)
):
    # 1. Retrieve System Key
    _, sk = key_manager.get_or_create_system_keypair(key_id)
    
    # 2. Read File
    encrypted_bytes = await file.read()
    
    # 3. Decrypt
    try:
        decrypted_bytes = encryption_engine.decrypt_file(
            encrypted_bytes,
            kyber_ciphertext,
            sk, 
            user_key
        )
        
        # 4. Log to Blockchain
        blockchain.add_block(
            event_type="FILE_DECRYPTION",
            key_id=key_id,
            user_id=user_id,
            data_reference=f"file-hash-{hash(file.filename)}"
        )
        
        # Return as downloadable file
        original_filename = file.filename.replace(".enc", "")
        return Response(
            content=decrypted_bytes,
            media_type="application/octet-stream",
            headers={"Content-Disposition": f"attachment; filename={original_filename}"}
        )
    except Exception as e:
        blockchain.add_block(
            event_type="FILE_DECRYPTION_FAILED",
            key_id=key_id,
            user_id=user_id,
            data_reference="N/A"
        )
        raise HTTPException(status_code=400, detail=f"Decryption failed. {str(e)}")
