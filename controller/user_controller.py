import os

from PIL import Image
from io import BytesIO
from fastapi import HTTPException, UploadFile

from database.models import *
from database.schema import *
from config.jwt_handler import JWT
from config.constant import ERROR_DIC
from config.s3 import upload_file_async
from database.base_model import DefaultModel


def post_user_join(request, session):
    response = DefaultModel()

    type = request.type
    login_id = request.login_id
    password = request.password
    name = request.name
    phone = request.phone
    email = request.email
    short_introduction = request.short_introduction
    introduction = request.introduction

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
    user.phone = phone
    user.email = email
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

        # if os.path.isfile(f'{upload_dir}{filename}.{extension}'):
        #     os.remove(f'{upload_dir}{filename}.{extension}')
        #
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
