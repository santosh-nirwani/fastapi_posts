from typing import Optional, List
from fastapi import FastAPI, Response, HTTPException, status, Depends
import psycopg2
from psycopg2.extras import RealDictCursor
from . import models, schema, config
from . database import engine, get_db, SessionLocal, sessionmaker
from sqlalchemy.orm import Session
from pydantic import BaseModel, ConfigDict
from .routers import post, user, auth


models.Base.metadata.create_all(bind=engine)


app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


# try:
#     conn = psycopg2.connect(host="localhost", database = 'fastapi', user='postgres', password='password'
#                            , cursor_factory=RealDictCursor)
#     cursor = conn.cursor()
#     print('Database connection Successful')
# except Exception as error:
#     print('Connection failed')
#     print('Error = ', error)

