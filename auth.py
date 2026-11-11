import bcrypt
from fastapi import Request
from sqlalchemy.orm import Session
from models import User

def hash_password(password: str) -> str:
    """Directly hash the password using bcrypt safely."""
    # Encode password to bytes and truncate if it exceeds 72 bytes to avoid errors
    pwd_bytes = password.encode('utf-8')
    if len(pwd_bytes) > 72:
        pwd_bytes = pwd_bytes[:72]
        
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(pwd_bytes, salt)
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify plain password against the stored bcrypt hash."""
    pwd_bytes = plain_password.encode('utf-8')
    if len(pwd_bytes) > 72:
        pwd_bytes = pwd_bytes[:72]
        
    return bcrypt.checkpw(pwd_bytes, hashed_password.encode('utf-8'))

def get_current_user(request: Request, db: Session):
    user_id = request.cookies.get("user_id")
    if not user_id:
        return None
    try:
        user = db.query(User).filter(User.id == int(user_id)).first()
        return user
    except ValueError:
        return None