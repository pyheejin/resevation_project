from datetime import date, timedelta, datetime
from marshmallow import Schema, fields

from database.models import *
from database.database import *


class LoginSchema(Schema):
    id = fields.Int()
    status = fields.Int()
    type = fields.Int()
    name = fields.String()
    phone = fields.String()
    login_id = fields.String()
    email = fields.String()


login_schema = LoginSchema(many=False)


class UserDetailSchema(Schema):
    id = fields.Int()
    status = fields.Int()
    type = fields.Int()
    login_count = fields.Int()
    point = fields.Int()
    name = fields.String()
    phone = fields.String()
    login_id = fields.String()
    email = fields.String()
    last_login_date = fields.DateTime('%Y-%m-%d %H:%M:%S')


user_detail_schema = UserDetailSchema(many=False)


class LecturerSchema(Schema):
    id = fields.Int()
    status = fields.Int()
    lecture_count = fields.Int()
    total_lecture_price = fields.Method('get_total_lecture_price')
    image_url = fields.String()
    login_id = fields.String()
    name = fields.String()
    nickname = fields.String()
    position = fields.String()
    created_at = fields.DateTime('%Y.%m.%d(%H:%M:%S)')
    updated_at = fields.DateTime('%Y.%m.%d(%H:%M:%S)')
    # category = fields.Method('get_category')

    @classmethod
    def get_total_lecture_price(cls, obj):
        if obj.total_lecture_price is not None:
            return f'{obj.total_lecture_price:,}'
        else:
            return str(0)

    # @classmethod
    # def get_category(cls, obj):
    #     session = next(get_db())
    #     try:
    #         if obj.category_ids is not None:
    #             category_ids = list(map(int, obj.category_ids.split(',')))
    #             categories = session.query(Category).filter(Category.id.in_(category_ids)).all()
    #             return categories_name_schema.dump(categories)
    #         else:
    #             return None
    #     finally:
    #         session.close()


lecturers_schema = LecturerSchema(many=True)