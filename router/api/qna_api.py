from pydantic import BaseModel
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, APIRouter

from config import common
from database import base_model
from database.database import *
from database.models import User
from controller import qna_controller


router = APIRouter(
    prefix='/qna',
    dependencies=[Depends(common.get_access_token)]
)


class PostQnaModel(BaseModel):
    course_id: int
    question: str


class PutQnaModel(BaseModel):
    course_id: int
    question: str


@router.get('', tags=['qna'], summary='문의 목록')
def get_qna(session: Session = Depends(get_db),
            g: User = Depends(common.get_access_token)):
    result_msg = '문의 목록'
    try:
        response = qna_controller.get_qna(session=session,
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


@router.post('', tags=['qna'], summary='문의 등록')
def post_qna(request: PostQnaModel,
             session: Session = Depends(get_db),
             g: User = Depends(common.get_access_token)):
    result_msg = '문의 등록'
    try:
        response = qna_controller.post_qna(request=request,
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


@router.get('/{qna_id}', tags=['qna'], summary='문의 상세')
def get_qna_detail(qna_id: int,
                   session: Session = Depends(get_db)):
    result_msg = '문의 상세'
    try:
        response = qna_controller.get_qna_detail(qna_id=qna_id,
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


@router.put('/{qna_id}', tags=['qna'], summary='문의 수정')
def put_qna_detail(qna_id: int,
                   request: PutQnaModel,
                   session: Session = Depends(get_db),
                   g: User = Depends(common.get_access_token)):
    result_msg = '문의 수정'
    try:
        response = qna_controller.put_qna_detail(qna_id=qna_id,
                                                 request=request,
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


@router.delete('/{qna_id}', tags=['qna'], summary='문의 삭제')
def delete_qna_detail(qna_id: int,
                      session: Session = Depends(get_db)):
    result_msg = '문의 삭제'
    try:
        response = qna_controller.delete_qna_detail(qna_id=qna_id,
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