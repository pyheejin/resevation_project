from typing import Optional
from pydantic import BaseModel
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, APIRouter

from config import common, constant
from database import base_model
from database.database import *
from database.models import User
from admin_controller import review_controller


router = APIRouter(
    prefix='/review',
    dependencies=[Depends(common.get_access_token)]
)


@router.get('', tags=['review'], summary='리뷰 목록')
def get_review(user_name: Optional[str] = None,
               course_name: Optional[str] = None,
               page: Optional[int] = constant.DEFAULT_PAGE,
               page_size: Optional[int] = constant.DEFAULT_PAGE_SIZE,
               session: Session = Depends(get_db),
               g: User = Depends(common.get_access_token)):
    result_msg = '리뷰 목록'
    try:
        response = review_controller.get_review(user_name=user_name,
                                                course_name=course_name,
                                                page=page,
                                                page_size=page_size,
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


@router.get('/{review_id}', tags=['review'], summary='리뷰 상세')
def get_review_detail(review_id: int,
                      session: Session = Depends(get_db),
                      g: User = Depends(common.get_access_token)):
    result_msg = '리뷰 상세'
    try:
        response = review_controller.get_review_detail(review_id=review_id,
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


@router.post('/{review_id}/best', tags=['review'], summary='베스트 리뷰로 등록')
def post_review_detail_best(review_id: int,
                            session: Session = Depends(get_db)):
    result_msg = '베스트 리뷰로 등록'
    try:
        response = review_controller.post_review_detail_best(review_id=review_id,
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