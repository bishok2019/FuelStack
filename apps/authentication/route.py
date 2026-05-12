from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from apps.authentication.schemas import Token, UserCreate, UserLogin
from apps.database import get_db

router = APIRouter()


@router.post("/signup", response_model=Token)
def signup(payload: UserCreate, db: Session = Depends(get_db)):
    pass


@router.post("/login", response_model=Token)
def login(payload: UserLogin, db: Session = Depends(get_db)):
    pass


@router.post("/refresh", response_model=Token)
def refresh_token():
    pass


@router.get("/me")
def me():
    pass
