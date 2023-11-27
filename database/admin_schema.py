from datetime import date, timedelta, datetime
from marshmallow import Schema, fields


class JWTPayloadSchema(Schema):
    id = fields.Int()


jwt_payload_schema = JWTPayloadSchema(many=False)


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
    name = fields.String()
    phone = fields.String()
    login_id = fields.String()
    email = fields.String()
    last_login_date = fields.DateTime('%Y-%m-%d %H:%M:%S')


user_detail_schema = UserDetailSchema(many=False)


class ProductListSchema(Schema):
    id = fields.Int()
    status = fields.Int()
    title = fields.String()
    description = fields.String()
    created_at = fields.DateTime('%Y-%m-%d %H:%M:%S')
    updated_at = fields.DateTime('%Y-%m-%d %H:%M:%S')


product_list_schema = ProductListSchema(many=True)


class ProductDetailSchema(Schema):
    id = fields.Int()
    status = fields.Int()
    title = fields.String()
    description = fields.String()
    created_at = fields.DateTime('%Y-%m-%d %H:%M:%S')
    updated_at = fields.DateTime('%Y-%m-%d %H:%M:%S')


product_detail_schema = ProductDetailSchema(many=False)


class TicketListSchema(Schema):
    id = fields.Int()
    status = fields.Int()
    cost = fields.Int()
    price = fields.Int()
    title = fields.String()
    description = fields.String()
    created_at = fields.DateTime('%Y-%m-%d %H:%M:%S')
    updated_at = fields.DateTime('%Y-%m-%d %H:%M:%S')


ticket_list_schema = TicketListSchema(many=True)


class TicketDetailSchema(Schema):
    id = fields.Int()
    status = fields.Int()
    cost = fields.Int()
    price = fields.Int()
    title = fields.String()
    description = fields.String()
    created_at = fields.DateTime('%Y-%m-%d %H:%M:%S')
    updated_at = fields.DateTime('%Y-%m-%d %H:%M:%S')


ticket_detail_schema = TicketDetailSchema(many=False)


class QnaListSchema(Schema):
    id = fields.Int()
    status = fields.Int()
    is_reply = fields.Int()
    user_id = fields.Int()
    product_id = fields.Int()
    question = fields.String()
    created_at = fields.DateTime('%Y-%m-%d %H:%M:%S')
    updated_at = fields.DateTime('%Y-%m-%d %H:%M:%S')


qna_list_schema = QnaListSchema(many=True)


class QnaDetailSchema(Schema):
    id = fields.Int()
    status = fields.Int()
    is_reply = fields.Int()
    user_id = fields.Int()
    product_id = fields.Int()
    question = fields.String()
    answer = fields.String()
    created_at = fields.DateTime('%Y-%m-%d %H:%M:%S')
    updated_at = fields.DateTime('%Y-%m-%d %H:%M:%S')


qna_detail_schema = QnaDetailSchema(many=False)


class ReviewListSchema(Schema):
    id = fields.Int()
    status = fields.Int()
    is_best = fields.Int()
    satisfaction = fields.Int()
    user_id = fields.Int()
    product_id = fields.Int()
    title = fields.String()
    created_at = fields.DateTime('%Y-%m-%d %H:%M:%S')
    updated_at = fields.DateTime('%Y-%m-%d %H:%M:%S')


review_list_schema = ReviewListSchema(many=True)


class ReviewDetailSchema(Schema):
    id = fields.Int()
    status = fields.Int()
    is_best = fields.Int()
    satisfaction = fields.Int()
    user_id = fields.Int()
    product_id = fields.Int()
    title = fields.String()
    description = fields.String()
    created_at = fields.DateTime('%Y-%m-%d %H:%M:%S')
    updated_at = fields.DateTime('%Y-%m-%d %H:%M:%S')


review_detail_schema = ReviewDetailSchema(many=False)