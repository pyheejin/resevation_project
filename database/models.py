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
    login_count = Column(Integer, default=0, comment='방문 횟수')
    last_login_date = Column(DateTime, comment='최종 방문일')
    total_amount = Column(Integer, default=0, comment='총 구매 금액')
    last_paid_at = Column(DateTime, comment='최종 결제일')
    point = Column(Integer, default=0, comment='보유 적립금')
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


class Business(Base):
    __tablename__ = 'business'

    id = Column(Integer, primary_key=True, index=True)
    status = Column(Integer, default=constant.STATUS_ACTIVE, comment='1:활성화, 0:비 활성화, -1:삭제')
    user_id = Column(Integer, ForeignKey('user.id'), comment='user id')
    name = Column(String(45), comment='이름')
    email = Column(String(45), comment='이메일')
    description = Column(String(45), comment='소개')
    company_name = Column(String(45), comment='상호명')
    representative_name = Column(String(45), comment='대표자명')
    cs_number = Column(String(45), comment='고객센터 번호')
    identity = Column(String(45), comment='사업자등록번호')
    zip_code = Column(String(45), comment='우편번호')
    address = Column(String(45), comment='사업장 소재지')
    address_detail = Column(String(45), comment='사업장 소재지')
    image_url = Column(String(255), comment='logo image url')
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    user = relationship('User')


class Product(Base):
    __tablename__ = 'product'

    id = Column(Integer, primary_key=True, index=True)
    status = Column(Integer, default=constant.STATUS_ACTIVE, comment='1:활성화, 0:비 활성화, -1:삭제')
    user_id = Column(Integer, ForeignKey('user.id'), comment='user id')
    is_option = Column(Integer, default=constant.STATUS_ACTIVE, comment='옵션 여부')
    name = Column(String(45), comment='이름')
    description = Column(String(45), comment='소개')
    price = Column(Integer, default=constant.STATUS_INACTIVE, comment='원가')
    discount_rate = Column(Integer, default=constant.STATUS_INACTIVE, comment='할인률')
    discount_price = Column(Integer, default=constant.STATUS_INACTIVE, comment='할인가')
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    user = relationship('User')
    product_images = relationship('ProductImage', back_populates='product')
    product_options = relationship('ProductOption', back_populates='product')


class ProductOption(Base):
    __tablename__ = 'product_option'

    id = Column(Integer, primary_key=True, index=True)
    status = Column(Integer, default=constant.STATUS_ACTIVE, comment='1:활성화, 0:비 활성화, -1:삭제')
    product_id = Column(Integer, ForeignKey('product.id'), comment='product id')
    name = Column(String(45), comment='이름')
    description = Column(Text, comment='소개')
    price = Column(Integer, default=constant.STATUS_INACTIVE, comment='원가')
    discount_rate = Column(Integer, default=constant.STATUS_INACTIVE, comment='할인률')
    discount_price = Column(Integer, default=constant.STATUS_INACTIVE, comment='할인가')
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    product = relationship('Product', back_populates='product_options')


class ProductImage(Base):
    __tablename__ = 'product_image'

    id = Column(Integer, primary_key=True, index=True)
    status = Column(Integer, default=constant.STATUS_ACTIVE, comment='1:활성화, 0:비 활성화, -1:삭제')
    product_id = Column(Integer, ForeignKey('product.id'), comment='product id')
    image_url = Column(String(255), comment='image url')
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    product = relationship('Product', back_populates='product_images')


class Review(Base):
    __tablename__ = 'review'

    id = Column(Integer, primary_key=True, index=True)
    status = Column(Integer, default=constant.STATUS_ACTIVE, comment='1:활성화, 0:비 활성화, -1:삭제')
    product_id = Column(Integer, ForeignKey('product.id'), comment='product id')
    satisfaction = Column(Integer, default=constant.STATUS_INACTIVE, comment='만족도')
    description = Column(Text, comment='소개')
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    product = relationship('Product')


class ReviewImage(Base):
    __tablename__ = 'review_image'

    id = Column(Integer, primary_key=True, index=True)
    status = Column(Integer, default=constant.STATUS_ACTIVE, comment='1:활성화, 0:비 활성화, -1:삭제')
    review_id = Column(Integer, ForeignKey('review.id'), comment='review id')
    image_url = Column(String(255), comment='image url')
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    review = relationship('Review')


class Qna(Base):
    __tablename__ = 'qna'

    id = Column(Integer, primary_key=True, index=True)
    status = Column(Integer, default=constant.STATUS_ACTIVE, comment='1:활성화, 0:비 활성화, -1:삭제')
    is_show = Column(Integer, default=constant.STATUS_ACTIVE, comment='공개 여부')
    user_id = Column(Integer, ForeignKey('user.id'), comment='user id')
    product_id = Column(Integer, ForeignKey('product.id'), comment='product id')
    question = Column(Text, comment='문의 내용')
    answer = Column(Text, comment='답변')
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    user = relationship('User')
    product = relationship('Product')