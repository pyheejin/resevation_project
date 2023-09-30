import jwt

from datetime import datetime, timedelta

from database.base_model import DefaultModel
from config.config import SECRET_KEY, ALGORITHM


class JWT:
    def __init__(self):
        self.algorithm = ALGORITHM
        self.secret_key = SECRET_KEY

    def create_access_token(self, payloads: dict):
        payloads.update({'exp': datetime.utcnow() + timedelta(minutes=15)})
        return jwt.encode(payloads, key=self.secret_key, algorithm=self.algorithm)
    
    def create_refresh_token(self, payloads: dict):
        payloads.update({'exp': datetime.utcnow() + timedelta(days=1)})
        return jwt.encode(payloads, key=self.secret_key, algorithm=self.algorithm)
    
    def verify_token(self, token):
        response = DefaultModel()
        try:
            response = jwt.decode(token, key=self.secret_key, algorithms=self.algorithm)
        except jwt.ExpiredSignatureError:  # 토큰 인증 시간 만료
            response.result_code = 302
            response.result_msg = '토큰 기간이 만료되었습니다.'
            return response
        except jwt.InvalidTokenError:  # 토큰 검증 실패
            response.result_code = 301
            response.result_msg = '토큰이 잘못되었습니다.'
            return response
        finally:
            return response

