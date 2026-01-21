from fastapi import APIRouter, Depends, HTTPException
from app.blockchain.chain import Blockchain
from app.rbac.dependencies import RoleChecker, UserRole

router = APIRouter()
blockchain = Blockchain()

# RBAC: Only AUDITOR and ADMIN can view the ledger
allow_audit = RoleChecker([UserRole.AUDITOR, UserRole.ADMIN])

@router.get("/ledger", dependencies=[Depends(allow_audit)])
async def get_ledger():
    try:
        # No need to load_chain() manually, get_chain() queries DB
        chain = blockchain.get_chain()
        
        if not blockchain.is_chain_valid():
            raise HTTPException(status_code=500, detail="Blockchain integrity compromised!")
            
        return {"chain": [block.to_dict() for block in chain]}
    except Exception as e:
        print(f"DEBUG: Ledger Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/validate", dependencies=[Depends(allow_audit)])
async def validate_chain():
    is_valid = blockchain.is_chain_valid()
    return {"is_valid": is_valid}
