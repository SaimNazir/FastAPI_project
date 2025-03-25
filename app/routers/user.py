from fastapi import Body, Response, status, HTTPException, APIRouter, Depends

from pydantic import BaseModel
from typing import Optional, List


from .. import schemas, utils
from ..database import get_db



router = APIRouter(
    prefix="/users", 
    tags=["users"]
)





@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db=Depends(get_db)):
    cursor = db.cursor()

    hashed_psw = utils.hash_password(user.password)
    user.password = hashed_psw

    cursor.execute("INSERT INTO users (email, password) VALUES (%s, %s) RETURNING *", (user.email, user.password))
    user = cursor.fetchone()
    db.commit()

    return user


@router.get("/{user_id}", response_model=schemas.UserOut)
def get_user(user_id: int, db=Depends(get_db)):
    cursor = db.cursor()

    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user