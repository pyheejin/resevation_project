from fastapi import HTTPException
from sqlalchemy.orm import contains_eager

from database.models import *
from database.schema import *
from config.constant import ERROR_DIC
from database.base_model import DefaultModel


def get_qna(session, g):
    response = DefaultModel()

    user_id = g.result_data.get('user', None).get('id', None)
    qnas = session.query(Qna).outerjoin(User, User.id == Qna.user_id
                            ).outerjoin(Course, Course.id == Qna.course_id
                            ).filter(Qna.user_id == user_id,
                                     Qna.status >= constant.STATUS_INACTIVE
                            ).options(contains_eager(Qna.user),
                                      contains_eager(Qna.course)).all()

    response.result_data = {
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


def get_qna_detail(qna_id, session):
    response = DefaultModel()

    qna = session.query(Qna).outerjoin(User, User.id == Qna.user_id
                            ).outerjoin(Course, Course.id == Qna.course_id
                            ).filter(Qna.id == qna_id,
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

    qna = session.query(Qna).filter(Qna.id == qna_id,
                                    Qna.status >= constant.STATUS_INACTIVE).first()
    if qna is None:
        raise HTTPException(detail=ERROR_DIC[constant.ERROR_DATA_NOT_EXIST][1],
                            status_code=ERROR_DIC[constant.ERROR_DATA_NOT_EXIST][0])

    qna.status = constant.STATUS_DELETED
    return response