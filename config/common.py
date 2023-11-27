from fastapi import Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from config.constant import *
from config.jwt_handler import JWT
from database.base_model import DefaultModel


def get_access_token(token: HTTPAuthorizationCredentials = Depends(HTTPBearer(auto_error=False))):
    if token is None:
        raise HTTPException(status_code=ERROR_DIC[ERROR_UNAUTHORIZED][0],
                            detail=ERROR_DIC[ERROR_UNAUTHORIZED][1])
    else:
        jwt_data = JWT()
        user = jwt_data.verify_token(token.credentials)
        return user


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


