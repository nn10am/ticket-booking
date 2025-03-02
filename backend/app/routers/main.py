from fastapi import APIRouter


router = APIRouter()
@router.get("/home")
async def homepage():
    return {"message": "This is the home page!"}