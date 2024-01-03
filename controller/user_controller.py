from fastapi import HTTPException

from database.models import *
from database.schema import *
from config.jwt_handler import JWT
from config.constant import ERROR_DIC
from database.base_model import DefaultModel


def post_user_join(request, session):
    response = DefaultModel()

    type = request.type
    login_id = request.login_id
    password = request.password
    name = request.name
    nickname = request.nickname
    phone = request.phone
    email = request.email

    user = session.query(User).filter(User.login_id == login_id,
                                      User.status == constant.STATUS_ACTIVE).first()
    if user is not None:
        raise HTTPException(detail=ERROR_DIC[constant.ERROR_USER_EXIST][1],
                            status_code=ERROR_DIC[constant.ERROR_USER_EXIST][0])

    user = User()
    session.add(user)
    session.flush()

    user.type = type
    user.login_id = login_id
    user._password = password
    user.name = name
    user.nickname = nickname
    user.phone = phone
    user.email = email

    response.result_data = {
        'user': user_detail_schema.dump(user),
    }
    return response


def post_user_login(request, session):
    response = DefaultModel()

    login_id = request.login_id
    password = request.password

    user = session.query(User).filter(User.login_id == login_id,
                                      User.status == constant.STATUS_ACTIVE).first()
    if user is None:
        raise HTTPException(detail=ERROR_DIC[constant.ERROR_DATA_NOT_EXIST][1],
                            status_code=ERROR_DIC[constant.ERROR_DATA_NOT_EXIST][0])

    if user._password != password:
        raise HTTPException(detail=ERROR_DIC[constant.ERROR_DOESNT_MATCH_ID_OR_PASSWORD][1],
                            status_code=ERROR_DIC[constant.ERROR_DOESNT_MATCH_ID_OR_PASSWORD][0])

    payload = {
        'user': jwt_payload_schema.dump(user)
    }

    jwt = JWT()
    access_token = jwt.create_access_token(payload)
    refresh_token = jwt.create_refresh_token(payload)

    user.access_token = access_token
    user.refresh_token = refresh_token
    user.last_login_date = datetime.now()

    response.result_data = {
        'access_token': access_token,
        'refresh_token': refresh_token
    }
    return response


def post_user_logout(session, request, response_cookie):
    response = DefaultModel()

    user = session.query(User).filter(User.refresh_token == request.cookies.get('refresh_token'),
                                      User.status == constant.STATUS_ACTIVE).first()

    user.refresh_token = None

    response_cookie.delete_cookie('access_token')
    response_cookie.delete_cookie('refresh_token')
    return response


def get_user(session, type, g):
    response = DefaultModel()

    filter_list = []
    if type is not None:
        filter_list.append(User.type == type)

    users = session.query(User).filter(User.status == constant.STATUS_ACTIVE,
                                       *filter_list).all()
    response.result_data = {
        'users': user_list_schema.dump(users)
    }
    return response