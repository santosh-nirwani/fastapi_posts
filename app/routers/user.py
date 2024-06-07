from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException, status, Response, APIRouter
from ..schema import User
from ..utils import hash
from typing import List

from ..database import get_db
from typing import Optional, List
from .. import schema, models

router = APIRouter(tags=['Users'])

@router.get('/users', response_model=List[schema.UserResponse])
def get_user(db: Session = Depends(get_db)):
    users = db.query(models.Users).all()
    return users

@router.get('/users/{id}', response_model=schema.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    users = db.query(models.Users).filter(models.Users.id == id).first()
    print(type(users))
    if not users:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The user with ID does not exists")
    
    return users

@router.post('/users', response_model=schema.UserResponse)
def create_user(user: schema.User, db: Session = Depends(get_db)):
    hashed_password = hash(user.password) 
    user.password = hashed_password
    new_user = models.Users(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
