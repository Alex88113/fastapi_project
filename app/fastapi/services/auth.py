from fastapi import Depends, HTTPException
from fastapi.security import APIKeyHeader, HTTPBasic, HTTPBasicCredentials
from secrets import compare_digest

api_key = APIKeyHeader(name='X-Key')
fake_keys  = ['secret']

def get_key(key: str = Depends(api_key)):
    if key not in fake_keys:
        raise HTTPException(status_code=401, detail='invalid API Key')
    return key

basic = HTTPBasic()

def get_user(credentials: HTTPBasicCredentials = Depends(basic)):
    if not compare_digest(credentials.password, "pass"):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return credentials.username


def admin_only(user: str = Depends(get_user)):
    if user != "admin":
        raise HTTPException(status_code=403, detail="Admins only")
    return user
