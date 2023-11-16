import jwt

from fastapi import HTTPException
from datetime import datetime, timedelta

from config.constant import *
from database.base_model import DefaultModel
from config.config import SECRET_KEY, ALGORITHM


class JWT:
    def __init__(self):
        self.algorithm = ALGORITHM
        self.secret_key = SECRET_KEY

    def create_access_token(self, payloads: dict):
        payloads.update({'exp': datetime.utcnow() + timedelta(minutes=5)})
        return jwt.encode(payloads, key=self.secret_key, algorithm=self.algorithm)
    
    def create_refresh_token(self, payloads: dict):
        payloads.update({'exp': datetime.utcnow() + timedelta(days=1)})
        return jwt.encode(payloads, key=self.secret_key, algorithm=self.algorithm)
    
    def verify_token(self, token):
        response = DefaultModel()

        try:
            response.result_data = jwt.decode(token, key=self.secret_key, algorithms=self.algorithm)
        except jwt.ExpiredSignatureError as e:  # 토큰 인증 시간 만료
            raise HTTPException(detail=ERROR_DIC[ERROR_TOKEN_EXPIRED][1],
                                status_code=ERROR_DIC[ERROR_TOKEN_EXPIRED][0])
        except jwt.InvalidTokenError as e:  # 토큰 검증 실패
            print(f'InvalidTokenError : {e}')
            raise HTTPException(detail=ERROR_DIC[ERROR_UNAUTHORIZED][1],
                                status_code=ERROR_DIC[ERROR_UNAUTHORIZED][0])
        return response

