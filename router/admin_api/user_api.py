from pydantic import BaseModel
from typing import Optional, List
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, APIRouter, Request, Form, File, UploadFile

from config import common, constant
from database import base_model
from database.database import *
from database.models import User
from admin_controller import user_controller


router = APIRouter(
    prefix='/user',
)


class PostUserJoinModel(BaseModel):
    login_id: str
    password: str
    name: str
    nickname: Optional[str]
    email: str
    phone: str
    short_introduction: Optional[str]
    introduction: Optional[str]
    image_file: Optional[UploadFile] = File(None)

    @classmethod
    def as_form(cls,
                login_id: str = Form(),
                password: str = Form(),
                name: str = Form(),
                nickname: Optional[str] = Form(None),
                email: str = Form(),
                phone: str = Form(),
                short_introduction: Optional[str] = Form(None),
                introduction: Optional[str] = Form(None),
                image_file: Optional[UploadFile] = File(None)):
        return cls(login_id=login_id,
                   password=password,
                   name=name,
                   nickname=nickname,
                   email=email,
                   phone=phone,
                   short_introduction=short_introduction,
                   introduction=introduction,
                   image_file=image_file)


class PostUserLoginModel(BaseModel):
    login_id: str = 'admin'
    password: str = 'admin'


class PutUserProfileModel(BaseModel):
    name: Optional[str]
    nickname: Optional[str]
    short_introduction: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    introduction: Optional[str]
    image_file: Optional[UploadFile] = File(None)

    @classmethod
    def as_form(cls,
                name: Optional[str] = Form(None),
                nickname: Optional[str] = Form(None),
                short_introduction: Optional[str] = Form(None),
                email: Optional[str] = Form(None),
                phone: Optional[str] = Form(None),
                introduction: Optional[str] = Form(None),
                image_file: Optional[UploadFile] = File(None)):
        return cls(name=name,
                   nickname=nickname,
                   short_introduction=short_introduction,
                   email=email,
                   phone=phone,
                   introduction=introduction,
                   image_file=image_file)


class PostUserTicketCourseModel(BaseModel):
    user_ticket_id: int
    course_id: int


@router.post('/join', tags=['user'], summary='유저 회원가입')
def post_user_join(request: PostUserJoinModel = Depends(PostUserJoinModel.as_form),
                   session: Session = Depends(get_db)):
    result_msg = '유저 회원가입'
    try:
        response = user_controller.post_user_join(request=request,
                                                  session=session)
        response.result_msg = f'{response.result_msg}'
    except HTTPException as e:
        print(e.detail)

        session.rollback()

        response = base_model.DefaultModel()
        common.error_response(response, e.detail, f'{result_msg} 실패')
    except Exception as e:
        print(e.args[0])

        session.rollback()

        response = base_model.DefaultModel()
        common.error_response(response, e.args[0], f'{result_msg} 실패')
    else:
        if response is None:
            response = base_model.DefaultModel()
        if response.result_msg is not None:
            response.result_msg = result_msg + ' 성공'
    finally:
        session.commit()
    return response


@router.post('/login', tags=['user'], summary='유저 로그인')
def post_user_login(request: PostUserLoginModel,
                    session: Session = Depends(get_db)):
    result_msg = '유저 로그인'
    try:
        response = user_controller.post_user_login(request=request,
                                                   session=session)
        response.result_msg = f'{response.result_msg}'
    except HTTPException as e:
        print(e.detail)

        session.rollback()

        response = base_model.DefaultModel()
        common.error_response(response, e.detail, f'{result_msg} 실패')
    except Exception as e:
        print(e.args[0])

        session.rollback()

        response = base_model.DefaultModel()
        common.error_response(response, e.args[0], f'{result_msg} 실패')
    else:
        if response is None:
            response = base_model.DefaultModel()
        if response.result_msg is not None:
            response.result_msg = result_msg + ' 성공'
    finally:
        session.commit()
    return response


@router.put('/profile', tags=['user'], summary='프로필 수정', dependencies=[Depends(common.get_access_token)])
def put_user_profile(request: PutUserProfileModel = Depends(PutUserProfileModel.as_form),
                     g: User = Depends(common.get_access_token),
                     session: Session = Depends(get_db)):
    result_msg = '프로필 수정'
    try:
        response = user_controller.put_user_profile(request=request,
                                                    g=g,
                                                    session=session)
        response.result_msg = f'{response.result_msg}'
    except HTTPException as e:
        print(e.detail)

        session.rollback()

        response = base_model.DefaultModel()
        common.error_response(response, e.detail, f'{result_msg} 실패')
    except Exception as e:
        print(e.args[0])

        session.rollback()

        response = base_model.DefaultModel()
        common.error_response(response, e.args[0], f'{result_msg} 실패')
    else:
        if response is None:
            response = base_model.DefaultModel()
        if response.result_msg is not None:
            response.result_msg = result_msg + ' 성공'
    finally:
        session.commit()
    return response


@router.post('/ticket-course', tags=['user'], summary='티켓 수업 연결')
def post_user_ticket_course(request: PostUserTicketCourseModel,
                            session: Session = Depends(get_db),
                            g: User = Depends(common.get_access_token)):
    result_msg = '티켓 수업 연결'
    try:
        response = user_controller.post_user_ticket_course(request=request,
                                                           session=session,
                                                           g=g)
        response.result_msg = f'{response.result_msg}'
    except HTTPException as e:
        print(e.detail)

        session.rollback()

        response = base_model.DefaultModel()
        common.error_response(response, e.detail, f'{result_msg} 실패')
    except Exception as e:
        print(e.args[0])

        session.rollback()

        response = base_model.DefaultModel()
        common.error_response(response, e.args[0], f'{result_msg} 실패')
    else:
        if response is None:
            response = base_model.DefaultModel()
        if response.result_msg is not None:
            response.result_msg = result_msg + ' 성공'
    finally:
        session.commit()
    return response


@router.get('/excel', tags=['user'], summary='유저 내려받기', dependencies=[Depends(common.get_access_token)])
def get_user_excel(session: Session = Depends(get_db),
                   g: User = Depends(common.get_access_token),
                   user_name: Optional[str] = None,
                   course_name: Optional[str] = None):
    result_msg = '유저 내려받기'
    try:
        response = user_controller.get_user_excel(session=session,
                                                  g=g,
                                                  user_name=user_name,
                                                  course_name=course_name)
        response.result_msg = f'{response.result_msg}'
    except HTTPException as e:
        print(e.detail)

        session.rollback()

        response = base_model.DefaultModel()
        common.error_response(response, e.detail, f'{result_msg} 실패')
    except Exception as e:
        print(e.args[0])

        session.rollback()

        response = base_model.DefaultModel()
        common.error_response(response, e.args[0], f'{result_msg} 실패')
    else:
        if response is None:
            response = base_model.DefaultModel()
        if response.result_msg is not None:
            response.result_msg = result_msg + ' 성공'
    finally:
        session.commit()
    return response


@router.get('', tags=['user'], summary='유저 목록', dependencies=[Depends(common.get_access_token)])
def get_user(session: Session = Depends(get_db),
             g: User = Depends(common.get_access_token),
             user_name: Optional[str] = None,
             course_name: Optional[str] = None,
             page: Optional[int] = constant.DEFAULT_PAGE,
             page_size: Optional[int] = constant.DEFAULT_PAGE_SIZE):
    result_msg = '유저 목록'
    try:
        response = user_controller.get_user(session=session,
                                            g=g,
                                            user_name=user_name,
                                            course_name=course_name,
                                            page=page,
                                            page_size=page_size)
        response.result_msg = f'{response.result_msg}'
    except HTTPException as e:
        print(e.detail)

        session.rollback()

        response = base_model.DefaultModel()
        common.error_response(response, e.detail, f'{result_msg} 실패')
    except Exception as e:
        print(e.args[0])

        session.rollback()

        response = base_model.DefaultModel()
        common.error_response(response, e.args[0], f'{result_msg} 실패')
    else:
        if response is None:
            response = base_model.DefaultModel()
        if response.result_msg is not None:
            response.result_msg = result_msg + ' 성공'
    finally:
        session.commit()
    return response


@router.get('/{user_id}', tags=['user'], summary='유저 상세', dependencies=[Depends(common.get_access_token)])
def get_user_detail(user_id: int,
                    g: User = Depends(common.get_access_token),
                    session: Session = Depends(get_db)):
    result_msg = '유저 상세'
    try:
        response = user_controller.get_user_detail(user_id=user_id,
                                                   g=g,
                                                   session=session)
        response.result_msg = f'{response.result_msg}'
    except HTTPException as e:
        print(e.detail)

        session.rollback()

        response = base_model.DefaultModel()
        common.error_response(response, e.detail, f'{result_msg} 실패')
    except Exception as e:
        print(e.args[0])

        session.rollback()

        response = base_model.DefaultModel()
        common.error_response(response, e.args[0], f'{result_msg} 실패')
    else:
        if response is None:
            response = base_model.DefaultModel()
        if response.result_msg is not None:
            response.result_msg = result_msg + ' 성공'
    finally:
        session.commit()
    return response


@router.delete('/{user_id}', tags=['user'], summary='유저 삭제', dependencies=[Depends(common.get_access_token)])
def delete_user_detail(user_id: int,
                       session: Session = Depends(get_db)):
    result_msg = '유저 삭제'
    try:
        response = user_controller.delete_user_detail(user_id=user_id,
                                                      session=session)
        response.result_msg = f'{response.result_msg}'
    except HTTPException as e:
        print(e.detail)

        session.rollback()

        response = base_model.DefaultModel()
        common.error_response(response, e.detail, f'{result_msg} 실패')
    except Exception as e:
        print(e.args[0])

        session.rollback()

        response = base_model.DefaultModel()
        common.error_response(response, e.args[0], f'{result_msg} 실패')
    else:
        if response is None:
            response = base_model.DefaultModel()
        if response.result_msg is not None:
            response.result_msg = result_msg + ' 성공'
    finally:
        session.commit()
    return response