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


class UserListSchema(Schema):
    id = fields.Int()
    name = fields.String()


user_list_schema = UserListSchema(many=True)


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


class ProductListSchema(Schema):
    id = fields.Int()
    status = fields.Int()
    is_option = fields.Int()
    name = fields.String()
    description = fields.String()
    price = fields.Int()
    discount_rate = fields.Int()
    discount_price = fields.Int()
    created_at = fields.DateTime('%Y-%m-%d %H:%M:%S')
    updated_at = fields.DateTime('%Y-%m-%d %H:%M:%S')


product_list_schema = ProductListSchema(many=True)


class ProductDetailSchema(Schema):
    id = fields.Int()
    status = fields.Int()
    is_option = fields.Int()
    name = fields.String()
    description = fields.String()
    price = fields.Int()
    discount_rate = fields.Int()
    discount_price = fields.Int()
    created_at = fields.DateTime('%Y-%m-%d %H:%M:%S')
    updated_at = fields.DateTime('%Y-%m-%d %H:%M:%S')


product_detail_schema = ProductDetailSchema(many=False)