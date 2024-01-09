from fastapi import HTTPException
from sqlalchemy.orm import contains_eager

from database.models import *
from database.schema import *
from config.constant import ERROR_DIC
from database.base_model import DefaultModel


def get_review(course_name, user_name, page, page_size, session, g):
    response = DefaultModel()

    filter_list = []
    if user_name is not None:
        filter_list.append(User.name.like(f'%{user_name}%'))

    if course_name is not None:
        filter_list.append(Course.title.like(f'%{course_name}%'))

    user_id = g.result_data.get('user', None).get('id', None)
    review_query = session.query(Review).outerjoin(User, User.id == Review.user_id
                                        ).outerjoin(Course, Course.id == Review.course_id
                                        ).filter(Review.user_id == user_id,
                                                 Review.status >= constant.STATUS_INACTIVE
                                        ).options(contains_eager(Review.user),
                                                  contains_eager(Review.course))
    review_filter = review_query.filter(*filter_list)
    reviews = review_filter.offset(page_size * (page - 1)).limit(page_size).all()

    response.result_data = {
        'total_count': len(review_query.all()),
        'search_count': len(review_filter.all()),
        'reviews': review_list_schema.dump(reviews)
    }
    return response


def post_review(request, session, g):
    response = DefaultModel()

    user_id = g.result_data.get('user', None).get('id', None)
    course = session.query(Course).filter(Course.id == request.course_id,
                                          Course.status == constant.STATUS_ACTIVE).first()
    if course is None:
        raise HTTPException(detail=ERROR_DIC[constant.ERROR_DATA_NOT_EXIST][1],
                            status_code=ERROR_DIC[constant.ERROR_DATA_NOT_EXIST][0])

    review = Review()
    session.add(review)
    session.flush()

    review.user_id = user_id
    review.course_id = course.id
    review.question = request.question

    response.result_data = {
        'review': review_detail_schema.dump(review)
    }
    return response


def get_review_detail(review_id, session, g):
    response = DefaultModel()

    user_id = g.result_data.get('user', None).get('id', None)
    review = session.query(Review).outerjoin(User, User.id == Review.user_id
                                    ).outerjoin(Course, Course.id == Review.course_id
                                    ).filter(Review.id == review_id,
                                             Review.user_id == user_id,
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


def put_review_detail(review_id, request, session, g):
    response = DefaultModel()

    user_id = g.result_data.get('user', None).get('id', None)

    review = session.query(Review).filter(Review.id == review_id,
                                          Review.user_id == user_id,
                                          Review.status >= constant.STATUS_INACTIVE).first()
    if review is None:
        raise HTTPException(detail=ERROR_DIC[constant.ERROR_DATA_NOT_EXIST][1],
                            status_code=ERROR_DIC[constant.ERROR_DATA_NOT_EXIST][0])

    course = session.query(Course).filter(Course.id == request.course_id,
                                          Course.status == constant.STATUS_ACTIVE).first()
    if course is None:
        raise HTTPException(detail=ERROR_DIC[constant.ERROR_DATA_NOT_EXIST][1],
                            status_code=ERROR_DIC[constant.ERROR_DATA_NOT_EXIST][0])

    review.course_id = course.id
    review.question = request.question

    response.result_data = {
        'review': review_detail_schema.dump(review)
    }
    return response


def delete_review_detail(review_id, session, g):
    response = DefaultModel()

    user_id = g.result_data.get('user', None).get('id', None)
    review = session.query(Review).filter(Review.id == review_id,
                                          Review.user_id == user_id,
                                          Review.status >= constant.STATUS_INACTIVE).first()
    if review is None:
        raise HTTPException(detail=ERROR_DIC[constant.ERROR_DATA_NOT_EXIST][1],
                            status_code=ERROR_DIC[constant.ERROR_DATA_NOT_EXIST][0])

    review.status = constant.STATUS_DELETED
    return response