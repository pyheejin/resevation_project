from fastapi import Depends, HTTPException, APIRouter
from fastapi.responses import Response
from typing import Optional
from typing_extensions import Annotated
from pydantic import BaseModel
from sqlalchemy.orm import Session

from config import common, constant
from database import base_model
from database.database import *
from controller import product_controller


router = APIRouter(
    prefix='/product',
    dependencies=[Depends(common.get_current_active_user)]
)


class PostProductModel(BaseModel):
    login_id: str = 'heejin'
    password: str = 'heejin'


@router.get('', tags=['product'], summary='상품 목록')
def admin_get_product(session: Session = Depends(get_db)):
    result_msg = '상품 목록'
    try:
        response = product_controller.admin_get_product(session=session)
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


@router.get('/{product_id}', tags=['product'], summary='상품 상세')
def admin_get_product_detail(product_id: int,
                             session: Session = Depends(get_db)):
    result_msg = '상품 상세'
    try:
        response = product_controller.admin_get_product_detail(product_id=product_id,
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