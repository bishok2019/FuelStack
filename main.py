from fastapi import APIRouter, FastAPI

from apps.authentication.route import router as auth_router

app = FastAPI(
    title="FastAPI Learning Project",
    description="Title",
    version="1.0.0",
    contact={
        "name": "Bishok Paudel",
        "email": "bishokpaudel57@gmail.com",
    },
)

v1_router = APIRouter(prefix="/api/v1")

v1_router.include_router(
    auth_router,
    prefix="/auth",
    tags=["Authentication"],
)

app.include_router(v1_router)
