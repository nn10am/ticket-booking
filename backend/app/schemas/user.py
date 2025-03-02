from pydantic import BaseModel

class UserBase(BaseModel):
    id: int
    username: str
    email: str
    

class UserCreate(UserBase):
    hashed_password: str

class User(UserBase):
    id: int

    class Config:
        from_attributes = True
        