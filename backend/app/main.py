from fastapi import FastAPI, Depends, HTTPException
from .database import engine, Base, get_db
from .auth.routes import router as auth_router
# from typing import Annotated
# from sqlalchemy.orm import Session
# from . import models, crud, schemas

app = FastAPI()
app.include_router(auth_router, prefix="/auth")

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
#         # simple query to check connection
#         res = db.execute(text("SELECT 1"))
#         return {"status": "Connection successful!", "result": res.fetchone()}
#     except Exception as e:
#         print(f"Connection failed: {e}")
#         raise HTTPException(status_code=500, detail="Connection failed: " + str(e))
