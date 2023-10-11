from fastapi import APIRouter
from typing_extensions import Annotated
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from database.models import User
from database.database import get_db

from router.admin_api import product_api


routers = APIRouter(
    prefix=''
)


@routers.post("/token")
async def token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    session = next(get_db())

    user = session.query(User).filter(User.login_id == form_data.username).first()
    session.close()
    if form_data.password != user._password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    return {"access_token": user.name, "token_type": "bearer"}


routers.include_router(product_api.router)