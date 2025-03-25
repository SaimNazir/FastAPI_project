from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from .. import schemas, utils, oauth2
from ..database import get_db



router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/login", response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db=Depends(get_db)):
    cursor = db.cursor()

    query = "SELECT * FROM users WHERE email = %s"
    cursor.execute(query, (user_credentials.username,))
    user = cursor.fetchone()

    hashed_password = user["password"]

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
    
    if not utils.verify_password(user_credentials.password, hashed_password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
    
    acces_token = oauth2.create_access_token(data = {"user_id": user["id"]})

    return {"access_token": acces_token, "token_type": "bearer"}