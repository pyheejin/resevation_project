from fastapi import HTTPException

from database.models import *
from database.schema import *
from config.jwt_handler import JWT
from config.constant import ERROR_DIC
from database.base_model import DefaultModel


def post_user_join(request, session):
    response = DefaultModel()

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
    user.login_id = login_id
    user._password = password
    user.name = name
    user.nickname = nickname
    user.phone = phone
    user.email = email
    session.add(user)

    response.result_data = {
        'user': user_detail_schema.dump(user),
    }
    return response


def post_user_login(request, session, response_cookie):
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

    # 로그인 성공 시 토큰 발급
    payload = {
        'user': login_schema.dump(user)
    }

    jwt = JWT()

    # 쿠키 유효시간
    refresh_expires = (datetime.now() + timedelta(minutes=10)).strftime('%Y-%m-%d %T')

    access_token = jwt.create_access_token(payload)
    refresh_token = jwt.create_refresh_token(payload)

    user.access_token = access_token
    user.refresh_token = refresh_token
    user.last_login_date = datetime.now()

    # 리프레시 토큰 업뎃
    response_cookie.set_cookie(key='refresh_token',
                               value=refresh_token,
                               httponly=True,
                               expires=refresh_expires)

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


def get_user(session, g):
    response = DefaultModel()

    users = session.query(User).filter(User.status == constant.STATUS_ACTIVE).all()
    response.result_data = user_list_schema.dump(users)
    return response