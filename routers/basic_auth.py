from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

router = APIRouter(prefix="/login",
                   tags=['login'], responses={404: {"message": "Not Found"}})

oauth2 = OAuth2PasswordBearer(tokenUrl="login")


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
        "password": "123456"
    },
    "repository": {
        "username": "repository",
        "full_name": "User",
        "email": "user@gmail.com",
        "disabled": True,
        "password": "123"
    }
}


def search_user_db(username: str):
    if username in users_db:
        return UserDb(**users_db[username])


def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])


def current_user(token: str = Depends(oauth2)):
    user = search_user(token)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Credentials are not authorized", headers={"WWW-Authenticate": "Bearer"})

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

    user = search_user(form.username)

    if not form.password == user.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Password incorrect")

    return {"access_token": user.username, "token_type": "bearer"}


@router.get('/users/me')
async def me(user: User = Depends(current_user)):
    return user
