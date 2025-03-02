from fastapi import FastAPI, Depends, HTTPException, APIRouter
from .db.base import Base
from .db.session import engine
from .auth.routes import router as auth_router
from .routers.admin import router as admin_router
from .routers.main import router as main_router
# from typing import Annotated
# from sqlalchemy.orm import Session
# from . import models, crud, schemas

app = FastAPI()
app.include_router(auth_router, prefix="/auth", tags=["auth"])

app.include_router(admin_router, prefix="/admin", tags=["admin"])

app.include_router(main_router, prefix="/", tags=["main"])

Base.metadata.create_all(bind=engine)




# @app.get("/users/{user_id}", response_model=schemas.User)
# def read_user(user_id: int, db: Session = Depends(get_db)):
#     db_user = crud.get_user(db, user_id=user_id)
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return db_user

# @app.get("/check-db-connection")

# def check_db_connection(db: Session = Depends(get_db)):
#     try:
        
#         res = db.execute(text("SELECT 1"))
#         return {"status": "Connection successful!", "result": res.fetchone()}
#     except Exception as e:
#         print(f"Connection failed: {e}")
#         raise HTTPException(status_code=500, detail="Connection failed: " + str(e))

