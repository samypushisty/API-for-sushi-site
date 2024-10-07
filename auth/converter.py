from fastapi.exceptions import HTTPException
from sqlalchemy.orm import DeclarativeBase


class RequestAnswer(HTTPException):
    pass


class Base(DeclarativeBase):
    pass


def tojson(table: Base):
    result = {}
    for i in vars(table):
        if not (i.startswith("__") or i.startswith("_") or i == "metadata"):
            result[i] = getattr(table, i)
    return result
