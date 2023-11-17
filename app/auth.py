from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from passlib.context import CryptContext
from . import models_and_schemas
from jose import jwt
from datetime import datetime, timedelta

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(user: models_and_schemas.User):
    claims = {
        "sub": user.username,
        "email": user.email,
        "role": user.role,
        "active": user.is_active,
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    return jwt.encode(claims=claims, key=SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token):
    claims = jwt.decode(token, key=SECRET_KEY)
    return claims


def check_active(token: str = Depends(oauth2_scheme)):
    claims = decode_token(token)
    print(claims.get("active"))
    if claims.get("active"):
        return claims
    raise HTTPException(
        status_code=401,
        detail="Bitte aktiviere Deinen Account!",
        headers={"WWW-Authenticate": "Bearer"}
    )

def check_admin(claims: dict = Depends(check_active)):
    role = claims.get("role")
    if role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Nur für Admin erreichbar!",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return claims
