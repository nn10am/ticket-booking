from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from typing import List, Dict
from ..models.user import Users
from ..schemas.user import UserBase
from ..services.admin import admin_auth
# from ..dependencies import get_current_users

router = APIRouter()


@router.get("/home")
async def admin_homepage():
    return {"message": "This is the admin home page!"}