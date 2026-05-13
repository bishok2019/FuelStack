# from fastapi import APIRouter

# # include user and auth route
# from apps.authentication.auth_route import router as auth_router
# from apps.authentication.user_route import router as user_router

# # mounts auth routes under /authentication/...
# #  - POST /authentication/register
# #  - POST /authentication/login
# router = APIRouter(
#     # prefix="/authentication",
#     # tags=["authentication"],
# )
# router.include_router(
#     auth_router,
#     prefix="/auth",
#     tags=["auth"],
# )

# # mounts users under /authentication/users/...
# router.include_router(
#     user_router,
#     prefix="/users",
#     tags=["users"],
# )
