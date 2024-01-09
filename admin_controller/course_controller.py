from datetime import datetime
from fastapi import HTTPException
from sqlalchemy import and_
from sqlalchemy.orm import contains_eager

from database.models import *
from database.admin_schema import *
from config.constant import ERROR_DIC
from database.base_model import DefaultModel


def get_course(session, status, page, page_size, g):
    response = DefaultModel()

    user_id = g.result_data.get('user', None).get('id', None)

    filter_list = []
    if status is not None:
        filter_list.append(Course.status == status)

    course_query = session.query(Course).outerjoin(CourseDetail, and_(Course.id == CourseDetail.course_id,
                                                                      CourseDetail.status == constant.STATUS_ACTIVE)
                                        ).filter(Course.user_id == user_id
                                        ).options(contains_eager(Course.course_detail))
    course_filter = course_query.filter(*filter_list)
    courses = course_filter.offset(page_size * (page - 1)).limit(page_size).all()

    response.result_data = {
        'total_count': len(course_query.all()),
        'search_count': len(course_filter.all()),
        'courses': course_list_schema.dump(courses)
    }
    return response


def post_course(request, session, g):
    response = DefaultModel()

    user_id = g.result_data.get('user', None).get('id', None)

    title = request.title
    description = request.description

    course_check = session.query(Course).filter(Course.title == title,
                                                Course.user_id == user_id,
                                                Course.status >= constant.STATUS_INACTIVE).first()
    if course_check is not None:
        raise HTTPException(detail=ERROR_DIC[constant.ERROR_DATA_EXIST][1],
                            status_code=ERROR_DIC[constant.ERROR_DATA_EXIST][0])

    course = Course()
    session.add(course)
    session.flush()

    course.user_id = user_id
    course.title = title
    course.description = description

    for idx, detail in enumerate(request.course_detail):
        course_detail = CourseDetail()
        session.add(course_detail)
        session.flush()

        course_date = datetime.strptime(detail.course_date, '%Y-%m-%d %H:%M')

        course_detail.course_id = course.id
        course_detail.title = detail.title
        course_detail.course_date = course_date
        # todo 주소 open api로 조회하면 좋을 것 같음
        course_detail.address = detail.address
        course_detail.address_detail = detail.address_detail

        if len(request.course_detail) == idx + 1:
            course.last_course_date = course_date

    response.result_data = {
        'course': course_schema.dump(course)
    }
    return response


def get_course_detail(course_id, session):
    response = DefaultModel()

    course = session.query(Course).filter(Course.id == course_id,
                                          Course.status >= constant.STATUS_INACTIVE).first()
    if course is None:
        raise HTTPException(detail=ERROR_DIC[constant.ERROR_DATA_NOT_EXIST][1],
                            status_code=ERROR_DIC[constant.ERROR_DATA_NOT_EXIST][0])

    response.result_data = {
        'course': course_schema.dump(course)
    }
    return response


def put_course_detail(course_id, request, session):
    response = DefaultModel()

    course = session.query(Course).outerjoin(CourseDetail, and_(Course.id == CourseDetail.course_id,
                                                                CourseDetail.status == constant.STATUS_ACTIVE)
                                ).filter(Course.id == course_id,
                                         Course.status >= constant.STATUS_INACTIVE
                                ).options(contains_eager(Course.course_detail)).all()
    course = course[0]
    if course is None:
        raise HTTPException(detail=ERROR_DIC[constant.ERROR_DATA_NOT_EXIST][1],
                            status_code=ERROR_DIC[constant.ERROR_DATA_NOT_EXIST][0])

    title = request.title
    description = request.description

    course_check = session.query(Course).filter(Course.title == title,
                                                Course.title != Course.title,
                                                Course.status >= constant.STATUS_INACTIVE).first()
    if course_check is not None:
        raise HTTPException(detail=ERROR_DIC[constant.ERROR_DATA_EXIST][1],
                            status_code=ERROR_DIC[constant.ERROR_DATA_EXIST][0])

    course.title = title
    course.description = description
    course.count = len(request.course_detail)

    session.query(CourseDetail).filter(CourseDetail.course_id == course_id
                            ).update({'status': constant.STATUS_DELETED}, synchronize_session=False)

    for idx, detail in enumerate(request.course_detail):
        course_detail = CourseDetail()
        session.add(course_detail)
        session.flush()

        course_date = datetime.strptime(detail.course_date, '%Y-%m-%d %H:%M')

        course_detail.course_id = course.id
        course_detail.title = detail.title
        course_detail.course_date = course_date
        course_detail.address = detail.address
        course_detail.address_detail = detail.address_detail

        if len(request.course_detail) == idx + 1:
            course.last_course_date = course_date

    response.result_data = {
        'course': course_schema.dump(course)
    }
    return response


def delete_course_detail(course_id, session):
    response = DefaultModel()

    course = session.query(Course).filter(Course.id == course_id,
                                          Course.status >= constant.STATUS_INACTIVE).first()
    if course is None:
        raise HTTPException(detail=ERROR_DIC[constant.ERROR_DATA_NOT_EXIST][1],
                            status_code=ERROR_DIC[constant.ERROR_DATA_NOT_EXIST][0])

    course.status = constant.STATUS_DELETED
    session.query(CourseDetail).filter(CourseDetail.course_id == course_id
                            ).update({'status': constant.STATUS_DELETED}, synchronize_session=False)
    return response