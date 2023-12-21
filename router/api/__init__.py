from fastapi import APIRouter

from router.api import user_api, course_api


routers = APIRouter(
    prefix=''
)


routers.include_router(user_api.router)
routers.include_router(course_api.router)
