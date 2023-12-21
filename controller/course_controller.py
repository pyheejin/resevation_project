from sqlalchemy import and_
from sqlalchemy.orm import contains_eager
from fastapi import HTTPException

from database.models import *
from database.schema import *
from config.constant import ERROR_DIC
from database.base_model import DefaultModel


def get_course(session, user_id, page, page_size):
    response = DefaultModel()

    filter_list = []
    if user_id is not None:
        filter_list.append(Course.user_id == user_id)

    courses = session.query(Course).outerjoin(User, and_(User.id == Course.user_id,
                                                         User.status == constant.STATUS_ACTIVE)
                                    ).filter(Course.status == constant.STATUS_ACTIVE,
                                             *filter_list
                                    ).options(contains_eager(Course.user)
                                    ).offset(page_size * (page - 1)).limit(page_size).all()
    response.result_data = course_list_schema.dump(courses)
    return response


def get_course_detail(course_id, session):
    response = DefaultModel()

    course = session.query(Course).outerjoin(User, and_(User.id == Course.user_id,
                                                        User.status == constant.STATUS_ACTIVE)
                                    ).filter(Course.id == course_id
                                    ).options(contains_eager(Course.user)).first()
    if course is None:
        raise HTTPException(detail=ERROR_DIC[constant.ERROR_DATA_NOT_EXIST][1],
                            status_code=ERROR_DIC[constant.ERROR_DATA_NOT_EXIST][0])

    response.result_data = {
        'course': course_detail_schema.dump(course)
    }
    return response