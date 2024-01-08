from fastapi import HTTPException
from sqlalchemy import and_, or_
from sqlalchemy.orm import contains_eager

from database.models import *
from database.admin_schema import *
from config.constant import ERROR_DIC
from database.base_model import DefaultModel


def get_review(course_name, user_name, session, g):
    response = DefaultModel()

    filter_list = []
    if user_name is not None:
        filter_list.append(or_(User.name.like(f'%{user_name}%'),
                               User.nickname.like(f'%{user_name}%')))

    if course_name is not None:
        filter_list.append(Course.title.like(f'%{course_name}%'))

    user_id = g.result_data.get('user', None).get('id', None)
    review_query = session.query(Review).outerjoin(User, User.id == Review.user_id
                                        ).outerjoin(Course, Course.id == Review.course_id
                                        ).filter(Course.user_id == user_id,
                                                 Review.status >= constant.STATUS_INACTIVE
                                        ).options(contains_eager(Review.user),
                                                  contains_eager(Review.course))
    reviews = review_query.filter(*filter_list).all()

    response.result_data = {
        'total_count': len(review_query.all()),
        'search_count': len(reviews),
        'reviews': review_list_schema.dump(reviews)
    }
    return response


def get_review_detail(review_id, g, session):
    response = DefaultModel()

    user_id = g.result_data.get('user', None).get('id', None)
    review = session.query(Review).outerjoin(User, User.id == Review.user_id
                            ).outerjoin(Course, Course.id == Review.course_id
                            ).filter(Review.id == review_id,
                                     Course.user_id == user_id,
                                     Review.status >= constant.STATUS_INACTIVE
                            ).options(contains_eager(Review.user),
                                      contains_eager(Review.course)).first()

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

    review.is_best = constant.STATUS_ACTIVE

    response.result_data = {
        'review': review_detail_schema.dump(review)
    }
    return response