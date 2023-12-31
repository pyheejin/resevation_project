from fastapi import APIRouter

from router.admin_api import (product_api, qna_api, review_api, ticket_api, user_api)


routers = APIRouter(
    prefix=''
)


routers.include_router(product_api.router)
routers.include_router(qna_api.router)
routers.include_router(review_api.router)
routers.include_router(ticket_api.router)
routers.include_router(user_api.router)