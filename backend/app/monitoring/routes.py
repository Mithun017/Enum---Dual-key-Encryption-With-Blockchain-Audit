from fastapi import APIRouter, Depends
from app.monitoring.alerts import check_anomalies
from app.rbac.dependencies import RoleChecker, UserRole

router = APIRouter()

# Only ADMIN can view alerts
allow_monitor = RoleChecker([UserRole.ADMIN])

@router.get("/alerts", dependencies=[Depends(allow_monitor)])
async def get_alerts():
    return {"alerts": check_anomalies()}

@router.get("/stats", dependencies=[Depends(allow_monitor)])
async def get_stats():
    from app.monitoring.analytics import get_security_stats
    return get_security_stats()
