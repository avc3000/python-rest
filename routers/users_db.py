from fastapi import APIRouter, HTTPException, status
from db.models.user import User
from db.schemas.user import user_schema, users_schema
from db.client import db_client
from bson import ObjectId

router = APIRouter(prefix="/users_db", tags=['users_db'],
                   responses={status.HTTP_404_NOT_FOUND: {"message": "Not Found"}})


@router.get('/', response_model=list[User])
async def users():
    return users_schema(db_client.users.find())


@router.get('/{id}')
async def userQuery(id: str):
    return search_user("_id", ObjectId(id))


@router.get('/by_id/')
async def userQuery(id: str):
    return search_user("_id", ObjectId(id))


@router.post('/', response_model=User, status_code=status.HTTP_201_CREATED)
async def userPost(user: User):
    if (type(search_user("email", user.email)) == User):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="The user exists in the database.")

    user_dict = dict(user)
    del user_dict["id"]

    id = db_client.users.insert_one(user_dict).inserted_id
    new_user = user_schema(db_client.users.find_one({"_id": id}))

    return User(**new_user)


@router.put('/', response_model=User)
async def userPut(user: User):
    user_dict = dict(user)
    del user_dict['id']

    try:
        db_client.users.find_one_and_replace(
            {"_id": ObjectId(user.id)}, user_dict)
    except:
        return {"Message": "The user not exist."}

    return search_user("_id", ObjectId(user.id))


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def userDelete(id: str):
    found = db_client.users.find_one_and_delete({"_id": ObjectId(id)})

    if not found:
        return {"Message": "The user has not been deleted."}


def search_user(key: str, value):
    try:
        user = db_client.users.find_one({key: value})
        return User(**user_schema(user))
    except:
        return []
