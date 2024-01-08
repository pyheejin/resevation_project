import os

from PIL import Image
from io import BytesIO
from openpyxl import Workbook
from sqlalchemy import and_, or_
from sqlalchemy.orm import contains_eager
from fastapi import HTTPException, UploadFile

from database.models import *
from config.jwt_handler import JWT
from database.admin_schema import *
from config.constant import ERROR_DIC
from config.s3 import upload_file_async
from database.base_model import DefaultModel


def post_user_join(request, session):
    response = DefaultModel()

    login_id = request.login_id
    password = request.password
    name = request.name
    nickname = request.nickname
    email = request.email
    phone = request.phone
    short_introduction = request.short_introduction
    introduction = request.introduction

    # 아이디 중복 체크
    user = session.query(User).filter(User.login_id == login_id,
                                      User.status == constant.STATUS_ACTIVE).first()
    if user is not None:
        raise HTTPException(detail=ERROR_DIC[constant.ERROR_USER_EXIST][1],
                            status_code=ERROR_DIC[constant.ERROR_USER_EXIST][0])

    user = User()
    session.add(user)
    session.flush()

    user.type = constant.USER_TYPE_SELLER
    user.login_id = login_id
    user._password = password
    user.name = name
    user.nickname = nickname
    user.email = email
    user.phone = phone
    user.short_introduction = short_introduction
    user.introduction = introduction

    # 프로필 이미지
    if request.image_file is not None:
        image = request.image_file

        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        upload_dir = os.path.join(base_dir, 'static/image/user/')
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir, exist_ok=True)

        file_data = image.filename.split('.')
        filename = f"user_profile_{user.id}_{file_data[0][:10]}"
        extension = 'jpeg'

        with open(os.path.join(upload_dir, f'{filename}.{extension}'), 'wb+') as file:
            file.write(image.file.read())
            file.close()

        img = Image.open(f'{upload_dir}{filename}.{extension}')
        img.save(f'{upload_dir}{filename}.{extension}', format=extension, quality=50)  # 압축률 50%
        img.close()

        image_url = f'{upload_dir}{filename}.{extension}'
        user.image_url = image_url

        # if os.path.isfile(f'{upload_dir}{filename}.{extension}'):
        #     os.remove(f'{upload_dir}{filename}.{extension}')

        # # aws에 이미지 업로드
        # img = Image.open(BytesIO(image.file.read()))
        #
        # image_data = BytesIO()
        # img.save(image_data, format=extension, quality=75)
        # image_data.seek(0)
        #
        # webp_upload_file = UploadFile(image_data, filename=filename)
        # file_path, image_url = upload_file_async(file=webp_upload_file,
        #                                          bucket_folder='user',
        #                                          extension=extension,
        #                                          object_name=filename)

    response.result_data = {
        'user': login_schema.dump(user)
    }
    return response


def post_user_login(request, session):
    response = DefaultModel()

    login_id = request.login_id
    password = request.password

    user = session.query(User).filter(User.login_id == login_id,
                                      User.type >= constant.USER_TYPE_SELLER,
                                      User.status == constant.STATUS_ACTIVE).first()
    if user is None:
        raise HTTPException(detail=ERROR_DIC[constant.ERROR_DATA_NOT_EXIST][1],
                            status_code=ERROR_DIC[constant.ERROR_DATA_NOT_EXIST][0])

    if user._password != password:
        raise HTTPException(detail=ERROR_DIC[constant.ERROR_DOESNT_MATCH_ID_OR_PASSWORD][1],
                            status_code=ERROR_DIC[constant.ERROR_DOESNT_MATCH_ID_OR_PASSWORD][0])

    # 로그인 성공 시 토큰 발급
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
        'user': login_schema.dump(user)
    }
    return response


def put_user_profile(request, g, session):
    response = DefaultModel()

    user_id = g.result_data.get('user', None).get('id', None)
    user = session.query(User).filter(User.id == user_id,
                                      User.status >= constant.STATUS_INACTIVE).first()
    if user is None:
        raise HTTPException(detail=ERROR_DIC[constant.ERROR_DATA_NOT_EXIST][1],
                            status_code=ERROR_DIC[constant.ERROR_DATA_NOT_EXIST][0])

    if request.name is not None:
        user.name = request.name

    if request.nickname is not None:
        user.nickname = request.nickname

    if request.short_introduction is not None:
        user.short_introduction = request.short_introduction

    if request.email is not None:
        user.email = request.email

    if request.phone is not None:
        user.phone = request.phone

    if request.introduction is not None:
        user.introduction = request.introduction

    # 프로필 이미지
    if request.image_file is not None:
        image = request.image_file

        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        upload_dir = os.path.join(base_dir, 'static/image/user/')
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir, exist_ok=True)

        file_data = image.filename.split('.')
        filename = f"user_{user.id}_profile_{file_data[0][:10]}"
        extension = 'jpeg'

        with open(os.path.join(upload_dir, f'{filename}.{extension}'), 'wb+') as file:
            file.write(image.file.read())
            file.close()

        img = Image.open(f'{upload_dir}{filename}.{extension}')
        img.save(f'{upload_dir}{filename}.{extension}', format=extension, quality=50)  # 압축률 50%
        img.close()

        image_url = f'{upload_dir}{filename}.{extension}'
        user.image_url = image_url

    response.result_data = {
        'user': user_profile_schema.dump(user)
    }
    return response


def post_user_ticket_course(request, session, g):
    response = DefaultModel()

    user_ticket = session.query(UserTicket).filter(UserTicket.id == request.user_ticket_id,
                                                   UserTicket.status >= constant.STATUS_INACTIVE).first()
    if user_ticket is None:
        raise HTTPException(detail=ERROR_DIC[constant.ERROR_DATA_NOT_EXIST][1],
                            status_code=ERROR_DIC[constant.ERROR_DATA_NOT_EXIST][0])

    course = session.query(Course).filter(Course.id == request.course_id,
                                          Course.status == constant.STATUS_ACTIVE).first()
    if course is None:
        raise HTTPException(detail=ERROR_DIC[constant.ERROR_DATA_NOT_EXIST][1],
                            status_code=ERROR_DIC[constant.ERROR_DATA_NOT_EXIST][0])

    user_id = g.result_data.get('user', None).get('id', None)
    if course.user_id != user_id:
        raise HTTPException(detail=ERROR_DIC[constant.ERROR_UNAUTHORIZED][1],
                            status_code=ERROR_DIC[constant.ERROR_UNAUTHORIZED][0])

    user_ticket.course_id = course.id
    user_ticket.remain_count -= 1
    return response


def get_user_excel(session, g, user_name, course_name):
    response = DefaultModel()

    filter_list = []
    if user_name is not None:
        filter_list.append(or_(User.name.like(f'%{user_name}%'),
                               User.nickname.like(f'%{user_name}%')))

    if course_name is not None:
        filter_list.append(Course.title.like(f'%{course_name}%'))

    user_id = g.result_data.get('user', None).get('id', None)
    user_query = session.query(UserTicket).outerjoin(User, User.id == UserTicket.user_id
                                        ).outerjoin(Course, Course.id == UserTicket.course_id
                                        ).outerjoin(Ticket, Ticket.id == UserTicket.ticket_id
                                        ).filter(Ticket.user_id == user_id,
                                                 Course.id is not None,
                                                 User.status >= constant.STATUS_INACTIVE,
                                        ).options(contains_eager(UserTicket.user),
                                                  contains_eager(UserTicket.ticket),
                                                  contains_eager(UserTicket.course))
    users = user_query.filter(*filter_list).all()

    # 엑셀파일 쓰기
    write_wb = Workbook()

    # Sheet1에다 입력
    write_ws = write_wb.active

    # 행 단위로 추가
    write_ws.append(['No', '수업명', '유저명', '수강권', '잔여회차', '구매일'])

    for idx, row in enumerate(users):
        if row.course is not None:
            course_title = row.course.title
        else:
            course_title = ''

        write_ws.append([idx+1, course_title, row.user.name, f'{row.ticket.count}회차 수강권', row.remain_count, row.created_at])

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    upload_dir = os.path.join(base_dir, 'download')
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir, exist_ok=True)

    path = f'{upload_dir}/{datetime.now().date()}.xlsx'
    write_wb.save(path)

    response.result_data = {
        'file_path': path
    }
    return response


def get_user(session, g, user_name, course_name, page, page_size):
    """
    로그인 한 강사의 티켓을 구매한 유저만 표시 되어야 함
    """
    response = DefaultModel()

    filter_list = []
    if user_name is not None:
        filter_list.append(or_(User.name.like(f'%{user_name}%'),
                               User.nickname.like(f'%{user_name}%')))

    if course_name is not None:
        filter_list.append(Course.title.like(f'%{course_name}%'))

    user_id = g.result_data.get('user', None).get('id', None)
    user_query = session.query(UserTicket).outerjoin(User, User.id == UserTicket.user_id
                                            ).outerjoin(Course, Course.id == UserTicket.course_id
                                            ).outerjoin(Ticket, Ticket.id == UserTicket.ticket_id
                                            ).filter(Ticket.user_id == user_id,
                                                     User.status >= constant.STATUS_INACTIVE,
                                            ).options(contains_eager(UserTicket.user),
                                                      contains_eager(UserTicket.ticket),
                                                      contains_eager(UserTicket.course))
    users = user_query.filter(*filter_list).offset(page_size * (page - 1)).limit(page_size).all()

    response.result_data = {
        'users': user_list_schema.dump(users)
    }
    return response


def get_user_detail(user_id, g, session):
    response = DefaultModel()

    login_user_id = g.result_data.get('user', None).get('id', None)
    user_query = session.query(User).outerjoin(UserTicket, and_(UserTicket.user_id == User.id,
                                                                UserTicket.user_id == user_id,
                                                                UserTicket.status >= constant.STATUS_INACTIVE)
                                    ).outerjoin(Ticket, Ticket.id == UserTicket.ticket_id
                                    ).outerjoin(Course, Course.id == UserTicket.course_id
                                    ).outerjoin(Review, and_(Review.course_id == Course.id,
                                                             Review.user_id == user_id,
                                                             Review.status == constant.STATUS_ACTIVE)
                                    ).filter(User.id == user_id,
                                             Ticket.user_id == login_user_id,
                                    ).options(contains_eager(User.user_ticket),
                                              contains_eager(User.user_ticket).contains_eager(UserTicket.ticket),
                                              contains_eager(User.user_ticket).contains_eager(UserTicket.course),
                                              contains_eager(User.user_ticket).contains_eager(UserTicket.course
                                                                                ).contains_eager(Course.review),
                                    ).all()
    if len(user_query) == 0:
        raise HTTPException(detail=ERROR_DIC[constant.ERROR_DATA_NOT_EXIST][1],
                            status_code=ERROR_DIC[constant.ERROR_DATA_NOT_EXIST][0])
    user = user_query[0]

    response.result_data = {
        'user': user_detail_schema.dump(user)
    }
    return response


def delete_user_detail(user_id, session):
    response = DefaultModel()

    user = session.query(User).filter(User.id == user_id,
                                      User.status >= constant.STATUS_INACTIVE).first()
    if user is None:
        raise HTTPException(detail=ERROR_DIC[constant.ERROR_DATA_NOT_EXIST][1],
                            status_code=ERROR_DIC[constant.ERROR_DATA_NOT_EXIST][0])

    user.status = constant.STATUS_DELETED
    return response