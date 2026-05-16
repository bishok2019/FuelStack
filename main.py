from fastapi import APIRouter, FastAPI
from fastapi.staticfiles import StaticFiles

from apps.authentication.auth_route import router as auth_router
from apps.authentication.user_route import router as user_router
from apps.dealers.models import Brand, Dealer, Hub
from apps.dealers.route import brand_router, dealer_router, hub_router
from apps.inventory.route import router as inventory_router

app = FastAPI(
    title="FuelStack Project",
    # description="Title",
    version="1.0.0",
    contact={
        "name": "Bishok Paudel",
        "email": "bishokpaudel57@gmail.com",
    },
)

app.mount("/static", StaticFiles(directory="staticfiles"), name="static")
app.mount("/media", StaticFiles(directory="media"), name="media")

v1_router = APIRouter(prefix="/api/v1")
v1_router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
v1_router.include_router(user_router, prefix="/users", tags=["Users"])
v1_router.include_router(inventory_router, prefix="/inventory", tags=["Inventory"])
v1_router.include_router(brand_router, prefix="/dealers/brands", tags=["Brands"])
v1_router.include_router(dealer_router, prefix="/dealers", tags=["Dealers"])
v1_router.include_router(hub_router, prefix="/dealers/hubs", tags=["Hubs"])

app.include_router(v1_router)
