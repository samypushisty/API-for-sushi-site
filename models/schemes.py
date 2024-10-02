from pydantic import BaseModel


class User(BaseModel):
    email: str
    username: str
    password: str
    number: str
    addresses: str



class UserSignIn(BaseModel):
    email: str
    password: str



