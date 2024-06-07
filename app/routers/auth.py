from fastapi import APIRouter, Response, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from ..database import get_db, SessionLocal, sessionmaker
from .. import schema,models,utils,oauth2
from sqlalchemy.orm import Session


router = APIRouter(tags=['Authentication'])

@router.post('/login')
def login(userlogin: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.email == userlogin.username).first()
    print(user.email, user.id)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not authorized")
    
    
    if not utils.verify(userlogin.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not authorized")
    
    token = oauth2.create_access_token(data={"user_id": user.id, "username": user.email })
    return {"access_token":token, "token_type": "bearer"}
