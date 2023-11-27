from sqlalchemy import and_
from sqlalchemy.orm import contains_eager
from fastapi import HTTPException

from database.models import *
from database.schema import *
from config.constant import ERROR_DIC
from database.base_model import DefaultModel


def get_product(session, user_id):
    response = DefaultModel()

    filter_list = []
    if user_id is not None:
        filter_list.append(Product.user_id == user_id)

    products = session.query(Product).outerjoin(User, and_(User.id == Product.user_id,
                                                           User.status == constant.STATUS_ACTIVE)
                                    ).filter(Product.status == constant.STATUS_ACTIVE,
                                             *filter_list
                                    ).options(contains_eager(Product.user)).all()
    response.result_data = product_list_schema.dump(products)
    return response


def get_product_detail(product_id, session):
    response = DefaultModel()

    product = session.query(Product).outerjoin(User, and_(User.id == Product.user_id,
                                                          User.status == constant.STATUS_ACTIVE)
                                    ).filter(Product.id == product_id
                                    ).options(contains_eager(Product.user)).first()
    if product is None:
        raise HTTPException(detail=ERROR_DIC[constant.ERROR_DATA_NOT_EXIST][1],
                            status_code=ERROR_DIC[constant.ERROR_DATA_NOT_EXIST][0])

    response.result_data = {
        'product': product_detail_schema.dump(product)
    }
    return response