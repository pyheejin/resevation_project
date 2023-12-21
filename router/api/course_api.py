from typing import Optional
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, APIRouter

from config import common, constant
from database.database import *
from database import base_model
from controller import course_controller


router = APIRouter(
    prefix='/course',
    dependencies=[Depends(common.get_access_token)]
)


@router.get('', tags=['course'], summary='수업 목록')
def get_course(session: Session = Depends(get_db),
               user_id: Optional[int] = None,
               page: Optional[int] = constant.DEFAULT_PAGE,
               page_size: Optional[int] = constant.DEFAULT_PAGE_SIZE):
    result_msg = '수업 목록'
    try:
        response = course_controller.get_course(session=session,
                                                user_id=user_id,
                                                page=page,
                                                page_size=page_size)
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


@router.get('/{course_id}', tags=['course'], summary='수업 상세')
def get_course_detail(course_id: int,
                      session: Session = Depends(get_db)):
    result_msg = '수업 상세'
    try:
        response = course_controller.get_course_detail(course_id=course_id,
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