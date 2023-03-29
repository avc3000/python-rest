def user_schema(user) -> dict:
    return {"id": str(user["_id"]), "name": user["name"], "surname": user["surname"], "email": user["email"]}


def users_schema(users) -> list:
    return [user_schema(user) for user in users]
