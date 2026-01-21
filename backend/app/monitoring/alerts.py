from typing import List, Dict
from app.blockchain.chain import Blockchain
import time

blockchain = Blockchain()

def check_decryption_failures(threshold: int = 3, time_window: int = 600) -> List[Dict]:
    """
    Check for multiple decryption failures within a time window.
    """
    current_time = time.time()
    failures = []
    
    # In a real system, we would query a database or indexed logs.
    # Here we iterate the chain (inefficient for large chains, but fine for MVP).
    recent_blocks = [b for b in blockchain.get_chain() if current_time - b.timestamp < time_window]
    
    user_failures = {}
    
    for block in recent_blocks:
        if block.event_type == "DECRYPTION_FAILED":
            user_id = block.user_id
            user_failures[user_id] = user_failures.get(user_id, 0) + 1
            
    for user_id, count in user_failures.items():
        if count >= threshold:
            failures.append({
                "user_id": user_id,
                "issue": "Excessive Decryption Failures",
                "count": count,
                "severity": "HIGH"
            })
            
    return failures

def check_anomalies() -> List[Dict]:
    alerts = []
    alerts.extend(check_decryption_failures())
    return alerts
