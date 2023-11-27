from fastapi import HTTPException

from database.models import *
from database.admin_schema import *
from config.constant import ERROR_DIC
from database.base_model import DefaultModel


def get_product(session, user_id):
    response = DefaultModel()

    filter_list = []
    if user_id is not None:
        filter_list.append(Product.user_id == user_id)

    products = session.query(Product).filter(Product.status == constant.STATUS_ACTIVE,
                                             *filter_list).all()
    response.result_data = {
        'products': product_list_schema.dump(products)
    }
    return response


def post_product(request, session, g):
    response = DefaultModel()

    user_id = g.result_data.get('user', None).get('id', None)

    title = request.title
    description = request.description

    product_check = session.query(Product).filter(Product.title == title,
                                                  Product.user_id == user_id,
                                                  Product.status >= constant.STATUS_INACTIVE).first()
    if product_check is not None:
        raise HTTPException(detail=ERROR_DIC[constant.ERROR_DATA_EXIST][1],
                            status_code=ERROR_DIC[constant.ERROR_DATA_EXIST][0])

    product = Product()
    session.add(product)
    session.flush()

    product.user_id = user_id
    product.title = title
    product.description = description

    response.result_data = {
        'product': product_detail_schema.dump(product)
    }
    return response


def get_product_detail(product_id, session):
    response = DefaultModel()

    product = session.query(Product).filter(Product.id == product_id,
                                            Product.status >= constant.STATUS_INACTIVE).first()
    if product is None:
        raise HTTPException(detail=ERROR_DIC[constant.ERROR_DATA_NOT_EXIST][1],
                            status_code=ERROR_DIC[constant.ERROR_DATA_NOT_EXIST][0])

    response.result_data = {
        'product': product_detail_schema.dump(product)
    }
    return response


def put_product_detail(product_id, request, session):
    response = DefaultModel()

    product = session.query(Product).filter(Product.id == product_id,
                                            Product.status >= constant.STATUS_INACTIVE).first()
    if product is None:
        raise HTTPException(detail=ERROR_DIC[constant.ERROR_DATA_NOT_EXIST][1],
                            status_code=ERROR_DIC[constant.ERROR_DATA_NOT_EXIST][0])

    title = request.title
    description = request.description

    product_check = session.query(Product).filter(Product.title == title,
                                                  Product.title != product.title,
                                                  Product.status >= constant.STATUS_INACTIVE).first()
    if product_check is not None:
        raise HTTPException(detail=ERROR_DIC[constant.ERROR_DATA_EXIST][1],
                            status_code=ERROR_DIC[constant.ERROR_DATA_EXIST][0])

    product.title = title
    product.description = description

    response.result_data = {
        'product': product_detail_schema.dump(product)
    }
    return response


def delete_product_detail(product_id, session):
    response = DefaultModel()

    product = session.query(Product).filter(Product.id == product_id,
                                            Product.status >= constant.STATUS_INACTIVE).first()
    if product is None:
        raise HTTPException(detail=ERROR_DIC[constant.ERROR_DATA_NOT_EXIST][1],
                            status_code=ERROR_DIC[constant.ERROR_DATA_NOT_EXIST][0])

    product.status = constant.STATUS_DELETED
    return response