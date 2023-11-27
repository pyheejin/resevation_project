import jwt

from fastapi import HTTPException
from datetime import datetime, timedelta

from config.constant import *
from database.base_model import DefaultModel
from config.config import SECRET_KEY, ALGORITHM


class JWT:
    def __init__(self):
        self.ALGORITHM = ALGORITHM
        self.SECRET_KEY = SECRET_KEY

    def create_access_token(self, payload: dict):
        expired_at = datetime.utcnow() + timedelta(days=1)
        payload.update({'exp': expired_at,
                        'expired_at': (expired_at + timedelta(hours=9)).strftime('%Y-%m-%d %H:%M:%S')})
        result = jwt.encode(payload, key=self.SECRET_KEY, algorithm=self.ALGORITHM)
        return result

    def create_refresh_token(self, payload: dict):
        expired_at = datetime.utcnow() + timedelta(days=14)
        payload.update({'exp': expired_at,
                        'expired_at': (expired_at + timedelta(hours=9)).strftime('%Y-%m-%d %H:%M:%S')})
        result = jwt.encode(payload, key=self.SECRET_KEY, algorithm=self.ALGORITHM)
        return result
    
    def verify_token(self, token):
        response = DefaultModel()

        try:
            response.result_data = jwt.decode(token, key=self.SECRET_KEY, algorithms=self.ALGORITHM)
        except jwt.ExpiredSignatureError as e:  # 토큰 인증 시간 만료
            raise HTTPException(detail=ERROR_DIC[ERROR_TOKEN_EXPIRED][1],
                                status_code=ERROR_DIC[ERROR_TOKEN_EXPIRED][0])
        except jwt.InvalidTokenError as e:  # 토큰 검증 실패
            raise HTTPException(detail=ERROR_DIC[ERROR_UNAUTHORIZED][1],
                                status_code=ERROR_DIC[ERROR_UNAUTHORIZED][0])
        return response

