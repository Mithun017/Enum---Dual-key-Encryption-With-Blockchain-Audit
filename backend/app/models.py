from sqlalchemy import Column, Integer, String, LargeBinary, DateTime, Enum, Float
from .database import Base
import enum
from datetime import datetime

class UserRole(str, enum.Enum):
    ADMIN = "ADMIN"
    SERVICE = "SERVICE"
    AUDITOR = "AUDITOR"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    password = Column(String(100)) # In production, store HASHED passwords!
    role = Column(Enum(UserRole))

class SystemKey(Base):
    __tablename__ = "system_keys"

    key_id = Column(String(100), primary_key=True, index=True)
    public_key = Column(LargeBinary)
    private_key = Column(LargeBinary)

class LedgerBlock(Base):
    __tablename__ = "ledger"

    id = Column(Integer, primary_key=True, index=True)
    index = Column(Integer, unique=True, index=True)
    timestamp = Column(String(50)) # Store as string to preserve exact precision for hashing
    event_type = Column(String(50))
    key_id = Column(String(100))
    user_id = Column(String(50))
    data_reference = Column(String(255))
    previous_hash = Column(String(64))
    hash = Column(String(64))
