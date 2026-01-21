from enum import Enum
from pydantic import BaseModel

class UserRole(str, Enum):
    ADMIN = "ADMIN"
    SERVICE = "SERVICE"
    AUDITOR = "AUDITOR"

class User(BaseModel):
    username: str
    role: UserRole
