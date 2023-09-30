IS_REAL_SERVER = False

STATUS_ACTIVE = 1
STATUS_INACTIVE = 0
STATUS_DELETED = -1

DEFAULT_PAGE_SIZE = 10

USER_TYPE_CUSTOMER = 1
USER_TYPE_SELLER = 50
USER_TYPE_ADMIN = 99

ERROR_BAD_REQUEST = 'bad_request'
ERROR_UNAUTHORIZED = 'unauthorized'
ERROR_FORBIDDEN = 'forbidden'
ERROR_ADMIN_AUTHORITY = 'admin_authority'
ERROR_INTERNAL_SERVER = 'internal_server'
ERROR_NOT_IMPLEMENTED = 'not_implemented'
ERROR_DATA_NOT_EXIST = 'data_not_exist'
ERROR_USER_NOT_EXIST = 'user_not_exist'
ERROR_NEED_MORE_POINT = 'need_more_point'
ERROR_INVALID_TOKEN = 'invalid_token'
ERROR_ACCESS_TOKEN_EXPIRED = 'access_token_expired'
ERROR_REFRESH_TOKEN_EXPIRED = 'refresh_token_expired'
ERROR_OTHER_DEVICE_LOGGED_IN = 'other_device_logged_in'
ERROR_NEED_ESTATE_AGENT_INFORMATION = 'need_estate_agent_information'
ERROR_FAILED_DELETE_ROOM = 'failed_delete_room'
ERROR_OVER_TIME_AUTHORITY = 'over_time_authority'
ERROR_BLOCK_USER = 'block_user'
ERROR_WRONG_NICKNAME_LENGTH = 'wrong_nickname_length'
ERROR_WRONG_NICKNAME_GRAMMAR = 'wrong_nickname_grammar'
ERROR_WRONG_EMAIL_FORM = 'wrong_email_form'
ERROR_CHANGE_PASSWORD = 'change_password'

ERROR_DIC = {
    ERROR_BAD_REQUEST: (400, '잘못된 요청입니다'),
    ERROR_UNAUTHORIZED: (401, '인증정보가 잘못되었습니다.'),
    ERROR_FORBIDDEN: (403, '권한이 없습니다'),
    ERROR_ADMIN_AUTHORITY: (444, '해당 권한이 없어 이용하실 수 없습니다.'),
    ERROR_INTERNAL_SERVER: (500, '시스템 에러입니다.'),
    ERROR_NOT_IMPLEMENTED: (501, '업데이트 예정입니다'),
    ERROR_DATA_NOT_EXIST: (204, '데이터가 존재하지 않습니다'),
    ERROR_USER_NOT_EXIST: (210, '해당 전화번호로 가입하신 계정이 존재하지 않습니다.'),
    ERROR_NEED_MORE_POINT: (300, '포인트가 부족합니다.'),
    ERROR_INVALID_TOKEN: (301, '토큰이 잘못되었습니다.'),
    ERROR_ACCESS_TOKEN_EXPIRED: (302, '토큰 기간이 만료되었습니다.'),
    ERROR_REFRESH_TOKEN_EXPIRED: (303, '갱신토큰 기간이 만료되었습니다.'),
    ERROR_OTHER_DEVICE_LOGGED_IN: (304, '다른 기기에서 로그인하였습니다.'),
    ERROR_OVER_TIME_AUTHORITY: (230, '인증 시간이 초과된 인증번호 입니다.'),
    ERROR_BLOCK_USER: (240, '차단한 유저 입니다.'),
    ERROR_WRONG_NICKNAME_LENGTH: (260, '3자 이상 16자 이하로 입력해주세요.'),
    ERROR_WRONG_NICKNAME_GRAMMAR: (270, '.과 _외 특수문자 및 공백은 사용할 수 없습니다.'),
    ERROR_WRONG_EMAIL_FORM: (280, '올바른 이메일 형식이 아닙니다.'),
    ERROR_CHANGE_PASSWORD: (290, '비밀번호를 변경해주세요.'),
}