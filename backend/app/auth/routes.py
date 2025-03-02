from datetime import timedelta, datetime
from typing import Annotated, Union
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status
from ..models.user import Users
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from dotenv import load_dotenv
from ..db.session import SessionLocal
from email_validator import validate_email, EmailNotValidError
import os


load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

router = APIRouter()

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

class CreateUserRequest(BaseModel):
    username: str
    password: str
    email: str

class Token(BaseModel):
    access_token: str
    token_type: str

class AdminLoginResponse(BaseModel):
    message: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency,
                      create_user_request: CreateUserRequest):
    # Validate email
    try:
        validate_email(create_user_request.email)
    except EmailNotValidError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    create_user_model = Users(
        username = create_user_request.username,
        hashed_password = bcrypt_context.hash(create_user_request.password),
        email = create_user_request.email,
        is_admin=False
        )
    
    db.add(create_user_model)
    db.commit()

@router.post("/token", response_model=Union[Token, AdminLoginResponse])
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                 db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail = 'Could not validate user')
    
    token = create_access_token(user.username, user.id, user.is_admin, timedelta(minutes=15))
    # redirecting admin to admin page
    if user.is_admin:
        return JSONResponse(content= {
            "access_token": token,
            "token_type": "bearer",
            "redirect_url": "/admin/home"
        })
    return {'access_token': token, 'token_type': 'bearer'}

def authenticate_user(identifier: str, password: str, db):
    # check identifier validation
    try:
        validate_email(identifier)
        user = db.query(Users).filter(Users.email == identifier).first()
    except EmailNotValidError:
        user = db.query(Users).filter(Users.username == identifier).first()
    
    if not user or not bcrypt_context.verify(password, user.hashed_password):
        return False
    
    return user

def create_access_token(username: str, user_id: int, is_admin: bool, expires_delta: timedelta):
    encode = {'sub': username, 'id': user_id, 'is_admin': is_admin}
    expires = datetime.utcnow() + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

        