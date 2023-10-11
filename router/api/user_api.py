from fastapi import Depends, Request, APIRouter, HTTPException
from fastapi.responses import Response
from typing import Optional
from typing_extensions import Annotated
from pydantic import BaseModel
from sqlalchemy.orm import Session

from config import common, constant
from database import base_model
from database.database import *
from database.models import User
from controller import user_controller


router = APIRouter(
    prefix='/user'
)


class PostUserLoginModel(BaseModel):
    login_id: str = 'heejin'
    password: str = 'heejin'


class PostUserJoinModel(BaseModel):
    login_id: str = 'heejin'
    password: str = 'heejin'
    name: Optional[str] = 'heejin'
    phone: Optional[str] = '010-0000-0000'
    email: Optional[str] = 'heejin@heejin.com'


@router.post('/join', tags=['user'], summary='회원가입')
def post_user_join(request: PostUserJoinModel,
                   session: Session = Depends(get_db)):
    result_msg = '회원가입'
    try:
        response = user_controller.post_user_join(request=request,
                                                  session=session)
        response.result_msg = f'{response.result_msg}'
    except HTTPException as e:
        print(e.detail)

        session.rollback()

        response = base_model.DefaultModel()
        common.error_response(response, e.detail, f'{result_msg} 실패')
    except Exception as e:
        print(e.args[0])

        session.rollback()

        response = base_model.DefaultModel()
        common.error_response(response, e.args[0], f'{result_msg} 실패')
    else:
        session.commit()

        if response is None:
            response = base_model.DefaultModel()
        if response.result_msg is not None:
            response.result_msg = result_msg + ' 성공'
    finally:
        session.close()
    return response



@router.post('/login', tags=['user'], summary='로그인')
def post_user_login(request: PostUserLoginModel,
                    response_cookie: Response,
                    session: Session = Depends(get_db)):
    result_msg = '로그인'
    try:
        response = user_controller.post_user_login(request=request,
                                                   response_cookie=response_cookie,
                                                   session=session)
        response.result_msg = f'{response.result_msg}'
    except HTTPException as e:
        print(e.detail)

        session.rollback()

        response = base_model.DefaultModel()
        common.error_response(response, e.detail, f'{result_msg} 실패')
    except Exception as e:
        print(e.args[0])
        print(e)

        session.rollback()

        response = base_model.DefaultModel()
        common.error_response(response, e.args[0], f'{result_msg} 실패')
    else:
        session.commit()

        if response is None:
            response = base_model.DefaultModel()
        if response.result_msg is not None:
            response.result_msg = result_msg + ' 성공'
    finally:
        session.close()
    return response


@router.post('/logout', tags=['user'], summary='로그아웃')
def post_user_logout(request: Request,
                     session: Session = Depends(get_db)):
    result_msg = '로그아웃'
    try:
        response = user_controller.post_user_logout(request=request,
                                                    session=session)
        response.result_msg = f'{response.result_msg}'
    except HTTPException as e:
        print(e.detail)

        session.rollback()

        response = base_model.DefaultModel()
        common.error_response(response, e.detail, f'{result_msg} 실패')
    except Exception as e:
        print(e.args[0])
        print(e)

        session.rollback()

        response = base_model.DefaultModel()
        common.error_response(response, e.args[0], f'{result_msg} 실패')
    else:
        session.commit()

        if response is None:
            response = base_model.DefaultModel()
        if response.result_msg is not None:
            response.result_msg = result_msg + ' 성공'
    finally:
        session.close()
    return response


@router.get('', tags=['user'], summary='유저 목록', dependencies=[Depends(common.get_current_active_user)])
def get_user(session: Session = Depends(get_db)):
    result_msg = '유저 목록'
    try:
        response = user_controller.get_user(session=session)
        response.result_msg = f'{response.result_msg}'
    except HTTPException as e:
        print(e.detail)

        session.rollback()

        response = base_model.DefaultModel()
        common.error_response(response, e.detail, f'{result_msg} 실패')
    except Exception as e:
        print(e.args[0])
        print(e)

        session.rollback()

        response = base_model.DefaultModel()
        common.error_response(response, e.args[0], f'{result_msg} 실패')
    else:
        session.commit()

        if response is None:
            response = base_model.DefaultModel()
        if response.result_msg is not None:
            response.result_msg = result_msg + ' 성공'
    finally:
        session.close()
    return response