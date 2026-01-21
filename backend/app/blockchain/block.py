import hashlib
import json
import time
from typing import Any, Dict

class Block:
    def __init__(self, index: int, timestamp: float, event_type: str, 
                 key_id: str, user_id: str, data_reference: str, 
                 previous_hash: str):
        self.index = index
        self.timestamp = timestamp
        self.event_type = event_type
        self.key_id = key_id
        self.user_id = user_id
        self.data_reference = data_reference
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self) -> str:
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "event_type": self.event_type,
            "key_id": self.key_id,
            "user_id": self.user_id,
            "data_reference": self.data_reference,
            "previous_hash": self.previous_hash
        }, sort_keys=True)
        
        return hashlib.sha256(block_string.encode()).hexdigest()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "event_type": self.event_type,
            "key_id": self.key_id,
            "user_id": self.user_id,
            "data_reference": self.data_reference,
            "previous_hash": self.previous_hash,
            "hash": self.hash
        }
