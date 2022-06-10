import jwt
from fastapi import HTTPException
from datetime import datetime, timedelta
from decouple import config
from fastapi.security import HTTPAuthorizationCredentials


def id_from_access_token(credentials: HTTPAuthorizationCredentials) -> int:
    token = credentials.credentials
    return Auth.decode_access_token(token)["sub"]



class Auth():
    SECRET_KEY = config("SECRET_KEY")
    
    @staticmethod
    def encode_access_token(subject):
        payload = {
            'exp' : datetime.utcnow() + timedelta(days=0, minutes=50),
            'iat' : datetime.utcnow(),
	    'scope': 'access_token',
            'sub' : subject
        }
        return jwt.encode(
            payload=payload, 
            key=Auth.SECRET_KEY,
            algorithm='HS256'
        )
    
    @staticmethod
    def decode_access_token(token):
        try:
            payload = jwt.decode(token, Auth.SECRET_KEY, algorithms=['HS256'])
            if (payload['scope'] == 'access_token'):
                return payload
            raise HTTPException(status_code=401, detail='Scope for the token is invalid')
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail='Token expired')
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail='Invalid token')
	  
   
    @staticmethod 
    def encode_refresh_token(subject):
        payload = {
            'exp' : datetime.utcnow() + timedelta(days=10, hours=10),
            'iat' : datetime.utcnow(),
	        'scope': 'refresh_token',
            'sub' : subject
        }
        return jwt.encode(
            payload=payload, 
            key=Auth.SECRET_KEY,
            algorithm='HS256'
        )
        
        
    @staticmethod
    def refresh_token(refresh_token):
        try:
            payload = jwt.decode(refresh_token, Auth.SECRET_KEY, algorithms=['HS256'])
            if (payload['scope'] == 'refresh_token'):
                subject = payload['sub']
                new_token = Auth.encode_access_token(subject)
                return new_token
            raise HTTPException(status_code=401, detail='Invalid scope for token')
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail='Refresh token expired')
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail='Invalid refresh token')