from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from starlette import status
from pydantic import BaseModel, Field
from ..models import Users
from passlib.context import CryptContext
from ..database import SessionLocal
from .auth import get_current_user

router = APIRouter(
    prefix="/user", tags=["user"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserVerification(BaseModel):
    password: str
    new_password: str = Field(min_length=6)


@router.get("/me", status_code=status.HTTP_200_OK)
def get_user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    db_user = db.query(Users).filter(Users.id == user['id']).first()
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return db_user


@router.put("/password", status_code=status.HTTP_204_NO_CONTENT)
def change_password(user_data: UserVerification, user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    db_user = db.query(Users).filter(Users.id == user['id']).first()
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    if not bcrypt_context.verify(user_data.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect password"
        )
    hashed_new_password = bcrypt_context.hash(user_data.new_password)
    db_user.hashed_password = hashed_new_password
    db.add(db_user)
    db.commit()
    return


@router.put("/phonenumber/{phone_number}", status_code=status.HTTP_204_NO_CONTENT)
def change_phone_number(user: user_dependency, db: db_dependency, phone_number: str = Path(min_length=10, max_length=15),):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    db_user = db.query(Users).filter(Users.id == user['id']).first()
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    db_user.phone_number = phone_number
    db.add(db_user)
    db.commit()
    return
