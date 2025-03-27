from fastapi import FastAPI, Body, Response, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel
from typing import Optional, List

from . import schemas, utils
from .routers import post, user, auth
from .config import settings



app = FastAPI()


origins = [
    "http://localhost",
    "http://localhost:8080",
    
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


@app.get("/")
def root():
    return {"message": "Hello World"}