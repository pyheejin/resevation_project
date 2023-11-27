from fastapi import APIRouter

from router.api import user_api, product_api


routers = APIRouter(
    prefix=''
)


routers.include_router(user_api.router)
routers.include_router(product_api.router)
