from fastapi import HTTPException
from sqlalchemy.orm import contains_eager

from database.models import *
from database.admin_schema import *
from config.constant import ERROR_DIC
from database.base_model import DefaultModel


def get_qna(session):
    response = DefaultModel()

    qnas = session.query(Qna).outerjoin(User, User.id == Qna.user_id
                            ).outerjoin(Course, Course.id == Qna.course_id
                            ).filter(Qna.status >= constant.STATUS_INACTIVE
                            ).options(contains_eager(Qna.user),
                                      contains_eager(Qna.course)).all()

    response.result_data = {
        'qnas': qna_list_schema.dump(qnas)
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


def delete_qna_detail(qna_id, session):
    response = DefaultModel()

    qna = session.query(Qna).filter(Qna.id == qna_id,
                                    Qna.status >= constant.STATUS_INACTIVE).first()
    if qna is None:
        raise HTTPException(detail=ERROR_DIC[constant.ERROR_DATA_NOT_EXIST][1],
                            status_code=ERROR_DIC[constant.ERROR_DATA_NOT_EXIST][0])

    qna.status = constant.STATUS_DELETED
    return response


def post_qna_detail_answer(qna_id, request, session):
    response = DefaultModel()

    qna = session.query(Qna).filter(Qna.id == qna_id,
                                    Qna.status >= constant.STATUS_INACTIVE).first()
    if qna is None:
        raise HTTPException(detail=ERROR_DIC[constant.ERROR_DATA_NOT_EXIST][1],
                            status_code=ERROR_DIC[constant.ERROR_DATA_NOT_EXIST][0])

    qna.answer = request.answer

    response.result_data = {
        'qna': qna_detail_schema.dump(qna)
    }
    return response