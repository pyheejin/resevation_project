IS_REAL_SERVER = False

STATUS_ACTIVE = 1
STATUS_INACTIVE = 0
STATUS_DELETED = -1

DEFAULT_PAGE = 1
DEFAULT_PAGE_SIZE = 10

USER_TYPE_CUSTOMER = 1
USER_TYPE_SELLER = 50
USER_TYPE_ADMIN = 99

ERROR_DATA_NOT_EXIST = 'data_not_exist'
ERROR_USER_EXIST = 'user_already_exist'
ERROR_DATA_EXIST = 'data_already_exist'
ERROR_WRONG_NICKNAME_LENGTH = 'wrong_nickname_length'
ERROR_WRONG_NICKNAME_GRAMMAR = 'wrong_nickname_grammar'
ERROR_WRONG_EMAIL_FORM = 'wrong_email_form'
ERROR_DOESNT_MATCH_ID_OR_PASSWORD = "doesn't match id or password"
ERROR_BAD_REQUEST = 'bad_request'
ERROR_UNAUTHORIZED = 'unauthorized'
ERROR_TOKEN_EXPIRED = 'token_expired'
ERROR_FORBIDDEN = 'forbidden'
ERROR_ADMIN_AUTHORITY = 'admin_authority'
ERROR_INTERNAL_SERVER = 'internal_server'
ERROR_NOT_IMPLEMENTED = 'not_implemented'

ERROR_DIC = {
    ERROR_DATA_NOT_EXIST: (204, '데이터가 존재하지 않습니다'),
    ERROR_USER_EXIST: (211, '중복된 아이디 입니다.'),
    ERROR_DATA_EXIST: (212, '이미 존재하는 데이터 입니다.'),
    ERROR_WRONG_NICKNAME_LENGTH: (260, '3자 이상 16자 이하로 입력해주세요.'),
    ERROR_WRONG_NICKNAME_GRAMMAR: (270, '.과 _외 특수문자 및 공백은 사용할 수 없습니다.'),
    ERROR_WRONG_EMAIL_FORM: (280, '올바른 이메일 형식이 아닙니다.'),
    ERROR_DOESNT_MATCH_ID_OR_PASSWORD: (291, '아이디 혹은 비밀번호가 일치하지 않습니다.'),
    ERROR_BAD_REQUEST: (400, '잘못된 요청입니다'),
    ERROR_UNAUTHORIZED: (401, '인증정보가 잘못되었습니다.'),
    ERROR_TOKEN_EXPIRED: (402, '토큰 기간이 만료되었습니다.'),
    ERROR_FORBIDDEN: (403, '권한이 없습니다'),
    ERROR_ADMIN_AUTHORITY: (444, '해당 권한이 없어 이용하실 수 없습니다.'),
    ERROR_INTERNAL_SERVER: (500, '시스템 에러입니다.'),
}