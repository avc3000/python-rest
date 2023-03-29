from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta

router = APIRouter(prefix="/jwt-login",
                   tags=['jwt-login'], responses={404: {"message": "Not Found"}})

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 1
SECRET = "b47f4228330fc7ab35f8ef576c4615a5"

crypt = CryptContext(schemes=['bcrypt'])


class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool


class UserDb(User):
    password: str


users_db = {
    "antony": {
        "username": "antony",
        "full_name": "Antony Jordan",
        "email": "antony@gmail.com",
        "disabled": False,
        "password": "$2a$12$sjcC6317DP60vTgS00D/VublJqTGu60lMtIp0jM78nC/rUHB91WBS"
    },
    "repository": {
        "username": "repository",
        "full_name": "User",
        "email": "user@gmail.com",
        "disabled": True,
        "password": "$2a$12$BouHEYtB7IfuPlvJ4aFu4uyyXHnLULXeGdZsgzmgf.h3ZHJ75AvYW"
    }
}


def search_user_db(username: str):
    if username in users_db:
        return UserDb(**users_db[username])


def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])


async def auth_user(token: str = Depends(oauth2)):
    exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                              detail="Credentials are not authorized", headers={"WWW-Authenticate": "Bearer"})
    try:
        username = jwt.decode(token, SECRET, algorithms=[ALGORITHM]).get("sub")
        if username is None:
            raise exception
    except JWTError:
        raise exception

    return search_user(username)


def current_user(user: User = Depends(auth_user)):
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")

    return user


@router.post('/')
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)

    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User not found")

    user = search_user_db(form.username)

    if not crypt.verify(form.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Password incorrect")

    access_token = {"sub": user.username,
                    "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)}

    return {"access_token": jwt.encode(access_token, SECRET, algorithm=ALGORITHM, ), "token_type": "bearer"}


@router.get('/users/me')
async def me(user: User = Depends(current_user)):
    return user
