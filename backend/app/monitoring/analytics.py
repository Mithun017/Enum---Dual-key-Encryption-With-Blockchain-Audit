from typing import Dict, List
from app.blockchain.chain import Blockchain
import time
from datetime import datetime, timedelta

blockchain = Blockchain()

def get_security_stats() -> Dict:
    """
    Aggregates blockchain events for visualization.
    Returns:
        - total_events
        - events_last_24h
        - event_distribution (Encryption vs Decryption vs Failures)
        - timeline (Events per hour for last 24h)
    """
    chain = blockchain.get_chain()
    
    stats = {
        "total_events": len(chain),
        "events_last_24h": 0,
        "distribution": {
            "ENCRYPTION": 0,
            "DECRYPTION": 0,
            "FAILURE": 0,
            "OTHER": 0
        },
        "timeline": []
    }
    
    now = time.time()
    twenty_four_hours_ago = now - 86400
    
    # Initialize timeline buckets (last 24 hours)
    timeline_buckets = {}
    for i in range(24):
        hour_key = (datetime.fromtimestamp(now) - timedelta(hours=i)).strftime("%H:00")
        timeline_buckets[hour_key] = 0

    for block in chain:
        # 1. Count Last 24h
        if block.timestamp > twenty_four_hours_ago:
            stats["events_last_24h"] += 1
            
            # Add to timeline
            block_time = datetime.fromtimestamp(block.timestamp)
            hour_key = block_time.strftime("%H:00")
            if hour_key in timeline_buckets:
                timeline_buckets[hour_key] += 1

        # 2. Distribution
        evt = block.event_type
        if "ENCRYPTION" in evt:
            stats["distribution"]["ENCRYPTION"] += 1
        elif "DECRYPTION_FAILED" in evt:
            stats["distribution"]["FAILURE"] += 1
        elif "DECRYPTION" in evt:
            stats["distribution"]["DECRYPTION"] += 1
        else:
            stats["distribution"]["OTHER"] += 1

    # Format timeline for frontend
    # Sort by time (oldest to newest)
    sorted_hours = sorted(timeline_buckets.keys(), key=lambda x: datetime.strptime(x, "%H:00") if x else 0)
    # Actually, simple string sort might fail if crossing midnight, but for MVP it's okay-ish. 
    # Better to just reverse the list of last 24h generated.
    
    final_timeline = []
    # Re-generate keys in correct order (oldest to newest)
    for i in range(23, -1, -1):
        t = datetime.fromtimestamp(now) - timedelta(hours=i)
        key = t.strftime("%H:00")
        final_timeline.append({
            "time": key,
            "events": timeline_buckets.get(key, 0)
        })
        
    stats["timeline"] = final_timeline
    
    return stats
