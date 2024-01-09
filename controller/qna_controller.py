from fastapi import HTTPException
from sqlalchemy.orm import contains_eager

from database.models import *
from database.schema import *
from config.constant import ERROR_DIC
from database.base_model import DefaultModel


def get_qna(course_name, user_name, page, page_size, session, g):
    response = DefaultModel()

    filter_list = []
    if user_name is not None:
        filter_list.append(User.name.like(f'%{user_name}%'))

    if course_name is not None:
        filter_list.append(Course.title.like(f'%{course_name}%'))

    user_id = g.result_data.get('user', None).get('id', None)
    qna_query = session.query(Qna).outerjoin(User, User.id == Qna.user_id
                                ).outerjoin(Course, Course.id == Qna.course_id
                                ).filter(Qna.user_id == user_id,
                                         Qna.status >= constant.STATUS_INACTIVE
                                ).options(contains_eager(Qna.user),
                                          contains_eager(Qna.course))
    qna_filter = qna_query.filter(*filter_list)
    qnas = qna_filter.offset(page_size * (page - 1)).limit(page_size).all()

    response.result_data = {
        'total_count': len(qna_query.all()),
        'search_count': len(qna_filter.all()),
        'qnas': qna_list_schema.dump(qnas)
    }
    return response


def post_qna(request, session, g):
    response = DefaultModel()

    user_id = g.result_data.get('user', None).get('id', None)
    course = session.query(Course).filter(Course.id == request.course_id,
                                          Course.status == constant.STATUS_ACTIVE).first()
    if course is None:
        raise HTTPException(detail=ERROR_DIC[constant.ERROR_DATA_NOT_EXIST][1],
                            status_code=ERROR_DIC[constant.ERROR_DATA_NOT_EXIST][0])

    qna = Qna()
    session.add(qna)
    session.flush()

    qna.user_id = user_id
    qna.course_id = course.id
    qna.question = request.question

    response.result_data = {
        'qna': qna_detail_schema.dump(qna)
    }
    return response


def get_qna_detail(qna_id, session, g):
    response = DefaultModel()

    user_id = g.result_data.get('user', None).get('id', None)
    qna = session.query(Qna).outerjoin(User, User.id == Qna.user_id
                            ).outerjoin(Course, Course.id == Qna.course_id
                            ).filter(Qna.id == qna_id,
                                     Qna.user_id == user_id,
                                     Qna.status >= constant.STATUS_INACTIVE
                            ).options(contains_eager(Qna.user),
                                      contains_eager(Qna.course)).first()

    if qna is None:
        raise HTTPException(detail=ERROR_DIC[constant.ERROR_DATA_NOT_EXIST][1],
                            status_code=ERROR_DIC[constant.ERROR_DATA_NOT_EXIST][0])

    response.result_data = {
        'qna': qna_detail_schema.dump(qna)
    }
    return response


def put_qna_detail(qna_id, request, session, g):
    response = DefaultModel()

    user_id = g.result_data.get('user', None).get('id', None)

    qna = session.query(Qna).filter(Qna.id == qna_id,
                                    Qna.user_id == user_id,
                                    Qna.status >= constant.STATUS_INACTIVE).first()
    if qna is None:
        raise HTTPException(detail=ERROR_DIC[constant.ERROR_DATA_NOT_EXIST][1],
                            status_code=ERROR_DIC[constant.ERROR_DATA_NOT_EXIST][0])

    course = session.query(Course).filter(Course.id == request.course_id,
                                          Course.status == constant.STATUS_ACTIVE).first()
    if course is None:
        raise HTTPException(detail=ERROR_DIC[constant.ERROR_DATA_NOT_EXIST][1],
                            status_code=ERROR_DIC[constant.ERROR_DATA_NOT_EXIST][0])

    qna.course_id = course.id
    qna.question = request.question

    response.result_data = {
        'qna': qna_detail_schema.dump(qna)
    }
    return response


def delete_qna_detail(qna_id, session):
    response = DefaultModel()

    user_id = g.result_data.get('user', None).get('id', None)

    qna = session.query(Qna).filter(Qna.id == qna_id,
                                    Qna.user_id == user_id,
                                    Qna.status >= constant.STATUS_INACTIVE).first()
    if qna is None:
        raise HTTPException(detail=ERROR_DIC[constant.ERROR_DATA_NOT_EXIST][1],
                            status_code=ERROR_DIC[constant.ERROR_DATA_NOT_EXIST][0])

    qna.status = constant.STATUS_DELETED
    return response