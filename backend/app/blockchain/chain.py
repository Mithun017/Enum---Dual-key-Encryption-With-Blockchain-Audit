import time
from typing import List
from .block import Block
from app.models import LedgerBlock
from app.database import SessionLocal
import datetime

class Blockchain:
    def __init__(self):
        # We don't keep the whole chain in memory anymore for scalability
        # But for validation, we might need to query.
        pass

    def get_latest_block(self) -> Block:
        db = SessionLocal()
        try:
            # Get block with max index
            last_db_block = db.query(LedgerBlock).order_by(LedgerBlock.index.desc()).first()
            if not last_db_block:
                # Should have been created by init_db, but if not:
                return Block(0, time.time(), "GENESIS", "SYSTEM", "SYSTEM", "GENESIS_BLOCK", "0")
            
            return Block(
                last_db_block.index,
                float(last_db_block.timestamp), # Convert string back to float
                last_db_block.event_type,
                last_db_block.key_id,
                last_db_block.user_id,
                last_db_block.data_reference,
                last_db_block.previous_hash
            )
        finally:
            db.close()

    def add_block(self, event_type: str, key_id: str, user_id: str, data_reference: str):
        latest_block = self.get_latest_block()
        new_index = latest_block.index + 1
        new_timestamp = time.time()
        
        # Calculate hash (using Block class logic)
        # Block(index, timestamp, event_type, key_id, user_id, data_reference, previous_hash)
        temp_block = Block(
            new_index,
            new_timestamp,
            event_type,
            key_id,
            user_id,
            data_reference,
            latest_block.hash # Use hash of previous block
        )
        
        # Save to DB
        db = SessionLocal()
        try:
            db_block = LedgerBlock(
                index=new_index,
                timestamp=str(new_timestamp), # Store as string
                event_type=event_type,
                key_id=key_id,
                user_id=user_id,
                data_reference=data_reference,
                previous_hash=latest_block.hash,
                hash=temp_block.hash
            )
            db.add(db_block)
            db.commit()
            return temp_block
        finally:
            db.close()

    def get_chain(self) -> List[Block]:
        """
        Retrieves the full chain from the database.
        """
        db = SessionLocal()
        try:
            db_blocks = db.query(LedgerBlock).order_by(LedgerBlock.index.asc()).all()
            chain = []
            for db_b in db_blocks:
                b = Block(
                    db_b.index,
                    float(db_b.timestamp), # Convert string back to float
                    db_b.event_type,
                    db_b.key_id,
                    db_b.user_id,
                    db_b.data_reference,
                    db_b.previous_hash
                )
                b.hash = db_b.hash
                chain.append(b)
            return chain
        finally:
            db.close()

    def is_chain_valid(self) -> bool:
        chain = self.get_chain()
        for i in range(1, len(chain)):
            current_block = chain[i]
            previous_block = chain[i-1]

            if current_block.hash != current_block.calculate_hash():
                return False

            if current_block.previous_hash != previous_block.hash:
                return False
        return True
