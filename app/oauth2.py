import jwt
from jwt.exceptions import InvalidTokenError
from datetime import datetime, timedelta, timezone
from . import schema, config
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import os



oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')


SECRET_KEY: str = config.settings.secret_key
ALGORITHM:str = config.settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES: int = config.settings.access_token_expire


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    token = jwt.encode(to_encode,key=SECRET_KEY, algorithm=ALGORITHM)
    return token

def verify_access_token(token: str, credentials_exception):
    
    try:
        payload = jwt.decode(token, key=SECRET_KEY, algorithms=ALGORITHM)
        id: int = payload.get("user_id")
        #email = payload.get("email")
        if id is None:
            raise credentials_exception
        tokendata = schema.TokenData(id=id)
    except InvalidTokenError:
        raise credentials_exception
    
    return tokendata
    

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    return verify_access_token(token, credentials_exception)




