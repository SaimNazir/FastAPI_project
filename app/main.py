from fastapi import FastAPI, Body, Response, status, HTTPException

from pydantic import BaseModel
from typing import Optional, List

from . import schemas, utils
from .routers import post, user, auth
from .config import settings



app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


@app.get("/")
def root():
    return {"message": "Hello World"}