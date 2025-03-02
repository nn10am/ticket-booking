from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..models.user import Users
from ..db.session import get_db

def admin_auth(db: Session = Depends(get_db)):
    user = db.query(Users).filter(Users.is_admin == True).first()
    if user:
        return user
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Admin authentication required!")