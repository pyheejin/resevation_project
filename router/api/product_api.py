from typing import Optional
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, APIRouter

from config import common
from database.database import *
from database import base_model
from database.models import User
from controller import product_controller


router = APIRouter(
    prefix='/product',
    dependencies=[Depends(common.get_access_token)]
)


@router.get('', tags=['product'], summary='상품 목록')
def get_product(session: Session = Depends(get_db),
                user_id: Optional[int] = None):
    result_msg = '상품 목록'
    try:
        response = product_controller.get_product(session=session,
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


@router.get('/{product_id}', tags=['product'], summary='상품 상세')
def get_product_detail(product_id: int,
                       session: Session = Depends(get_db)):
    result_msg = '상품 상세'
    try:
        response = product_controller.get_product_detail(product_id=product_id,
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