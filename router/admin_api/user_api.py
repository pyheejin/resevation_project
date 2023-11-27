from pydantic import BaseModel
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, APIRouter

from config import common
from database import base_model
from database.database import *
from admin_controller import user_controller


router = APIRouter(
    prefix='/user',
)


class PutUserModel(BaseModel):
    login_id: str
    password: str
    name: str
    nickname: str
    phone: str
    email: str


@router.get('', tags=['user'], summary='유저 목록', dependencies=[Depends(common.get_access_token)])
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

        session.rollback()

        response = base_model.DefaultModel()
        common.error_response(response, e.args[0], f'{result_msg} 실패')
    else:
        if response is None:
            response = base_model.DefaultModel()
        if response.result_msg is not None:
            response.result_msg = result_msg + ' 성공'
    finally:
        session.commit()
    return response


@router.get('/{user_id}', tags=['user'], summary='유저 상세', dependencies=[Depends(common.get_access_token)])
def get_user_detail(user_id: int,
                    session: Session = Depends(get_db)):
    result_msg = '유저 상세'
    try:
        response = user_controller.get_user_detail(user_id=user_id,
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
        if response is None:
            response = base_model.DefaultModel()
        if response.result_msg is not None:
            response.result_msg = result_msg + ' 성공'
    finally:
        session.commit()
    return response


@router.put('/{user_id}', tags=['user'], summary='유저 수정', dependencies=[Depends(common.get_access_token)])
def put_user_detail(user_id: int,
                    request: PutUserModel,
                    session: Session = Depends(get_db)):
    result_msg = '유저 수정'
    try:
        response = user_controller.put_user_detail(user_id=user_id,
                                                   request=request,
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
        if response is None:
            response = base_model.DefaultModel()
        if response.result_msg is not None:
            response.result_msg = result_msg + ' 성공'
    finally:
        session.commit()
    return response


@router.delete('/{user_id}', tags=['user'], summary='유저 삭제', dependencies=[Depends(common.get_access_token)])
def delete_user_detail(user_id: int,
                       session: Session = Depends(get_db)):
    result_msg = '유저 삭제'
    try:
        response = user_controller.delete_user_detail(user_id=user_id,
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
        if response is None:
            response = base_model.DefaultModel()
        if response.result_msg is not None:
            response.result_msg = result_msg + ' 성공'
    finally:
        session.commit()
    return response