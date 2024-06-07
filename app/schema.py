from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr


class User(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    email: str
    id: int
    createdon: datetime

class Userlogin(BaseModel):
    email: EmailStr
    password: str

class Post(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    title: str
    content: str
    
            
class PostRespnse(Post):
    id: int
    owner_id: int
    owner: UserResponse



class TokenData(BaseModel):
    id: int
    #email: str


