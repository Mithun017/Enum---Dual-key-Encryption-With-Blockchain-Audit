from fastapi import APIRouter, Body, HTTPException, Depends
from sqlalchemy.orm import Session
from app.auth.jwt_handler import signJWT
from app.rbac.models import User as PydanticUser, UserRole
from app.models import User as DBUser
from app.database import get_db
from pydantic import BaseModel

router = APIRouter()

class LoginRequest(BaseModel):
    user: PydanticUser
    password: str

@router.post("/login", tags=["authentication"])
async def user_login(request: LoginRequest, db: Session = Depends(get_db)):
    user = request.user
    password = request.password
    
    # Case-insensitive lookup
    # SQLAlchemy filter(func.lower(User.username) == username.lower())
    # But for simplicity and since usernames are unique, we can just fetch all or filter.
    # Let's use filter.
    
    db_user = db.query(DBUser).filter(DBUser.username == user.username).first()
    
    # If not found, try case-insensitive manually (or use func.lower if imported)
    if not db_user:
         # Fallback: iterate all users (inefficient for large DB, but fine for MVP)
         # Better: use ILIKE or func.lower
         # For now, let's assume exact match or handle case in frontend?
         # No, requirement was case-insensitive.
         all_users = db.query(DBUser).all()
         for u in all_users:
             if u.username.lower() == user.username.lower():
                 db_user = u
                 break
    
    if db_user and db_user.password == password:
        # Verify role matches
        # Convert DB enum to string for comparison if needed
        if db_user.role.value != user.role.value:
             raise HTTPException(status_code=403, detail="Role mismatch")
        
        return signJWT(db_user.username, user.role)
    
    raise HTTPException(status_code=401, detail="Invalid login details")
