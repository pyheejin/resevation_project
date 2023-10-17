from typing_extensions import Annotated
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status

from database.models import User
from database.database import get_db
from config.constant import ERROR_DIC
from database.base_model import DefaultModel


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


async def get_current_user(token: str = Depends(oauth2_scheme)):
    print(token)
    session = next(get_db())
    user = session.query(User).filter(User.login_id == token).first()
    session.close()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid authentication credentials',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    return user


async def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]):
    if current_user is None:
        raise HTTPException(status_code=400, detail='Inactive user')
    return current_user


def error_response(response: DefaultModel, error_msg: str, result_msg: str):
    if response is None:
        response = DefaultModel()

    if error_msg is None:
        return

    response.result_data = {}
    if error_msg in ERROR_DIC.keys():
        response.result_code = ERROR_DIC[error_msg][0]
        response.result_msg = f'[{result_msg}] {ERROR_DIC[error_msg][1]}'
    else:
        response.result_code = 210
        response.result_msg = f'[{result_msg}] {error_msg}'
    return response


