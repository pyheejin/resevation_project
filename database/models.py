import cryptocode

from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import Column, ForeignKey, Integer, String, Text, DateTime

from database.database import Base
from config import constant, config


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True)
    status = Column(Integer, default=constant.STATUS_ACTIVE, comment='1:활성화, 0:비 활성화, -1:삭제')
    type = Column(Integer, default=constant.USER_TYPE_CUSTOMER, comment='1:일반 유저, 50:강사, 99:관리자')
    login_id = Column(String(45), comment='아이디')
    password = Column(String(255), comment='비밀번호')
    name = Column(String(45), comment='이름')
    email = Column(String(45), comment='이메일')
    phone = Column(String(45), comment='전화 번호')
    short_introduction = Column(String(45), comment='한 줄 소개')
    introduction = Column(Text, comment='자기소개')
    image_url = Column(String(255), comment='프로필 이미지')
    last_login_date = Column(DateTime, comment='최종 방문일')
    access_token = Column(Text, comment='Access Token')
    refresh_token = Column(Text, comment='Refresh Token')
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    user_ticket = relationship('UserTicket', back_populates='user')
    qna_user = relationship('Qna', back_populates='user')
    review_user = relationship('Review', back_populates='user')

    # 부분 암호화
    @hybrid_property
    def _password(self):
        return cryptocode.decrypt(self.password, config.KEY)

    @_password.setter
    def _password(self, value):
        self.password = cryptocode.encrypt(value, config.KEY)


class Course(Base):
    __tablename__ = 'course'

    id = Column(Integer, primary_key=True, index=True)
    status = Column(Integer, default=constant.STATUS_ACTIVE, comment='1:활성화, 0:비 활성화, -1:삭제')
    user_id = Column(Integer, ForeignKey('user.id'), comment='user id')
    title = Column(String(45), comment='제목')
    description = Column(Text, comment='내용')
    count = Column(Integer, comment='수업 회차')
    last_course_date = Column(DateTime, comment='마지막 수업일')
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    user = relationship('User')
    ticket = relationship('UserTicket', back_populates='course')
    qna_course = relationship('Qna', back_populates='course')
    review_course = relationship('Review', back_populates='course', uselist=False)
    course_detail = relationship('CourseDetail', back_populates='course')


class CourseDetail(Base):
    __tablename__ = 'course_detail'

    id = Column(Integer, primary_key=True, index=True)
    status = Column(Integer, default=constant.STATUS_ACTIVE, comment='1:활성화, 0:비 활성화, -1:삭제')
    course_id = Column(Integer, ForeignKey('course.id'), comment='course id')
    title = Column(String(45), comment='제목')
    course_date = Column(DateTime, comment='수업일')
    address = Column(String(45), comment='연습실 주소')
    address_detail = Column(String(45), comment='연습실 상세 주소')
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    course = relationship('Course', back_populates='course_detail')


class Ticket(Base):
    __tablename__ = 'ticket'

    id = Column(Integer, primary_key=True, index=True)
    status = Column(Integer, default=constant.STATUS_ACTIVE, comment='1:활성화, 0:비 활성화, -1:삭제')
    user_id = Column(Integer, ForeignKey('user.id'), comment='user id')
    count = Column(Integer, comment='회차')
    cost = Column(Integer, default=0, comment='원가')
    price = Column(Integer, default=0, comment='판매가')
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    user = relationship('User')
    user_ticket = relationship('UserTicket', back_populates='ticket')


class UserTicket(Base):
    __tablename__ = 'user_ticket'

    id = Column(Integer, primary_key=True, index=True)
    status = Column(Integer, default=constant.STATUS_ACTIVE, comment='1:사용, 0:미사용, -1:삭제')
    user_id = Column(Integer, ForeignKey('user.id'), comment='user id')
    ticket_id = Column(Integer, ForeignKey('ticket.id'), comment='ticket id')
    course_id = Column(Integer, ForeignKey('course.id'), comment='course id')
    remain_count = Column(Integer, comment='잔여 회차')
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    user = relationship('User', back_populates='user_ticket')
    ticket = relationship('Ticket', back_populates='user_ticket')
    course = relationship('Course', back_populates='ticket')


class Payment(Base):
    __tablename__ = 'payment'

    id = Column(Integer, primary_key=True, index=True)
    status = Column(Integer, default=constant.STATUS_ACTIVE, comment='1:활성화, 0:비 활성화, -1:삭제')
    user_id = Column(Integer, ForeignKey('user.id'), comment='user id')
    ticket_id = Column(Integer, ForeignKey('ticket.id'), comment='ticket id')
    data = Column(Text, comment='결제 데이터')
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    user = relationship('User')
    ticket = relationship('Ticket')


class Review(Base):
    __tablename__ = 'review'

    id = Column(Integer, primary_key=True, index=True)
    status = Column(Integer, default=constant.STATUS_ACTIVE, comment='1:활성화, 0:비 활성화, -1:삭제')
    is_best = Column(Integer, default=constant.STATUS_INACTIVE, comment='1:베스트 리뷰')
    satisfaction = Column(Integer, default=constant.STATUS_INACTIVE, comment='만족도')
    user_id = Column(Integer, ForeignKey('user.id'), comment='user id')
    course_id = Column(Integer, ForeignKey('course.id'), comment='course id')
    title = Column(String(45), comment='제목')
    description = Column(Text, comment='내용')
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    user = relationship('User', back_populates='review_user')
    course = relationship('Course', back_populates='review_course')


class Qna(Base):
    __tablename__ = 'qna'

    id = Column(Integer, primary_key=True, index=True)
    status = Column(Integer, default=constant.STATUS_ACTIVE, comment='1:활성화, 0:비 활성화, -1:삭제')
    is_reply = Column(Integer, default=constant.STATUS_INACTIVE, comment='1:답변완료')
    user_id = Column(Integer, ForeignKey('user.id'), comment='user id')
    course_id = Column(Integer, ForeignKey('course.id'), comment='course id')
    question = Column(Text, comment='문의 내용')
    answer = Column(Text, comment='답변')
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    user = relationship('User', back_populates='qna_user')
    course = relationship('Course', back_populates='qna_course')