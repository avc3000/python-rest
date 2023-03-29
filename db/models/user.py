from pydantic import BaseModel


class User(BaseModel):
    id: str | None
    name: str
    surname: str
    email: str
