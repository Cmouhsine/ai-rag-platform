# from fastapi import FastAPI

# from app.core.config import settings

# app = FastAPI(
#     title=settings.app_name,
#     version=settings.app_version,
# )


# @app.get("/", tags=["Health"])
# async def health_check():
#     return {
#         "application": settings.app_name,
#         "version": settings.app_version,
#         "status": "running",
#     }

from fastapi import FastAPI

from app.api.api import api_router
from app.core.config import settings

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
)

app.include_router(api_router)


@app.get("/")
def root():
    return {
        "message": "AI Knowledge Assistant API"
    }