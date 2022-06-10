from fastapi import APIRouter, Security
from fastapi.security import HTTPAuthorizationCredentials as HAC, HTTPBearer
from jwt_token import Auth
from schemas import Token

router = APIRouter()
security = HTTPBearer()


@router.put('/auth/refresh-token', response_model=Token)
def refresh_token(credentials: HAC = Security(security)):
    refresh_token = credentials.credentials
    new_token = Auth.refresh_token(refresh_token)
    return {'access_token': new_token}