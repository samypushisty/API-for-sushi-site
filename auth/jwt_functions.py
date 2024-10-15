import time
import jwt
from config import SECRET_KEY
from datafunctions import naive_utcnow, naive_utcfromtimestamp
from fastapi import Request
from fastapi.exceptions import HTTPException


def validation(request: Request):
    jwt_info = JwtInfo(request.cookies.get("jwt"))
    if jwt_info.valid:
        return jwt_info
    else:
        raise HTTPException(status_code=500, detail=jwt_info.info_except)


def create_jwt(name: str, id: int):
    return jwt.encode(payload={'name': name, "expires": time.time() + 3600, 'id': id},
                      key=SECRET_KEY, algorithm='HS256')


class JwtInfo:
    def __init__(self, token: str):
        self.valid = False
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            self._expires = data.get("expires")
            self.id = data.get("id")
            self._verefy_jwt()
        except:
            self._expires = None
            self.id = None
            self.info_except = "invalid token or you haven't token"



    def _verefy_jwt(self):
        if self._expires is None:
            self.valid = False
            self.info_except = "data expire is none"
        elif naive_utcnow() > naive_utcfromtimestamp(self._expires):
            self.valid = False
            self.info_except = "expired"
        else:
            self.valid = True
            self.info_except = None
