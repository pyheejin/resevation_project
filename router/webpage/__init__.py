from fastapi import APIRouter


routers = APIRouter(
    prefix=''
)


@routers.get('/index')
def index():
    return {'app': 'reservation'}
