from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from app.database import SQLALCHEMY_DATABASE_URL, engine, SessionLocal
from app.models import Base, User, UserRole, LedgerBlock
from app.blockchain.block import Block
import datetime
import time

def init_db():
    # 1. Create Database if not exists
    if not database_exists(SQLALCHEMY_DATABASE_URL):
        create_database(SQLALCHEMY_DATABASE_URL)
        print(f"Created database: {SQLALCHEMY_DATABASE_URL}")
    else:
        print(f"Database already exists: {SQLALCHEMY_DATABASE_URL}")

    # 2. Create Tables
    # DROP ALL TABLES TO RESET SCHEMA AND DATA
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    print("Created tables (dropped old ones).")

    # 3. Seed Initial Users
    db = SessionLocal()
    
    # Check if users exist
    if not db.query(User).first():
        users = [
            User(username="admin", role=UserRole.ADMIN, password="password"),
            User(username="service", role=UserRole.SERVICE, password="password"),
            User(username="auditor", role=UserRole.AUDITOR, password="password"),
            User(username="Mithun", role=UserRole.ADMIN, password="password")
        ]
        db.add_all(users)
        db.commit()
        print("Seeded initial users.")
    else:
        print("Users already exist.")

    # 4. Seed Genesis Block if Ledger is empty
    if not db.query(LedgerBlock).first():
        # Block(index, timestamp, event_type, key_id, user_id, data_reference, previous_hash)
        # Use current time as float
        current_time = time.time()
        
        genesis_block = Block(
            index=0,
            timestamp=current_time,
            event_type="GENESIS",
            key_id="SYSTEM",
            user_id="SYSTEM",
            data_reference="GENESIS_BLOCK",
            previous_hash="0"
        )
        
        db_block = LedgerBlock(
            index=genesis_block.index,
            timestamp=str(genesis_block.timestamp), # Store as string
            event_type=genesis_block.event_type,
            key_id=genesis_block.key_id,
            user_id=genesis_block.user_id,
            data_reference=genesis_block.data_reference,
            previous_hash=genesis_block.previous_hash,
            hash=genesis_block.hash
        )
        db.add(db_block)
        db.commit()
        print("Seeded Genesis Block.")
    
    db.close()

if __name__ == "__main__":
    init_db()
