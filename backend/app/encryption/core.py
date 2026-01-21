import base64
import os
import hashlib
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from .kyber_utils import encapsulate_secret, decapsulate_secret

class DualKeyEncryption:
    def __init__(self):
        self.backend = default_backend()

    def _derive_master_key(self, kyber_secret: bytes, user_key_str: str) -> bytes:
        """
        Combines Kyber Shared Secret (System) and User Key (String)
        to generate the final AES-256 Master Key.
        """
        # Hash user key to ensure 32 bytes
        user_key_bytes = hashlib.sha256(user_key_str.encode()).digest()
        
        # Combine secrets (Concatenate and Hash)
        combined = kyber_secret + user_key_bytes
        master_key = hashlib.sha256(combined).digest()
        return master_key

    def _encrypt_aes(self, data: bytes, key: bytes) -> bytes:
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=self.backend)
        encryptor = cipher.encryptor()
        
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(data) + padder.finalize()
        
        encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
        return iv + encrypted_data

    def _decrypt_aes(self, data_with_iv: bytes, key: bytes) -> bytes:
        iv = data_with_iv[:16]
        ciphertext = data_with_iv[16:]
        
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=self.backend)
        decryptor = cipher.decryptor()
        
        padded_data = decryptor.update(ciphertext) + decryptor.finalize()
        
        unpadder = padding.PKCS7(128).unpadder()
        data = unpadder.update(padded_data) + unpadder.finalize()
        return data

    def encrypt_data(self, data: str, system_public_key: bytes, user_key: str) -> dict:
        """
        Encrypts data using Hybrid Dual-Key Scheme.
        1. Encapsulate secret against System Kyber Public Key -> (ciphertext, shared_secret)
        2. Derive Master Key from (shared_secret + user_key)
        3. Encrypt data with Master Key (AES)
        
        Returns: {
            "encrypted_data": base64_str,
            "kyber_ciphertext": base64_str
        }
        """
        # 1. Kyber Encapsulation
        kyber_ciphertext, kyber_secret = encapsulate_secret(system_public_key)
        
        # 2. Derive Master Key
        master_key = self._derive_master_key(kyber_secret, user_key)
        
        # 3. AES Encryption
        data_bytes = data.encode('utf-8')
        encrypted_bytes = self._encrypt_aes(data_bytes, master_key)
        
        return {
            "encrypted_data": base64.b64encode(encrypted_bytes).decode('utf-8'),
            "kyber_ciphertext": base64.b64encode(kyber_ciphertext).decode('utf-8')
        }

    def decrypt_data(self, encrypted_data_b64: str, kyber_ciphertext_b64: str, system_private_key: bytes, user_key: str) -> str:
        """
        Decrypts data using Hybrid Dual-Key Scheme.
        1. Decapsulate secret using System Kyber Private Key -> shared_secret
        2. Derive Master Key from (shared_secret + user_key)
        3. Decrypt data with Master Key (AES)
        """
        # Decode inputs
        encrypted_bytes = base64.b64decode(encrypted_data_b64)
        kyber_ciphertext = base64.b64decode(kyber_ciphertext_b64)
        
        # 1. Kyber Decapsulation
        kyber_secret = decapsulate_secret(kyber_ciphertext, system_private_key)
        
        # 2. Derive Master Key
        master_key = self._derive_master_key(kyber_secret, user_key)
        
        # 3. AES Decryption
        decrypted_bytes = self._decrypt_aes(encrypted_bytes, master_key)
        
        return decrypted_bytes.decode('utf-8')
    def encrypt_file(self, file_bytes: bytes, system_public_key: bytes, user_key: str) -> dict:
        """
        Encrypts a file using Hybrid Dual-Key Scheme.
        Returns: {
            "encrypted_file": bytes,
            "kyber_ciphertext": base64_str
        }
        """
        # 1. Kyber Encapsulation
        kyber_ciphertext, kyber_secret = encapsulate_secret(system_public_key)
        
        # 2. Derive Master Key
        master_key = self._derive_master_key(kyber_secret, user_key)
        
        # 3. AES Encryption
        encrypted_bytes = self._encrypt_aes(file_bytes, master_key)
        
        return {
            "encrypted_file": encrypted_bytes,
            "kyber_ciphertext": base64.b64encode(kyber_ciphertext).decode('utf-8')
        }

    def decrypt_file(self, encrypted_file_bytes: bytes, kyber_ciphertext_b64: str, system_private_key: bytes, user_key: str) -> bytes:
        """
        Decrypts a file using Hybrid Dual-Key Scheme.
        """
        # Decode Kyber ciphertext
        kyber_ciphertext = base64.b64decode(kyber_ciphertext_b64)
        
        # 1. Kyber Decapsulation
        kyber_secret = decapsulate_secret(kyber_ciphertext, system_private_key)
        
        # 2. Derive Master Key
        master_key = self._derive_master_key(kyber_secret, user_key)
        
        # 3. AES Decryption
        decrypted_bytes = self._decrypt_aes(encrypted_file_bytes, master_key)
        
        return decrypted_bytes
