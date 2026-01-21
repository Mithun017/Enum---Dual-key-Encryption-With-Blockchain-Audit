from app.encryption.kyber_utils import generate_kyber_keypair
from app.models import SystemKey
from app.database import SessionLocal

class KeyManager:
    def __init__(self):
        # No longer need file path checks
        pass
            
    def get_or_create_system_keypair(self, key_id: str):
        """
        Returns (public_key, private_key) for the given key_id.
        Creates them if they don't exist in the DB.
        """
        db = SessionLocal()
        try:
            key_record = db.query(SystemKey).filter(SystemKey.key_id == key_id).first()
            
            if key_record:
                return key_record.public_key, key_record.private_key
            else:
                # Generate new Kyber Keypair
                pk, sk = generate_kyber_keypair()
                
                new_key = SystemKey(
                    key_id=key_id,
                    public_key=pk,
                    private_key=sk
                )
                db.add(new_key)
                db.commit()
                db.refresh(new_key)
                return new_key.public_key, new_key.private_key
        finally:
            db.close()
