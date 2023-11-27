from typing import Optional
from pydantic import BaseModel
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, APIRouter

from config import common
from database import base_model
from database.database import *
from database.models import User
from admin_controller import ticket_controller


router = APIRouter(
    prefix='/ticket',
    dependencies=[Depends(common.get_access_token)]
)


class PostTicketModel(BaseModel):
    cost: int
    price: int
    title: str
    description: str


@router.get('', tags=['ticket'], summary='티켓 목록')
def get_ticket(session: Session = Depends(get_db),
               user_id: Optional[int] = None):
    result_msg = '티켓 목록'
    try:
        response = ticket_controller.get_ticket(session=session,
                                                user_id=user_id)
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


@router.post('', tags=['ticket'], summary='티켓 등록')
def post_ticket(request: PostTicketModel,
                session: Session = Depends(get_db),
                g: User = Depends(common.get_access_token)):
    result_msg = '티켓 등록'
    try:
        response = ticket_controller.post_ticket(request=request,
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


@router.get('/{ticket_id}', tags=['ticket'], summary='티켓 상세')
def get_ticket_detail(ticket_id: int,
                      session: Session = Depends(get_db)):
    result_msg = '티켓 상세'
    try:
        response = ticket_controller.get_ticket_detail(ticket_id=ticket_id,
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


@router.put('/{ticket_id}', tags=['ticket'], summary='티켓 수정')
def put_ticket_detail(ticket_id: int,
                      request: PostTicketModel,
                      session: Session = Depends(get_db)):
    result_msg = '티켓 수정'
    try:
        response = ticket_controller.put_ticket_detail(ticket_id=ticket_id,
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


@router.delete('/{ticket_id}', tags=['ticket'], summary='티켓 삭제')
def delete_ticket_detail(ticket_id: int,
                         session: Session = Depends(get_db)):
    result_msg = '티켓 삭제'
    try:
        response = ticket_controller.delete_ticket_detail(ticket_id=ticket_id,
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