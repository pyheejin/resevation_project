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
    type = Column(Integer, default=constant.USER_TYPE_CUSTOMER, comment='1:일반 유저, 50:판매자, 99:관리자')
    login_id = Column(String(45), comment='아이디')
    password = Column(String(255), comment='비밀번호')
    name = Column(String(45), comment='이름')
    nickname = Column(String(45), comment='닉네임')
    phone = Column(String(45), comment='전화 번호')
    email = Column(String(45), comment='이메일')
    last_login_date = Column(DateTime, comment='최종 방문일')
    access_token = Column(Text, comment='Access Token')
    refresh_token = Column(Text, comment='Refresh Token')
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    # 부분 암호화
    @hybrid_property
    def _password(self):
        return cryptocode.decrypt(self.password, config.KEY)

    @_password.setter
    def _password(self, value):
        self.password = cryptocode.encrypt(value, config.KEY)


class Product(Base):
    __tablename__ = 'product'

    id = Column(Integer, primary_key=True, index=True)
    status = Column(Integer, default=constant.STATUS_ACTIVE, comment='1:활성화, 0:비 활성화, -1:삭제')
    user_id = Column(Integer, ForeignKey('user.id'), comment='user id')
    title = Column(String(45), comment='제목')
    description = Column(Text, comment='내용')
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    user = relationship('User')


class Ticket(Base):
    __tablename__ = 'ticket'

    id = Column(Integer, primary_key=True, index=True)
    status = Column(Integer, default=constant.STATUS_ACTIVE, comment='1:활성화, 0:비 활성화, -1:삭제')
    user_id = Column(Integer, ForeignKey('user.id'), comment='user id')
    title = Column(String(45), comment='제목')
    description = Column(Text, comment='내용')
    cost = Column(Integer, default=0, comment='원가')
    price = Column(Integer, default=0, comment='판매가')
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    user = relationship('User')


class TicketProduct(Base):
    __tablename__ = 'ticket_product'

    id = Column(Integer, primary_key=True, index=True)
    status = Column(Integer, default=constant.STATUS_ACTIVE, comment='1:활성화, 0:비 활성화, -1:삭제')
    user_id = Column(Integer, ForeignKey('user.id'), comment='user id')
    ticket_id = Column(Integer, ForeignKey('ticket.id'), comment='ticket id')
    product_id = Column(Integer, ForeignKey('product.id'), comment='product id')
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    user = relationship('User')
    ticket = relationship('Ticket')
    product = relationship('Product')


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
    product_id = Column(Integer, ForeignKey('product.id'), comment='product id')
    title = Column(String(45), comment='제목')
    description = Column(Text, comment='내용')
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    product = relationship('Product')


class Qna(Base):
    __tablename__ = 'qna'

    id = Column(Integer, primary_key=True, index=True)
    status = Column(Integer, default=constant.STATUS_ACTIVE, comment='1:활성화, 0:비 활성화, -1:삭제')
    is_reply = Column(Integer, default=constant.STATUS_INACTIVE, comment='1:답변완료')
    user_id = Column(Integer, ForeignKey('user.id'), comment='user id')
    product_id = Column(Integer, ForeignKey('product.id'), comment='product id')
    question = Column(Text, comment='문의 내용')
    answer = Column(Text, comment='답변')
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    user = relationship('User')
    product = relationship('Product')