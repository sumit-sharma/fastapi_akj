from requests import Session
import core.auth.auth_bearer
import time
from typing import Dict, List
from fastapi import Depends, Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, OAuth2PasswordBearer
from datetime import datetime, timedelta
from jose import JWTError, jwt
import database, models


JWT_SECRET = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_TIME = 60* 60 * 24 * 30 *6

get_db = database.get_db

def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return {}
    
    
def token_response(token: str):
    return {
        "access_token": token,
        "token_type": "bearer",
        "expires_at": datetime.now() + timedelta(seconds=ACCESS_TOKEN_EXPIRE_TIME)
    }


def signJWT(user_id: str) -> Dict[str, str]:
    payload = {
        "user_id": user_id,
        "expires": time.time() + (ACCESS_TOKEN_EXPIRE_TIME)
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return token_response(token)

    
    

class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            else:
                result =  decodeJWT(credentials.credentials)
                return (credentials.credentials)
                return request.items
                return request.url._url.split(request.base_url._url)
                return request.url._url.__contains__('api/v1/user1')
                return request.base_url._url
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, jwtoken: str) -> bool:
        isTokenValid: bool = False
        try:
            payload = decodeJWT(jwtoken)
        except:
            payload = None
        if payload:
            isTokenValid = True
        return isTokenValid
    
    
    
    