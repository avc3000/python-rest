from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(tags=['users'])

# Entity User


class User(BaseModel):
    id: int
    name: str
    surname: str
    email: str
    age: int


user_list = [User(id=1, name="Antony", surname="John", email="antony3000@gmail.com", age=30),
             User(id=2, name="Juan", surname="Loo",
                  email="juan3000@gmail.com", age=33),
             User(id=3, name="Pedro", surname="Show", email="pedro3000@gmail.com", age=35)]


@router.get('/usersJson')
async def usersJson():
    return [{"name": "Antony", "surname": "John", "email": "antony3000@gmail.com", "age": 30}]


@router.get('/users/')
async def users():
    return list(user_list)

# Path


@router.get('/usersClass/{id}')
async def usersClass(id: int):
    users = filter(lambda user: user.id == id, user_list)
    try:
        return list(users)[0]
    except:
        return []

# Query


@router.get('/userQuery/')
async def userQuery(id: int):
    return search_user(id)


@router.post('/user/', status_code=201)
async def userPost(user: User):
    if (type(search_user(user.id)) == User):
        raise HTTPException(
            status_code=404, detail="The user exists in the database.")
    else:
        user_list.append(user)

        return user


@router.put('/user/')
async def userPut(user: User):
    if (type(search_user(user.id)) == User):
        user_update = search_user(user.id)
        user_update.name = user.name
        user_update.surname = user.surname
        user_update.email = user.email
        user_update.age = user.age

        return user_update
    else:
        return {"Message": "The user not exist."}


@router.delete('/user/{id}')
async def userDelete(id: int):
    found = False

    for index, saved_user in enumerate(user_list):
        if saved_user.id == id:
            del user_list[index]
            found = True

            return saved_user

    if not found:
        return {"Message": "The user has not been deleted."}


def search_user(id: int):
    users = filter(lambda user: user.id == id, user_list)
    try:
        return list(users)[0]
    except:
        return []
