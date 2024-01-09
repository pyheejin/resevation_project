from typing import Optional, List
from pydantic import BaseModel
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, APIRouter

from config import common, constant
from database import base_model
from database.database import *
from database.models import User
from admin_controller import course_controller


router = APIRouter(
    prefix='/course',
    dependencies=[Depends(common.get_access_token)]
)


class PostCourseDetailModel(BaseModel):
    title: str
    course_date: str
    address: Optional[str]
    address_detail: Optional[str]


class PostCourseModel(BaseModel):
    title: str
    description: str
    course_detail: List[PostCourseDetailModel]


@router.get('', tags=['course'], summary='수업 목록')
def get_course(session: Session = Depends(get_db),
               status: Optional[int] = constant.STATUS_ACTIVE,
               page: Optional[int] = constant.DEFAULT_PAGE,
               page_size: Optional[int] = constant.DEFAULT_PAGE_SIZE,
               g: User = Depends(common.get_access_token)):
    result_msg = '수업 목록'
    try:
        response = course_controller.get_course(session=session,
                                                status=status,
                                                page=page,
                                                page_size=page_size,
                                                g=g)
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


@router.post('', tags=['course'], summary='수업 등록')
def post_course(request: PostCourseModel,
                session: Session = Depends(get_db),
                g: User = Depends(common.get_access_token)):
    result_msg = '수업 등록'
    try:
        response = course_controller.post_course(request=request,
                                                 session=session,
                                                 g=g)
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


@router.put('/{course_id}', tags=['course'], summary='수업 수정')
def put_course_detail(course_id: int,
                      request: PostCourseModel,
                      session: Session = Depends(get_db)):
    result_msg = '수업 수정'
    try:
        response = course_controller.put_course_detail(course_id=course_id,
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


@router.delete('/{course_id}', tags=['course'], summary='수업 삭제')
def delete_course_detail(course_id: int,
                         session: Session = Depends(get_db)):
    result_msg = '수업 삭제'
    try:
        response = course_controller.delete_course_detail(course_id=course_id,
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