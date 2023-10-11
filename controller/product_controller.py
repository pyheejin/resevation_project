from fastapi import HTTPException

from database.models import *
from database.schema import *
from config.jwt_handler import JWT
from config.constant import ERROR_DIC
from database.base_model import DefaultModel


def admin_post_product(request, session, g):
    response = DefaultModel()

    is_option = request.is_option
    name = request.name
    description = request.description
    price = request.price
    discount_rate = request.discount_rate
    discount_price = request.discount_price

    product_check = session.query(Product).filter(Product.name == name,
                                                  Product.status == constant.STATUS_ACTIVE).first()
    if product_check is not None:
        raise HTTPException(detail=ERROR_DIC[constant.ERROR_USER_EXIST][1],
                            status_code=ERROR_DIC[constant.ERROR_USER_EXIST][0])

    product = Product()
    session.add(product)

    product.is_option = is_option
    product.name = name
    product.description = description
    product.price = price
    product.discount_rate = discount_rate
    product.discount_price = discount_price

    response.result_data = {
        'product': product_detail_schema.dump(product)
    }
    return response


def admin_get_product(session):
    response = DefaultModel()

    products = session.query(Product).all()
    response.result_data = product_list_schema.dump(products)
    return response


def admin_get_product_detail(product_id, session):
    response = DefaultModel()

    product = session.query(Product).filter(Product.id == product_id).first()
    if product is None:
        raise HTTPException(detail=ERROR_DIC[constant.ERROR_DATA_NOT_EXIST][1],
                            status_code=ERROR_DIC[constant.ERROR_DATA_NOT_EXIST][0])

    response.result_data = {
        'product': product_detail_schema.dump(product)
    }
    return response