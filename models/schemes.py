from pydantic import BaseModel


class User(BaseModel):
    email: str
    username: str
    password: str


class UserSignIn(BaseModel):
    email: str
    password: str


class AddBook(BaseModel):
    title: str
    description: str

