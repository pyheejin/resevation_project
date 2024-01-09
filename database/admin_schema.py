from datetime import date, timedelta, datetime
from marshmallow import Schema, fields


class JWTPayloadSchema(Schema):
    id = fields.Int()


jwt_payload_schema = JWTPayloadSchema(many=False)


class LoginSchema(Schema):
    id = fields.Int()
    status = fields.Int()
    type = fields.Int()
    login_id = fields.String()
    name = fields.String()
    email = fields.String()
    phone = fields.String()
    access_token = fields.String()
    refresh_token = fields.String()


login_schema = LoginSchema(many=False)


class UserProfileSchema(Schema):
    id = fields.Int()
    status = fields.Int()
    type = fields.Int()
    login_id = fields.String()
    name = fields.String()
    email = fields.String()
    phone = fields.String()
    short_introduction = fields.String()
    introduction = fields.String()
    last_login_date = fields.DateTime('%Y-%m-%d %H:%M:%S')


user_profile_schema = UserProfileSchema(many=False)


class CourseListSchema(Schema):
    id = fields.Int()
    status = fields.Int()
    count = fields.Int()
    title = fields.String()
    description = fields.String()
    last_course_date = fields.DateTime('%Y-%m-%d')
    created_at = fields.DateTime('%Y-%m-%d %H:%M:%S')


course_list_schema = CourseListSchema(many=True)


class CourseDetailSchema(Schema):
    id = fields.Int()
    course_id = fields.Int()
    title = fields.String()
    course_date = fields.DateTime('%Y-%m-%d %H:%M')
    address = fields.String()
    address_detail = fields.String()


course_detail_schema = CourseDetailSchema(many=True)


class CourseSchema(Schema):
    id = fields.Int()
    status = fields.Int()
    count = fields.Int()
    title = fields.String()
    description = fields.String()
    created_at = fields.DateTime('%Y-%m-%d %H:%M:%S')
    updated_at = fields.DateTime('%Y-%m-%d %H:%M:%S')
    course_detail = fields.Nested(CourseDetailSchema(), many=True)


course_schema = CourseSchema(many=False)


class IsReviewSchema(Schema):
    id = fields.Int()
    status = fields.Int()
    is_best = fields.Int()


class CourseNameSchema(Schema):
    id = fields.Int()
    title = fields.String()


class CourseNameReviewSchema(Schema):
    id = fields.Int()
    title = fields.String()
    review = fields.Nested(IsReviewSchema(), many=False)


class TicketNameSchema(Schema):
    id = fields.Int()
    count = fields.Int()


class TicketListSchema(Schema):
    id = fields.Int()
    status = fields.Int()
    count = fields.Int()
    cost = fields.Int()
    price = fields.Int()
    created_at = fields.DateTime('%Y-%m-%d %H:%M:%S')


ticket_list_schema = TicketListSchema(many=True)


class TicketDetailSchema(Schema):
    id = fields.Int()
    status = fields.Int()
    count = fields.Int()
    cost = fields.Int()
    price = fields.Int()
    created_at = fields.DateTime('%Y-%m-%d %H:%M:%S')
    updated_at = fields.DateTime('%Y-%m-%d %H:%M:%S')


ticket_detail_schema = TicketDetailSchema(many=False)


class UserNameSchema(Schema):
    id = fields.Int()
    name = fields.String()


class UserTicketListSchema(Schema):
    id = fields.Int()
    remain_count = fields.Int()
    created_at = fields.DateTime('%Y-%m-%d %H:%M:%S')

    user = fields.Nested(UserNameSchema(), many=False)
    course = fields.Nested(CourseNameReviewSchema(), many=False)
    ticket = fields.Nested(TicketNameSchema(), many=False)


user_list_schema = UserTicketListSchema(many=True)
user_detail_schema = UserTicketListSchema(many=False)


class UserListSchema(Schema):
    id = fields.Int()
    name = fields.String()

    user_ticket = fields.Nested(UserTicketListSchema(), many=True)





class QnaListSchema(Schema):
    id = fields.Int()
    status = fields.Int()
    is_reply = fields.Int()
    question = fields.String()
    created_at = fields.DateTime('%Y-%m-%d %H:%M:%S')

    course = fields.Nested(CourseNameSchema(), many=False)
    user = fields.Nested(UserNameSchema(), many=False)


qna_list_schema = QnaListSchema(many=True)


class QnaDetailSchema(Schema):
    id = fields.Int()
    status = fields.Int()
    is_reply = fields.Int()
    question = fields.String()
    answer = fields.String()
    created_at = fields.DateTime('%Y-%m-%d %H:%M:%S')

    course = fields.Nested(CourseNameSchema(), many=False)
    user = fields.Nested(UserNameSchema(), many=False)


qna_detail_schema = QnaDetailSchema(many=False)


class ReviewListSchema(Schema):
    id = fields.Int()
    status = fields.Int()
    is_best = fields.Int()
    satisfaction = fields.Int()
    title = fields.String()
    created_at = fields.DateTime('%Y-%m-%d %H:%M:%S')

    course = fields.Nested(CourseNameSchema(), many=False)
    user = fields.Nested(UserNameSchema(), many=False)


review_list_schema = ReviewListSchema(many=True)


class ReviewDetailSchema(Schema):
    id = fields.Int()
    status = fields.Int()
    is_best = fields.Int()
    satisfaction = fields.Int()
    title = fields.String()
    description = fields.String()
    created_at = fields.DateTime('%Y-%m-%d %H:%M:%S')

    course = fields.Nested(CourseNameSchema(), many=False)
    user = fields.Nested(UserNameSchema(), many=False)


review_detail_schema = ReviewDetailSchema(many=False)