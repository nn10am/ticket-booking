from fastapi import Request
from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..models.user import Users
from ..db.session import get_db



# admin gets all users
def get_all_users(db: Session):
    admin = db.query(Users).filter(Users.is_admin == True).order_by(Users.id.asc()).all()
    standard_users = db.query(Users).filter(Users.is_admin == False).order_by(Users.id.asc()).all()
    
    response = {
        "Admin": admin,
        "Users": standard_users
    }

    return response

