from fastapi import HTTPException

from database.models import *
from database.admin_schema import *
from config.constant import ERROR_DIC
from database.base_model import DefaultModel


def get_review(session):
    response = DefaultModel()

    reviews = session.query(Review).filter(Review.status >= constant.STATUS_INACTIVE).all()

    response.result_data = {
        'reviews': review_list_schema.dump(reviews)
    }
    return response


def get_review_detail(review_id, session):
    response = DefaultModel()

    review = session.query(Review).filter(Review.id == review_id,
                                          Review.status >= constant.STATUS_INACTIVE).first()
    if review is None:
        raise HTTPException(detail=ERROR_DIC[constant.ERROR_DATA_NOT_EXIST][1],
                            status_code=ERROR_DIC[constant.ERROR_DATA_NOT_EXIST][0])

    response.result_data = {
        'review': review_detail_schema.dump(review)
    }
    return response


def post_review_detail_best(review_id, session):
    response = DefaultModel()

    review = session.query(Review).filter(Review.id == review_id,
                                          Review.status >= constant.STATUS_INACTIVE).first()
    if review is None:
        raise HTTPException(detail=ERROR_DIC[constant.ERROR_DATA_NOT_EXIST][1],
                            status_code=ERROR_DIC[constant.ERROR_DATA_NOT_EXIST][0])

    if review.is_best == constant.STATUS_ACTIVE:
        review.is_best = constant.STATUS_INACTIVE
    else:
        review.is_best = constant.STATUS_ACTIVE

    response.result_data = {
        'review': review_detail_schema.dump(review)
    }
    return response