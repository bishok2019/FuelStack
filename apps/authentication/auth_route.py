from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from apps.authentication.models import User, UserType
from apps.authentication.schemas import Token, UserCreate, UserLogin, UserRegister
from apps.customer.models import Customer
from apps.database import get_db
from base.route import StandardResponse

from .utils import (
    create_access_token,
    create_refresh_token,
    hash_password,
    verify_password,
)

router = APIRouter()


@router.post("/register", response_model=StandardResponse)
def register(user: UserRegister, db: Session = Depends(get_db)):
    """Register a new user"""
    # Check if user already exists
    existing_user = (
        db.query(User)
        .filter((User.username == user.username) | (User.email == user.email))
        .first()
    )
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=StandardResponse.error_response(
                message="Username or email already registered",
                errors=[
                    {
                        "field": "username/email",
                        "message": "Username or email already registered",
                    }
                ],
            ).model_dump(),
        )

    # Create new user
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hash_password(user.password),
        is_active=True,
        is_superuser=False,
        # is_verified=False,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    if db_user.user_type == UserType.CUSTOMER:
        customer_profile = Customer(
            user_id=db_user.id,
            # Add other customer fields here from user or request if needed
        )
        db.add(customer_profile)
        db.commit()

    return StandardResponse.success_response(
        data={
            "id": db_user.id,
            "username": db_user.username,
            "email": db_user.email,
        },
        message="User registered successfully",
    )


@router.post("/login")
def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    """Login user and return JWT tokens"""
    # Find user
    user = db.query(User).filter(User.username == user_credentials.username).first()

    if not user or not verify_password(user_credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=StandardResponse.error_response(
                # message="Invalid username or password",
                error="Invalid credentials",
            ).model_dump(),
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=StandardResponse.error_response(
                message="Inactive user account"
            ).model_dump(),
        )

    # Create tokens
    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})

    return StandardResponse.success_response(
        data={
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
            },
            "roles": [role.name for role in user.user_roles],
            "permissions": [perm.code_name for perm in user.user_permissions],
        },
        message="Login successful",
    )
