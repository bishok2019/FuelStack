from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from apps.database import get_db
from base.pagination import paginate
from base.route import StandardResponse

from .models import User
from .schemas import UserCreate, UserList, UserLogin, UserRetrieve, UserUpdate
from .utils import hash_password, verify_password

router = APIRouter()


@router.post(
    "/create", response_model=StandardResponse, status_code=status.HTTP_201_CREATED
)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """Create a new user"""
    # Check if user exists already
    existing_user = (
        db.query(User)
        .filter((User.username == user.username) | (User.email == user.email))
        .first()
    )
    if existing_user:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=StandardResponse.error_response(
                message="Username or email already registered."
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

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=StandardResponse.success_response(
            data=UserRetrieve.model_validate(db_user),
            message="User created successfully.",
        ).model_dump(),
    )


@router.get("/list", response_model=StandardResponse)
def get_users(
    page: int = 1,  # we are passing page and page_size in paginate() directly
    page_size: int = 1,
    db: Session = Depends(get_db),
):
    """Get all users with pagination"""
    result = paginate(
        query=db.query(User),
        page=page,  # we are passing page and page_size in paginate() directly
        page_size=page_size,
        schema=UserList,
    )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=StandardResponse.success_response(
            data=result.data,
            message="Users fetched successfully.",
            meta=result.meta,
        ).model_dump(),
    )


@router.get("/retrieve/{user_id}", response_model=StandardResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """Get a specific user by ID"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=StandardResponse.error_response(
                message="User not found.",
            ).model_dump(),
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=StandardResponse.success_response(
            data=UserRetrieve.model_validate(user),
            message="User retrieved successfully.",
        ).model_dump(),
    )
